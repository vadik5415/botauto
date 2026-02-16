from typing import Dict


def compare_models(left: Dict, right: Dict) -> Dict:
    """Сравнивает две модели по базовым параметрам."""
    return {
        "price_diff": left.get("price", 0) - right.get("price", 0),
        "reliability_diff": left.get("reliability", 0) - right.get("reliability", 0),
    }
