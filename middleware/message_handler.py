import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import parse_message
from middleware.client_service import ClientService
from middleware.day_grouper_caller import DayGrouperCaller
from middleware.funny_filter_caller import FunnyFilterCaller
from middleware.ingestion_service_caller import IngestionServiceCaller
from middleware.like_filter_caller import LikeFilterCaller
from middleware.max_caller import MaxCaller
from middleware.request_repository import RequestRepository
from middleware.storage_service_caller import StorageServiceCaller
from middleware.trending_filter_caller import TrendingFilterCaller

class MessageHandler:
    def __init__(self, config_params):
        self.ingestion_service_caller = IngestionServiceCaller()
        request_repository = RequestRepository()
        self.like_filter_caller = LikeFilterCaller(config_params)
        self.trending_filter_caller = TrendingFilterCaller(config_params)
        self.funny_filter_caller = FunnyFilterCaller(config_params)
        self.day_grouper_caller = DayGrouperCaller(config_params)
        self.max_caller = MaxCaller()
        self.storage_service_caller = StorageServiceCaller()
        self.client_service = ClientService(self.ingestion_service_caller, self.trending_filter_caller, 
                                            self.storage_service_caller, request_repository)

    def run(self):
        self.ingestion_service_caller.connect()
        self.like_filter_caller.connect()
        self.trending_filter_caller.connect()
        self.funny_filter_caller.connect()
        self.day_grouper_caller.connect()
        self.max_caller.connect()
        self.storage_service_caller.connect()

    def handle_message(self, ch, method, props, body):
        logging.info("Handling message {}".format(body))
        message = body.decode(UTF8_ENCODING)
        message_parsed = parse_message(message)
        self.__process_message(ch, method, props, message_parsed)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    def __process_message(self, ch, method, props, message: Message):
        if CLIENT_MESSAGE_ID == message.id:
            if (message.operation_id == START_PROCESS_OP_ID):
                logging.info("Init data process")
                self.client_service.start_data_process(ch, method, props, message)
            elif (message.operation_id == PROCESS_DATA_OP_ID):
                logging.info("Processing data")
                self.client_service.process_data(ch, method, props, message)
            elif (message.operation_id == END_PROCESS_OP_ID):
                logging.info("End data process")
                self.client_service.end_data_process(ch, method, props, message)
            elif (message.operation_id == SEND_RESULTS_OP_ID):
                logging.info("Sending Results!")
                self.client_service.send_results(ch, method, props, message)
            else:
                logging.info("Client method not found!")
        elif SERVICE_MESSAGE_ID == message.id:
            if LIKE_FILTER_GROUP_ID == message.destination_id:
                logging.info("Handling Filter By Likes")
                self.like_filter_caller.filter_by_likes(message)
            elif TRENDING_FILTER_GROUP_ID == message.destination_id:
                logging.info("Handling Filter By Trending")
                self.trending_filter_caller.filter_by_trending(message)
            elif FUNNY_FILTER_GROUP_ID == message.destination_id:
                logging.info("Handling Filter by Tag Funny")
                self.funny_filter_caller.filter_by_funny_tag(message)
            elif DAY_GROUPER_GROUP_ID == message.destination_id:
                logging.info("Handling Group by Day")
                self.day_grouper_caller.group_by_day(message)
            elif MAX_WORKER_ID == message.destination_id:
                logging.info("Handling Max")
                self.max_caller.get_max(message)
            elif STORAGE_DATA_WORKER_ID == message.destination_id:
                logging.info("Handling Storage data")
                self.storage_service_caller.storage_data(message)
            else:
                logging.info("Service method not found!")
        else:
            logging.info("Method not found!")