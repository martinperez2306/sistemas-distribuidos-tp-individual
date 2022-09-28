from middleware.base_service import BaseService
from middleware.constants import *
from dependencies.commons.message import Message

class FunnyFilterService(BaseService):
    def __init__(self):
        BaseService.__init__(self, FUNNY_FILTER_QUEUE)
    
    def filter_by_funny_tag(self, message: Message):
        filter_by_like_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, FUNNY_FILTER_OP_ID, message.body)
        self.publish_data(filter_by_like_message.to_string())