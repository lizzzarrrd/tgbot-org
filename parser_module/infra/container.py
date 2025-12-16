from __future__ import annotations

from dataclasses import dataclass

from parser_module.adapters.llm_adapter import YandexGptAdapter
from parser_module.use_cases.parse_service import ParseService

from .settings import Settings

class Container:
    settings: Settings

    def llm(self) -> YandexGptAdapter:
        return YandexGptAdapter(
            api_key=self.settings.YANDEX_API_KEY,
            model_uri=self.settings.YANDEX_MODEL_URI,
        )

    def parse_service(self) -> ParseService:
        return ParseService(llm=self.llm())
