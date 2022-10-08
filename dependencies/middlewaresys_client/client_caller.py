import logging
import pika
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.work_caller import WorkCaller

class ClientCaller:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
    
    def send_results(self, result_message: Message):
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            reply_to=result_message.destination_id,
            correlation_id=result_message.request_id,
        )
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data_with_props(result_message.to_string(), properties)
        self.close()

    def upload_thumbnail(self, upload_message: Message):
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            reply_to=upload_message.destination_id,
            correlation_id=upload_message.request_id,
        )
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data_with_props(upload_message.to_string(), properties)
        self.close()

    def upload_complete(self, upload_message: Message):
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            reply_to=upload_message.destination_id,
            correlation_id=upload_message.request_id,
        )
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data_with_props(upload_message.to_string(), properties)
        self.close()

    def publish_data_with_props(self, data: str, properties: pika.BasicProperties):
        logging.debug("Publish data [{}] in queue [{}] with properties [{}]".format(data, properties.reply_to, properties))
        self.channel.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            body=data.encode(UTF8_ENCODING),
            properties=properties)

    def close(self):
        self.connection.close()