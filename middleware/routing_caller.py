import pika
from dependencies.commons.constants import *

class RoutingCaller:
    def __init__(self, publish_exchange_name):
        self.connection = None
        self.channel = None
        self.publish_exchange_name = publish_exchange_name

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.publish_exchange_name, exchange_type='direct')

    def publish_data(self, data: str, routing_key):
        self.channel.basic_publish(
            exchange=self.publish_exchange_name, 
            routing_key=routing_key, 
            body=data.encode(UTF8_ENCODING))

    def shutdown(self):
        self.connection.close()