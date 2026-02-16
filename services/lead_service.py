class LeadService:
    """Сервис работы с квалифицированными лидами."""

    def __init__(self):
        self._leads: list[dict] = []

    async def create_lead(self, user_id: int, readiness_score: int, preferences: dict, estimated_cost: float | None):
        lead = {
            "user_id": user_id,
            "readiness_score": readiness_score,
            "preferences": preferences,
            "estimated_cost": estimated_cost,
        }
        self._leads.append(lead)
        return lead
