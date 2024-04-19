# rabbitmq/rabbitmq_worker.py

import pika
import json
import os
from contextlib import contextmanager

load_dotenv()

rabbitmq_url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost:5672/')

class RabbitMQManager:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.setup_connection()

    def setup_connection(self):
        try:
            params = pika.URLParameters(rabbitmq_url)
            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue='queue_rainvolume', durable=True)
            self.channel.queue_declare(queue='queue_temperature', durable=True)
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Cannot connect to RabbitMQ: {e}")
            raise

    def send_task_to_queue(self, task, queue_name):
        if not self.channel:
            raise Exception("RabbitMQ channel is not set up.")
        if not isinstance(task, str):
            task = json.dumps(task)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=task.encode('utf-8'),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json', 
            ))
        print(f" [x] Sent task to {queue_name}")

    @contextmanager
    def get_channel(self):
        if not self.connection or self.connection.is_closed:
            self.setup_connection()
        yield self.channel
        self.connection.close()

    def close(self):
        if self.connection:
            self.connection.close()
            print("RabbitMQ connection closed.")
