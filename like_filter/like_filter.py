import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

MIN_LIKES_COUNT = 5000000

class LikeFilter(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        RoutingService.__init__(self, id, group_id, LIKE_FILTER_EXCHANGE)

    def work(self, ch, method, properties, body):
        like_filter_message = self.middleware_system_client.parse_message(body)
        if PROCESS_DATA_OP_ID == like_filter_message.operation_id:
            self.__process_filter_by_like(ch, method, properties, body, like_filter_message)
        else:
            self.__propagate_message(ch, method, properties, body, like_filter_message)

    def __process_filter_by_like(self, ch, method, properties, body, like_filter_message: Message):
        video = json_to_video(like_filter_message.body)
        logging.debug("Video {}".format(str(video)))
        try:
            likes_count = int(video.likes)
            if likes_count > MIN_LIKES_COUNT:
                logging.info("Video is popular: [{}]".format(str(video)))
                self.middleware_system_client.call_filter_by_tag(like_filter_message)
                self.middleware_system_client.call_group_by_day(like_filter_message)
        except ValueError:
            pass

    def __propagate_message(self, ch, method, properties, body, like_filter_message: Message):
        self.middleware_system_client.call_filter_by_tag(like_filter_message)
        self.middleware_system_client.call_group_by_day(like_filter_message)
