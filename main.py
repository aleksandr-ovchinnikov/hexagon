from fastapi import FastAPI
from db.database import init_db
from routers.test import router as test_router
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn


app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(test_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
