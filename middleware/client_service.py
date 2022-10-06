import logging
import pika
from dependencies.commons.VideosQuery import VideosQuery

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import to_json
from middleware.ingestion_service_caller import IngestionServiceCaller
from middleware.request import Request
from middleware.request_repository import RequestRepository
from middleware.storage_service_caller import StorageServiceCaller
from middleware.trending_filter_caller import TrendingFilterCaller

ACK_MESSAGE = "ACK"

class ClientService:
    def __init__(self, ingestion_service_caller: IngestionServiceCaller, 
                        trending_filter_caller: TrendingFilterCaller,
                        storage_service_caller: StorageServiceCaller, 
                        request_repository: RequestRepository):
        self.request_count = 0
        self.ingestion_service_caller = ingestion_service_caller
        self.trending_filter_caller = trending_filter_caller
        self.storage_service_caller = storage_service_caller
        self.request_repository = request_repository

    def start_data_process(self, ch, method, props, message: Message):
        logging.info("Starting data process")
        self.request_count += 1
        request_id = self.request_count
        query = VideosQuery.from_json(message.body)
        logging.debug("Saving request with ID [{}] CLIENT_ID [{}] CORRELATION_ID[{}] CLIENT_QUEUE [{}]"\
            .format(request_id, message.source_id, props.correlation_id, props.reply_to))
        #Create request and save it to trace client
        request = Request(request_id, message.source_id, props.correlation_id, props.reply_to)
        self.request_repository.add(request_id, request)
        #Save categories
        categories_message = Message(MIDDLEWARE_MESSAGE_ID, request_id, message.source_id, LOAD_CATEGORIES_OP_ID, STORAGE_DATA_WORKER_ID, to_json(query.categories))
        self.storage_service_caller.storage_data(categories_message)
        #Save total countries
        total_countries_message = Message(MIDDLEWARE_MESSAGE_ID, request_id, message.source_id, LOAD_TOTAL_COUNTRIES, TRENDING_FILTER_GROUP_ID, query.total_countries)
        self.trending_filter_caller.filter_by_trending(total_countries_message)
        #Propagate start process data with Request ID
        propagate = Message(MIDDLEWARE_MESSAGE_ID, request_id, message.source_id, message.operation_id, INGEST_DATA_WORKER_ID, request_id)
        self.ingestion_service_caller.connect()
        self.ingestion_service_caller.ingest_data(propagate)
        #Responde to client
        response = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, message.source_id, request_id)
        self.__respond(ch, method, props, message, response)

    def process_data(self, ch, method, props, message: Message):
        logging.info("Processing Data [{}]".format(message.to_string()))
        #Process data with Request ID
        self.ingestion_service_caller.ingest_data(message)
        #Responde to client
        response = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, message.source_id, ACK_MESSAGE)
        self.__respond(ch, method, props, message, response)

    def end_data_process(self, ch, method, props, message: Message):
        logging.info("Ending data process")
        #Propagate end process data with Request ID
        self.ingestion_service_caller.ingest_data(message)
        self.ingestion_service_caller.close()
        #Responde to client
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
                        body=message.to_string().encode(UTF8_ENCODING))
        
