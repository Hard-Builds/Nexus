from typing import TypeVar, Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from starlette.responses import JSONResponse

from app.database.database import DBClient
from app.database.models import Base
from app.enums.http_config import HttpStatusCode

ModelType = TypeVar("ModelType", bound=Base)


class DataAccessLayer:
    def __init__(self, model: ModelType):
        db_instance = DBClient.get_instance()
        self.__db_client = db_instance.client
        self.model = model

    def __update_data(self, item) -> Any:
        json_compatible_item_data = jsonable_encoder(item)
        return JSONResponse(content=json_compatible_item_data)

    def get_by_id(self, id):
        row_obj = self.__db_client.query(self.model).filter(
            self.model.id == id, self.model.is_deleted == False
        ).first()
        print(f"row_obj : {row_obj}")
        return row_obj

    def get_all(self):
        row_list: list = list(self.__db_client.query(self.model).all())
        row_list: list = self.__update_data(row_list)
        print(f"row_list : {row_list}")
        return row_list

    def add_row(self, obj_in):
        db = self.__db_client
        try:
            print(f"obj_in : {obj_in}")
            db_obj = self.model(**obj_in.dict())
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            print(f"db_obj : {db_obj}")
            return db_obj
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=HttpStatusCode.NOT_FOUND,
                                detail="Failed to create item")

    def update_row(self, model_obj):
        db = self.__db_client
        db.add(model_obj)
        db.commit()
        db.refresh(model_obj)
        model_obj = self.__update_data(model_obj)
        print(f"model_obj : {model_obj}")
        return model_obj

    def get_first_row_by_filter(self, filters):
        row_obj = self.__db_client.query(self.model).filter(and_(*filters)).first()
        print(f"row_obj : {row_obj}")
        return row_obj
