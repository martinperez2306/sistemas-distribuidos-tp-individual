import json
import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video

MIN_LIKES_COUNT = 5000000

class LikeFilter(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.popular_videos = list()
        super().__init__(id, group_id, LIKE_FILTER_EXCHANGE)

    def work(self, ch, method, properties, body):
        like_filter_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == like_filter_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == like_filter_message.operation_id:
            self.__process_filter_by_like(like_filter_message)
        elif END_PROCESS_OP_ID == like_filter_message.operation_id:
            self.__next_stage(like_filter_message)
        else:
            pass

    def __process_filter_by_like(self, like_filter_message: Message):
        video = json_to_video(like_filter_message.body)
        logging.debug("Video {}".format(str(video)))
        try:
            likes_count = int(video.likes)
            if likes_count > MIN_LIKES_COUNT:
                logging.info("Video is popular: [{}]".format(str(video)))
                self.popular_videos.append(video)
        except ValueError:
            pass

    def __next_stage(self, like_filter_message: Message):
        self.middleware_system_client.connect()
        init_message = Message(like_filter_message.id, like_filter_message.request_id, like_filter_message.source_id,
                                        START_PROCESS_OP_ID, like_filter_message.destination_id, "")
        self.middleware_system_client.call_filter_by_tag(init_message)
        self.middleware_system_client.call_group_by_day(init_message)
        for popular_video in self.popular_videos:
            popular_video_message = Message(like_filter_message.id, like_filter_message.request_id, like_filter_message.source_id,
                                        PROCESS_DATA_OP_ID, like_filter_message.destination_id, json.dumps(popular_video.__dict__))
            self.middleware_system_client.call_filter_by_tag(popular_video_message)
            self.middleware_system_client.call_group_by_day(popular_video_message)
        end_message = Message(like_filter_message.id, like_filter_message.request_id, like_filter_message.source_id,
                                        END_PROCESS_OP_ID, like_filter_message.destination_id, "")
        self.middleware_system_client.call_filter_by_tag(end_message)
        self.middleware_system_client.call_group_by_day(end_message)
        self.middleware_system_client.close()
