from __future__ import annotations
from aiogram import types
from datetime import datetime
from adapters.state import RegistrationState
from adapters.send_message import MessageSender
from adapters.utils import clean_text
from adapters.buttons import confirm_buttons


class MessageHandler:
    """
    Основная ручка: получает любое текстовое сообщение от пользователя.
    """

    def __init__(self, registration_state: RegistrationState, draft_repo, sender: MessageSender, parse_service):
        self.registration_state = registration_state
        self.draft_repo = draft_repo
        self.sender = sender
        self.parse_service = parse_service

    async def handle(self, message: types.Message) -> None:
        tg_id = message.from_user.id
        text = clean_text(message.text)

        if not await self.registration_state.is_registered(tg_id):
            await self.sender.send_text(
                chat_id=message.chat.id,
                text="Похоже, ты ещё не зарегистрирован. Нажми /start"
            )
            return

        draft_id = await self.draft_repo.create_draft(
            tg_id=tg_id,
            raw_text=text,
            created_at=datetime.utcnow()
        )

        parsed = await self.parse_service.parse(text)

        if parsed:
            await self.draft_repo.update_draft(draft_id, parsed)

            title = parsed.get("title", text[:40])
            start = parsed.get("start", "???")

            await self.sender.send_text(
                chat_id=message.chat.id,
                text=f"Я нашёл событие:\n📌 {title}\n🕒 Начало: {start}\n\nПодтверждаешь?",
                reply_markup=confirm_buttons()
            )
        else:
            await self.sender.send_text(
                chat_id=message.chat.id,
                text="Я получил твоё сообщение, но не смог распарсить.\nХочешь ввести данные вручную?"
            )