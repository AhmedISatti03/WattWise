import asyncio
import json
import re
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import FastAPI, Query, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import AwareDatetime, BeforeValidator
from starlette.exceptions import HTTPException

from .config import Settings
from .db import build_engine, database_ready

Scenario = Literal["normal", "empty", "partial-data", "device-disconnected", "error"]
DEMO_WEEK_START = datetime.fromisoformat("2026-10-21T00:00:00+03:00")
DEMO_DAY_START = datetime.fromisoformat("2026-10-27T00:00:00+03:00")
DEMO_PERIOD_END = datetime.fromisoformat("2026-10-28T00:00:00+03:00")
DEMO_TIMESTAMP_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})")


def require_timestamp_text(value: str) -> str:
    if not isinstance(value, str) or DEMO_TIMESTAMP_PATTERN.fullmatch(value) is None:
        raise ValueError("Use an RFC 3339 timestamp with a timezone offset.")
    return value


DemoTimestamp = Annotated[AwareDatetime, BeforeValidator(require_timestamp_text)]


def error_body(request: Request, code: str, message: str, retryable: bool = False,
               field_errors: list | None = None) -> dict:
    return {"meta": {"contractVersion": "0.1-draft", "requestId": request.state.request_id},
            "error": {"code": code, "message": message, "retryable": retryable,
                      "retryAfterSeconds": None, "fieldErrors": field_errors or []}}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()
    engine = build_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        engine.dispose()

    app = FastAPI(title="WattWise local foundation", version="0.1.0", lifespan=lifespan,
                  description="Health and opt-in synthetic fixture API only. No household business API is implemented.")
    app.state.engine = engine
    app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
                       allow_credentials=False, allow_methods=["GET"], allow_headers=["Content-Type"])

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request.state.request_id = str(uuid4())
        try:
            response = await call_next(request)
        except Exception:
            response = JSONResponse(error_body(request, "internal_error", "The service could not complete the request.", True), status_code=500)
        response.headers["X-Request-ID"] = request.state.request_id
        response.headers["Cache-Control"] = "no-store"
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        fields = [{"path": ".".join(str(part) for part in e["loc"]),
                   "code": e["type"], "message": e["msg"]} for e in exc.errors()]
        return JSONResponse(error_body(request, "validation_error", "Check the request fields.", field_errors=fields), status_code=422)

    @app.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return JSONResponse(error_body(request, "not_found" if exc.status_code == 404 else "request_error", str(exc.detail)), status_code=exc.status_code, headers=exc.headers)

    @app.get("/api/v1/health/live", tags=["foundation"])
    def live():
        return {"status": "ok", "service": "wattwise", "version": "0.1.0", "mode": "foundation", "demoApiEnabled": settings.enable_demo_api}

    @app.get("/api/v1/health/ready", tags=["foundation"])
    def ready(request: Request):
        if not database_ready(engine):
            return JSONResponse(error_body(request, "database_not_ready", "Database unavailable or migrations not at the expected revision.", True), status_code=503)
        return {"status": "ready", "database": "ok", "schema": "current"}

    if settings.enable_demo_api:
        async def fixture(request: Request, scenario: Scenario, delay_ms: int, last_complete_day: bool = False):
            if delay_ms:
                await asyncio.sleep(delay_ms / 1000)
            try:
                data = json.loads((settings.fixture_directory / f"{scenario}.json").read_text(encoding="utf-8"))
                if not isinstance(data, dict) or not isinstance(data.get("meta"), dict):
                    raise ValueError("Invalid fixture envelope")
                if last_complete_day and scenario != "error":
                    path = settings.fixture_directory / "periods" / "last-complete-day-contributions.json"
                    contributions = json.loads(path.read_text(encoding="utf-8"))[scenario]
                    period = contributions["period"]
                    buckets = [
                        bucket for bucket in data["trend"]["buckets"]
                        if bucket["start"] == period["start"] and bucket["endExclusive"] == period["endExclusive"]
                    ]
                    if len(buckets) != (0 if scenario == "empty" else 1):
                        raise ValueError("Fixture does not contain the selected trend bucket")
                    data["trend"].update(period=period, buckets=buckets)
                    data["contributions"] = contributions
                    data["selectedPeriodEnergy"] = {**contributions["household"], "period": period}
            except (OSError, ValueError, TypeError, KeyError):
                return JSONResponse(error_body(request, "fixture_unavailable", "The requested development fixture is unavailable."), status_code=503)
            data["meta"]["requestId"] = request.state.request_id
            if scenario == "error":
                return JSONResponse(data, status_code=503, headers={"X-WattWise-Source": "synthetic-fixture"})
            return data

        @app.get("/api/v1/demo/overview", tags=["synthetic fixtures"])
        async def demo_overview(
            request: Request,
            scenario: Scenario = "normal",
            delay_ms: int = Query(0, ge=0, le=2000),
            start: DemoTimestamp | None = None,
            end_exclusive: Annotated[DemoTimestamp | None, Query(alias="endExclusive")] = None,
            resolution: Literal["day"] = "day",
        ):
            if start is None and end_exclusive is None:
                return await fixture(request, scenario, delay_ms)
            if start not in (DEMO_WEEK_START, DEMO_DAY_START) or end_exclusive != DEMO_PERIOD_END:
                message = "Choose the sample week or its last complete day."
                fields = [{"path": "query", "code": "unsupported_period", "message": message}]
                return JSONResponse(
                    error_body(request, "validation_error", message, field_errors=fields),
                    status_code=422,
                )
            return await fixture(request, scenario, delay_ms, last_complete_day=start == DEMO_DAY_START)

        @app.get("/api/v1/demo/devices", tags=["synthetic fixtures"])
        async def demo_devices(request: Request, scenario: Scenario = "normal", delay_ms: int = Query(0, ge=0, le=2000)):
            result = await fixture(request, scenario, delay_ms)
            if isinstance(result, JSONResponse):
                return result
            return {key: result[key] for key in ("meta", "devices", "collector") if key in result}

    return app
