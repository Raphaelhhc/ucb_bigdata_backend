# restapi/rainvolume_restapi.py

from flask import request, jsonify
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import current_app
from bson import json_util

from data_collector.rainvolume_collectors import RainVolumeCollector
from data_analyzer.rainvolume_analyzer import RainVolumeAnalyzer

blp_rainvolumecollector = Blueprint('rainvolumecollector', 'rainvolumecollector', description='Operations on rainvolumecollector')
blp_rainvolumeanalyzer = Blueprint('rainvolumeanalyzer', 'rainvolumeanalyzer', description='Operations on rainvolumeanalyzer')

@blp_rainvolumecollector.route('/rainvolumecollector')
class RainVolumeCollectorResource(MethodView):
    
    @blp_rainvolumecollector.response(201)
    def post(self):
        print("start rainvolumecollector api!")
        data = request.json
        print("received data:", data)
        if not data:
            abort(400, description="No data provided")
        rain_collector = RainVolumeCollector(
            place=data.get('place'),
            lat=data.get('lat'),
            lon=data.get('lon'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span')
        )
        print("rain collector ctreated!")
        if not all([
            rain_collector.place, 
            rain_collector.lat, 
            rain_collector.lon, 
            rain_collector.this_year, 
            rain_collector.past_span
        ]):
            abort(400, description="Missing necessary rain volume data")
        try:
            print("start sendtask_get_save_rain_volume!")
            rain_collector.sendtask_get_save_rain_volume()
            print("start collect_rain_volumes_after_task_process!")
            rain_collector.collect_rain_volumes_after_task_process()
            print("start save_rain_volumes!")
            rain_collector.save_rain_volumes()
            print("start get_collect_rain_volumes!")
            rain_volume_lists = rain_collector.get_collect_rain_volumes()
        except Exception as e:
            current_app.logger.error(f"Failed processing in /rainvolumecollector: {str(e)}")
            abort(500, description=f"An error occurred while saving the data: {e}")
        return {"rain_volume_lists": rain_volume_lists}


@blp_rainvolumeanalyzer.route('/rainvolumeanalyzer')
class RainVolumeAnalyzerResource(MethodView):
        
    @blp_rainvolumeanalyzer.response(201)
    def post(self):
        data = request.json
        if not data:
            abort(400, description="No data provided")
        rain_analyzer = RainVolumeAnalyzer(
            place=data.get('place'),
            this_year=data.get('this_year'),
            past_span=data.get('past_span'),
            day_span=data.get('day_span'),
            rain_volume_lists=data.get('rain_volume_lists')
        )
        if not all([
            rain_analyzer.place, 
            rain_analyzer.this_year, 
            rain_analyzer.past_span, 
            rain_analyzer.day_span, 
            rain_analyzer.rain_volume_lists
        ]):
            abort(400, description="Missing necessary rain volume data")
        try:
            rain_analyzer.calculate_rain_volume_probabilities()
            rain_analyzer.calculate_rain_volume_scores()
            rain_analyzer.save_rain_volume_probabilities()
            rain_analyzer.save_rain_volume_scores()
            rain_volume_probabilities = rain_analyzer.get_rain_volume_probabilities()
            rain_volume_scores = rain_analyzer.get_rain_volume_scores()
        except Exception as e:
            abort(500, description=f"An error occurred while saving the data: {e}")
        return {"rain_volume_probabilities": rain_volume_probabilities, "rain_volume_scores": rain_volume_scores}
