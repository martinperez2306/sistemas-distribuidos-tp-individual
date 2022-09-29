from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class IngestionServiceCaller(BaseCaller):
    def __init__(self):
        BaseCaller.__init__(self, INGESTION_SERVICE_QUEUE)
    
    def ingest_data(self, message: Message):
        ingest_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, INGEST_DATA_WORKER_ID, message.body)
        self.publish_data(ingest_message.to_string())