# package: restapi
# recommend_restapi.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import current_app
from bson import json_util

from data_collector.rainvolume_collectors import RainVolumeCollector
from data_analyzer.rainvolume_analyzer import RainVolumeAnalyzer
from data_collector.temperature_collectors import TemperatureCollector
from data_analyzer.temperature_analyzer import TemperatureAnalyzer
from data_analyzer.recommend_analyzer import RecommendAnalyzer

blp_recommend = Blueprint('recommend', 'recommend', description='Operations on recommend')

####################
blp_test = Blueprint('test', 'test', description='Test operations')
@blp_test.route('/test')
class TestResource(MethodView):
        @blp_test.response(200)
        def post(self):
            data = request.json
            if not data:
                abort(400, description="No data provided")
            return {
                "input":{
                    "place": data.get('place'),
                    "this_year": data.get('this_year'),
                    "past_span": data.get('past_span'),
                    "day_span": data.get('day_span'),
                },
                "recommend_date": [('24/01/01', '24/03/20'), ('24/12/05', '24/12/30')],
                "recommend_date_probability": [
                    [
                        {'no rain': 0.4, 'slight rain': 0.44, 'heavy rain': 0.16, 'very heavy rain': 0.0},
                        {'very cold': 0.0, 'cold': 0.04, 'cool': 0.14, 'medium': 0.64, 'warm': 0.18, 'hot': 0.0, 'very hot': 0.0},
                        {'no rain': 0.44, 'slight rain': 0.42, 'heavy rain': 0.14, 'very heavy rain': 0.0},
                        {'very cold': 0.0, 'cold': 0.0, 'cool': 0.1, 'medium': 0.3, 'warm': 0.52, 'hot': 0.08, 'very hot': 0.0}
                    ],
                    [
                        {'no rain': 0.32, 'slight rain': 0.54, 'heavy rain': 0.1, 'very heavy rain': 0.04},
                        {'very cold': 0.0, 'cold': 0.0, 'cool': 0.1, 'medium': 0.46, 'warm': 0.38, 'hot': 0.06, 'very hot': 0.0},
                        {'no rain': 0.34, 'slight rain': 0.5, 'heavy rain': 0.14, 'very heavy rain': 0.02},
                        {'very cold': 0.0, 'cold': 0.02, 'cool': 0.34, 'medium': 0.36, 'warm': 0.28, 'hot': 0.0, 'very hot': 0.0}
                    ]
                ]
            }
####################

@blp_recommend.route('/recommend')
class RecommendResource(MethodView):
    
    @blp_recommend.response(200)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No data provided")
        recommend_analyzer = RecommendAnalyzer(
            place=data.get('place'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span'),
            day_span=data.get('day_span'),
            rain_volume_probabilities=data.get('rain_volume_probabilities'),
            temperature_probabilities=data.get('temperature_probabilities'),
            rain_volume_scores=data.get('rain_volume_scores'),
            temperature_scores=data.get('temperature_scores')
        )
        if not all([
            recommend_analyzer.place, 
            recommend_analyzer.this_year, 
            recommend_analyzer.past_span, 
            recommend_analyzer.day_span,
            recommend_analyzer.overall_scores,
            recommend_analyzer.rain_volume_probabilities,
            recommend_analyzer.temperature_probabilities,
            recommend_analyzer.recommend_date,
            recommend_analyzer.recommend_date_probability
        ]):
            abort(400, description="Missing necessary recommendation data")
        try:
            recommend_analyzer.calculate_recommend_date()
            recommend_analyzer.save_recommend_date()
        except Exception as e:
            abort(500, description=f"An error occurred while saving the data: {e}")
        recommenddate = recommend_analyzer.get_recommend_date()
        recommenddate_probability = recommend_analyzer.get_recommend_date_probability()
        return {
                "input":{
                    "place": data.get('place'),
                    "this_year": data.get('this_year'),
                    "past_span": data.get('past_span'),
                    "day_span": data.get('day_span'),
                },
                "recommend_date": recommenddate,
                "recommend_date_probability": recommenddate_probability
            }