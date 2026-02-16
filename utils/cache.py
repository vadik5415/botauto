import json
from typing import Any, Optional
import redis.asyncio as redis


class RedisCache:
    """Асинхронная обертка над Redis для кеширования ответов."""

    def __init__(self, redis_url: str):
        self.client = redis.from_url(redis_url)

    async def get_json(self, key: str) -> Optional[dict]:
        raw = await self.client.get(key)
        if not raw:
            return None
        return json.loads(raw)

    async def set_json(self, key: str, value: Any, ttl_seconds: int = 600) -> None:
        await self.client.set(key, json.dumps(value), ex=ttl_seconds)
