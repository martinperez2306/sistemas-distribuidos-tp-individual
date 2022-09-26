import re
import logging

from .client_service import ClientService
from .constants import *
from .ingestion_service import IngestionService
from .like_filter_service import LikeFilterService
from .message import Message

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
        self.client_service = ClientService(ingestion_service)

    def handle_message(self, ch, method, props, body):
        logging.info("Handling message {}".format(body))
        message_parsed = self.__parse_message(str(body))
        self.__process_message(ch, method, props, message_parsed)

    def __parse_message(self, body: str) -> Message:
        message_id = re.search(MESSAGE_ID_REGEX,body).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX,body).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX,body).group(1)
        operation_id = -1
        try:
            op_id = int(re.search(MESSAGE_OPERATION_ID_REGEX,body).group(1))
            operation_id = op_id
        except ValueError:
            pass
        body = re.search(MESSAGE_BODY_REGEX,body).group(1)
        message = Message(message_id, request_id, client_id, operation_id, body)
        logging.info("Message: {}".format(message.to_string()))
        return message
    
    def __process_message(self, ch, method, props, message: Message):
        if (message.operation_id == START_PROCESS_ID):
            logging.info("Init data process")
            self.client_service.start_data_process(ch, method, props, message)
        elif (message.operation_id == PROCESS_DATA_ID):
            logging.info("Processing data")
            self.client_service.process_data(ch, method, props, message)
        elif (message.operation_id == END_PROCESS_ID):
            logging.info("End data process")
            self.client_service.end_data_process(ch, method, props, message)
        elif (message.operation_id == GET_RESULTS_ID):
            logging.info("Returning Results!")
            self.client_service.send_results(ch, method, props, message)
        elif (message.operation_id == LIKE_FILTER_ID):
            logging.info("Filtering by Likes")
            self.like_filter_service.filter_by_likes(message)
        else:
            logging.info("Method not found!")