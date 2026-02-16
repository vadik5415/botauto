import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from telegram import Update
from telegram.ext import ContextTypes

from ai.llm_client import LLMClient
from ai.prompts.consultant import CONSULTANT_SYSTEM_PROMPT
from ai.rag.vector_store import VectorStore
from ai.tools.cost_calculator import CostCalculator
from services.conversation_service import ConversationService
from services.lead_service import LeadService
from services.intent_service import IntentService


class AIConversationHandler:
    """Обработчик AI-диалога с клиентом."""

    def __init__(
        self,
        llm_client: LLMClient,
        vector_store: VectorStore,
        calculator: CostCalculator,
        conversation_service: ConversationService,
        lead_service: LeadService,
    ):
        self.llm = llm_client
        self.vector_store = vector_store
        self.calculator = calculator
        self.conv_service = conversation_service
        self.lead_service = lead_service
        self.intent_service = IntentService()

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        message_text = update.message.text

        await self.conv_service.save_message(user_id=user.id, role="user", content=message_text)
        history = await self.conv_service.get_recent_history(user.id, limit=10)
        intent = await self.intent_service.detect(message_text)

        context_text = None
        if intent["needs_knowledge"]:
            context_text = await self.vector_store.search_relevant_info(
                query=message_text,
                collection_name=intent["collection"],
            )

        if intent["needs_calculation"]:
            calc_result = await self._handle_cost_calculation(message_text)
            if calc_result:
                await self.conv_service.save_message(user_id=user.id, role="assistant", content=calc_result)
                await update.message.reply_text(calc_result)
                return

        system_prompt = CONSULTANT_SYSTEM_PROMPT.format(current_date=datetime.now().strftime("%Y-%m-%d"))
        ai_response = await self.llm.generate_response(
            system_prompt=system_prompt,
            conversation_history=history,
            user_message=message_text,
            context=context_text,
        )

        await self.conv_service.save_message(user_id=user.id, role="assistant", content=ai_response)
        readiness = await self._assess_readiness(user.id, history, message_text)

        if readiness["score"] >= 7:
            await self.lead_service.create_lead(
                user_id=user.id,
                readiness_score=readiness["score"],
                preferences=readiness["preferences"],
                estimated_cost=readiness.get("estimated_cost"),
            )

        await update.message.reply_text(ai_response)

    async def _handle_cost_calculation(self, message: str) -> Optional[str]:
        year_match = re.search(r"(20\d{2})", message)
        engine_match = re.search(r"(\d(?:[\.,]\d)?)\s*(?:л|литр)", message.lower())
        price_match = re.search(r"\$?(\d{4,6})", message.replace(" ", ""))

        if not (year_match and engine_match and price_match):
            return None

        year = int(year_match.group(1))
        engine = float(engine_match.group(1).replace(",", "."))
        price = float(price_match.group(1))

        calc = self.calculator.calculate_total_cost(car_price_usd=price, engine_volume=engine, year=year)
        return self.calculator.format_calculation_for_message(calc)

    async def _assess_readiness(self, user_id: int, history: List, last_message: str) -> Dict[str, Any]:
        score = 5
        if any(token in last_message.lower() for token in ["готов", "оформить", "покупаю", "свяжитесь"]):
            score = 8
        return {"score": score, "preferences": {}, "estimated_cost": None}
