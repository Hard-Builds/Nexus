import os

import redis

from app.enums.os_vars import OSVarsEnum

REDIS_HOST = os.environ[OSVarsEnum.REDIS_HOST.value]
REDIS_PORT = os.environ[OSVarsEnum.REDIS_PORT.value]


class RedisClient:
    __instance = None

    def __init__(self):
        if RedisClient.__instance is not None:
            raise Exception("Singleton class, use get_instance() instead.")
        else:
            self.client = None
            RedisClient.__instance = self
            self.init_client()

    def init_client(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,
                                  decode_responses=True)

    @staticmethod
    def get_client():
        if RedisClient.__instance is None:
            raise Exception("Redis Instance Not Found!")
        return RedisClient.__instance.client
