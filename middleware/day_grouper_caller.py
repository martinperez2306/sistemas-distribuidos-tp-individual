import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import json_to_video
from middleware.routing_caller import RoutingCaller

class DayGrouperCaller(RoutingCaller):
    def __init__(self, total_routes: int):
        RoutingCaller.__init__(self, DAY_GROUPER_EXCHANGE)
        self.total_routes = total_routes

    def group_by_day(self, message: Message):
        group_by_day_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, DAY_GROUPER_ROUTER_ID, message.body)
        if PROCESS_DATA_OP_ID == message.operation_id:
            video = json_to_video(group_by_day_message.body)
            trending_date = video.trending_date
            routing_key = (hash(trending_date) % self.total_routes) + 1
            self.publish_data(group_by_day_message.to_string(), str(routing_key))
        else:
            for route in range(self.total_routes):
                routing_key = route + 1
                self.publish_data(group_by_day_message.to_string(), str(routing_key))