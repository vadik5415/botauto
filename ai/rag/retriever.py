from ai.rag.vector_store import VectorStore


class KnowledgeRetriever:
    """Ретривер, выбирающий релевантный контекст из векторной БД."""

    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store

    async def retrieve(self, query: str, collection: str = "car") -> str:
        return await self.vector_store.search_relevant_info(query=query, collection_name=collection)
