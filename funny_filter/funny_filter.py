import logging
import pika

from dependencies.commons.message import Message
from dependencies.commons.video import Video
from dependencies.middlewaresys_client.constants import *
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
FUNNY_FILTER_QUEUE = "funny_filter_queue"
FUNNY_FILTER_ID = "funny_filter" ##TODO: Obtener de configuracion
FUNNY_TAG = "funny"

class LikeFilter:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, FUNNY_FILTER_ID)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=FUNNY_FILTER_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            funny_filter_message = self.middleware_system_client.parse_message(body)
            if PROCESS_DATA_OP_ID == funny_filter_message.operation_id:
                self.__process_filter_by_funny_tag(ch, method, properties, body, funny_filter_message)
            else:
                self.__propagate_message(ch, method, properties, body, funny_filter_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=FUNNY_FILTER_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __process_filter_by_funny_tag(self, ch, method, properties, body, funny_filter_message: Message):
        video = Video(funny_filter_message.body)
        logging.info("Video {}".format(str(video)))
        tags = video.tags.split("|")
        if FUNNY_TAG in tags:
            self.middleware_system_client.call_storage_data(funny_filter_message)

    def __propagate_message(self, ch, method, properties, body, funny_filter_message: Message):
        self.middleware_system_client.call_storage_data(funny_filter_message)