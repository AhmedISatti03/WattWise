# WattWise backend — local review increment

**State:** runnable foundation and public synthetic mock only. Technology and shared business/API proposals remain pending Ahmed's review. This is not the completed local demonstration from the v1.0 handoff.

Implemented: configuration, SQLAlchemy database connection, explicit Alembic migrations, liveness/readiness checks, consistent errors, request IDs, restricted development CORS, and opt-in mock overview/device routes. There are no account, ingestion, simulator, tariff-calculation, bill-processing or chat endpoints yet. No private household data should be stored in this scaffold.

Read the [design proposal](../docs/backend/design-proposal.md), [decision log](../docs/backend/decision-log.md), [draft shared contract](../docs/api/frontend-contract.md), and [task mapping](../docs/backend/task-mapping.md). The uploaded backend handoff v1.0 is byte-identical to the committed Word document; its finalized text was preserved.

## Requirements

Python **3.12 or newer** (tested on 3.12.14). SQLite is included with Python and is the simplest portable smoke-test profile. PostgreSQL 17 is the proposed target and has a separate optional startup below. The source layout expects the complete repository, including `docs/api/examples/v0.1`; do not copy just a wheel or `backend/` without the example files when using mock mode.

Runtime and test versions are pinned in `requirements.lock` with platform markers for Windows. `uv.lock` provides the corresponding resolver lock; uv is optional for running the project. Current lock includes test/build tooling for local review, not a minimal production deployment.

## Quick start — Windows PowerShell

Run from the repository's `backend` directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -m pip install --no-deps --no-build-isolation -e .
Copy-Item .env.example .env
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn wattwise.main:create_app --factory --host 127.0.0.1 --port 8100
```

No PowerShell activation-policy change is needed because these commands invoke the virtual environment's Python directly. Install Python 3.12 first if `py` is unavailable. PostgreSQL and Docker are not needed for this SQLite profile. Do not commit `.env` or database files.

## Quick start — macOS/Linux

```sh
cd backend
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock
.venv/bin/python -m pip install --no-deps --no-build-isolation -e .
cp .env.example .env
.venv/bin/python -m alembic upgrade head
.venv/bin/python -m uvicorn wattwise.main:create_app --factory --host 127.0.0.1 --port 8100
```

Migrations are deliberately separate from server startup. SQLite relative paths resolve beneath `backend`, not the caller's current directory. The default database is `backend/var/wattwise.db`, ignored by Git. Existing environment variables override `.env` values; inspect your selected configuration if changing `.env` appears ineffective.

## Check the service

- [Liveness](http://127.0.0.1:8100/api/v1/health/live): process responding, even before migration.
- [Readiness](http://127.0.0.1:8100/api/v1/health/ready): database responds and the exact expected migration and foundation table exist. Returns 503 for missing schema/database failure, without exposing connection strings.
- [Interactive API documentation](http://127.0.0.1:8100/docs): actual implemented routes only.

The foundation migration creates only `service_state` plus Alembic's revision table. It does not prematurely decide account or reading schemas. A readiness pass is not proof of complete household functionality.

In another terminal, verify that a temporary service-metadata record survives reopening the database:

```sh
.venv/bin/python -m wattwise.verify_database
```

On Windows use `.\.venv\Scripts\python.exe -m wattwise.verify_database`. The command deletes only its uniquely named verification record after checking it; no user-data reset is exposed.

## Mock API for frontend development (#12)

Set `WATTWISE_ENABLE_DEMO_API=true` in the local `.env` and restart the backend. Demo routes do not exist when this flag is false. They are public only because all responses are synthetic public examples. Do not deploy this opt-in mock alongside private real-household data.

```text
GET /api/v1/demo/overview?scenario=normal
GET /api/v1/demo/devices?scenario=device-disconnected
```

Scenarios: `normal`, `empty`, `partial-data`, `device-disconnected`, `error`. The error scenario returns HTTP 503, not a successful dashboard with zero values. Optional `delay_ms=0..2000` lets the frontend exercise loading; invalid scenario/delay returns 422 with field errors. Missing/corrupt fixture files return an actionable 503. Request IDs in headers/metadata identify the actual call; snapshot times stay fixed.

Examples live in `docs/api/examples/v0.1/`; their versioned schema is `docs/api/dashboard-response.schema.json`. The sample snapshot is **28 October 2026, 14:30 Europe/Istanbul**, not the actual server clock. Normal arithmetic is household 12 kWh including 4+1+2 appliance kWh and 5 other kWh; cost325.20 and dated forecast900 use fictional energy-only charges. The shared contract explains different periods and forecast time. Partial and disconnected scenarios withhold only values their missing inputs affect.

These responses do not pass through ingestion, create stored readings, or prove backend calculations. They address the independent mock increment, not #17/#18. Real integrated demo routes must later use authorized stored records and agreed calculation services.

### Frontend connection check

The current foundation branch still imports `sample.ts`; Miray's branch helper imports JSON. Neither calls this service automatically. Frontend #20 should adopt one shared HTTP adapter after interface review. For now, test from the Vite page's browser console:

```js
fetch('http://127.0.0.1:8100/api/v1/demo/overview?scenario=normal')
  .then(async response => ({ status: response.status, body: await response.json() }))
  .then(console.log)
```

Development CORS permits only `http://localhost:5173` and `http://127.0.0.1:5173` by default, without cookies. Set `WATTWISE_CORS_ORIGINS` to a JSON list of exact origins if your dev port differs. CORS is not authentication. The future session/CSRF choice is still a proposed contract and not implemented here. Keep the service bound to loopback for local use.

## Optional PostgreSQL profile

Use an existing local database or the included Compose service. For Compose, set a local password in the shell or `.env` as `WATTWISE_POSTGRES_PASSWORD`; choose it yourself and keep it out of Git. Then:

```sh
docker compose up -d --wait database
```

The database binds only `127.0.0.1:5433` and persists in a named volume. Configure `WATTWISE_DATABASE_URL=postgresql+psycopg://wattwise:YOUR_URL_ENCODED_PASSWORD@127.0.0.1:5433/wattwise`, run `alembic upgrade head`, start the backend and check readiness. URI-encode special password characters; never paste the real connection URI into reports. The SQLite URL remains the no-Docker option.

Run the same `wattwise.verify_database` command in this configuration. `docker compose stop database` retains data; `docker compose start database` resumes it. Removing a volume destroys records, so this guide does not suggest that as a routine restart/reset step.

## Tests

```sh
.venv/bin/python -m pytest -q
.venv/bin/python -m pip check
```

Windows: substitute `.\.venv\Scripts\python.exe`. Tests use isolated temporary SQLite files, not your configured household database. They verify migration idempotence/downgrade/re-upgrade, metadata persistence across engine/application recreation, readiness failures, explicit mock gating, scenario schema/content, coherent worked values, timestamp bounds, sanitized errors and CORS.

PostgreSQL checks are recorded separately in the local work report, including the actual commands and limits. A teammate still needs to follow the guide independently; automated setup does not represent human review or Ahmed's approval.

## Layout and next steps

```text
backend/
  src/wattwise/       app factory, configuration, health/mock routes, database check
  migrations/        explicit versioned Alembic history
  tests/             request, mock-contract and migration tests
  requirements.lock  cross-platform pinned local-review dependencies
  uv.lock            resolver lock
  compose.yaml       optional local PostgreSQL service
docs/api/            proposed contract, schema and JSON examples
docs/backend/        proposal, decisions, scenarios and task mapping
```

After Ahmed confirms the affected recommendations and the frontend review agrees the schema, proceed #16 → #17 → #18, then consumption, forecasts, bills, insights and assistant integration in the handoff sequence. Real plug #4 still needs accessible hardware; synthetic fixtures are not its acceptance evidence. Do not silently change existing field names or claim production APIs are implemented because they appear in a proposal.
