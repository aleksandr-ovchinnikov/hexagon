from dotenv import load_dotenv
from utils.loggers import logger
from datetime import datetime, date
import requests
import json
import os


load_dotenv(dotenv_path=".env")
API_KEY = os.environ.get("API_KEY")


def validate_city(city: str) -> bool:
    # init
    url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={API_KEY}"

    # Send request
    response = requests.get(url=url)
    if not response.ok:
        logger.info(f"Code: {response.status_code}, text: {response.text}")
        return False
    return True


def get_weather_by_city(city: str) -> dict:
    try:
        # init
        url = f"https://api.weatherapi.com/v1/current.json?q={city}&key={API_KEY}"
        output = {}

        # Send request
        response = requests.get(url=url)
        if not response.ok:
            logger.error(
                f"An error in weather reponse for city [{city}]: {response.text}"
            )
            return {
                "status": "error",
                "code": response.status_code,
                "text": response.text,
            }

        data = json.loads(response.text)["current"]
        output = {
            "city": city,
            "temperature": data.get("temp_c"),
            "conditions": data.get("condition", {}).get("text"),
            "wind_speed": data.get("wind_kph"),
            "date_and_time": datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return {"status": "done", "data": output}

    except Exception as e:
        logger.error(f"An error occurred while getting weather for city[{city}]: {e}")
        return {"status": "error", "text": e}
