import logging
import traceback
import pika
import signal
import time

from dependencies.commons.constants import *
from dependencies.commons.work_service import WorkService
from middleware.message_handler import MessageHandler

class Middleware(WorkService):

    def __init__(self, config_params):
        super().__init__(config_params, MIDDLEWARE_QUEUE)
        self.ingested_videos = list()
        self.message_handler = MessageHandler(self.middleware_system_client, config_params)

    def work(self, ch, method, properties, body):
        self.message_handler.handle_message(ch, method, properties, body)