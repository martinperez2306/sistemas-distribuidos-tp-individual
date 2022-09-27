from middleware.base_service import BaseService
from middleware.constants import *
from dependencies.commons.message import Message

class StorageService(BaseService):
    def __init__(self):
        BaseService.__init__(self, REPORTING_SERVICE_QUEUE)
    
    def storage_data(self, message: Message):
        storage_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, STORAGE_DATA_ID, message.body)
        self.publish_data(storage_message.to_string())