from __future__ import annotations

from dataclasses import asdict

from parser_module.infra.container import Container
from parser_module.infra.settings import Settings
from parser_module.domain.models import NoEventFound, EventParseError


def handle_message(message_text: str) -> dict:
    """
    Входная точка: “текст от бота” -> use_cases -> доменный Event -> dict наружу.

    Снаружи передаётся только текст сообщения, а контейнер и настройки
    собираются здесь, на основе переменных окружения.
    """
    settings = Settings()
    settings.validate()

    container = Container()
    container.settings = settings

    parse_service = container.parse_service()
    event = parse_service.parse_event(message_text)

    d = asdict(event)
    return d
