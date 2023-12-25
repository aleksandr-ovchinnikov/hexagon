from sqlmodel import SQLModel, Field, JSON, Column
from typing import List, Optional
from datetime import datetime, date


class City(SQLModel, table=True):
    name: str = Field(primary_key=True, description="Name of the city")


class WeatherHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    city: Optional[str] = Field(default=None, foreign_key="city.name")
    temperature: float = Field(description="Temperature outside", default=None)
    conditions: str = Field(description="Weather conditions in text", default=None)
    wind_speed: float = Field(description="Wind speed", default=None)
    date_and_time: datetime = Field(
        description="Date and time of mesurement", default=None
    )
