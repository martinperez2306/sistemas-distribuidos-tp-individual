import logging
import pika

from middlewaresys_client.src.core.middlewaresys_client import MiddlewareSystemClient
from middlewaresys_client.src.core.constants import *
#Dev import
#from ....base_images.middlewaresys_client.src.core.middlewaresys_client import MiddlewareSystemClient
#from ....base_images.middlewaresys_client.src.core.constants import *

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
REPORTING_SERVICE_QUEUE = "reporting_service_queue"
REPORTING_SERVICE_ID="reporting_service" ##TODO: Obtener de configuracion

class ReportingService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, REPORTING_SERVICE_ID)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=REPORTING_SERVICE_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            reporting_message = self.middleware_system_client.parse_message(str(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=REPORTING_SERVICE_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
    
    