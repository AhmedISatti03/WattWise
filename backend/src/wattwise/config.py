from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_ROOT.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="WATTWISE_", env_file=BACKEND_ROOT / ".env", extra="ignore"
    )
    database_url: str = "sqlite:///./var/wattwise.db"
    enable_demo_api: bool = False
    cors_origins: list[str] = Field(default_factory=lambda: [
        "http://localhost:5173", "http://127.0.0.1:5173"
    ])
    fixture_directory: Path = REPO_ROOT / "docs/api/examples/v0.1"
