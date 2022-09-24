#!/usr/bin/env python3

import logging
import pika
import signal

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"

class Middleware:

    def __init__(self):
        self.connection = None
        self.channel = None
        signal.signal(signal.SIGINT, self.__exit_gracefully)
        signal.signal(signal.SIGTERM, self.__exit_gracefully)

    # graceful shutdown the server
    def __exit_gracefully(self, *args):
        logging.info("Proceed to shutdown middleware gracefully")
        self.connection.close()

    def run(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=MIDDLEWARE_QUEUE)   

        def handle_message(body):
            logging.info("Received {}".format(body))

        self.channel.basic_consume(
            queue=MIDDLEWARE_QUEUE, on_message_callback=handle_message, auto_ack=True)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()