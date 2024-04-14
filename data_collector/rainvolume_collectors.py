# package: data_collector
# rainvolume_collectors.py

import requests
from typing import List, Any
from dataclasses import asdict
from flask import current_app

from model.rainvolume_models import RainVolume

class RainVolumeCollector:
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
        self.rain_volume_lists: List[List[float]] = []

    def get_rain_volume(self, lat: float, lon: float, year: int) -> List[float]:
        url: str = "https://archive-api.open-meteo.com/v1/archive"
        params: dict = {
            "latitude": lat,
            "longitude": lon,
            "start_date": f"{year}-01-01",
            "end_date": f"{year}-12-31",
            "daily": "rain_sum"
        }
        response: Any = requests.get(url, params=params)
        data: dict = response.json()
        rain_volume: List[float] = data['daily']['rain_sum']
        return rain_volume
    
    def collect_rain_volumes(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            rain_volume: List[float] = self.get_rain_volume(self.lat, self.lon, year)
            self.rain_volume_lists.append(rain_volume)
    
    def get_collect_rain_volumes(self) -> List[List[float]]:
        return self.rain_volume_lists
    
    def save_rain_volumes(self) -> None:
        rain_volume = RainVolume(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            rainvolume_days=self.rain_volume_lists
        )
        try:
            current_app.db.rainvolume.insert_one(asdict(rain_volume))
        except Exception as e:
            print(f"An database storage error occurred: {e}")