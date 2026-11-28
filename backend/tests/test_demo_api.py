import json
from datetime import datetime
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator, FormatChecker

from wattwise.config import REPO_ROOT
from wattwise.main import create_app


LAST_COMPLETE_DAY = {
    "start": "2026-10-27T00:00:00+03:00",
    "endExclusive": "2026-10-28T00:00:00+03:00",
}


@pytest.fixture
def client(settings):
    with TestClient(create_app(settings.model_copy(update={"enable_demo_api": True}))) as client:
        yield client


@pytest.fixture(scope="module")
def dashboard_validator():
    schema = json.loads((REPO_ROOT / "docs/api/dashboard-response.schema.json").read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker())


@pytest.mark.parametrize("scenario", ["normal", "empty", "partial-data", "device-disconnected", "error"])
def test_all_scenarios_match_schema_and_samples(client, settings, dashboard_validator, scenario):
    response = client.get(f"/api/v1/demo/overview?scenario={scenario}")
    assert response.status_code == (503 if scenario == "error" else 200)
    actual = response.json()
    dashboard_validator.validate(actual)
    UUID(actual["meta"]["requestId"])
    assert actual["meta"]["requestId"] == response.headers["x-request-id"]
    assert actual["meta"]["sample"] is True
    expected = json.loads((settings.fixture_directory / f"{scenario}.json").read_text(encoding="utf-8"))
    expected["meta"]["requestId"] = actual["meta"]["requestId"]
    assert actual == expected
    assert response.headers["cache-control"] == "no-store"


def test_incomplete_setup_example_preserves_independent_energy_metrics(dashboard_validator):
    path = REPO_ROOT / "docs/api/examples/v0.1/settings/incomplete-setup.json"
    dashboard = json.loads(path.read_text(encoding="utf-8"))
    dashboard_validator.validate(dashboard)

    assert {field["code"] for field in dashboard["setupCompleteness"]["missingFields"]} == {
        "tariff_missing", "budget_missing",
    }
    assert dashboard["selectedPeriodEnergy"]["value"] == 70
    forecast = dashboard["forecast"]
    assert forecast["energyEligible"] is True
    assert forecast["projectedEnergyKwh"] == 200
    assert forecast["eligible"] is False
    for group, reason in (("cost", "tariff_missing"), ("forecast", "tariff_missing"), ("budget", "budget_missing")):
        assert dashboard[group]["value"] is None
        assert dashboard[group]["unavailableReason"] == reason
    assert dashboard["budgetPosition"]["state"] == "unavailable"
    assert dashboard["budgetPosition"]["unavailableReason"] == "budget_missing"


def test_values_and_partial_coverage(client):
    normal = client.get("/api/v1/demo/overview").json()
    c = normal["contributions"]
    assert c["household"]["value"] == 70
    assert sum(a["value"] for a in c["appliances"]) + c["other"]["value"] == 70
    assert normal["cost"]["value"] == 325.2
    assert normal["forecast"]["value"] == 900
    assert normal["budget"]["value"] == 800
    empty = client.get("/api/v1/demo/overview?scenario=empty").json()
    assert empty["currentPower"]["value"] is None
    partial = client.get("/api/v1/demo/overview?scenario=partial-data").json()
    assert partial["forecast"]["value"] is None
    disconnected = client.get("/api/v1/demo/overview?scenario=device-disconnected").json()
    assert disconnected["contributions"]["household"]["value"] == 70
    assert disconnected["contributions"]["other"]["value"] is None
    assert next(a for a in disconnected["contributions"]["appliances"] if a["deviceId"] == "plug-fridge")["value"] is None


@pytest.mark.parametrize("scenario", ["normal", "empty", "partial-data", "device-disconnected"])
def test_selected_period_views_shift_together(client, dashboard_validator, scenario):
    weekly = client.get("/api/v1/demo/overview", params={"scenario": scenario}).json()
    daily_response = client.get(
        "/api/v1/demo/overview", params={"scenario": scenario, "resolution": "day", **LAST_COMPLETE_DAY}
    )
    assert daily_response.status_code == 200
    daily = daily_response.json()
    dashboard_validator.validate(daily)
    assert daily["trend"]["period"] == LAST_COMPLETE_DAY
    assert weekly["trend"]["period"] != daily["trend"]["period"]
    for payload, expected in ((weekly, 70), (daily, 12)):
        contributions = payload["contributions"]
        trend = payload["trend"]
        selected_period = payload["selectedPeriodEnergy"]
        assert trend["period"] == contributions["period"] == selected_period["period"]
        assert selected_period == {**contributions["household"], "period": trend["period"]}
        if scenario == "empty":
            assert selected_period["value"] is None
            assert trend["buckets"] == []
        else:
            assert selected_period["value"] == expected == sum(bucket["value"] for bucket in trend["buckets"])
            if scenario == "device-disconnected":
                assert contributions["other"]["value"] is None
            else:
                assert contributions["other"]["value"] + sum(a["value"] for a in contributions["appliances"]) == expected
        assert payload["budgetPosition"]["period"] == payload["billingCycle"]
    for group in ("currentPower", "todayEnergy", "billingCycle", "cost", "forecast", "budget", "budgetPosition"):
        assert daily[group] == weekly[group]


def test_explicit_demo_week_accepts_equivalent_utc_offsets(client):
    response = client.get(
        "/api/v1/demo/overview",
        params={"start": "2026-10-20T21:00:00Z", "endExclusive": "2026-10-27T21:00:00Z"},
    )
    assert response.status_code == 200
    assert response.json()["selectedPeriodEnergy"]["value"] == 70


def test_selected_period_preserves_error_scenario(client):
    response = client.get("/api/v1/demo/overview", params={"scenario": "error", **LAST_COMPLETE_DAY})
    assert response.status_code == 503
    assert response.json()["meta"]["sample"] is True
    assert response.headers["x-wattwise-source"] == "synthetic-fixture"


@pytest.mark.parametrize(
    "params",
    [
        {"start": LAST_COMPLETE_DAY["start"]},
        {"endExclusive": LAST_COMPLETE_DAY["endExclusive"]},
        {"start": "2026-10-26T00:00:00+03:00", "endExclusive": LAST_COMPLETE_DAY["endExclusive"]},
        {"start": "2026-10-27T00:00:00", "endExclusive": LAST_COMPLETE_DAY["endExclusive"]},
        {"start": "1793048400", "endExclusive": LAST_COMPLETE_DAY["endExclusive"]},
        {**LAST_COMPLETE_DAY, "resolution": "hour"},
    ],
)
def test_unsupported_demo_periods_return_validation_errors(client, params):
    response = client.get("/api/v1/demo/overview", params=params)
    assert response.status_code == 422
    assert response.json()["error"]["fieldErrors"]


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
