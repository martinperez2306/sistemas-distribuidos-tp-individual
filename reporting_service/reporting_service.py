import logging
import pika
from dependencies.commons.message import Message

from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from reporting_service.reporting_check import ReportingCheck
from reporting_service.result_repository import ResultRepository
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient
from reporting_service.results import Results
from reporting_service.video_result import VideoResult

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"
REPORTING_SERVICE_QUEUE = "reporting_service_queue"
REPORTING_SERVICE_ID="reporting_service" ##TODO: Obtener de configuracion

class ReportingService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.middleware_system_client = MiddlewareSystemClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE, REPORTING_SERVICE_ID)
        self.result_repository = ResultRepository()
        self.reporting_check = ReportingCheck()

    def run(self):
        self.middleware_system_client.connect()
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=REPORTING_SERVICE_QUEUE, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            reporting_message = self.middleware_system_client.parse_message(body)
            if PROCESS_DATA_OP_ID == reporting_message.operation_id:
                self.__storage_video(ch, method, properties, body, reporting_message)
            if END_PROCESS_OP_ID == reporting_message.operation_id:
                self.__handle_end_process(ch, method, properties, body, reporting_message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=REPORTING_SERVICE_QUEUE, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def __storage_video(self, ch, method, properties, body, reporting_message: Message):
        video = json_to_video(reporting_message.body)
        videoResult = VideoResult(video.id, video.title, video.category_id)
        request_id = reporting_message.request_id
        self.result_repository.save_filtered_video(request_id, videoResult)

    def __handle_end_process(self, ch, method, properties, body, message: Message):
        if FUNNY_FILTER_WORKER_ID == message.source_id:
            self.reporting_check.check_filter()
        elif MAX_WORKER_ID in message.source_id:
            self.result_repository.save_most_viewed_day(message.body)
            self.reporting_check.check_grouper()
        else:
            pass
        if self.reporting_check.check():
            filtered_videos = self.result_repository.get_filtered_videos(message.request_id)
            most_viewed_day = self.result_repository.get_most_viewed_day()
            results = Results(filtered_videos, most_viewed_day)
            self.middleware_system_client.call_send_results(message.request_id, str(results))
    
    