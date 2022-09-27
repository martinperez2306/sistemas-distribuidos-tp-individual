import logging
import pika

from dependencies.commons.video import Video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
LIKE_FILTER_QUEUE = "like_filter_queue"
LIKE_FILTER_ID = "like_filter" ##TODO: Obtener de configuracion
MIN_LIKES_COUNT = 10000000

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
            logging.info("Received {}".format(body))
            like_filter_message = self.middleware_system_client.parse_message(body)
            video = Video(like_filter_message.body)
            logging.info("Video {}".format(str(video)))
            try:
                likes_count = int(video.likes)
                if likes_count > MIN_LIKES_COUNT:
                    self.middleware_system_client.call_storage_data(like_filter_message.request_id, like_filter_message.body)
            except ValueError:
                pass
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=LIKE_FILTER_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()