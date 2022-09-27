#!/usr/bin/env python3
import logging
import uuid
import pika
import re

from ....commons.src.commons.message import Message
from .constants import *

MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_CLIENT_ID_REGEX=r'CLIENT_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY(?:\[+)(.*)(?:\]+)'

class MiddlewareClient:
    def __init__(self, host, middleware_queue_id):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.client_id = 1
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.corr_id = None

    def connect(self):
        logging.info("Connecting to Middleware ")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.__on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = None

    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            response = str(body)
            logging.info("Response recieved: {}".format(response))
            self.response = self.__parse_message(response)

    def call_start_data_process(self):
        request = Message(CLIENT_MESSAGE_ID, 0, self.client_id, START_PROCESS_ID, "")
        return self.__request(request)

    def call_process_data(self, request_id: int, data: str):
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, PROCESS_DATA_ID, data)
        return self.__request(request)

    def call_end_data_process(self, request_id: int):
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, END_PROCESS_ID, "")
        return self.__request(request)

    def call_get_results(self, request_id: int):
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, GET_RESULTS_ID, "")
        return self.__request(request)

    def __request(self, message: Message):
        logging.info("Send request message: {}".format(message.to_string()))
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='', 
            routing_key=self.middleware_queue_id, 
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message.to_string())
        self.connection.process_data_events(time_limit=None)
        return self.response

    def __parse_message(self, body: str) -> Message:
        message_id = re.search(MESSAGE_ID_REGEX,body).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX,body).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX,body).group(1)
        operation_id = -1
        try:
            op_id = int(re.search(MESSAGE_OPERATION_ID_REGEX,body).group(1))
            operation_id = op_id
        except ValueError:
            pass
        body = re.search(MESSAGE_BODY_REGEX,body).group(1)
        message = Message(message_id, request_id, client_id, operation_id, body)
        logging.info("Message: {}".format(message.to_string()))
        return message

    def close(self):
        self.connection.close()