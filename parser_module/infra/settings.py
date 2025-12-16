import os
from dataclasses import dataclass


class Settings:
    YANDEX_API_KEY: str = os.getenv("YANDEX_API_KEY", "")
    YANDEX_MODEL_URI: str = os.getenv(
        "YANDEX_MODEL_URI",
        "gpt://<folder_id>/yandexgpt-lite",
    )

    def validate(self) -> None:
        if not self.YANDEX_API_KEY:
            raise RuntimeError("Missing env YANDEX_API_KEY")
        if "<folder_id>" in self.YANDEX_MODEL_URI or not self.YANDEX_MODEL_URI:
            raise RuntimeError("Set env YANDEX_MODEL_URI to valid modelUri")
