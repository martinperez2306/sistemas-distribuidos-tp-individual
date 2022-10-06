from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class MaxCaller(BaseCaller):
    def __init__(self):
        super().__init__(MAX_QUEUE)
    
    def get_max(self, message: Message):
        self.connect()
        max_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, MAX_WORKER_ID, message.body)
        self.publish_data(max_message.to_string())
        self.close()