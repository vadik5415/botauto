class UserService:
    """Управление профилями пользователей."""

    async def get_or_create(self, user_id: int, username: str | None = None) -> dict:
        return {"user_id": user_id, "username": username}
