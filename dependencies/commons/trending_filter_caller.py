from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from dependencies.commons.message import Message
from dependencies.commons.routing_caller import RoutingCaller


class TrendingFilterCaller(RoutingCaller):
    def __init__(self, config_params):
        super().__init__(TRENDING_FILTER_EXCHANGE)
        self.total_routes = int(config_params["service_instances"])
    
    def filter_by_trending(self, message: Message):
        filter_by_trending_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, TRENDING_FILTER_GROUP_ID, message.body)
        if LOAD_TOTAL_COUNTRIES == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(filter_by_trending_message)
            self.close()
        elif START_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(filter_by_trending_message)
        elif PROCESS_DATA_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            video = json_to_video(filter_by_trending_message.body)
            video_id = video.id
            routing_key = TRENDING_FILTER_GROUP_ID + "_" + str((hash(video_id) % self.total_routes) + 1)
            self.publish_data(filter_by_trending_message.to_string(), str(routing_key))
        elif END_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(filter_by_trending_message)
            self.close()
        else:
            pass

    def __broadcast(self, message):
        for route in range(self.total_routes):
            routing_key = routing_key = TRENDING_FILTER_GROUP_ID + "_" + str((route + 1))
            self.publish_data(message.to_string(), str(routing_key))