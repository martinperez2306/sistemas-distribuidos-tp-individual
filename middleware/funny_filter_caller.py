from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from dependencies.commons.message import Message
from middleware.routing_caller import RoutingCaller

class FunnyFilterCaller(RoutingCaller):
    def __init__(self, config_params):
        RoutingCaller.__init__(self, FUNNY_FILTER_EXCHANGE)
        self.total_routes = int(config_params["service_instances"])
    
    def filter_by_funny_tag(self, message: Message):
        filter_by_tag_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, FUNNY_FILTER_GROUP_ID, message.body)
        if PROCESS_DATA_OP_ID == message.operation_id:
            video = json_to_video(filter_by_tag_message.body)
            video_id = video.id
            routing_key = FUNNY_FILTER_GROUP_ID + "_" + str((hash(video_id) % self.total_routes) + 1)
            self.publish_data(filter_by_tag_message.to_string(), str(routing_key))
        else:
            for route in range(self.total_routes):
                routing_key = routing_key = FUNNY_FILTER_GROUP_ID + "_" + str((route + 1))
                self.publish_data(filter_by_tag_message.to_string(), str(routing_key))