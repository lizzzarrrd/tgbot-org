from typing import Dict, Any
from parser_module.infra.container import Container
from parser_module.domain.models import Event, EventField, NoEventFound, EventParseError

def handle_message(message_text: str) -> dict:
    """Обработка входящего текста (использует ParseService + LLM)."""
    container = Container()
    parser = container.parse_service()

    try:
        event = parser.parse_event(message_text)
        return {
            "status": "success",
            "data": event.model_dump(mode='json')
        }
    except NoEventFound:
        return {"status": "info", "msg": "Мероприятие не найдено."}
    except EventParseError as e:
        return {"status": "error", "msg": f"Ошибка обработки: {e}"}
    except Exception as e:
        return {"status": "error", "msg": f"Внутренняя ошибка: {str(e)}"}


def handle_event_update(current_event_data: Dict[str, Any], field_key: str, new_value: str) -> dict:
    """Обработка редактирования (использует EventService)."""
    container = Container()
    editor = container.event_service()

    try:
        try:
            target_field = EventField(field_key)
        except ValueError:
            return {"status": "error", "msg": "Недопустимое поле."}
        current_event = Event.model_validate(current_event_data)

        updated_event = editor.update_field(
            current_event=current_event,
            field=target_field,
            new_value=new_value
        )

        return {
            "status": "success",
            "data": updated_event.model_dump(mode='json')
        }

    except EventParseError as e:
        return {"status": "error", "msg": str(e)}
    except Exception as e:
        return {"status": "error", "msg": f"Внутренняя ошибка: {str(e)}"}