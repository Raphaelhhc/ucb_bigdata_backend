# integratedtest/test_recommend_restapi.py

import pytest
import os
from app import app as flask_app
from unittest.mock import patch
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

@patch('data_analyzer.recommend_analyzer.RecommendAnalyzer.calculate_recommend_date')
@patch('data_analyzer.recommend_analyzer.RecommendAnalyzer.save_recommend_date')
@patch('data_analyzer.recommend_analyzer.RecommendAnalyzer.get_recommend_date')
@patch('data_analyzer.recommend_analyzer.RecommendAnalyzer.get_recommend_date_probability')
def test_recommend_post(mock_get_recommend_date_probability, mock_get_recommend_date, mock_save_recommend_date, mock_calculate_recommend_date, client):
    mock_get_recommend_date.return_value = [['23/06/03', '23/06/10']]
    mock_get_recommend_date_probability.return_value = [
        [{'rain': 0.3, 'temperature': 0.7}, {'rain': 0.4, 'temperature': 0.6}]
    ]

    response = client.post('/recommend', json={
        'place': 'New York',
        'this_year': 2023,
        'past_span': 5,
        'day_span': 30,
        'rain_volume_probabilities': {'0': {'light rain': 0.2}},
        'temperature_probabilities': {'0': {'moderate': 0.5}},
        'rain_volume_scores': [(0, 0.2)],
        'temperature_scores': [(0, 0.5)]
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'recommend_date' in data
    assert data['recommend_date'] == [['23/06/03', '23/06/10']]
    assert 'recommend_date_probability' in data
    assert data['recommend_date_probability'] == [
        [{'rain': 0.3, 'temperature': 0.7}, {'rain': 0.4, 'temperature': 0.6}]
    ]

    mock_calculate_recommend_date.assert_called_once()
    mock_save_recommend_date.assert_called_once()
    mock_get_recommend_date.assert_called_once()
    mock_get_recommend_date_probability.assert_called_once()
