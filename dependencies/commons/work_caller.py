import logging
import pika
from dependencies.commons.constants import *

class WorkCaller:
    def __init__(self, publish_queue_name):
        self.connection = None
        self.channel = None
        self.publish_queue_name = publish_queue_name
    
    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.publish_queue_name, durable=True)

    def publish_data(self, data: str):
        logging.debug("Publish data [{}] in queue [{}]".format(data, self.publish_queue_name))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            body=data.encode(UTF8_ENCODING),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def publish_data_with_props(self, data: str, properties: pika.BasicProperties):
        logging.debug("Publish data [{}] in queue [{}] with properties [{}]".format(data, self.publish_queue_name, properties))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.publish_queue_name,
            body=data.encode(UTF8_ENCODING),
            properties=properties)

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()