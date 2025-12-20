from parser_module.adapters.llm_adapter import YandexGptAdapter
from parser_module.use_cases.parse_service import ParseService
from parser_module.use_cases.event_service import EventService
from core.config import settings

YANDEX_API_KEY = settings.yandex_api_key
YANDEX_MODEL_URI = settings.yandex_model_uri

class Container:
    
    def llm(self) -> YandexGptAdapter:
        return YandexGptAdapter(
            api_key=YANDEX_API_KEY,
            model_uri=YANDEX_MODEL_URI,
        )

    def parse_service(self) -> ParseService:
        """Сервис для парсинга через LLM"""
        return ParseService(llm=self.llm())

    def event_service(self) -> EventService:
        """Сервис для ручного редактирования"""
        return EventService()