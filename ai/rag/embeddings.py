from langchain_openai import OpenAIEmbeddings


def build_embeddings(model: str = "text-embedding-3-small") -> OpenAIEmbeddings:
    """Создает embedding-клиент для RAG."""
    return OpenAIEmbeddings(model=model)
