from typing import Any

from app.client.redis import RedisClient


class CacheService:
    def __init__(self):
        self.__redis_client = RedisClient.get_client()

    def put_object(self, name: str, val: Any, ttl: int) -> bool:
        data = self.__redis_client.set(name, val)
        if ttl:
            self.__setup_ttl(name, ttl)
        return data

    def __setup_ttl(self, name: str, ttl: int) -> bool:
        return self.__redis_client.expire(name, ttl)

    def get_object(self, key: str):
        val_obj = self.__redis_client.get(key)
        return val_obj
