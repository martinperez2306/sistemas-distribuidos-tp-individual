from .base_service import BaseService
from .constants import *
from .message import Message

class LikeFilterService(BaseService):
    def __init__(self):
        BaseService.__init__(self, LIKE_FILTER_QUEUE)
    
    def filter_by_likes(self, message: Message):
        filter_by_like_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, LIKE_FILTER_ID, message.body)
        self.publish_data(filter_by_like_message.to_string())