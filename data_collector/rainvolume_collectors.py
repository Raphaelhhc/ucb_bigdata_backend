# data_collector/rainvolume_collectors.py

import requests
import json
from typing import List, Any
from dataclasses import asdict
from flask import current_app
import time

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
    
    def sendtask_get_save_rain_volume(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            task_data = {
                "lat": self.lat,
                "lon": self.lon,
                "year": year
            }
            current_app.rabbitmq_manager.send_task_to_queue(task_data, "queue_rainvolume")
    
    def collect_rain_volumes_after_task_process(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            retries = 10
            delay = 1
            while retries > 0:
                document = current_app.db.rainvolume_eachyear.find_one({
                    "lat": self.lat,
                    "lon": self.lon,
                    "year": year
                })
                if document:
                    self.rain_volume_lists.append(document['rain_volume'])
                    break
                else:
                    time.sleep(delay)
                    retries -= 1
            if retries == 0:
                print(f"Failed to get rain volume data for year {year}")
    
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