import datetime
import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

DAY_GROUPER_ID="day_grouper_1"##TODO: Obtener de configuracion
DATE_FORMAT='%Y-%m-%dT%H:%M:%SZ'

class DayGrouper:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, DAY_GROUPER_ID)
        self.group_id = DAY_GROUPER_ID.split("_")[2]
        self.days_grouped = dict()

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=DAY_GROUPER_EXCHANGE, exchange_type='direct')
        result = self.channel.queue_declare(queue='', exclusive=True)#TODO: Tal vez definir yo la queue?
        queue_name = result.method.queue
        self.channel.queue_bind(exchange=DAY_GROUPER_EXCHANGE, queue=queue_name, routing_key=self.group_id)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            gruping_message = self.middleware_system_client.parse_message(body)
            if PROCESS_DATA_OP_ID == gruping_message.operation_id:
                self.__save_by_group(gruping_message)
            else:
                self.__propagate_message(ch, method, properties, body, gruping_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue_name, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __save_by_group(self, gruping_message: Message):
        video = Video(gruping_message.body)
        logging.info("Video {}".format(str(video)))
        #trending_date = datetime.datetime.strptime(video.trending_date, DATE_FORMAT)
        trending_date = video.trending_date
        logging.info("Trending date {}".format(trending_date))
        if self.days_grouped.get(trending_date):
            self.days_grouped[trending_date] = self.days_grouped[trending_date] + video.view_count
        else:
            self.days_grouped[trending_date] = video.view_count
        logging.info("View Count for date {} is {}".format(trending_date, self.days_grouped[trending_date]))

    def __propagate_message(self, ch, method, properties, body, gruping_message: Message):
        self.middleware_system_client.call_storage_data(gruping_message)