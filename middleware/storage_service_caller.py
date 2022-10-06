from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class StorageServiceCaller(BaseCaller):
    def __init__(self):
        super().__init__(REPORTING_SERVICE_QUEUE)
    
    def storage_data(self, message: Message):
        storage_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, STORAGE_DATA_WORKER_ID, message.body)
        self.publish_data(storage_message.to_string())