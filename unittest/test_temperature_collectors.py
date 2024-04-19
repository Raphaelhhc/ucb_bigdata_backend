# unittest/test_temperature_collectors.py

import unittest
from unittest.mock import patch, MagicMock
from data_collector.temperature_collectors import TemperatureCollector
from app import app
from flask import current_app
import os

class TestTemperatureCollector(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True 
        self.app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI_TEST', 'mongodb://localhost:27017/testdb') 
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.collector = TemperatureCollector(
            place="TestPlace",
            lat=34.05,
            lon=-118.25,
            this_year=2023,
            past_span=5
        )
    
    def tearDown(self):
        self.app_context.pop()
    
    @patch('data_collector.temperature_collectors.current_app')
    def test_sendtask_get_save_temperature(self, mock_app):
        mock_manager = MagicMock()
        mock_app.rabbitmq_manager = mock_manager
        self.collector.sendtask_get_save_temperature()
        self.assertEqual(mock_manager.send_task_to_queue.call_count, 5)

    @patch('data_collector.temperature_collectors.current_app')
    def test_collect_temperature_after_task_process(self, mock_app):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_app.db.temperature_eachyear = mock_collection
        mock_collection.find_one.return_value = {'temperature': [0.0, 1.0]}
        
        self.collector.collect_temperature_after_task_process()
        self.assertEqual(len(self.collector.temperature_lists), 5) 
        mock_collection.find_one.assert_called()

    

if __name__ == '__main__':
    unittest.main()
