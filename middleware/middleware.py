import logging
import pika
import signal

from dependencies.commons.constants import *
from middleware.message_handler import MessageHandler

class Middleware:

    def __init__(self, config_params):
        self.connection = None
        self.channel = None
        self.message_handler = MessageHandler(config_params)
        signal.signal(signal.SIGINT, self.__exit_gracefully)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    # graceful shutdown the middleware
    def __exit_gracefully(self, *args):
        logging.info("Proceed to shutdown middleware gracefully")
        self.connection.close()

    def run(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=MIDDLEWARE_QUEUE)   

        def handle_message(ch, method, props, body):
            logging.info("Received {}".format(body))
            self.message_handler.handle_message(ch, method, props, body)

        self.channel.basic_consume(
            queue=MIDDLEWARE_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()