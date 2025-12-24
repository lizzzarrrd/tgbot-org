from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Project settings loaded from .env"""

    db_path: str = Field(..., description="Path to sqlite db file")
    api_token_bot: str
    yandex_api_key: str
    yandex_model_uri: str

    google_client_id: str
    google_client_secret: str | None = None
    google_redirect_uri: str
    oauth_listen_host: str = "0.0.0.0"
    oauth_listen_port: int = 8080

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    class Config:
        env_file = ".env"


settings = Settings()
