import datetime
import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

class Max:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, MAX_WORKER_ID)

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=MAX_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            max_message = self.middleware_system_client.parse_message(body)
            if END_PROCESS_OP_ID == max_message.operation_id:
                self.__process_max(ch, method, properties, body, max_message)
            else:
                self.__propagate_message(ch, method, properties, body, max_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=MAX_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __process_max(self, ch, method, properties, body, max_message: Message):
        days_grouped: dict() = eval(max_message.body)
        max = 0
        max_trend_date = None
        for trending_date in days_grouped:
            if max < days_grouped[trending_date]:
                max = days_grouped[trending_date]
                max_trend_date = trending_date
        result_message: Message = Message(max_message.id, max_message.request_id, 
                                            max_message.source_id, max_message.operation_id,
                                            max_message.destination_id, max_trend_date)
        self.__propagate_message(ch, method, properties, body, result_message)

    def __propagate_message(self, ch, method, properties, body, max_message: Message):
        self.middleware_system_client.call_storage_data(max_message)