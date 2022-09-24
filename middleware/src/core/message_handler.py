import re
import logging

from .client_service import ClientService
from .constants import *
from .message import Message

MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_CLIENT_ID_REGEX=r'CLIENT_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY\[(.*?)\]'


class MessageHandler:
    def __init__(self):
        self.client_service = ClientService()

    def handle_message(self, ch, method, props, body):
        logging.info("Handling client message {}".format(body))
        message_parsed = self.__parse_message(body)
        self.__process_message(ch, method, props, message_parsed)

    def __parse_message(self, request: str) -> Message:
        message_id = re.search(MESSAGE_ID_REGEX,request).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX,request).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX,request).group(1)
        operation_id = re.search(MESSAGE_OPERATION_ID_REGEX,request).group(1)
        body = re.search(MESSAGE_BODY_REGEX,request).group(1)
        return Message(message_id, request_id, client_id, operation_id, body)
    
    def __process_message(self, ch, method, props, message: Message):
        if (message.operation_id == START_PROCESS_ID):
            logging.info("Init data process")
            self.client_service.start_data_process(ch, method, props, message)
        elif (message.operation_id == PROCESS_DATA_ID):
            logging.info("Processing data")
        elif (message.operation_id == END_PROCESS_ID):
            logging.info("End data process")
        elif (message.operation_id == GET_RESULTS_ID):
            logging.info("Returning Results!")
        else:
            logging.info("Method not found!")