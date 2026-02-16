class NotificationService:
    """Сервис отправки уведомлений менеджерам."""

    async def notify_manager(self, chat_id: int, text: str) -> None:
        _ = (chat_id, text)
