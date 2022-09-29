from middleware.base_service import BaseCaller
from middleware.constants import *
from dependencies.commons.message import Message

class StorageService(BaseCaller):
    def __init__(self):
        BaseCaller.__init__(self, REPORTING_SERVICE_QUEUE)
    
    def storage_data(self, message: Message):
        storage_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, STORAGE_DATA_WORKER_ID, message.body)
        self.publish_data(storage_message.to_string())