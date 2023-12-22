from dotenv import load_dotenv
from db.database import engine
from celery import Celery
from typing import Optional, List
import os

load_dotenv(dotenv_path=".env")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
celery.conf.timezone = "Europe/Moscow"
