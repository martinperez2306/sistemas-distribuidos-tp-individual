import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from middleware.ingestion_service_caller import IngestionServiceCaller
from middleware.request import Request
from middleware.request_repository import RequestRepository

ACK_MESSAGE = "ACK"

class ClientService:
    def __init__(self, ingestion_service_caller: IngestionServiceCaller, request_repository: RequestRepository):
        self.request_count = 0
        self.ingestion_service = ingestion_service_caller
        self.request_repository = request_repository

    def start_data_process(self, ch, method, props, message: Message):
        logging.info("Starting data process")
        self.request_count += 1
        request_id = self.request_count
        logging.info("Saving request with ID [{}] CLIENT_ID [{}] CORRELATION_ID[{}] CLIENT_QUEUE [{}]"\
            .format(request_id, message.source_id, props.correlation_id, props.reply_to))
        request = Request(request_id, message.source_id, props.correlation_id, props.reply_to)
        self.request_repository.add(request_id, request)
        propagate = Message(MIDDLEWARE_MESSAGE_ID, request_id, message.source_id, message.operation_id, INGEST_DATA_WORKER_ID, request_id)
        response = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, message.source_id, request_id)
        #Propagate start process data with Request ID
        self.ingestion_service.ingest_data(propagate)
        self.__respond(ch, method, props, message, response)

    def process_data(self, ch, method, props, message: Message):
        logging.info("Processing Data [{}]".format(message.to_string()))
        #Process data with Request ID
        self.ingestion_service.ingest_data(message)
        response = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, message.source_id, ACK_MESSAGE)
        self.__respond(ch, method, props, message, response)

    def end_data_process(self, ch, method, props, message: Message):
        logging.info("Ending data process")
        #Propagate end process data with Request ID
        self.ingestion_service.ingest_data(message)
        response = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, message.source_id, ACK_MESSAGE)
        self.__respond(ch, method, props, message, response)

    def send_results(self, ch, method, props, message: Message):
        logging.info("Sending results")
        request: Request = self.request_repository.get(message.request_id)
        if request:
            logging.info("Sending results to request[{}]".format(request))
            properties = pika.BasicProperties(reply_to=request.client_queue, correlation_id=request.correlation_id,)
            response = Message(MIDDLEWARE_MESSAGE_ID, request.request_id, message.source_id, message.operation_id, request.client_id, message.body)
            self.__send(ch, method, properties, response)
            self.request_repository.delete(message.request_id)
        else:
            logging.info("Request with ID[{}] not found".format(message.request_id))

    def __respond(self, ch, method, props, request: Message, response: Message):
        logging.info("Respond to client [{}] with [{}]".format(request.source_id, response.to_string()))
        self.__send(ch, method, props, response)

    def __send(self, ch, method, props, message: Message):
        logging.info("Send to [{}] with correlation [{}] message [{}]".format(props.reply_to, props.correlation_id, message.to_string()))
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = props.correlation_id),
                        body=message.to_string())
        
