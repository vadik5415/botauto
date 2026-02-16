from typing import Dict


def format_lead_summary(lead: Dict) -> str:
    """Форматирует короткую сводку лида для менеджера."""
    return (
        f"Лид #{lead.get('user_id')}\n"
        f"Готовность: {lead.get('readiness_score')}\n"
        f"Предпочтения: {lead.get('preferences', {})}"
    )
