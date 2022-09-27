#!/usr/bin/env python3
import logging
import pika
import re

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.middlewaresys_client.constants import *

MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_CLIENT_ID_REGEX=r'CLIENT_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY(?:\[+)(.*)(?:\]+)'

class MiddlewareSystemClient:
    def __init__(self, host, middleware_queue_id, client_id):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.client_id = client_id
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id)

    def parse_message(self, body) -> Message:
        body = body.decode(UTF8_ENCODING)
        message_id = re.search(MESSAGE_ID_REGEX , body).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX, body).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX, body).group(1)
        operation_id = -1
        try:
            op_id = int(re.search(MESSAGE_OPERATION_ID_REGEX, body).group(1))
            operation_id = op_id
        except ValueError:
            pass
        body = re.search(MESSAGE_BODY_REGEX, body).group(1)
        message = Message(message_id, request_id, client_id, operation_id, body)
        logging.info("Message: {}".format(message.to_string()))
        return message 


    def call_filter_by_likes(self, request_id: int, data: str):
        message = Message(SERVICE_MESSAGE_ID, request_id, self.client_id, LIKE_FILTER_ID, data)
        self.__request(message)

    def call_storage_data(self, request_id: int, data: str):
        message = Message(SERVICE_MESSAGE_ID, request_id, self.client_id, STORAGE_DATA_ID, data)
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