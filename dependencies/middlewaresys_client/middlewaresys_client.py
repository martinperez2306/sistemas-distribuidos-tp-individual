#!/usr/bin/env python3
import base64
import logging
import pika
import re

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.thumbnail import Thumbnail
from dependencies.commons.utils import parse_message, to_json

class MiddlewareSystemClient:
    def __init__(self, host, middleware_queue_id, group_id):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.group_id = group_id
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id, durable=True)

    def parse_message(self, body) -> Message:
        body = body.decode(UTF8_ENCODING)
        return parse_message(body)

    #Deprecated
    def call_filter_by_likes(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, LIKE_FILTER_GROUP_ID, request_message.body)
        self.__request(message)

    #Deprecated
    def call_filter_by_trending(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, TRENDING_FILTER_GROUP_ID, request_message.body)
        self.__request(message)

    def call_filter_by_likes_and_trending(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, LIKE_FILTER_GROUP_ID + "_" +TRENDING_FILTER_GROUP_ID, request_message.body)
        self.__request(message)

    def call_filter_by_tag(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, FUNNY_FILTER_GROUP_ID, request_message.body)
        self.__request(message)

    def call_group_by_day(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, DAY_GROUPER_GROUP_ID, request_message.body)
        self.__request(message)

    def call_max(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, MAX_WORKER_ID, request_message.body)
        self.__request(message)

    def call_storage_data(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, STORAGE_DATA_WORKER_ID, request_message.body)
        self.__request(message)

    def call_send_results(self, request_id: str, results: str):
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, SEND_RESULTS_OP_ID, MIDDLEWARE_ID, results)
        self.__request(message)

    def call_upload_thumbnail(self, request_id: str, filename:str, thumbnailb: bytes):
        thumbnail = Thumbnail(filename, base64.b64encode(thumbnailb).decode(UTF8_ENCODING))
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, DOWNLOAD_THUMBNAILS, MIDDLEWARE_ID, to_json(thumbnail.__dict__))
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
        self.__request_prop(message, properties)

    def call_upload_complete(self, request_id: str):
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, DOWNLOAD_COMPLETE, MIDDLEWARE_ID, "")
        self.__request(message)

    def __request(self, message: Message):
        logging.debug("Send request message: {}".format(message.to_string()))
        self.channel.basic_publish(
            exchange='',
            routing_key=self.middleware_queue_id,
            body=message.to_string().encode(UTF8_ENCODING),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ))

    def __request_prop(self, message: Message, properties):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.middleware_queue_id,
            body=message.to_string().encode(UTF8_ENCODING),
            properties=properties)


    def close(self):
        self.connection.close()