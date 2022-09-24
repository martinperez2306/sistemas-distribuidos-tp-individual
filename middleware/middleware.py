#!/usr/bin/env python3

import logging
import pika

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"

def main():
    initialize_log("INFO")
    logging.info("Hi! Im am the middleware")
    run()

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def run():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST))

    channel = connection.channel()
    channel.queue_declare(queue=MIDDLEWARE_QUEUE)


    def callback(ch, method, properties, body):
        logging.info("Received {}".format(body))

    channel.basic_consume(
        queue=MIDDLEWARE_QUEUE, on_message_callback=callback, auto_ack=True)

    logging.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == "__main__":
    main()