from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from dependencies.commons.message import Message
from middleware.routing_caller import RoutingCaller

class LikeFilterCaller(RoutingCaller):
    def __init__(self, config_params):
        RoutingCaller.__init__(self, LIKE_FILTER_EXCHANGE)
        self.total_routes = int(config_params["service_instances"])
    
    def filter_by_likes(self, message: Message):
        filter_by_like_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, LIKE_FILTER_GROUP_ID, message.body)
        if START_PROCESS_OP_ID == message.operation_id:
            self.connect()
            self.__broadcast(filter_by_like_message)
        elif PROCESS_DATA_OP_ID == message.operation_id:
            video = json_to_video(filter_by_like_message.body)
            video_id = video.id
            routing_key = LIKE_FILTER_GROUP_ID + "_" + str((hash(video_id) % self.total_routes) + 1)
            self.publish_data(filter_by_like_message.to_string(), str(routing_key))
        elif END_PROCESS_OP_ID == message.operation_id:
            self.__broadcast(filter_by_like_message)
            self.close()
        else:
            pass

    def __broadcast(self, message):
        for route in range(self.total_routes):
            routing_key = routing_key = LIKE_FILTER_GROUP_ID + "_" + str((route + 1))
            self.publish_data(message.to_string(), str(routing_key))