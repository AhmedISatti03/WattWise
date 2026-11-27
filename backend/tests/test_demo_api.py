import json
from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from wattwise.config import REPO_ROOT
from wattwise.main import create_app


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings.model_copy(update={"enable_demo_api": True}))) as client:
        yield client


@pytest.mark.parametrize("scenario", ["normal", "empty", "partial-data", "device-disconnected", "error"])
def test_all_scenarios_match_schema_and_samples(client, settings, scenario):
    response = client.get(f"/api/v1/demo/overview?scenario={scenario}")
    assert response.status_code == (503 if scenario == "error" else 200)
    actual = response.json()
    schema = json.loads((REPO_ROOT / "docs/api/dashboard-response.schema.json").read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(actual)
    UUID(actual["meta"]["requestId"])
    assert actual["meta"]["requestId"] == response.headers["x-request-id"]
    assert actual["meta"]["sample"] is True
    expected = json.loads((settings.fixture_directory / f"{scenario}.json").read_text())
    expected["meta"]["requestId"] = actual["meta"]["requestId"]
    assert actual == expected
    assert response.headers["cache-control"] == "no-store"


def test_values_and_partial_coverage(client):
    normal = client.get("/api/v1/demo/overview").json()
    c = normal["contributions"]
    assert c["household"]["value"] == 12
    assert sum(a["value"] for a in c["appliances"]) + c["other"]["value"] == 12
    assert normal["cost"]["value"] == 325.2
    assert normal["forecast"]["value"] == 900
    assert normal["budget"]["value"] == 800
    empty = client.get("/api/v1/demo/overview?scenario=empty").json()
    assert empty["currentPower"]["value"] is None
    partial = client.get("/api/v1/demo/overview?scenario=partial-data").json()
    assert partial["forecast"]["value"] is None
    disconnected = client.get("/api/v1/demo/overview?scenario=device-disconnected").json()
    assert disconnected["contributions"]["household"]["value"] == 12
    assert disconnected["contributions"]["other"]["value"] is None
    assert next(a for a in disconnected["contributions"]["appliances"] if a["deviceId"] == "plug-fridge")["value"] is None


def test_devices_view_matches_overview(client):
    for scenario in ["normal", "empty", "partial-data", "device-disconnected"]:
        overview = client.get(f"/api/v1/demo/overview?scenario={scenario}").json()
        devices = client.get(f"/api/v1/demo/devices?scenario={scenario}").json()
        assert devices["devices"] == overview["devices"]
        assert devices["collector"] == overview["collector"]
        assert devices["meta"]["asOf"] == overview["meta"]["asOf"]
    assert client.get("/api/v1/demo/devices?scenario=error").status_code == 503


@pytest.mark.parametrize("query", ["scenario=../../../etc/passwd", "scenario=unknown", "delay_ms=-1", "delay_ms=2001", "delay_ms=text"])
def test_validation_not_path_traversal(client, query):
    r = client.get("/api/v1/demo/overview?" + query)
    assert r.status_code == 422
    assert r.json()["error"]["fieldErrors"]
    assert r.json()["meta"]["requestId"] == r.headers["x-request-id"]


def test_missing_fixtures_are_actionable_not_tracebacks(settings, tmp_path):
    config = settings.model_copy(update={"enable_demo_api": True, "fixture_directory": tmp_path})
    with TestClient(create_app(config)) as client:
        r = client.get("/api/v1/demo/overview")
        assert r.status_code == 503
        assert r.json()["error"]["code"] == "fixture_unavailable"
        assert str(tmp_path) not in r.text


def test_snapshots_do_not_claim_future_receipts(client):
    data = client.get("/api/v1/demo/overview").json()
    as_of = datetime.fromisoformat(data["meta"]["asOf"])
    for d in data["devices"]:
        if d["lastReceivedAt"]:
            assert datetime.fromisoformat(d["lastReceivedAt"]) <= as_of


@pytest.mark.parametrize("content", ["not json", "[]", '{"meta": null}'])
def test_corrupt_fixture_does_not_expose_details(settings, tmp_path, content):
    (tmp_path / "normal.json").write_text(content)
    config = settings.model_copy(update={"enable_demo_api": True, "fixture_directory": tmp_path})
    with TestClient(create_app(config)) as client:
        r = client.get("/api/v1/demo/overview")
        assert r.status_code == 503
        assert r.json()["error"]["code"] == "fixture_unavailable"


def test_http_error_preserves_allow_header(client):
    response = client.post("/api/v1/demo/overview")
    assert response.status_code == 405
    assert "GET" in response.headers["allow"]
    assert response.json()["meta"]["requestId"] == response.headers["x-request-id"]
