import logging
import pika

from dependencies.commons.constants import *
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
INGESTION_SERVICE_QUEUE = "ingestion_service_queue"
INGESTION_SERVICE_ID="ingestion_service"##TODO: Obtener de configuracion

class IngestionService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, INGESTION_SERVICE_ID)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=INGESTION_SERVICE_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            ingestion_message = self.middleware_system_client.parse_message(body)
            self.middleware_system_client.call_filter_by_likes(ingestion_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=INGESTION_SERVICE_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    