import logging
import pika
import signal
import time
from dependencies.commons.base_app import BaseApp

from dependencies.commons.constants import *
from middleware.message_handler import MessageHandler

class Middleware(BaseApp):

    def __init__(self, config_params):
        super().__init__("middleware")
        self.connection = None
        self.channel = None
        self.first_try = True
        signal.signal(signal.SIGINT, self.__exit_gracefully)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)
        self.message_handler = MessageHandler(config_params)

    def run(self):
        super().run()
        while self.running:
            try:
                self.message_handler.run()
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
            except Exception as e:
                logging.error('Error waiting for message: {}'.format(e))
                if self.first_try:
                    logging.debug('First try to connect rabbit. Waiting {} seconds'.format(WAIT_CONNECTION))
                    self.first_try = False
                    time.sleep(WAIT_CONNECTION)

    def __exit_gracefully(self, *args):
        super().exit_gracefully(*args)
        self.connection.close()