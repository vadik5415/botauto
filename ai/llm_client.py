from typing import Dict, List, Optional

from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
import structlog

logger = structlog.get_logger()


class LLMClient:
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
                model=self.model,
                tokens=response.response_metadata.get("token_usage", {}),
            )
            return response.content
        except Exception as exc:
            logger.error("ai_generation_failed", error=str(exc))
            return "Извините, AI временно недоступен. Давайте продолжим: уточните бюджет и желаемую модель."

    async def generate_with_tools(self, system_prompt: str, user_message: str, tools: List[Dict]) -> Dict:
        """Генерирует ответ с возможностью вызова функций (tools)."""
        payload = {
            "response": await self.generate_response(system_prompt, [], user_message),
            "tool_calls": [],
        }
        return payload
