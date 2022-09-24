#!/usr/bin/env python3
from .message import Message
from .constants import *
import logging
import uuid
import pika

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
            self.response = response

    def call_start_data_process(self):
        request = Message(CLIENT_MESSAGE_ID, 0, self.client_id, START_PROCESS_ID, "")
        return self.__request(request)

    def call_process_data(self, request_id, data):
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, PROCESS_DATA_ID, data)
        return self.__request(request)

    def call_end_data_process(self, request_id):
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, END_PROCESS_ID, "")
        return self.__request(request)

    def call_get_results(self, request_id):
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

    def close(self):
        self.connection.close()