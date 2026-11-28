from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine, make_url

from .config import BACKEND_ROOT

SCHEMA_REVISION = "0001_service_state"


def build_engine(database_url: str) -> Engine:
    url = make_url(database_url)
    kwargs = {"pool_pre_ping": True, "hide_parameters": True}
    if url.get_backend_name() == "sqlite":
        if url.database and url.database != ":memory:":
            path = Path(url.database)
            if not path.is_absolute():
                path = BACKEND_ROOT / path
            path.parent.mkdir(parents=True, exist_ok=True)
            url = url.set(database=str(path))
        kwargs["connect_args"] = {"check_same_thread": False, "timeout": 5}
    elif url.get_backend_name() == "postgresql":
        kwargs["connect_args"] = {"connect_timeout": 3}
    return create_engine(url, **kwargs)


def database_ready(engine: Engine) -> bool:
    # Migrations run explicitly; a responding database alone is not readiness.
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            revisions = set(conn.execute(text("SELECT version_num FROM alembic_version")).scalars())
            conn.execute(text("SELECT key, value FROM service_state LIMIT 1"))
            return revisions == {SCHEMA_REVISION}
    except Exception:
        # Do not expose credentials, driver details or connection strings via HTTP.
        return False
