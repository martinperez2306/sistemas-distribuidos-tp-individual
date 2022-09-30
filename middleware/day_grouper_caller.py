from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video
from middleware.routing_caller import RoutingCaller

class DayGrouperCaller(RoutingCaller):
    def __init__(self, total_routes):
        RoutingCaller.__init__(self, DAY_GROUPER_EXCHANGE)
        self.total_routes = total_routes

    def group_by_day(self, message: Message):
        group_by_day_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, DAY_GROUPER_WORKER_ID, message.body)
        video = Video(group_by_day_message.body)
        trending_date = video.trending_date
        routing_key = (hash(trending_date) % self.total_routes)
        self.publish_data(group_by_day_message.to_string(), routing_key)