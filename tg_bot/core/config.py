from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_path: str
    api_token_bot: str

    @property
    def database_url(self) -> str:
        return f"sqlite+aiosqlite:///{self.db_path}"

    class Config:
        env_file = ".env.bot"

settings = Settings()