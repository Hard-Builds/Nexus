import os

from pymongo import MongoClient

from app.enums.os_vars import OSVarsEnum

DATABASE_URL = os.environ[OSVarsEnum.DATABASE_URL.value]


class DBClient:
    __instance = None

    def __init__(self):
        if DBClient.__instance is not None:
            raise Exception("Singleton class, use get_instance() instead.")
        else:
            self.client = None
            DBClient.__instance = self
            self.init_pool()

    def init_pool(self):
        self.client = MongoClient(DATABASE_URL)

    @staticmethod
    def get_instance():
        if DBClient.__instance is None:
            DBClient()
        return DBClient.__instance
