import uvicorn as uvicorn
from fastapi import HTTPException
from starlette.responses import JSONResponse

from app import get_app
from app.api import api_router

app = get_app()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    api = request.url
    print("API = {}, exc.detail:{}".format(api, exc.detail))
    return JSONResponse(status_code=exc.status_code, content={
        "status_code": exc.status_code,
        "message": exc.detail,
        "data": {}
    })


if __name__ == "__main__":
    app.include_router(api_router)
    uvicorn.run(app, host="0.0.0.0", port=8000)
