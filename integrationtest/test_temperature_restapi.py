# integrationtest/test_temperature_restapi.py

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

@patch('data_collector.temperature_collectors.TemperatureCollector.sendtask_get_save_temperature')
@patch('data_collector.temperature_collectors.TemperatureCollector.collect_temperature_after_task_process')
@patch('data_collector.temperature_collectors.TemperatureCollector.get_collect_temperatures')
def test_temperature_collector_post(mock_get_collect_temperatures, mock_collect_temperature_after_task, mock_sendtask_get_save_temperature, client):
    mock_get_collect_temperatures.return_value = [[25.0, 22.5, 30.0]]
    response = client.post('/temperaturecollector', json={
        'place': 'Test City', 'lat': 40.7128, 'lon': -74.0060, 'this_year': 2023, 'past_span': 5
    })
    assert response.status_code == 201
    assert response.get_json() == {'temperature_lists': [[25.0, 22.5, 30.0]]}

    mock_sendtask_get_save_temperature.assert_called_once()
    mock_collect_temperature_after_task.assert_called_once()
    mock_get_collect_temperatures.assert_called_once()

@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.calculate_temperature_probabilities')
@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.calculate_temperature_scores')
@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.save_temperature_probabilities')
@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.save_temperature_scores')
@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.get_temperature_probabilities')
@patch('data_analyzer.temperature_analyzer.TemperatureAnalyzer.get_temperature_scores')
def test_temperature_analyzer_post(mock_get_scores, mock_get_probs, mock_save_scores, mock_save_probs, mock_calc_scores, mock_calc_probs, client):
    mock_get_scores.return_value = [(0, 0.5)]
    mock_get_probs.return_value = {'0': {'moderate': 0.7}}
    response = client.post('/temperatureanalyzer', json={
        'place': 'Test City', 'this_year': 2023, 'past_span': 5, 'day_span': 30, 'temperature_lists': [[25.0, 22.5, 30.0]]
    })
    assert response.status_code == 201
    assert response.get_json() == {
        'temperature_probabilities': {'0': {'moderate': 0.7}},
        'temperature_scores': [[0, 0.5]]
    }

    mock_calc_probs.assert_called_once()
    mock_calc_scores.assert_called_once()
    mock_save_probs.assert_called_once()
    mock_save_scores.assert_called_once()
    mock_get_probs.assert_called_once()
    mock_get_scores.assert_called_once()