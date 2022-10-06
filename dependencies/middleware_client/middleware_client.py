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

MIDDLEWARE_ID = "middleware"

class MiddlewareClient:
    def __init__(self, host, middleware_queue_id, storage_path):
        self.host = host
        self.middleware_queue_id = middleware_queue_id
        self.storage_path = storage_path
        self.client_id = 1
        self.connection = None
        self.channel = None
        self.callback_queue = None
        self.response = None
        self.corr_id = None
        self.waiting_results = False

    def connect(self):
        logging.info("Connecting to Middleware")
        self.corr_id = str(uuid.uuid4())
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.middleware_queue_id, durable=True)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

    def call_start_data_process(self, query: VideosQuery):
        logging.info("Calling start data process")
        request = Message(CLIENT_MESSAGE_ID, 0, self.client_id, START_PROCESS_OP_ID, MIDDLEWARE_ID, to_json(query.__dict__))
        self.__request(request)
        return self.corr_id

    def call_process_data(self, request_id: int, video: Video):
        logging.info("Calling process data")
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, PROCESS_DATA_OP_ID, MIDDLEWARE_ID, to_json(video.__dict__))
        self.__request(request)

    def call_end_data_process(self, request_id: int):
        logging.info("Calling end data process")
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, END_PROCESS_OP_ID, MIDDLEWARE_ID, "")
        self.__request(request)

    def call_download_thumbnails(self, request_id: int):
        logging.info("Calling download thumbnails")
        request = Message(CLIENT_MESSAGE_ID, request_id, self.client_id, DOWNLOAD_THUMBNAILS, MIDDLEWARE_ID, "")
        self.__request(request)

    def __on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            logging.debug("Recieved: {}".format(body))
            response = body.decode(UTF8_ENCODING)
            self.response = parse_message(response)
            if self.response.operation_id == SEND_RESULTS_OP_ID:
                logging.info("Results Recieved. Stop consuming.")
                self.channel.stop_consuming()
            elif self.response.operation_id == DOWNLOAD_THUMBNAILS:
                self.__storage(ch, method, props, body)
            elif self.response.operation_id == DOWNLOAD_COMPLETE:
                logging.info("Download complete. Stop consuming.")
                self.channel.stop_consuming()
            else:
                pass
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def wait_get_results(self, request_id: str):
        logging.info("Waiting for results of request_id [{}]".format(request_id))
        self.response = None
        self.waiting_results = True
        self.channel.basic_consume(
            queue=self.callback_queue, on_message_callback=self.__on_response)

        self.channel.start_consuming()
        return self.response

    def __request(self, message: Message):
        logging.debug("Send request message: {}".format(message.to_string()))
        self.channel.basic_publish(exchange='', 
            routing_key=self.middleware_queue_id, 
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message.to_string().encode(UTF8_ENCODING))

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
            logging.error("Error downloading thumbnail")
            traceback.print_exc()

    def close(self):
        logging.info("Closing connection to Middleware")
        self.connection.close()