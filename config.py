from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения с типобезопасной валидацией."""

    telegram_bot_token: str
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    database_url: str
    redis_url: str
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False
    manager_chat_id: int = 0
    notification_priority_threshold: int = 7
    vector_db_path: str = "./chroma_db"
    embedding_model: str = "text-embedding-3-small"
    default_company_commission: float = 2500.0
    default_shipping_buffer: float = 1.1
    max_requests_per_minute: int = 20
    max_tokens_per_day: int = 100000

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False)


settings = Settings()
