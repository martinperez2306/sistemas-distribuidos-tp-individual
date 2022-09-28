import re
import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from middleware.client_service import ClientService
from middleware.constants import *
from middleware.funny_filter_service import FunnyFilterService
from middleware.ingestion_service import IngestionService
from middleware.like_filter_service import LikeFilterService
from middleware.storage_service import StorageService

MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_CLIENT_ID_REGEX=r'CLIENT_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY(?:\[+)(.*)(?:\]+)'


class MessageHandler:
    def __init__(self):
        ingestion_service = IngestionService()
        ingestion_service.run()
        self.like_filter_service = LikeFilterService()
        self.like_filter_service.run()
        self.funny_filter_service = FunnyFilterService()
        self.funny_filter_service.run()
        self.storage_service = StorageService()
        self.storage_service.run()
        self.client_service = ClientService(ingestion_service)

    def handle_message(self, ch, method, props, body):
        logging.info("Handling message {}".format(body))
        message = body.decode(UTF8_ENCODING)
        message_parsed = self.__parse_message(message)
        self.__process_message(ch, method, props, message_parsed)

    def __parse_message(self, body: str) -> Message:
        logging.info("Parsing message {}".format(body))
        message_id = re.search(MESSAGE_ID_REGEX, body).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX, body).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX, body).group(1)
        operation_id = -1
        try:
            op_id = int(re.search(MESSAGE_OPERATION_ID_REGEX,body).group(1))
            operation_id = op_id
        except ValueError:
            pass
        body = re.search(MESSAGE_BODY_REGEX, body).group(1)
        message = Message(message_id, request_id, client_id, operation_id, body)
        logging.info("Message: {}".format(message.to_string()))
        return message
    
    def __process_message(self, ch, method, props, message: Message):
        if (message.operation_id == START_PROCESS_OP_ID):
            logging.info("Init data process")
            self.client_service.start_data_process(ch, method, props, message)
        elif (message.operation_id == PROCESS_DATA_OP_ID):
            logging.info("Processing data")
            self.client_service.process_data(ch, method, props, message)
        elif (message.operation_id == END_PROCESS_OP_ID):
            logging.info("End data process")
            self.client_service.end_data_process(ch, method, props, message)
        elif (message.operation_id == GET_RESULTS_OP_ID):
            logging.info("Returning Results!")
            self.client_service.send_results(ch, method, props, message)
        elif (message.operation_id == LIKE_FILTER_OP_ID):
            logging.info("Filtering by Likes")
            self.like_filter_service.filter_by_likes(message)
        elif (message.operation_id == FUNNY_FILTER_OP_ID):
            logging.info("Filtering by Tag Funny")
            self.funny_filter_service.filter_by_funny_tag(message)
        elif (message.operation_id == STORAGE_DATA_OP_ID):
            logging.info("Storaging data")
            self.storage_service.storage_data(message)
        else:
            logging.info("Method not found!")