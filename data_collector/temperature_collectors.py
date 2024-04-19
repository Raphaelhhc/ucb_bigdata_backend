# data_collector/temperature_collectors.py

import requests
import json
from typing import List, Any
from dataclasses import asdict
from flask import current_app
import time

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
    
    def sendtask_get_save_temperature(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            task_data = {
                "lat": self.lat,
                "lon": self.lon,
                "year": year
            }
            current_app.rabbitmq_manager.send_task_to_queue(task_data, "queue_temperature")
    
    def collect_temperature_after_task_process(self) -> None:
        for year in range(self.this_year - self.past_span, self.this_year):
            retries = 10
            delay = 1
            while retries > 0:
                document = current_app.db.temperature_eachyear.find_one({
                    "lat": self.lat,
                    "lon": self.lon,
                    "year": year
                })
                if document:
                    self.temperature_lists.append(document['temperature'])
                    break
                else:
                    time.sleep(delay)
                    retries -= 1
            if retries == 0:
                print(f"Failed to get temperature data for year {year}")
    
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
