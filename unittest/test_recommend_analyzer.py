# unittest/test_recommend_analyzer.py

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from data_analyzer.recommend_analyzer import RecommendAnalyzer

class TestRecommendAnalyzer(unittest.TestCase):
    def setUp(self):
        self.rain_volume_probabilities = {
            "0": {"low": 0.2, "medium": 0.3, "high": 0.5},
            "1": {"low": 0.3, "medium": 0.4, "high": 0.3},
            "2": {"low": 0.5, "medium": 0.4, "high": 0.1}
        }
        self.temperature_probabilities = {
            "0": {"cold": 0.1, "mild": 0.5, "hot": 0.4},
            "1": {"cold": 0.2, "mild": 0.3, "hot": 0.5},
            "2": {"cold": 0.6, "mild": 0.3, "hot": 0.1}
        }
        self.rain_volume_scores = [(0, 50), (1, 60), (2, 40)]
        self.temperature_scores = [(0, 40), (1, 50), (2, 60)]
        self.analyzer = RecommendAnalyzer(
            place="TestPlace",
            this_year=2023,
            past_span=3,
            day_span=1,
            rain_volume_probabilities=self.rain_volume_probabilities,
            temperature_probabilities=self.temperature_probabilities,
            rain_volume_scores=self.rain_volume_scores,
            temperature_scores=self.temperature_scores
        )

    def test_calculate_recommend_date(self):
        self.analyzer.calculate_recommend_date()
        start_of_year = datetime(2023, 1, 1)
        expected_start_day = start_of_year + timedelta(days=1)
        expected_end_day = start_of_year + timedelta(days=1 + self.analyzer.day_span)
        expected_dates = (expected_start_day.strftime("%y/%m/%d"), expected_end_day.strftime("%y/%m/%d"))
        actual_dates = self.analyzer.get_recommend_date()
        self.assertEqual(actual_dates[0], expected_dates)


if __name__ == '__main__':
    unittest.main()
