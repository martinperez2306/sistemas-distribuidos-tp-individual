#!/usr/bin/env python3
import base64
import io
import logging
import traceback
import uuid
import pika
import PIL.Image as Image
from dependencies.commons.thumbnail import Thumbnail
from dependencies.commons.videos_query import VideosQuery
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import parse_message, to_json
from dependencies.commons.video import Video
from dependencies.commons.ingestion_service_caller import IngestionServiceCaller
from dependencies.commons.trending_filter_caller import TrendingFilterCaller
from dependencies.commons.storage_service_caller import StorageServiceCaller


MIDDLEWARE_ID = "middleware"

class MiddlewareClient:
    def __init__(self, storage_path, config_params):
        self.storage_path = storage_path
        self.client_id = 1
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.corr_id = None
        self.results = None
        self.ingestion_service_caller = IngestionServiceCaller(config_params)
        self.trending_filter_caller = TrendingFilterCaller(config_params)
        self.storage_service_caller = StorageServiceCaller(config_params)

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(
            queue=self.callback_queue, on_message_callback=self.__on_response)
        logging.info("Connecting to broker and listening in queue [{}]".format(self.callback_queue))

    def call_start_data_process(self, query: VideosQuery):
        logging.info("Calling start data process")
        self.corr_id = str(uuid.uuid4())
        logging.info("Request ID [{}]".format(self.corr_id))
        #Send categories
        categories_message = Message(CLIENT_MESSAGE_ID, self.corr_id, self.client_id, LOAD_CATEGORIES_OP_ID, STORAGE_DATA_WORKER_ID, to_json(query.categories))
        self.storage_service_caller.storage_categories(categories_message)
        #Send total countries
        total_countries_message = Message(CLIENT_MESSAGE_ID, self.corr_id, self.client_id, LOAD_TOTAL_COUNTRIES, TRENDING_FILTER_GROUP_ID, query.total_countries)
        self.trending_filter_caller.load_total_countries(total_countries_message)
        #Send start data ingest
        request = Message(CLIENT_MESSAGE_ID, self.corr_id, self.client_id, START_PROCESS_OP_ID, INGEST_DATA_GROUP_ID, to_json(query.__dict__))
        self.ingestion_service_caller.ingest_data(request)
        return self.corr_id

    def call_process_data(self, request_id: int, video: Video):
        logging.info("Calling process data")
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, PROCESS_DATA_OP_ID, INGEST_DATA_GROUP_ID, to_json(video.__dict__))
        self.ingestion_service_caller.ingest_data(request)

    def call_end_data_process(self, request_id: int):
        logging.info("Calling end data process")
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, END_PROCESS_OP_ID, INGEST_DATA_GROUP_ID, "")
        self.ingestion_service_caller.ingest_data(request)

    def call_get_results(self, reques_id: int):
        logging.info("Calling get results")
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            reply_to=self.callback_queue,
            correlation_id=self.corr_id,
        )
        result_message = Message(CLIENT_MESSAGE_ID, reques_id, self.client_id, SEND_RESULTS_OP_ID, STORAGE_DATA_WORKER_ID, "")
        self.storage_service_caller.get_results(result_message, properties)

    def wait_get_results(self, request_id: str):
        logging.info("Waiting for results of request_id [{}]".format(request_id))
        self.response = None
        self.results = None
        self.channel.start_consuming()
        return self.results

    def __on_response(self, ch, method, props, body):
        logging.info("Getting response with correlation [{}]".format(props.correlation_id))
        if self.corr_id == props.correlation_id:
            logging.debug("Recieved: {}".format(body))
            response = body.decode(UTF8_ENCODING)
            self.response = parse_message(response)
            if self.response.operation_id == SEND_RESULTS_OP_ID:
                logging.info("Results Recieved.")
                self.__save_results()
            elif self.response.operation_id == DOWNLOAD_THUMBNAILS:
                logging.info("Downloading thumbnail.")
                self.__storage(ch, method, props, body)
            elif self.response.operation_id == DOWNLOAD_COMPLETE:
                logging.info("Download complete. Stop consuming.")
                self.channel.stop_consuming()
            else:
                pass
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def __save_results(self):
        self.results = self.response

    def __storage(self, ch, method, props, body):
        try:
            thumbnail = Thumbnail.from_json(self.response.body)
            filename = thumbnail.filename
            logging.info("Storaging file with name [{}]".format(filename))
            path = self.storage_path + "/" + filename
            b = base64.b64decode(thumbnail.base64)
            logging.info("b64 [{}]".format(b))
            image = Image.open(io.BytesIO(b))
            image.save(path)
        except Exception as e:
            logging.error("Error downloading thumbnail [{}]".format(self.response.body))
            traceback.print_exc()

    def close(self):
        logging.info("Closing connections to Middleware")
        self.connection.close()
        self.ingestion_service_caller.close()
        self.trending_filter_caller.close()
        self.storage_service_caller.close()