import os
from dataclasses import dataclass


class Settings:
    YANDEX_API_KEY: str = os.getenv("YANDEX_API_KEY", "")
    YANDEX_MODEL_URI: str = os.getenv(
        "YANDEX_MODEL_URI",
        "gpt://<folder_id>/yandexgpt-lite",
    )
