import logging
import pika
import signal
from dependencies.commons.base_app import BaseApp

from dependencies.commons.constants import MIDDLEWARE_QUEUE, RABBITMQ_HOST
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

class RoutingService(BaseApp):
    def __init__(self, service_id, group_id, exchange):
        BaseApp.__init__(self, service_id)
        self.connection = None
        self.channel = None
        self.service_id = service_id
        self.group_id = group_id
        self.exchange = exchange
        signal.signal(signal.SIGINT, self.__exit_gracefully)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, group_id)

    def run(self):
        super().run()
        while self.running:
            try:
                self.middleware_system_client.connect()
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
                result = self.channel.queue_declare(queue='', exclusive=True)#TODO: Tal vez definir yo la queue?
                queue_name = result.method.queue
                self.channel.queue_bind(exchange=self.exchange, queue=queue_name, routing_key=self.service_id)

                def handle_message(ch, method, properties, body):
                    logging.debug("Received {}".format(body))
                    self.work(ch, method, properties, body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)

                self.channel.basic_consume(queue=queue_name, on_message_callback=handle_message)

                logging.info('Waiting for messages. To exit press CTRL+C')
                self.channel.start_consuming()
            except Exception as e:
                logging.error('Error waiting for message: {}'.format(e))

    ##OVERRIDEABLE##
    def work(self, ch, method, properties, body):
        pass

    def __exit_gracefully(self, *args):
        super().exit_gracefully(*args)
        self.connection.close()