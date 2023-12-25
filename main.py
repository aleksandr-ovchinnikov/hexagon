from fastapi import FastAPI
from db.database import init_db
from routers.weather import router as weather_router
from routers.frontend import router as frontend_router
from starlette.middleware.base import BaseHTTPMiddleware
from middleware.requests_middleware import log_request
import uvicorn


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


app.add_middleware(BaseHTTPMiddleware, dispatch=log_request)
app.include_router(weather_router)
app.include_router(frontend_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
