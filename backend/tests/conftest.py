from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config

from wattwise.config import BACKEND_ROOT, Settings


@pytest.fixture
def settings(tmp_path):
    return Settings(_env_file=None, database_url=f"sqlite:///{tmp_path / 'test.db'}")


@pytest.fixture
def migrated(settings, monkeypatch):
    monkeypatch.setenv("WATTWISE_DATABASE_URL", settings.database_url)
    config = Config(str(BACKEND_ROOT / "alembic.ini"))
    command.upgrade(config, "head")
    return settings
