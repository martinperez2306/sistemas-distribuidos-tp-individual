import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import parse_message
from middleware.client_service import ClientService
from middleware.request_repository import RequestRepository

class MessageHandler:
    def __init__(self, middleware_system_client, config_params):
        request_repository = RequestRepository()
        self.client_service = ClientService(middleware_system_client, request_repository)

    def run(self):
        pass

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
            elif (message.operation_id == DOWNLOAD_THUMBNAILS):
                logging.info("Upload Thumbnails to client")
                self.client_service.upload_thumbnails(ch, method, props, message)
            elif (message.operation_id == DOWNLOAD_COMPLETE):
                logging.info("Upload Thumbnails to client complete")
                self.client_service.send_upload_complete(ch, method, props, message)
            else:
                logging.info("Client method not found!")
        else:
            logging.info("Method not found!")