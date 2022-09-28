import pika
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from middleware.constants import *

class BaseService:
    def __init__(self, publish_queue_name):
        self.connection = None
        self.channel = None
        self.publish_queue_name = publish_queue_name
    
    def run(self):
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

    def propagate_message(self, message: Message):
        propagate_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, message.body)
        self.publish_data(propagate_message.to_string()) 

    def shutdown(self):
        self.connection.close()