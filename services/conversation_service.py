class ConversationService:
    """Сервис хранения и выдачи истории сообщений."""

    def __init__(self):
        self._messages: dict[int, list[dict]] = {}

    async def save_message(self, user_id: int, role: str, content: str) -> None:
        self._messages.setdefault(user_id, []).append({"role": role, "content": content})

    async def get_recent_history(self, user_id: int, limit: int = 10) -> list[dict]:
        return self._messages.get(user_id, [])[-limit:]
