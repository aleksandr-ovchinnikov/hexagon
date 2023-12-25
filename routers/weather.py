from fastapi import APIRouter, Depends, Query, status
from utils.utils import validate_city, get_weather_by_city
from utils.loggers import logger
from db.database import get_session
from db.models import City, WeatherHistory
from sqlmodel import Session, text
from sqlalchemy.orm import aliased
from datetime import date
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from celery_worker import upload_weather

router = APIRouter(tags=["Работа с API погоды"], prefix="/api/v1")


@router.post(
    "/city",
    name="Добавить город",
    description="Функция добавления города в отслеживание погоды",
)
async def add_city(*, session: Session = Depends(get_session), city: str):
    try:
        if not validate_city(city=city):
            logger.error(f"City [{city}] not found on API!")
            return JSONResponse(
                jsonable_encoder({"status": "error", "text": "City not found"}),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        instance = session.query(City).where(City.name == city).first()
        if instance:
            return JSONResponse(
                jsonable_encoder({"status": "Already exists"}),
                status_code=status.HTTP_208_ALREADY_REPORTED,
            )

        new_city = City(name=city)
        session.add(new_city)
        session.commit()
        session.refresh(new_city)
        return JSONResponse(
            jsonable_encoder({"status": "Created"}), status_code=status.HTTP_201_CREATED
        )

    except Exception as e:
        logger.error(f"An error occurred while adding new city to DB: {e}")
        return JSONResponse(
            jsonable_encoder({"status": "error", "text": e}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.post(
    "/all",
    name="Загрузить вручную погоду по всем городам",
    description="Загрузить вручную погоду по всем городам и загрузить в БД",
)
def get_all_weather():
    upload_weather.delay()
    return JSONResponse(
        jsonable_encoder({"status": "Started. See flower..."}),
        status_code=status.HTTP_200_OK,
    )


@router.delete(
    "/city",
    name="Удалить город из отслеживания",
    description="Удалить город из отслеживания",
)
def delete_city(*, session: Session = Depends(get_session), city: str):
    try:
        city_to_delete = session.query(City).where(City.name == city).first()
        session.query(WeatherHistory).filter_by(city=city).delete()
        session.delete(city_to_delete)
        session.commit()
        return JSONResponse(
            jsonable_encoder({"status": "done"}), status_code=status.HTTP_200_OK
        )

    except Exception as e:
        logger.error(f"An error occurred while deleting city [{city}] from DB: {e}")
        return JSONResponse(
            jsonable_encoder({"status": "error", "text": e}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get(
    "/all",
    name="Получить последнюю погоду по всем городам",
    description="Получить последнюю погоду по всем городам",
)
def get_all_weather(*, session: Session = Depends(get_session)):
    try:
        # init
        output = []

        sql_query = text(
            """
            SELECT DISTINCT ON (city.name)
                city.name,
                weatherhistory.temperature,
                weatherhistory.conditions,
                weatherhistory.wind_speed,
                TO_CHAR(weatherhistory.date_and_time, 'YYYY-MM-DD HH24:MI:SS') AS date_and_time
            FROM
                city
                JOIN weatherhistory ON city.name = weatherhistory.city
            ORDER BY
                city.name,
                weatherhistory.date_and_time DESC
            """
        )

        result = session.execute(sql_query)
        output = result.fetchall()

        return JSONResponse(
            jsonable_encoder({"status": "done", "data": output}),
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"An error occurred while getting weather data from DB: {e}")
        return JSONResponse(
            jsonable_encoder({"status": "error", "text": e}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get(
    "/weather/city",
    name="Получить последнюю погоду по конкретному городу",
    description="Получить последнюю погоду по всем конкретному городу",
)
def get_all_weather(*, session: Session = Depends(get_session), city: str):
    try:
        # init
        output = []

        sql_query = text(
            f"""
            SELECT weatherhistory.temperature, weatherhistory.wind_speed
            FROM weatherhistory
            WHERE city = '{city}' 
            AND date_trunc('day', date_and_time) = current_date
            ORDER BY date_and_time ASC;
            """
        )

        result = session.execute(sql_query)
        output = result.fetchall()

        return JSONResponse(
            jsonable_encoder({"status": "done", "data": output}),
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"An error occurred while getting weather data from DB: {e}")
        return JSONResponse(
            jsonable_encoder({"status": "error", "text": e}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
