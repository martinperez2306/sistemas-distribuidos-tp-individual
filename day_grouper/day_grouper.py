import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.propagation import Propagation
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

class DayGrouper(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.propagations = dict()
        super().__init__(id, group_id, DAY_GROUPER_EXCHANGE)
        self.days_grouped = dict()

    def work(self, ch, method, properties, body):
        grouping_message = self.middleware_system_client.parse_message(body)
        if PROCESS_DATA_OP_ID == grouping_message.operation_id:
            self.__save_by_group(grouping_message)
        elif END_PROCESS_OP_ID == grouping_message.operation_id:
            max_message: Message = Message(grouping_message.id, grouping_message.request_id, 
                                                grouping_message.source_id, grouping_message.operation_id,
                                                grouping_message.destination_id, str(self.days_grouped))
            self.__propagate_message(ch, method, properties, body, max_message)
        else:
            self.__propagate_message(ch, method, properties, body, grouping_message)

    def __save_by_group(self, gruping_message: Message):
        video = json_to_video(gruping_message.body)
        logging.info("Video {}".format(str(video)))
        trending_date = video.trending_date
        logging.info("Trending date {}".format(trending_date))
        if self.days_grouped.get(trending_date):
            self.days_grouped[trending_date] = self.days_grouped[trending_date] + video.view_count
        else:
            self.days_grouped[trending_date] = video.view_count
        logging.info("View Count for date {} is {}".format(trending_date, self.days_grouped[trending_date]))

    def __propagate_message(self, ch, method, properties, body, gruping_message: Message):
        request_id = gruping_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        if START_PROCESS_OP_ID == gruping_message.operation_id:
            propagation.inc_start()
            if propagation.starts_count == self.total_routes:
                self.middleware_system_client.call_max(gruping_message)
        elif END_PROCESS_OP_ID == gruping_message.operation_id:
            propagation.inc_end()
            if propagation.ends_count == self.total_routes:
                self.middleware_system_client.call_max(gruping_message)
        else:
            pass
        self.propagations[str(request_id)] = propagation
        