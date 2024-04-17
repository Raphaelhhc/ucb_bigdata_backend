# restapi/recommend_restapi.py

from flask import request, jsonify, current_app
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

@blp_recommend.route('/recommend/cache')
class RecommendCacheResource(MethodView):
    
    @blp_recommend.response(200)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No data provided")
        findresult = current_app.db.recommend.find_one({
            "place": data.get('place'),
            "this_year": data.get('this_year'),
            "past_span": data.get('past_span'),
            "day_span": data.get('day_span')
        })
        if findresult:
            return {
                "input":{
                    "place": data.get('place'),
                    "this_year": data.get('this_year'),
                    "past_span": data.get('past_span'),
                    "day_span": data.get('day_span'),
                },
                "recommend_date": findresult.get('recommend_date'),
                "recommend_date_probability": findresult.get('recommend_date_probability')
            }
        else:
            return None

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
            recommend_analyzer.temperature_probabilities
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