from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_path: str
    api_token_bot: str
    yandex_api_key: str
    yandex_model_uri: str
    google_client_id: str

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    class Config:
        env_file = ".env"

settings = Settings()