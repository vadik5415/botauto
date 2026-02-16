from typing import Any, Dict


class IntentService:
    """Сервис определения намерения пользователя по тексту."""

    async def detect(self, message: str) -> Dict[str, Any]:
        message_lower = message.lower()
        calculation_keywords = ["сколько стоит", "цена", "стоимость", "расчет", "посчитай"]
        car_info_keywords = ["расскажи про", "что лучше", "сравни", "отличия"]
        customs_keywords = ["таможня", "растаможка", "пошлина", "документы"]

        needs_calculation = any(kw in message_lower for kw in calculation_keywords)
        needs_car_knowledge = any(kw in message_lower for kw in car_info_keywords)
        needs_customs_info = any(kw in message_lower for kw in customs_keywords)

        collection = "car"
        if needs_customs_info:
            collection = "customs"
        elif "faq" in message_lower or "как" in message_lower:
            collection = "faq"

        return {
            "needs_calculation": needs_calculation,
            "needs_knowledge": needs_car_knowledge or needs_customs_info,
            "collection": collection,
        }
