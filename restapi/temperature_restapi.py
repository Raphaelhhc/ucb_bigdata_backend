# restapi/temperature_restapi.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import current_app
from bson import json_util

from data_collector.temperature_collectors import TemperatureCollector
from data_analyzer.temperature_analyzer import TemperatureAnalyzer

blp_temperaturecollector = Blueprint('temperaturecollector', 'temperaturecollector', description='Operations on temperaturecollector')
blp_temperatureanalyzer = Blueprint('temperatureanalyzer', 'temperatureanalyzer', description='Operations on temperatureanalyzer')

@blp_temperaturecollector.route('/temperaturecollector')
class TemperatureCollectorResource(MethodView):
    
    @blp_temperaturecollector.response(201)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No data provided")
        temp_collector = TemperatureCollector(
            place=data.get('place'),
            lat=data.get('lat'),
            lon=data.get('lon'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span')
        )
        if not all([
            temp_collector.place, 
            temp_collector.lat, 
            temp_collector.lon, 
            temp_collector.this_year, 
            temp_collector.past_span
        ]):
            abort(400, description="Missing necessary temperature data")
        try:
            temp_collector.collect_temperatures()
            temp_collector.save_temperatures()
            temperature_lists = temp_collector.get_collect_temperatures()
        except Exception as e:
            abort(500, description=f"An error occurred while saving the data: {e}")
        return {"temperature_lists": temperature_lists}

@blp_temperatureanalyzer.route('/temperatureanalyzer')
class TemperatureAnalyzerResource(MethodView):
        
    @blp_temperatureanalyzer.response(201)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No data provided")
        temp_analyzer = TemperatureAnalyzer(
            place=data.get('place'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span'),
            day_span=data.get('day_span'),
            temperature_lists=data.get('temperature_lists')
        )
        if not all([
            temp_analyzer.place, 
            temp_analyzer.this_year, 
            temp_analyzer.past_span, 
            temp_analyzer.day_span, 
            temp_analyzer.temperature_lists
        ]):
            abort(400, description="Missing necessary temperature data")
        try:
            temp_analyzer.calculate_temperature_probabilities()
            temp_analyzer.calculate_temperature_scores()
            temp_analyzer.save_temperature_probabilities()
            temp_analyzer.save_temperature_scores()
            temperature_probabilities = temp_analyzer.get_temperature_probabilities()
            temperature_scores = temp_analyzer.get_temperature_scores()
        except Exception as e:
            abort(500, description=f"An error occurred while saving the data: {e}")
        return {"temperature_probabilities": temperature_probabilities, "temperature_scores": temperature_scores}