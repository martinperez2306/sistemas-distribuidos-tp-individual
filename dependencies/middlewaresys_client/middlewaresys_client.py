#!/usr/bin/env python3
import logging
import pika
import re

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import parse_message
from dependencies.middlewaresys_client.constants import *

class MiddlewareSystemClient:
    def __init__(self, host, middleware_queue_id, service_id):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.service_id = service_id
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id)

    def parse_message(self, body) -> Message:
        body = body.decode(UTF8_ENCODING)
        return parse_message(body)


    def call_filter_by_likes(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.service_id, request_message.operation_id, LIKE_FILTER_WORKER_ID, request_message.body)
        self.__request(message)

    def call_filter_by_tag(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.service_id, request_message.operation_id, FUNNY_FILTER_WORKER_ID, request_message.body)
        self.__request(message)

    def call_storage_data(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.service_id, request_message.operation_id, STORAGE_DATA_WORKER_ID, request_message.body)
        self.__request(message)

    def call_send_results(self, request_id: int, results: str):
        message = Message(CLIENT_MESSAGE_ID, request_id, self.service_id, SEND_RESULTS_OP_ID, MIDDLEWARE_ID, results)
        self.__request(message)

    def __request(self, message: Message):
        logging.info("Send request message: {}".format(message.to_string()))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.middleware_queue_id,
            body=message.to_string().encode(UTF8_ENCODING),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def close(self):
        self.connection.close()