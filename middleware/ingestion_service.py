from middleware.base_service import BaseService
from middleware.constants import *
from dependencies.commons.message import Message

class IngestionService(BaseService):
    def __init__(self):
        BaseService.__init__(self, INGESTION_SERVICE_QUEUE)
    
    def ingest_data(self, message: Message):
        ingest_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, INGEST_DATA_ID, message.body)
        self.publish_data(ingest_message.to_string())