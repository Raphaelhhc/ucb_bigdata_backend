# app.py

from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import certifi
import pika

from rabbitmq.rabbitmq_manager import RabbitMQManager
from restapi.rainvolume_restapi import blp_rainvolumecollector, blp_rainvolumeanalyzer
from restapi.temperature_restapi import blp_temperaturecollector, blp_temperatureanalyzer
from restapi.recommend_restapi import blp_recommend

load_dotenv()

# app initialization
app = Flask(__name__)
CORS(app)

# app configuration
app.config['MONGODB_URI'] = os.environ.get('MONGODB_URI')
app.config['API_TITLE'] = 'Weather Analysis API'
app.config['API_VERSION'] = 'v1'
app.config['OPENAPI_VERSION'] = '3.0.2'
app.config['OPENAPI_URL_PREFIX'] = '/'
app.config['OPENAPI_JSON_PATH'] = 'api-spec.json'
app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger'
app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'

# database connection
app.db = MongoClient(app.config['MONGODB_URI'], tlsCAFile=certifi.where()).WeatherPredictor

# rabbitmq connection
rabbitmq_manager = RabbitMQManager()
app.rabbitmq_manager = rabbitmq_manager

# api registration
api = Api(app)
api.register_blueprint(blp_rainvolumecollector)
api.register_blueprint(blp_rainvolumeanalyzer)
api.register_blueprint(blp_temperaturecollector)
api.register_blueprint(blp_temperatureanalyzer)
api.register_blueprint(blp_recommend)


if __name__ == '__main__':
    app.run(debug=True)
    rabbitmq_manager.close()