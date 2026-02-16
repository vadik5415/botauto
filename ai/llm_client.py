from typing import Dict, List, Optional

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger()


class LLMClient:
    """Клиент для работы с OpenAI/OpenRouter через OpenAI-совместимый API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        provider: str = "openai",
        base_url: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        request_timeout: int = 30,
        app_name: str = "ai-car-consultant-bot",
        site_url: Optional[str] = None,
    ):
        self.api_key = api_key
        self.model = model
        self.provider = provider

        client_kwargs: Dict = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "request_timeout": request_timeout,
        }

        if base_url:
            client_kwargs["base_url"] = base_url

        # OpenRouter рекомендует передавать служебные заголовки для трекинга приложения.
        if provider == "openrouter":
            default_headers = {"X-Title": app_name}
            if site_url:
                default_headers["HTTP-Referer"] = site_url
            client_kwargs["default_headers"] = default_headers

        self.client = ChatOpenAI(**client_kwargs)
    """Клиент для работы с OpenAI GPT моделями."""

    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.client = ChatOpenAI(
            api_key=api_key,
            model=model,
            temperature=0.7,
            max_tokens=1000,
            request_timeout=30,
        )

    async def generate_response(
        self,
        system_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        context: Optional[str] = None,
        tools: Optional[List] = None,
    ) -> str:
        """Генерирует ответ AI на основе промпта, истории и контекста."""
        try:
            messages = [SystemMessage(content=system_prompt)]
            if context:
                messages.append(
                    SystemMessage(content=f"Релевантная информация из базы знаний:\n{context}")
                )

            for msg in conversation_history[-10:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))

            messages.append(HumanMessage(content=user_message))
            response = await self.client.ainvoke(messages)

            logger.info(
                "ai_response_generated",
                provider=self.provider,
                model=self.model,
                tokens=response.response_metadata.get("token_usage", {}),
            )
            return response.content
        except Exception as exc:
            logger.error("ai_generation_failed", provider=self.provider, error=str(exc))
            logger.error("ai_generation_failed", error=str(exc))
            return "Извините, AI временно недоступен. Давайте продолжим: уточните бюджет и желаемую модель."

    async def generate_with_tools(self, system_prompt: str, user_message: str, tools: List[Dict]) -> Dict:
        """Генерирует ответ с возможностью вызова функций (tools)."""
        payload = {
            "response": await self.generate_response(system_prompt, [], user_message),
            "tool_calls": [],
        }
        return payload
