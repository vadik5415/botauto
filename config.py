from functools import lru_cache
from typing import Literal, Optional

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки приложения с типобезопасной валидацией."""

    telegram_bot_token: str

    # Унифицированные параметры LLM-провайдера.
    llm_provider: Literal["openai", "openrouter"] = "openai"
    llm_model: str = "gpt-4o-mini"
    llm_api_key: Optional[str] = None
    llm_base_url: Optional[str] = None
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1000
    llm_request_timeout: int = 30

    # Обратная совместимость со старым набором env-переменных.
    openai_api_key: Optional[str] = None
    openai_model: Optional[str] = None

    # Дополнительные заголовки для OpenRouter (рекомендуется провайдером).
    openrouter_site_url: Optional[str] = None
    openrouter_app_name: str = "ai-car-consultant-bot"

    # Настройки embeddings (можно оставить OpenAI даже при OpenRouter для чата).
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: Optional[str] = None
    embedding_base_url: Optional[str] = None

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

    @model_validator(mode="after")
    def validate_keys(self) -> "Settings":
        """Проверяет критичные ключи и заполняет совместимые значения."""
        if not self.llm_api_key and not self.openai_api_key:
            raise ValueError("Требуется LLM_API_KEY или OPENAI_API_KEY.")
        return self

    @property
    def resolved_llm_model(self) -> str:
        """Возвращает итоговую модель с учетом обратной совместимости."""
        return self.openai_model or self.llm_model

    @property
    def resolved_llm_api_key(self) -> str:
        """Возвращает итоговый API-ключ для LLM."""
        return self.llm_api_key or self.openai_api_key or ""

    @property
    def resolved_llm_base_url(self) -> Optional[str]:
        """Возвращает базовый URL провайдера (если нужен)."""
        if self.llm_base_url:
            return self.llm_base_url
        if self.llm_provider == "openrouter":
            return "https://openrouter.ai/api/v1"
        return None

    @property
    def resolved_embedding_api_key(self) -> str:
        """Возвращает ключ для embeddings."""
        return self.embedding_api_key or self.openai_api_key or self.resolved_llm_api_key


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Лениво загружает настройки приложения."""
    return Settings()

settings = Settings()
