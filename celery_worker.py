from dotenv import load_dotenv
from db.database import engine
from db.models import City, WeatherHistory
from sqlmodel import Session
from celery import Celery
from celery.schedules import crontab
from typing import Optional, List
from utils.loggers import logger
from utils.utils import get_weather_by_city
import os

load_dotenv(dotenv_path=".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.timezone = "Europe/Moscow"


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(crontab(minute="*/5"), upload_weather.s())


@celery.task
def upload_weather():
    with Session(engine) as session:
        logger.info(f"[WEATHER GATHER START]")

        # init
        output = []
        errors = 0

        # Get cities
        cities = session.query(City.name).all()

        # Get weather
        for city in cities:
            name = city["name"]
            result = get_weather_by_city(city=name)
            if result["status"] == "error":
                errors += 1
                continue

            data = result["data"]

            weather_history_record = WeatherHistory(
                city=name,
                temperature=data.get("temperature"),
                conditions=data.get("conditions"),
                wind_speed=data.get("wind_speed"),
                date_and_time=data.get("date_and_time"),
            )

            session.add(weather_history_record)
            output.append(data)

        session.commit()

        logger.info("[WEATHER GATHER RELOAD END]\n")
        return {"status": "Weather data uploaded"}
