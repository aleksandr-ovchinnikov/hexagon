from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session
from datetime import date
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(tags=["Тестовые эндпоинты"])


@router.get(
    "/test",
    name="Тестовое имя",
    description="Какое-то тестовое описание",
)
async def get_stocks_manual():
    return JSONResponse(jsonable_encoder({"status": "Done"}), status_code=status.HTTP_200_OK)
