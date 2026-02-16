import structlog

logger = structlog.get_logger()


def log_incoming(user_id: int, text: str) -> None:
    """Логирует входящие сообщения пользователя."""
    logger.info("incoming_message", user_id=user_id, text=text)
