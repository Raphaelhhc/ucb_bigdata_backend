# unittest/test_rainvolume_analyzer.py

import unittest
from unittest.mock import MagicMock
from data_analyzer.rainvolume_analyzer import RainVolumeAnalyzer
from util.constants import DAYS_OF_YEAR, RAIN_SCENES, RAIN_SCENES_WEIGHT

class TestRainVolumeAnalyzer(unittest.TestCase):
    def setUp(self):
        self.rain_volumes = [
            [0.0] * DAYS_OF_YEAR,
            [0.5] * DAYS_OF_YEAR,
            [10.0] * DAYS_OF_YEAR,
            [20.0] * DAYS_OF_YEAR
        ]
        self.analyzer = RainVolumeAnalyzer(
            place="TestPlace",
            this_year=2023,
            past_span=4,
            day_span=2,
            rain_volume_lists=self.rain_volumes
        )

    def test_calculate_rain_volume_probabilities(self):
        self.analyzer.calculate_rain_volume_probabilities()
        expected_probability = 1 / self.analyzer.past_span
        expected_probabilities = {scene: expected_probability if i < self.analyzer.past_span else 0 
                                  for i, scene in enumerate(RAIN_SCENES.keys())}
        for day in range(DAYS_OF_YEAR - self.analyzer.day_span):
            self.assertEqual(self.analyzer.get_rain_volume_probabilities()[str(day)], expected_probabilities)

    def test_calculate_rain_volume_scores(self):
        self.analyzer.calculate_rain_volume_probabilities()
        self.analyzer.calculate_rain_volume_scores()
        expected_score = sum([RAIN_SCENES_WEIGHT[scene] * (1 / self.analyzer.past_span) 
                              for scene in RAIN_SCENES.keys()])
        for day in range(DAYS_OF_YEAR - self.analyzer.day_span):
            self.assertAlmostEqual(self.analyzer.get_rain_volume_scores()[day][1], expected_score, places=2)


if __name__ == '__main__':
    unittest.main()
