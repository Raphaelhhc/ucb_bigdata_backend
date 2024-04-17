# unittest/test_temperature_collectors.py

import unittest
from unittest.mock import patch, MagicMock
from data_collector.temperature_collectors import TemperatureCollector

class TestTemperatureCollector(unittest.TestCase):
    def setUp(self):
        self.collector = TemperatureCollector(
            place="TestPlace",
            lat=34.05,
            lon=-118.25,
            this_year=2023,
            past_span=5
        )
    
    @patch('data_collector.temperature_collectors.requests.get')
    def test_get_temperature(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'daily': {'apparent_temperature_mean': [15.0, 15.5, 16.0]}
        }
        mock_get.return_value = mock_response
        result = self.collector.get_temperature(34.05, -118.25, 2023)
        self.assertEqual(result, [15.0, 15.5, 16.0])
        mock_get.assert_called_once_with(
            'https://archive-api.open-meteo.com/v1/archive',
            params={
                'latitude': 34.05,
                'longitude': -118.25,
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'daily': 'apparent_temperature_mean'
            }
        )
    
    @patch('data_collector.temperature_collectors.TemperatureCollector.get_temperature')
    def test_collect_temperatures(self, mock_get_temperature):
        mock_get_temperature.side_effect = [
            [10.0, 10.5], [11.0, 11.5], [12.0, 12.5], [13.0, 13.5], [14.0, 14.5]
        ]
        self.collector.collect_temperatures()
        self.assertEqual(len(self.collector.temperature_lists), 5)
        self.assertEqual(self.collector.temperature_lists[0], [10.0, 10.5])
        self.assertEqual(self.collector.temperature_lists[1], [11.0, 11.5])

    

if __name__ == '__main__':
    unittest.main()
