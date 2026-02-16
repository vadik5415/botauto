import logging
import structlog


def setup_logging(level: str = "INFO") -> None:
    """Настраивает структурированное логирование."""
    logging.basicConfig(level=level)
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ]
    )
