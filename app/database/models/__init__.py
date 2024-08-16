from sqlalchemy import Column, Boolean, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

from app.utils.DateUtils import DateUtils

Base = declarative_base()


class SQLAbstractBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    is_deleted = Column(Boolean, default=False)
    created_on = Column(DateTime, default=DateUtils.get_current_timestamp)
    modified_on = Column(DateTime, default=DateUtils.get_current_timestamp)
