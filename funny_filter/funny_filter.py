import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.propagation import Propagation
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

FUNNY_TAG = "funny"

class FunnyFilter(RoutingService):
    def __init__(self, config_params):
        self.connection = None
        self.channel = None
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.propagations = dict()
        RoutingService.__init__(self, id, group_id, FUNNY_FILTER_EXCHANGE)

    def work(self, ch, method, properties, body):
        funny_filter_message = self.middleware_system_client.parse_message(body)
        if PROCESS_DATA_OP_ID == funny_filter_message.operation_id:
            self.__process_filter_by_funny_tag(ch, method, properties, body, funny_filter_message)
        else:
            self.__propagate_message(ch, method, properties, body, funny_filter_message)

    def __process_filter_by_funny_tag(self, ch, method, properties, body, funny_filter_message: Message):
        video = json_to_video(funny_filter_message.body)
        logging.info("Video {}".format(str(video)))
        tags = video.tags.split("|")
        if FUNNY_TAG in tags:
            self.middleware_system_client.call_storage_data(funny_filter_message)

    def __propagate_message(self, ch, method, properties, body, funny_filter_message: Message):
        request_id = funny_filter_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        if START_PROCESS_OP_ID == funny_filter_message.operation_id:
            propagation.inc_start()
            if propagation.starts_count == self.total_routes:
                self.middleware_system_client.call_storage_data(funny_filter_message)
        elif END_PROCESS_OP_ID == funny_filter_message.operation_id:
            propagation.inc_end()
            if propagation.ends_count == self.total_routes:
                self.middleware_system_client.call_storage_data(funny_filter_message)
        else:
            pass
        self.propagations[str(request_id)] = propagation
        