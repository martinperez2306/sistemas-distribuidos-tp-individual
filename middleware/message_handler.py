import re
import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import parse_message
from middleware.client_service import ClientService
from middleware.funny_filter_caller import FunnyFilterCaller
from middleware.ingestion_service_caller import IngestionServiceCaller
from middleware.like_filter_caller import LikeFilterCaller
from middleware.request_repository import RequestRepository
from middleware.storage_service_caller import StorageServiceCaller

class MessageHandler:
    def __init__(self):
        ingestion_service_caller = IngestionServiceCaller()
        ingestion_service_caller.run()
        request_repository = RequestRepository()
        self.like_filter_caller = LikeFilterCaller()
        self.like_filter_caller.run()
        self.funny_filter_caller = FunnyFilterCaller()
        self.funny_filter_caller.run()
        self.storage_service_caller = StorageServiceCaller()
        self.storage_service_caller.run()
        self.client_service = ClientService(ingestion_service_caller, request_repository)

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
            if LIKE_FILTER_WORKER_ID == message.destination_id:
                logging.info("Filtering by Likes")
                self.like_filter_caller.filter_by_likes(message)
            elif FUNNY_FILTER_WORKER_ID == message.destination_id:
                logging.info("Filtering by Tag Funny")
                self.funny_filter_caller.filter_by_funny_tag(message)
            elif STORAGE_DATA_WORKER_ID == message.destination_id:
                logging.info("Storaging data")
                self.storage_service_caller.storage_data(message)
            else:
                logging.info("Service method not found!")
        else:
            logging.info("Method not found!")