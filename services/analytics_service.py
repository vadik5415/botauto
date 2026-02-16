class AnalyticsService:
    """Сервис аналитики запросов и токенов."""

    def __init__(self):
        self.total_tokens = 0

    async def add_tokens(self, amount: int) -> None:
        self.total_tokens += amount
