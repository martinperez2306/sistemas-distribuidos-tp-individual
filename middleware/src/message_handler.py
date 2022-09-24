import re
import logging

import constants
from .message import Message

MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_CLIENT_ID_REGEX=r'CLIENT_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY\[(.*?)\]'


class MessageHandler:
    def __init__(self):
        self.request_count = 0

    def handle_message(self, message: str) -> str:
        logging.info("Handling client message {}".format(message))
        message_parsed = self.__parse_message(message)
        self.__process_message(message_parsed)

    def __parse_message(self, request: str):
        message_id = re.search(MESSAGE_ID_REGEX,request).group(1)
        request_id = re.search(MESSAGE_REQUEST_ID_REGEX,request).group(1)
        client_id = re.search(MESSAGE_CLIENT_ID_REGEX,request).group(1)
        operation_id = re.search(MESSAGE_OPERATION_ID_REGEX,request).group(1)
        body = re.search(MESSAGE_BODY_REGEX,request).group(1)
        return Message(message_id, request_id, client_id, operation_id, body)
    
    def __process_message(self, message: Message):
        if (message.operation_id == constants.START_PROCESS_ID):
            logging.info("Init data process")
        elif (message.operation_id == constants.PROCESS_DATA_ID):
            logging.info("Processing data")
        elif (message.operation_id == constants.END_PROCESS_ID):
            logging.info("End data process")
        else:
            logging.info("No Processing")