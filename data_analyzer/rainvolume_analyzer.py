# data_analyzer/rainvolume_analyzer.py

from typing import List, Dict
from dataclasses import asdict
from flask import current_app

from util.constants import DAYS_OF_YEAR, RAIN_SCENES, RAIN_SCENES_WEIGHT
from model.rainvolume_models import RainVolumeProbability, RainVolumeScore

class RainVolumeAnalyzer:
    def __init__(
        self, 
        place: str, 
        this_year: int, 
        past_span: int, 
        day_span: int, 
        rain_volume_lists: List[List[float]]
    ):
        self.place: str = place
        self.this_year: int = this_year
        self.past_span: int = past_span
        self.day_span: int = day_span
        self.rain_volume_lists: List[List[float]] = rain_volume_lists
        self.rain_volume_probabilities: Dict[str, Dict[str, float]] = {}
        self.rain_volume_scores: List[tuple] = []
    
    def calculate_rain_volume_probabilities(self) -> None:
        for i in range(DAYS_OF_YEAR - self.day_span):
            counter: Dict[str, int] = {scene: 0 for scene in RAIN_SCENES.keys()}
            for j in range(self.day_span):
                for k in range(self.past_span):
                    rain_volume: float = self.rain_volume_lists[k][i + j]
                    for scene, upper_limit in RAIN_SCENES.items():
                        if upper_limit is None or rain_volume <= upper_limit:
                            counter[scene] += 1
                            break
            probability: Dict[str, float] = {scene: count / (self.day_span * self.past_span) for scene, count in counter.items()}
            self.rain_volume_probabilities[str(i)] = probability
    
    def calculate_rain_volume_scores(self) -> None:
        for i in range(DAYS_OF_YEAR - self.day_span):
            score: float = 0
            for scene, probability in self.rain_volume_probabilities[str(i)].items():
                score += RAIN_SCENES_WEIGHT[scene] * probability
            self.rain_volume_scores.append((i, score))
    
    def get_rain_volume_probabilities(self) -> Dict[str, Dict[str, float]]:
        return self.rain_volume_probabilities
    
    def get_rain_volume_scores(self) -> List[tuple]:
        return self.rain_volume_scores
    
    def save_rain_volume_probabilities(self) -> None:
        rain_volume_probability = RainVolumeProbability(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            day_span=self.day_span,
            rainvolume_probabilities=self.rain_volume_probabilities
        )
        try:
            current_app.db.rainvolume_probability.insert_one(asdict(rain_volume_probability))
        except Exception as e:
            print(f"An database storage error occurred: {e}")
    
    def save_rain_volume_scores(self) -> None:
        rain_volume_score = RainVolumeScore(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            day_span=self.day_span,
            rainvolume_scores=self.rain_volume_scores
        )
        try:
            current_app.db.rainvolume_score.insert_one(asdict(rain_volume_score))
        except Exception as e:
            print(f"An database storage error occurred: {e}")