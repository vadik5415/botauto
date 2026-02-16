import asyncio

from services.intent_service import IntentService


def test_detect_intent_for_customs_keywords():
    service = IntentService()
    intent = asyncio.run(service.detect("Какая таможня и пошлина?"))
    assert intent["collection"] == "customs"
