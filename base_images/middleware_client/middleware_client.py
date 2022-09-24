#!/usr/bin/env python3
import logging
import pika

class MiddlewareClient:
    def __init__(self, host, queue_id):
        self.host = host
        self.queue_id = queue_id
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_id)

    def close(self):
        self.connection.close()

    def send(self, message):
        logging.info("Send message: {}".format(message))
        self.channel.basic_publish(exchange='', routing_key=self.queue_id, body=message)