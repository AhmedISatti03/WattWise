"""Non-destructive foundation write/reopen check; no household acceptance claim."""
from uuid import uuid4

from sqlalchemy import text

from .config import Settings
from .db import build_engine, database_ready


def main():
    settings = Settings()
    key = f"verification-{uuid4()}"
    first = build_engine(settings.database_url)
    second = None
    try:
        if not database_ready(first):
            raise SystemExit("Database not ready. Run the documented migrations first.")
        with first.begin() as conn:
            conn.execute(text("INSERT INTO service_state (key,value) VALUES (:key,:value)"), {"key": key, "value": "restart-check"})
        first.dispose()
        second = build_engine(settings.database_url)
        with second.connect() as conn:
            value = conn.execute(text("SELECT value FROM service_state WHERE key=:key"), {"key": key}).scalar_one()
        if value != "restart-check":
            raise SystemExit("Persistence check failed.")
        print("PASS: database ready; committed service metadata survives engine restart.")
    finally:
        cleanup = second or first
        if database_ready(cleanup):
            with cleanup.begin() as conn:
                conn.execute(text("DELETE FROM service_state WHERE key=:key"), {"key": key})
        cleanup.dispose()
        first.dispose()


if __name__ == "__main__":
    main()
