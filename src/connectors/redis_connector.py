import logging
from typing import Any

import redis.asyncio as redis


class RedisConnector:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self) -> None:
        logging.info(f"Начинаю поддключение к Redis, host={self.host}, port={self.port}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Успешное поддключение к Redis, host={self.host}, port={self.port}")

    async def set(self, key: str, value: str, expire: int = None) -> None:
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str) -> Any:
        value = await self.redis.get(key)
        return value

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self) -> None:
        logging.info("Начинаю закрытие соединения с Redis")
        await self.redis.close()
        logging.info("Успешное закрытие соединения с Redis")
