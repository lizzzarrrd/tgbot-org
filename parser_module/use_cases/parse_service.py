import ast
import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from parser_module.adapters.llm_interface import LlmInterface
from parser_module.domain.models import Event, NoEventFound, EventParseError


PROMPT_TEMPLATE = """
Ты ассистент генерального директора большой компании. Твоя задача — по сообщению выделять информацию по мероприятию.

/Инструкции
Тебе поступает сообщение. Ты должен выделить дату мероприятия, краткое название, описание и место проведения (если указано).
Если в сообщении нет даты, но есть слова: “завтра”, “через неделю” и похожие, то ты должен записать дату отталкиваясь от сегодняшней.
Если сообщение не информативное (не содержит данных о встрече/мероприятии), то выводи “no mero”.

/Формат вывода:
Если сообщение содержит информацию про мероприятие, то вывод ОБЯЗАТЕЛЬНО должен быть в формате JSON:
{"date_start":"2025-12-05 13:00","date_end":"2025-12-05 14:30","name":"Встреча по продукту","description":"Обсуждение нового продукта","location":"Переговорная №1"}
Если невозможно выделить информацию по мероприятию, то выведи строку: no mero
Ничего лишнего кроме JSON или слова "no mero" выводить не нужно.""".strip()


def _parse_dt(s: str) -> datetime:
    return datetime.strptime(s.strip(), "%Y-%m-%d %H:%M")


def _parse_llm_response(text: str) -> Dict[str, Any]:
    t = text.strip()

    if t.lower() == "no mero":
        raise NoEventFound()

    if t.startswith("```"):
        lines = t.splitlines()
        if lines and lines[0].strip().startswith("```"):
            lines = lines[1:]
            lines = lines[:-1]

        t = "\n".join(lines).strip()

    # 1) Пытаемся как JSON (рекомендуемый формат)
    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            return obj
    except json.JSONDecodeError:
        pass

    # 2) если модель всё же вернула python-словарь
    try:
        obj = ast.literal_eval(t)
        if isinstance(obj, dict):
            return obj
    except Exception as e:
        pass

    pass


class ParseService:
    def __init__(self, llm: LlmInterface) -> None:
        self.llm = llm

    def parse_event(self, message_from_user: str) -> Event:
        now = datetime.now()
        cur_date = now.strftime("%Y-%m-%d")

        prompt = (
            PROMPT_TEMPLATE
            + f"\n==========\nСообщение: {message_from_user}\n==========\n"
            + f"Текущая дата: {cur_date}\n==========\nВыделенное мероприятие:\n"
        )
        answer = self.llm.complete(prompt)

        payload = _parse_llm_response(answer)

        try:
            date_start = _parse_dt(payload["date_start"])
            date_end = _parse_dt(payload["date_end"]) if payload.get("date_end") else None
            name = str(payload.get("name", "")).strip()
            description = str(payload.get("description", "")).strip()
            location = str(payload.get("location", "")).strip()
        except Exception as e:
            pass

        return Event(
            date_start=date_start,
            date_end=date_end,
            name=name,
            description=description,
            location=location,
        )
