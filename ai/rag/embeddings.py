from typing import Optional

from langchain_openai import OpenAIEmbeddings


def build_embeddings(
    model: str = "text-embedding-3-small",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> OpenAIEmbeddings:
    """Создает embedding-клиент для RAG."""
    kwargs = {"model": model}
    if api_key:
        kwargs["api_key"] = api_key
    if base_url:
        kwargs["base_url"] = base_url
    return OpenAIEmbeddings(**kwargs)
