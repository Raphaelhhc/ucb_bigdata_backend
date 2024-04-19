# unittest/test_rainvolume_collectors.py

import unittest
from unittest.mock import patch, MagicMock
from data_collector.rainvolume_collectors import RainVolumeCollector
from app import app
from flask import current_app
import os

class TestRainVolumeCollector(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI_TEST', 'mongodb://localhost:27017/testdb') 
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.collector = RainVolumeCollector(
            place="TestPlace",
            lat=34.05,
            lon=-118.25,
            this_year=2023,
            past_span=5
        )
    
    def tearDown(self):
        self.app_context.pop()
    
    @patch('data_collector.rainvolume_collectors.current_app')
    def test_sendtask_get_save_rain_volume(self, mock_app):
        mock_manager = MagicMock()
        mock_app.rabbitmq_manager = mock_manager
        self.collector.sendtask_get_save_rain_volume()
        self.assertEqual(mock_manager.send_task_to_queue.call_count, 5)

    @patch('data_collector.rainvolume_collectors.current_app')
    def test_collect_rain_volumes_after_task_process(self, mock_app):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_app.db.rainvolume_eachyear = mock_collection
        mock_collection.find_one.return_value = {'rain_volume': [0.0, 1.0]}
        
        self.collector.collect_rain_volumes_after_task_process()
        self.assertEqual(len(self.collector.rain_volume_lists), 5)
        mock_collection.find_one.assert_called()
    

if __name__ == '__main__':
    unittest.main()
