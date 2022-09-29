from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class FunnyFilterCaller(BaseCaller):
    def __init__(self):
        BaseCaller.__init__(self, FUNNY_FILTER_QUEUE)
    
    def filter_by_funny_tag(self, message: Message):
        filter_by_like_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, FUNNY_FILTER_WORKER_ID, message.body)
        self.publish_data(filter_by_like_message.to_string())