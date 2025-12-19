from parser_module.adapters.llm_adapter import YandexGptAdapter
from parser_module.use_cases.parse_service import ParseService
from parser_module.use_cases.event_service import EventService
from parser_module.infra.settings import Settings

class Container:
    def __init__(self):
        self.settings = Settings()

    def llm(self) -> YandexGptAdapter:
        return YandexGptAdapter(
            api_key=self.settings.YANDEX_API_KEY,
            model_uri=self.settings.YANDEX_MODEL_URI,
        )

    def parse_service(self) -> ParseService:
        """Сервис для парсинга через LLM"""
        return ParseService(llm=self.llm())

    def event_service(self) -> EventService:
        """Сервис для ручного редактирования"""
        return EventService()