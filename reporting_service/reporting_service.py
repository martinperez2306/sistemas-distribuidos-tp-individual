import logging
import pika

from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient
from dependencies.middlewaresys_client.constants import *
from dependencies.commons.video import Video
from reporting_service.result_repository import ResultRepository

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
REPORTING_SERVICE_QUEUE = "reporting_service_queue"
REPORTING_SERVICE_ID="reporting_service" ##TODO: Obtener de configuracion

class ReportingService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, REPORTING_SERVICE_ID)
        self.result_repository = ResultRepository()

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=REPORTING_SERVICE_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            reporting_message = self.middleware_system_client.parse_message(str(body))
            video = Video(reporting_message.body)
            request_id = reporting_message.request_id
            self.result_repository.save_filtered_video(request_id, video)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=REPORTING_SERVICE_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    