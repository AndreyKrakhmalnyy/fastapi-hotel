from typing import Optional
import redis.asyncio as redis


class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        """Устанавливает асинхронное подключение к redis"""
        self.redis = await redis.Redis(host=self.host, port=self.port)

    async def set(self, key: str, value: int, expire: Optional[int]):
        """Устанавливает значение по ключу и времени хранения.

        Args:
            key (str): Ключ
            value (int): Значение
            expire (Optional[int]): Время в секундах
        """
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        """Получает значение по ключу.

        Args:
            key (str): Ключ
        """
        return await self.redis.get(key)

    async def delete(self, key: str):
        """Удаляет значение по ключу.

        Args:
            key (str): Ключ
        """
        await self.redis.delete(key)

    async def close(self):
        """Закрывает сессию"""
        if self.redis:
            await self.redis.close()
