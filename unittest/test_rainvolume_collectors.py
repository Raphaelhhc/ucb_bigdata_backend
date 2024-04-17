# unittest/test_rainvolume_collectors.py

import unittest
from unittest.mock import patch, MagicMock
from data_collector.rainvolume_collectors import RainVolumeCollector

class TestRainVolumeCollector(unittest.TestCase):
    def setUp(self):
        self.collector = RainVolumeCollector(
            place="TestPlace",
            lat=34.05,
            lon=-118.25,
            this_year=2023,
            past_span=5
        )
    
    @patch('data_collector.rainvolume_collectors.requests.get')
    def test_get_rain_volume(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'daily': {'rain_sum': [0.0, 1.0, 0.5]}
        }
        mock_get.return_value = mock_response
        result = self.collector.get_rain_volume(34.05, -118.25, 2023)
        self.assertEqual(result, [0.0, 1.0, 0.5])
        mock_get.assert_called_once_with(
            'https://archive-api.open-meteo.com/v1/archive',
            params={
                'latitude': 34.05,
                'longitude': -118.25,
                'start_date': '2023-01-01',
                'end_date': '2023-12-31',
                'daily': 'rain_sum'
            }
        )
    
    @patch('data_collector.rainvolume_collectors.RainVolumeCollector.get_rain_volume')
    def test_collect_rain_volumes(self, mock_get_rain_volume):
        mock_get_rain_volume.side_effect = [
            [0.0, 1.0], [0.5, 0.2], [0.3, 0.3], [0.1, 0.0], [0.2, 0.4]
        ]
        self.collector.collect_rain_volumes()
        self.assertEqual(len(self.collector.rain_volume_lists), 5)
        self.assertEqual(self.collector.rain_volume_lists[0], [0.0, 1.0])
        self.assertEqual(self.collector.rain_volume_lists[1], [0.5, 0.2])
    

if __name__ == '__main__':
    unittest.main()
