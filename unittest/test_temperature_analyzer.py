# unittest/test_temperature_analyzer.py

import unittest
from unittest.mock import MagicMock
from data_analyzer.temperature_analyzer import TemperatureAnalyzer
from util.constants import DAYS_OF_YEAR, TEMPERATURE_SCENES, TEMPERATURE_SCENES_WEIGHT

class TestTemperatureAnalyzer(unittest.TestCase):
    def setUp(self):
        self.temperature_lists = [
            [-1] * DAYS_OF_YEAR,
            [5] * DAYS_OF_YEAR,
            [10] * DAYS_OF_YEAR,
            [17] * DAYS_OF_YEAR,
            [22] * DAYS_OF_YEAR,
            [27] * DAYS_OF_YEAR,
            [35] * DAYS_OF_YEAR
        ]
        self.analyzer = TemperatureAnalyzer(
            place="TestPlace",
            this_year=2023,
            past_span=7,
            day_span=2,
            temperature_lists=self.temperature_lists
        )

    def test_calculate_temperature_probabilities(self):
        self.analyzer.calculate_temperature_probabilities()
        expected_probability = 1 / self.analyzer.past_span
        for day in range(DAYS_OF_YEAR - self.analyzer.day_span):
            expected_probabilities = {scene: expected_probability for scene in TEMPERATURE_SCENES.keys()}
            self.assertEqual(self.analyzer.get_temperature_probabilities()[str(day)], expected_probabilities)

    def test_calculate_temperature_scores(self):
        self.analyzer.calculate_temperature_probabilities()
        self.analyzer.calculate_temperature_scores()
        expected_score = sum([TEMPERATURE_SCENES_WEIGHT[scene] * expected_probability 
                              for scene, expected_probability in zip(TEMPERATURE_SCENES.keys(), [1/7]*7)])
        for day in range(DAYS_OF_YEAR - self.analyzer.day_span):
            self.assertAlmostEqual(self.analyzer.get_temperature_scores()[day][1], expected_score, places=2)


if __name__ == '__main__':
    unittest.main()
