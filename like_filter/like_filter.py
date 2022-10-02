import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import json_to_video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
LIKE_FILTER_QUEUE = "like_filter_queue"
LIKE_FILTER_ID = "like_filter" ##TODO: Obtener de configuracion
MIN_LIKES_COUNT = 5000000

class LikeFilter:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, LIKE_FILTER_ID)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=LIKE_FILTER_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.debug("Received {}".format(body))
            like_filter_message = self.middleware_system_client.parse_message(body)
            if PROCESS_DATA_OP_ID == like_filter_message.operation_id:
                self.__process_filter_by_like(ch, method, properties, body, like_filter_message)
            else:
                self.__propagate_message(ch, method, properties, body, like_filter_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=LIKE_FILTER_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __process_filter_by_like(self, ch, method, properties, body, like_filter_message: Message):
        video = json_to_video(like_filter_message.body)
        logging.debug("Video {}".format(str(video)))
        try:
            likes_count = int(video.likes)
            if likes_count > MIN_LIKES_COUNT:
                logging.info("Video is popular: [{}]".format(str(video)))
                self.middleware_system_client.call_filter_by_tag(like_filter_message)
                self.middleware_system_client.call_group_by_day(like_filter_message)
        except ValueError:
            pass

    def __propagate_message(self, ch, method, properties, body, like_filter_message: Message):
        self.middleware_system_client.call_filter_by_tag(like_filter_message)
        self.middleware_system_client.call_group_by_day(like_filter_message)
