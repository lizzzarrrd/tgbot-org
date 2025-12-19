import json
import ast
import re
from datetime import datetime
from typing import Union, Dict, List, Any
from pydantic import ValidationError

from parser_module.adapters.llm_interface import LlmInterface
from parser_module.domain.models import Event, NoEventFound, EventParseError

PROMPT_TEMPLATE = """
Ты ассистент генерального директора большой компании. Твоя задача — по сообщению выделить информацию о ПЕРВОМ актуальном мероприятии.

/Инструкции
1. **Поиск события:** Проанализируй сообщение. Если оно не содержит данных о встречах или мероприятиях, выведи строго строку: no mero
2. **Выбор:** Если в тексте упоминается несколько мероприятий, выбери САМОЕ ПЕРВОЕ по хронологии, которое НЕ отменено. Игнорируй мероприятия с пометкой "отмена" или "перенос на неизвестный срок".
3. **Даты:** 
   - Рассчитывай даты, отталкиваясь от "Текущей даты" (указана ниже). Понимай слова "завтра", "в следующую пятницу" и т.д.
   - Формат даты строго: "YYYY-MM-DD HH:MM".
4. **Время окончания:**
   - Если указана длительность или время конца, заполни `date_end`, который будет вычислять относитнльно `date_start`.
   - Если время окончания или длительность НЕ указаны, поле `date_end` должно быть `null`.

/Формат вывода:
Если информация найдена, верни строго ОДИН JSON-объект. Без markdown, без пояснений.

Пример JSON:
{"date_start": "2025-12-05 13:00", "date_end": "2025-12-05 15:00", "name": "Встреча по продукту", "description": "Обсуждение нового продукта", "location": "Переговорная №1"}
""".strip()

class ParseService:
    def __init__(self, llm: LlmInterface) -> None:
        self.llm = llm

    def _clean_response(self, text: str) -> str:
        """Чистит markdown."""
        text = text.strip()
        if "```" in text:
            text = re.sub(r"```\w*", "", text).replace("```", "")
        return text.strip()

    def _safe_load_json(self, text: str) -> Union[Dict, List, None]:
        """Парсит JSON или Python dict."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        try:
            return ast.literal_eval(text)
        except (ValueError, SyntaxError):
            pass
        return None

    def parse_event(self, message_from_user: str) -> Event:
        now_str = datetime.now().strftime("%Y-%m-%d (%A)")

        prompt = (
            f"{PROMPT_TEMPLATE}\n\n"
            f"Текущая дата: {now_str}\n"
            f"Сообщение пользователя:\n{message_from_user}\n"
        )
        
        raw_response = self.llm.complete(prompt)
        cleaned_response = self._clean_response(raw_response)

        if "no mero" in cleaned_response.lower():
            raise NoEventFound()

        payload = self._safe_load_json(cleaned_response)
        
        if payload is None:
             raise EventParseError(f"Не удалось прочитать ответ LLM: {cleaned_response}")

        if isinstance(payload, list):
            if not payload:
                raise NoEventFound()
            payload = payload[0]
            
        if not isinstance(payload, dict):
            raise EventParseError(f"Ожидался словарь (JSON object), пришло: {type(payload)}")

        try:
            return Event.model_validate(payload)
        except ValidationError as e:
            raise EventParseError(f"Ошибка в данных события: {e}")