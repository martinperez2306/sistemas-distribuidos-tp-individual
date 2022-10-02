import logging
import pika

from dependencies.commons.constants import MIDDLEWARE_QUEUE, RABBITMQ_HOST
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

class RoutingService:
    def __init__(self, group_id, exchange):
        self.connection = None
        self.channel = None
        self.group_id = group_id
        self.exchange = exchange
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, group_id)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)#TODO: Tal vez definir yo la queue?
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.group_id)

        def handle_message(ch, method, properties, body):
            logging.debug("Received {}".format(body))
            self.work(ch, method, properties, body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue_name, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    ##OVERRIDEABLE##
    def work(self, ch, method, properties, body):
        pass