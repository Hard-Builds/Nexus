import uuid

import uvicorn as uvicorn
from fastapi import HTTPException, Request, Response
from starlette.responses import JSONResponse

from app import get_app
from app.api import api_router
from app.database.crud import DataAccessLayer
from app.database.indexe_reg import db_index_registry
from app.middleware.context import RequestContext

app = get_app()


@app.on_event("startup")
async def define_index():
    for col_name, index_list in db_index_registry.items():
        if not index_list: continue
        data_access_service = DataAccessLayer(
            model=None, collection_name=col_name)
        data_access_service.handle_indexes(index_list)


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    api = request.url
    print("API = {}, exc.detail:{}".format(api, exc.detail))
    return JSONResponse(status_code=exc.status_code, content={
        "status_code": exc.status_code,
        "message": exc.detail,
        "data": {}
    })


@app.middleware("http")
async def user_context_middleware(request: Request, call_next):
    """Setting up trace id"""
    RequestContext.set_context_var(key="trace_id", value=str(uuid.uuid4()))
    response: Response = await call_next(request)
    RequestContext.clear_context_data()
    return response


if __name__ == "__main__":
    app.include_router(api_router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
