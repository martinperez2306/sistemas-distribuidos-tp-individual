import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.propagation import Propagation
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video

class DayGrouper(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.propagations = dict()
        super().__init__(id, group_id, DAY_GROUPER_EXCHANGE)
        self.views_by_date = dict()

    def work(self, ch, method, properties, body):
        grouping_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == grouping_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == grouping_message.operation_id:
            self.__save_views_by_date(grouping_message)
        elif END_PROCESS_OP_ID == grouping_message.operation_id:
            max_message: Message = Message(grouping_message.id, grouping_message.request_id, 
                                                grouping_message.source_id, grouping_message.operation_id,
                                                grouping_message.destination_id, str(self.views_by_date))
            self.__check_next_stage(max_message)
        else:
            pass

    def __save_views_by_date(self, gruping_message: Message):
        video = json_to_video(gruping_message.body)
        logging.info("Saving views by date for Video {}".format(str(video)))
        trending_date = video.trending_date
        logging.info("Trending date {}".format(trending_date))
        if self.views_by_date.get(trending_date):
            self.views_by_date[trending_date] = self.views_by_date[trending_date] + video.view_count
        else:
            self.views_by_date[trending_date] = video.view_count
        logging.info("View Count for date {} is {}".format(trending_date, self.views_by_date[trending_date]))

    def __check_next_stage(self, gruping_message: Message):
        logging.info("Checking next stage")
        request_id = gruping_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        propagation.inc_end()
        if propagation.ends_count == self.total_routes:
            self.__next_stage(gruping_message)
        self.propagations[str(request_id)] = propagation

    def __next_stage(self, gruping_message: Message):
        self.middleware_system_client.connect()
        self.middleware_system_client.call_max(gruping_message)
        self.middleware_system_client.close()
        