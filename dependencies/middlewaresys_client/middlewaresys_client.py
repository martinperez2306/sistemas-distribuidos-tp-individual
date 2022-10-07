#!/usr/bin/env python3
import base64
import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.thumbnail import Thumbnail
from dependencies.commons.utils import parse_message, to_json
from dependencies.middlewaresys_client.like_filter_caller import LikeFilterCaller
from dependencies.middlewaresys_client.middleware_caller import MiddlewareCaller
from dependencies.middlewaresys_client.trending_filter_caller import TrendingFilterCaller
from dependencies.middlewaresys_client.funny_filter_caller import FunnyFilterCaller
from dependencies.middlewaresys_client.day_grouper_caller import DayGrouperCaller
from dependencies.middlewaresys_client.max_caller import MaxCaller
from dependencies.middlewaresys_client.storage_service_caller import StorageServiceCaller

class MiddlewareSystemClient:
    def __init__(self, host, group_id, config_params):
        self.host = host
        self.group_id = group_id
        self.like_filter_caller = LikeFilterCaller(config_params)
        self.trending_filter_caller = TrendingFilterCaller(config_params)
        self.funny_filter_caller = FunnyFilterCaller(config_params)
        self.day_grouper_caller = DayGrouperCaller(config_params)
        self.max_caller = MaxCaller(config_params)
        self.storage_service_caller = StorageServiceCaller(config_params)
        self.middleware_caller = MiddlewareCaller(config_params)

    def parse_message(self, body) -> Message:
        body = body.decode(UTF8_ENCODING)
        return parse_message(body)

    def call_filter_by_likes(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, LIKE_FILTER_GROUP_ID, request_message.body)
        self.like_filter_caller.filter_by_likes(message)

    def call_filter_by_trending(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, TRENDING_FILTER_GROUP_ID, request_message.body)
        self.trending_filter_caller.filter_by_trending(message)

    def call_filter_by_tag(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, FUNNY_FILTER_GROUP_ID, request_message.body)
        self.funny_filter_caller.filter_by_funny_tag(message)

    def call_group_by_day(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, DAY_GROUPER_GROUP_ID, request_message.body)
        self.day_grouper_caller.group_by_day(message)

    def call_max(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, MAX_WORKER_ID, request_message.body)
        self.max_caller.get_max(message)

    def call_storage_data(self, request_message: Message):
        message = Message(SERVICE_MESSAGE_ID, request_message.request_id, self.group_id, request_message.operation_id, STORAGE_DATA_WORKER_ID, request_message.body)
        self.storage_service_caller.storage_data(message)

    def call_send_results(self, request_id: str, results: str):
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, SEND_RESULTS_OP_ID, MIDDLEWARE_ID, results)
        self.middleware_caller.send_results(message)

    def call_upload_thumbnail(self, request_id: str, filename:str, thumbnailb: bytes):
        thumbnail = Thumbnail(filename, base64.b64encode(thumbnailb).decode(UTF8_ENCODING))
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, DOWNLOAD_THUMBNAILS, MIDDLEWARE_ID, to_json(thumbnail.__dict__))
        self.middleware_caller.upload_thumbnail(message)

    def call_upload_complete(self, request_id: str):
        message = Message(CLIENT_MESSAGE_ID, request_id, self.group_id, DOWNLOAD_COMPLETE, MIDDLEWARE_ID, "")
        self.middleware_caller.upload_complete(message)

    def close(self):
        self.like_filter_caller.close()
        self.trending_filter_caller.close()
        self.funny_filter_caller.close()
        self.day_grouper_caller.close()
        self.max_caller.close()
        self.storage_service_caller.close()
        self.middleware_caller.close()