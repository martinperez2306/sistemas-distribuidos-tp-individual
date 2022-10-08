import json
import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.propagation import Propagation
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video

FUNNY_TAG = "funny"

class FunnyFilter(RoutingService):
    def __init__(self, config_params):
        super().__init__(config_params, FUNNY_FILTER_EXCHANGE)
        self.funny_videos = list()
        self.propagations = dict()

    def work(self, ch, method, properties, body):
        funny_filter_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == funny_filter_message.operation_id:
            pass 
        elif PROCESS_DATA_OP_ID == funny_filter_message.operation_id:
            self.__process_filter_by_funny_tag(funny_filter_message)
        elif END_PROCESS_OP_ID == funny_filter_message.operation_id:
            self.__check_next_stage(funny_filter_message)
        else:
            pass

    def __process_filter_by_funny_tag(self, funny_filter_message: Message):
        video = json_to_video(funny_filter_message.body)
        logging.info("Video {}".format(str(video)))
        tags = video.tags.split("|")
        if FUNNY_TAG in tags:
            logging.info("Video is funny: [{}]".format(str(video)))
            self.funny_videos.append(video)

    def __check_next_stage(self, funny_filter_message: Message):
        request_id = funny_filter_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        propagation.inc_end()
        if propagation.ends_count == self.total_routes:
            self.__next_stage(funny_filter_message)
        self.propagations[str(request_id)] = propagation

    def __next_stage(self, funny_filter_message: Message):
        init_message = Message(funny_filter_message.id, funny_filter_message.request_id, funny_filter_message.source_id,
                                        START_PROCESS_OP_ID, funny_filter_message.destination_id, "")
        self.middleware_system_client.call_storage_data(init_message)
        for funny_video in self.funny_videos:
            funny_video_message = Message(funny_filter_message.id, funny_filter_message.request_id, funny_filter_message.source_id,
                                        PROCESS_DATA_OP_ID, funny_filter_message.destination_id, json.dumps(funny_video.__dict__))
            self.middleware_system_client.call_storage_data(funny_video_message)
        end_message = Message(funny_filter_message.id, funny_filter_message.request_id, funny_filter_message.source_id,
                                        END_PROCESS_OP_ID, funny_filter_message.destination_id, "")
        self.middleware_system_client.call_storage_data(end_message)
        