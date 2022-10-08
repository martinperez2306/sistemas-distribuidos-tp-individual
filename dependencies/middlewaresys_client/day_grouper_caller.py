import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.routing_caller import RoutingCaller

class DayGrouperCaller(RoutingCaller):
    def __init__(self, config_params):
        super().__init__(DAY_GROUPER_EXCHANGE)
        self.total_routes = int(config_params["service_instances"])
        self.previus_stage_eof = 0

    def group_by_day(self, message: Message):
        group_by_day_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, DAY_GROUPER_GROUP_ID, message.body)
        if START_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(group_by_day_message)
        elif PROCESS_DATA_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            video = json_to_video(group_by_day_message.body)
            trending_date = video.trending_date
            routing_key = DAY_GROUPER_GROUP_ID + "_" + str((hash(trending_date) % self.total_routes) + 1)
            self.publish_data(group_by_day_message.to_string(), str(routing_key))
        elif END_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(group_by_day_message)
            if self.previus_stage_eof >= self.total_routes:
                self.close()
        else:
            pass
            

    def __broadcast(self, message):
        for route in range(self.total_routes):
            routing_key = DAY_GROUPER_GROUP_ID + "_" + str(route + 1)
            self.publish_data(message.to_string(), str(routing_key))