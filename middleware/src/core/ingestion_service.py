import pika
from .constants import *

class IngestionService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = INGESTION_QUEUE_NAME
    
    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=INGESTION_QUEUE_NAME, durable=True)

    def ingest_data(self, data):
        self.channel.channel.basic_publish(
            exchange='',
            routing_key=INGESTION_QUEUE_NAME,
            body=str(data),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def shutdown(self):
        self.connection.close()