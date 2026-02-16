class AnalysisAgent:
    """Агент анализа потребностей клиента."""

    async def analyze(self, history: list[dict]) -> dict:
        return {"budget": None, "body_type": None}
