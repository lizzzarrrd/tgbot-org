import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    YANDEX_API_KEY: str
    YANDEX_MODEL_URI: str = "gpt://b1gmvq70i52iqts7bg87/yandexgpt-lite"

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env.parser"),
        env_file_encoding="utf-8"
    )