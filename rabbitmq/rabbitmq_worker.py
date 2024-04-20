# rabbitmq/rabbitmq_worker.py

import pika
import time
import json
import os
import requests
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi

load_dotenv()

mongodb_uri = os.environ.get('MONGODB_URI')
db_name = 'WeatherPredictor'

rabbitmq_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/')

def save_rainvolume_to_db(document):
    print("in save_rainvolume_to_db!")
    client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
    db = client[db_name]
    print("to save rain volume data to db!")
    db.rainvolume_eachyear.insert_one(document)
    print("rain volume data saved to db!")
    client.close()
    
def save_temperature_to_db(document):
    client = MongoClient(mongodb_uri, tlsCAFile=certifi.where())
    db = client[db_name]
    db.temperature_eachyear.insert_one(document)
    client.close()

def process_rainvolume_data(data):
    print("Processing rain volume data:", data)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": data.get('lat'),
        "longitude": data.get('lon'),
        "start_date": f"{data.get('year')}-01-01",
        "end_date": f"{data.get('year')}-12-31",
        "daily": "rain_sum"
    }
    response = requests.get(url, params=params)
    print("received response from open-meteo api")
    rain_volume = response.json()['daily']['rain_sum']
    document = {
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'year': data.get('year'),
        'rain_volume': rain_volume
    }
    print("to call save_rainvolume_to_db!")
    save_rainvolume_to_db(document)

def process_temperature_data(data):
    print("Processing temperature data:", data)
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": data.get('lat'),
        "longitude": data.get('lon'),
        "start_date": f"{data.get('year')}-01-01",
        "end_date": f"{data.get('year')}-12-31",
        "daily": "apparent_temperature_mean"
    }
    response = requests.get(url, params=params)
    temperature = response.json()['daily']['apparent_temperature_mean']
    document = {
        'lat': data.get('lat'),
        'lon': data.get('lon'),
        'year': data.get('year'),
        'temperature': temperature
    }
    save_temperature_to_db(document)

def callback_rainvolume(ch, method, properties, body):
    print("Received rain volume data")
    data = json.loads(body.decode('utf-8'))
    process_rainvolume_data(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_temperature(ch, method, properties, body):
    print("Received temperature data")
    data = json.loads(body.decode('utf-8'))
    process_temperature_data(data)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    params = pika.URLParameters(rabbitmq_url)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue='queue_rainvolume', durable=True)
    channel.queue_declare(queue='queue_temperature', durable=True)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='queue_rainvolume', on_message_callback=callback_rainvolume)
    channel.basic_consume(queue='queue_temperature', on_message_callback=callback_temperature)

    try:
        print(' [*] Waiting for messages. To exit press CTRL+C')
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Interrupted')
        channel.stop_consuming()
    finally:
        print("Closing connection")
        connection.close()

if __name__ == '__main__':
    main()