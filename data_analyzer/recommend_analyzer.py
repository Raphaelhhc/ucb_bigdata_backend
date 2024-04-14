# package: data_analyzer
# recommend_analyzer.py

from typing import List, Dict
from dataclasses import asdict
from flask import current_app
import numpy as np
import datetime

from model.recommend_models import RecommendDate

class RecommendAnalyzer:
    def __init__(
        self, 
        place: str, 
        this_year: int, 
        past_span: int, 
        day_span: int, 
        rain_volume_probabilities: Dict[str, Dict[str, float]],
        temperature_probabilities: Dict[str, Dict[str, float]],
        rain_volume_scores: List[tuple],
        temperature_scores: List[tuple]
    ):
        self.place: str = place
        self.this_year: int = this_year
        self.past_span: int = past_span
        self.day_span: int = day_span
        self.overall_scores: List[tuple] = [
            (i, rain_volume_scores[i][1] + temperature_scores[i][1]) for i in range(len(rain_volume_scores))
        ]
        self.rain_volume_probabilities: Dict[str, Dict[str, float]] = rain_volume_probabilities
        self.temperature_probabilities: Dict[str, Dict[str, float]] = temperature_probabilities
        self.recommend_date: List[tuple] = []
        self.recommend_date_probability: List[List[Dict[str, float]]] = []
    
    def recommend_index(self) -> List[int]:
        scores: List[float] = [score for _, score in self.overall_scores]
        deviation: float = np.std(scores)
        maxscore: float = max(scores)
        criteria: float = maxscore - (deviation / 4)
        recommend_index: List[int] = []
        sorted_overall_scores: List[tuple] = sorted(self.overall_scores, key=lambda x: x[1], reverse=True)
        for i, s in sorted_overall_scores:
            if s < criteria:
                break
            recommend_index.append(i)
        return recommend_index
    
    def group_recommend_index(self, recommend_index: List[int]) -> List[List[int]]:
        sorted_recommend_index: List[int] = sorted(recommend_index)
        recommend_index_groups: List[List[int]] = [[sorted_recommend_index[0]]]
        for index in sorted_recommend_index[1:]:
            if index <= recommend_index_groups[-1][-1] + self.day_span + 5:
                recommend_index_groups[-1].append(index)
            else:
                recommend_index_groups.append([index])
        return recommend_index_groups

    def calculate_recommend_date(self) -> None: 
        recommend_index = self.recommend_index()
        recommend_index_groups = self.group_recommend_index(recommend_index)
        start_of_year: datetime.date = datetime.date(self.this_year, 1, 1)
        for group in recommend_index_groups:
            start_day_index: int = group[0]
            start_day_date: datetime.date = start_of_year + datetime.timedelta(days=start_day_index)
            start_day_date_str: str = start_day_date.strftime("%y/%m/%d")
            end_day_index: int = group[-1] + self.day_span
            end_day_date: datetime.date = start_of_year + datetime.timedelta(days=end_day_index)
            end_day_date_str: str = end_day_date.strftime("%y/%m/%d")
            self.recommend_date.append((start_day_date_str, end_day_date_str))
            rain_probability_dict_start = self.rain_volume_probabilities[str(start_day_index)]
            temperature_probability_dict_start = self.temperature_probabilities[str(start_day_index)]
            rain_probability_dict_end = self.rain_volume_probabilities[str(end_day_index - self.day_span)]
            temperature_probability_dict_end = self.temperature_probabilities[str(end_day_index - self.day_span)]
            self.recommend_date_probability.append([rain_probability_dict_start, temperature_probability_dict_start, rain_probability_dict_end, temperature_probability_dict_end])
    
    def get_recommend_date(self) -> List[tuple]:
        return self.recommend_date
    
    def get_recommend_date_probability(self) -> List[List[Dict[str, float]]]:
        return self.recommend_date_probability
    
    def save_recommend_date(self) -> None:
        recommenddate = RecommendDate(
            place=self.place,
            this_year=self.this_year,
            past_span=self.past_span,
            day_span=self.day_span,
            recommend_date=self.recommend_date,
            recommend_date_probability=self.recommend_date_probability
        )
        try:
            current_app.db.recommend.insert_one(asdict(recommenddate))
        except Exception as e:
            print(f"An database storage error occurred: {e}")