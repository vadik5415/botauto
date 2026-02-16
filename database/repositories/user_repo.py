class UserRepository:
    """Репозиторий пользователей."""

    async def get(self, user_id: int):
        return {"id": user_id}
