class ConversationRepository:
    """Репозиторий истории сообщений."""

    async def list_recent(self, user_id: int, limit: int = 10):
        _ = user_id
        return []
