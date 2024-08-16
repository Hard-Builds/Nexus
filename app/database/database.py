import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base

DATABASE_URL = os.environ["DATABASE_URL"]


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
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                    bind=engine)
        self.client = SessionLocal()
        Base.metadata.create_all(bind=engine)

    @staticmethod
    def get_instance():
        if DBClient.__instance is None:
            DBClient()
        return DBClient.__instance
