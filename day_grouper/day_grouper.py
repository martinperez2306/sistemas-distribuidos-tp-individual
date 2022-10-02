import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

DAY_GROUPER_ID="day_grouper_1"##TODO: Obtener de configuracion

class DayGrouper(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        RoutingService.__init__(self, id, group_id, DAY_GROUPER_EXCHANGE)
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
        self.middleware_system_client.call_max(gruping_message)