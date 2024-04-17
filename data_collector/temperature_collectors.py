# data_collector/temperature_collectors.py

import requests
from typing import List, Any
from dataclasses import asdict
from flask import current_app

from model.temperature_models import Temperature

class TemperatureCollector:
    def __init__(
        self, 
        place: str, 
        lat: float, 
        lon: float, 
        this_year: int, 
        past_span: int
    ):
        self.place: str = place
        self.lat: float = lat
        self.lon: float = lon
        self.this_year: int = this_year
        self.past_span: int = past_span
        self.temperature_lists: List[List[float]] = []

    def get_temperature(self, lat: float, lon: float, year: int) -> List[float]:
        url: str = "https://archive-api.open-meteo.com/v1/archive"
        params: dict = {
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "apparent_temperature_mean"
        }
        response: Any = requests.get(url, params=params)
        data: dict = response.json()
        temperature: List[float] = data['daily']['apparent_temperature_mean']
        return temperature
    
    def collect_temperatures(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            temperature: List[float] = self.get_temperature(self.lat, self.lon, year)
            self.temperature_lists.append(temperature)
    
    def get_collect_temperatures(self) -> List[List[float]]:
        return self.temperature_lists
    
    def save_temperatures(self) -> None:
        temperature = Temperature(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            temperature_days=self.temperature_lists
        )
        try:
            current_app.db.temperature.insert_one(asdict(temperature))
        except Exception as e:
            print(f"An database storage error occurred: {e}")
