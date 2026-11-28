from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import text

from wattwise.config import BACKEND_ROOT
from wattwise.main import create_app


def test_liveness_not_database_readiness(settings):
    with TestClient(create_app(settings)) as client:
        assert client.get("/api/v1/health/live").status_code == 200
        response = client.get("/api/v1/health/ready")
        assert response.status_code == 503
        assert response.json()["error"]["code"] == "database_not_ready"
        assert settings.database_url not in response.text
        assert response.headers["x-request-id"] == response.json()["meta"]["requestId"]


def test_migrations_idempotence_and_restart_persistence(migrated):
    command.upgrade(Config(str(BACKEND_ROOT / "alembic.ini")), "head")
    app = create_app(migrated)
    with TestClient(app) as client:
        assert client.get("/api/v1/health/ready").status_code == 200
        with app.state.engine.begin() as conn:
            conn.execute(text("INSERT INTO service_state (key,value) VALUES (:key,:value)"), {"key": "test", "value": "persists"})
    second = create_app(migrated)
    with TestClient(second) as client:
        assert client.get("/api/v1/health/ready").status_code == 200
        with second.state.engine.connect() as conn:
            assert conn.execute(text("SELECT value FROM service_state WHERE key='test'")).scalar_one() == "persists"


def test_wrong_migration_revision_fails_readiness(migrated):
    app = create_app(migrated)
    with app.state.engine.begin() as conn:
        conn.execute(text("UPDATE alembic_version SET version_num='unknown'"))
    with TestClient(app) as client:
        assert client.get("/api/v1/health/ready").status_code == 503


def test_mock_disabled_and_not_in_openapi(settings):
    with TestClient(create_app(settings)) as client:
        assert client.get("/api/v1/demo/overview").status_code == 404
        assert "/api/v1/demo/overview" not in client.get("/openapi.json").json()["paths"]


def test_cors_exact_allowed_origin(settings):
    with TestClient(create_app(settings)) as client:
        allowed = client.get("/api/v1/health/live", headers={"Origin": "http://localhost:5173"})
        assert allowed.headers["access-control-allow-origin"] == "http://localhost:5173"
        denied = client.get("/api/v1/health/live", headers={"Origin": "https://untrusted.example"})
        assert "access-control-allow-origin" not in denied.headers
        assert "access-control-allow-credentials" not in allowed.headers


def test_migration_round_trip_and_no_business_tables(migrated):
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    command.downgrade(config, "base")
    with TestClient(create_app(migrated)) as client:
        assert client.get("/api/v1/health/ready").status_code == 503
    command.upgrade(config, "head")
    from sqlalchemy import inspect
    app = create_app(migrated)
    assert set(inspect(app.state.engine).get_table_names()) == {"alembic_version", "service_state"}
    app.state.engine.dispose()
