def is_admin(user_id: int, admin_ids: set[int]) -> bool:
    """Проверяет, является ли пользователь администратором."""
    return user_id in admin_ids
