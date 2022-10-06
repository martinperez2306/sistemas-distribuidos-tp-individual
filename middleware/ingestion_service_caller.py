from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class IngestionServiceCaller(BaseCaller):
    def __init__(self):
        super().__init__(INGESTION_SERVICE_QUEUE)
    
    def ingest_data(self, message: Message):
        ingest_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, INGEST_DATA_WORKER_ID, message.body)
        if START_PROCESS_OP_ID == message.operation_id:
            self.connect()
            self.publish_data(ingest_message.to_string())
        elif PROCESS_DATA_OP_ID == message.operation_id:
            self.publish_data(ingest_message.to_string())
        elif END_PROCESS_OP_ID == message.operation_id:
            self.publish_data(ingest_message.to_string())
            self.close()
        else:
            pass
        