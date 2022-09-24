#!/usr/bin/env python3
import logging
import uuid
import pika

class MiddlewareClient:
    def __init__(self, host, middleware_queue_id):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.corr_id = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def request(self, message):
        logging.info("Send message: {}".format(message))
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', 
            routing_key=self.middleware_queue_id, 
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message)
        self.connection.process_data_events(time_limit=None)
        return self.response

    def close(self):
        self.connection.close()