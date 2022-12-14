import pika
from dependencies.commons.constants import *

class BaseCaller:
    def __init__(self, publish_queue_name):
        self.connection = None
        self.channel = None
        self.publish_queue_name = publish_queue_name
    
    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.publish_queue_name, durable=True)

    def publish_data(self, data: str):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            body=data.encode(UTF8_ENCODING),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def close(self):
        self.connection.close()