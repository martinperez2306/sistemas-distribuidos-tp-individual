import logging
import pika

from dependencies.commons.constants import MIDDLEWARE_QUEUE, RABBITMQ_HOST
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

class WorkService:
    def __init__(self, service_id, service_queue):
        self.connection = None
        self.channel = None
        self.service_id = service_id
        self.service_queue = service_queue
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, service_id)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.service_queue, durable=True)

        def handle_message(ch, method, properties, body):
            logging.debug("Received {}".format(body))
            self.work(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.service_queue, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    ##OVERRIDEABLE##
    def work(self, ch, method, properties, body):
        pass