# integrationtest/test_rainvolume_restapi.py

import pytest
import os
from app import app as flask_app
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
import certifi

@pytest.fixture
def app():
    flask_app.config['TESTING'] = True
    test_mongodb_uri = os.environ.get('MONGODB_URI_TEST')
    flask_app.config['MONGODB_URI'] = test_mongodb_uri
    flask_app.db = MongoClient(test_mongodb_uri, tlsCAFile=certifi.where()).WeatherPredictorTest
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@patch('data_collector.rainvolume_collectors.RainVolumeCollector.sendtask_get_save_rain_volume')
@patch('data_collector.rainvolume_collectors.RainVolumeCollector.collect_rain_volumes_after_task_process')
@patch('data_collector.rainvolume_collectors.RainVolumeCollector.get_collect_rain_volumes')
def test_rain_volume_collector_post(mock_get_collect, mock_collect_after, mock_send_save, client):
    mock_get_collect.return_value = [[0.2, 0.3, 0.5]]
    response = client.post('/rainvolumecollector', json={
        'place': 'Test Place', 'lat': 34.05, 'lon': -118.25, 'this_year': 2023, 'past_span': 5
    })
    assert response.status_code == 201
    assert response.get_json() == {'rain_volume_lists': [[0.2, 0.3, 0.5]]}

    mock_send_save.assert_called_once()
    mock_collect_after.assert_called_once()
    mock_get_collect.assert_called_once()

@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.calculate_rain_volume_probabilities')
@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.calculate_rain_volume_scores')
@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.save_rain_volume_probabilities')
@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.save_rain_volume_scores')
@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.get_rain_volume_probabilities')
@patch('data_analyzer.rainvolume_analyzer.RainVolumeAnalyzer.get_rain_volume_scores')
def test_rain_volume_analyzer_post(mock_get_scores, mock_get_probs, mock_save_scores, mock_save_probs, mock_calc_scores, mock_calc_probs, client):
    mock_get_scores.return_value = [(0, 0.5)]
    mock_get_probs.return_value = {'0': {'no rain': 0.8, 'light rain': 0.2}}
    response = client.post('/rainvolumeanalyzer', json={
        'place': 'Test Place', 'this_year': 2023, 'past_span': 5, 'day_span': 30, 'rain_volume_lists': [[0.2, 0.3, 0.5]]
    })
    assert response.status_code == 201
    assert response.get_json() == {
        'rain_volume_probabilities': {'0': {'no rain': 0.8, 'light rain': 0.2}},
        'rain_volume_scores': [[0, 0.5]]
    }

    mock_calc_probs.assert_called_once()
    mock_calc_scores.assert_called_once()
    mock_save_probs.assert_called_once()
    mock_save_scores.assert_called_once()
    mock_get_probs.assert_called_once()
    mock_get_scores.assert_called_once()