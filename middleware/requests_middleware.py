from fastapi import Request
from fastapi.responses import JSONResponse
from uuid import uuid4
from contextvars import ContextVar
from utils.loggers import logger

request_id_var = ContextVar("request_id", default=None)


async def log_request(request: Request, call_next):
    request_id = str(uuid4())
    request_id_var.set(request_id)
    logger.info(f"[Request {request_id} started]")
    logger.info(f"Path: {request.method}:{request.url.path}")

    try:
        response = await call_next(request)
        logger.info(f"Request succeded!")
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return JSONResponse(content={"success": False}, status_code=400)
    finally:
        assert request_id_var.get() == request_id
        logger.info("[Request ended]\n")
    return response
