from typing import Dict, List, Optional

import chromadb
from chromadb.config import Settings

from ai.rag.embeddings import build_embeddings


class VectorStore:
    """Векторное хранилище для RAG."""

    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        embedding_model: str = "text-embedding-3-small",
        embedding_api_key: Optional[str] = None,
        embedding_base_url: Optional[str] = None,
    ):
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False),
        )
        self.car_collection = self.client.get_or_create_collection("car_knowledge")
        self.customs_collection = self.client.get_or_create_collection("customs_info")
        self.faq_collection = self.client.get_or_create_collection("faq")
        self.embeddings = build_embeddings(
            model=embedding_model,
            api_key=embedding_api_key,
            base_url=embedding_base_url,
        )

    def add_documents(self, collection_name: str, documents: List[Dict]) -> None:
        collection = getattr(self, f"{collection_name}_collection")
        texts = [doc["text"] for doc in documents]
        collection.add(
            embeddings=self.embeddings.embed_documents(texts),
            documents=texts,
            metadatas=[doc["metadata"] for doc in documents],
            ids=[doc["id"] for doc in documents],
        )

    async def search_relevant_info(self, query: str, collection_name: str = "car", n_results: int = 3) -> str:
        collection = getattr(self, f"{collection_name}_collection")
        query_embedding = self.embeddings.embed_query(query)
        results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
        parts = []
        for doc, metadata in zip(results.get("documents", [[]])[0], results.get("metadatas", [[]])[0]):
            parts.append(f"[{metadata.get('source', 'KB')}]: {doc}")
        return "\n\n".join(parts)
