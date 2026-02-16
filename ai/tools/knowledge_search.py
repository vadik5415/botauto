from ai.rag.retriever import KnowledgeRetriever


class KnowledgeSearchTool:
    """Инструмент поиска в базе знаний."""

    def __init__(self, retriever: KnowledgeRetriever):
        self.retriever = retriever

    async def search(self, query: str, collection: str) -> str:
        return await self.retriever.retrieve(query, collection)
