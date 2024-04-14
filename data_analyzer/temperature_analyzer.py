# package: data_analyzer
# temperature_analyzer.py

from typing import List, Dict
from dataclasses import asdict
from flask import current_app

from util.constants import DAYS_OF_YEAR, TEMPERATURE_SCENES, TEMPERATURE_SCENES_WEIGHT
from model.temperature_models import TemperatureProbability, TemperatureScore

class TemperatureAnalyzer:
    def __init__(
        self, 
        place: str, 
        this_year: int, 
        past_span: int, 
        day_span: int, 
        temperature_lists: List[List[float]]
    ):
        self.place: str = place
        self.this_year: int = this_year
        self.past_span: int = past_span
        self.day_span: int = day_span
        self.temperature_lists: List[List[float]] = temperature_lists
        self.temperature_probabilities: Dict[str, Dict[str, float]] = {}
        self.temperature_scores: List[tuple] = []
    
    def calculate_temperature_probabilities(self) -> None:
        for i in range(DAYS_OF_YEAR - self.day_span):
            counter: Dict[str, int] = {scene: 0 for scene in TEMPERATURE_SCENES.keys()}
            for j in range(self.day_span):
                for k in range(self.past_span):
                    temperature: float = self.temperature_lists[k][i + j]
                    for scene, upper_limit in TEMPERATURE_SCENES.items():
                        if upper_limit is None or temperature <= upper_limit:
                            counter[scene] += 1
                            break
            probability: Dict[str, float] = {scene: count / (self.day_span * self.past_span) for scene, count in counter.items()}
            self.temperature_probabilities[str(i)] = probability
    
    def calculate_temperature_scores(self) -> None:
        for i in range(DAYS_OF_YEAR - self.day_span):
            score: float = 0
            for scene, probability in self.temperature_probabilities[str(i)].items():
                score += TEMPERATURE_SCENES_WEIGHT[scene] * probability
            self.temperature_scores.append((i, score))
    
    def get_temperature_probabilities(self) -> Dict[str, Dict[str, float]]:
        return self.temperature_probabilities
    
    def get_temperature_scores(self) -> List[tuple]:
        return self.temperature_scores
    
    def save_temperature_probabilities(self) -> None:
        temperature_probability = TemperatureProbability(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            day_span=self.day_span,
            temperature_probabilities=self.temperature_probabilities
        )
        try:
            current_app.db.temperature_probability.insert_one(asdict(temperature_probability))
        except Exception as e:
            print(f"An database storage error occurred: {e}")
    
    def save_temperature_scores(self) -> None:
        temperature_score = TemperatureScore(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            day_span=self.day_span,
            temperature_scores=self.temperature_scores
        )
        try:
            current_app.db.temperature_score.insert_one(asdict(temperature_score))
        except Exception as e:
            print(f"An database storage error occurred: {e}")
