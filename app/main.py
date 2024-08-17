import os
import time
import uuid

import uvicorn as uvicorn
from fastapi import HTTPException, Request, Response
from fastapi.routing import APIRoute
from starlette.responses import JSONResponse

from app import get_app
from app.api import api_router
from app.database.crud import DataAccessLayer
from app.database.indexe_reg import db_index_registry
from app.enums.os_vars import OSVarsEnum
from app.middleware.context import RequestContext

app = get_app()
env = os.environ[OSVarsEnum.ENV.value]

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
async def middleware_function(request: Request, call_next):
    start_time: time = time.time()

    trace_id: str = str(uuid.uuid4())

    RequestContext.set_context_var(key="trace_id", value=trace_id)
    response: Response = await call_next(request)
    response.headers.append("trace_id", trace_id)

    request_url_path: str = request.url.path
    time_taken: time = time.time() - start_time
    response_status_code: int = response.status_code

    route = request.scope.get("route")
    if route and isinstance(route, APIRoute):
        tags: list = route.tags
    else:
        tags: list = []

    print(
        f"Env: {env}, "
        f"API tag: {tags}, "
        f"Http Method: {request.method}, "
        f"Request Path: {request_url_path}, "
        f"Time Taken: {time_taken}, "
        f"Request ID: {trace_id}, "
        f"Response Status Code: {response_status_code}, "
        f"Query Parameters: {dict(request.query_params)}"
    )
    return response


if __name__ == "__main__":
    app.include_router(api_router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
