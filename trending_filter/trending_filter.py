import json
import logging
import pika

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.routing_serivce import RoutingService
from dependencies.commons.utils import json_to_video

TRENDING_DAYS_COUNT = 21

class TrendingFilter(RoutingService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_countries = 0
        self.trending_dates_by_video = dict()
        self.countries_by_video = dict()
        self.trending_videos = list()
        super().__init__(id, group_id, TRENDING_FILTER_EXCHANGE)

    def work(self, ch, method, properties, body):
        trending_filter_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == trending_filter_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == trending_filter_message.operation_id:
            self.__process_trending(trending_filter_message)
        elif END_PROCESS_OP_ID == trending_filter_message.operation_id:
            self.__next_stage(trending_filter_message)
        elif LOAD_TOTAL_COUNTRIES == trending_filter_message.operation_id:
            self.__storage_total_countries(trending_filter_message)
        else:
            pass

    def __storage_total_countries(self, trending_filter_message: Message):
        self.categories_by_country = trending_filter_message.body
        logging.info("Total Countries [{}]".format(self.categories_by_country))

    def __process_trending(self, like_filter_message: Message):
        video = json_to_video(like_filter_message.body)
        logging.debug("Video {}".format(str(video)))
        if self.trending_dates_by_video.get(video.id):
            trending_dates: list = self.trending_dates_by_video.get(video.id)
            trending_dates.append(video.trending_date)
        else:
            trending_dates = list()
            trending_dates.append(video.trending_date)
        if self.countries_by_video.get(video.id):
            countries: list = self.countries_by_video.get(video.id)
            countries.append(video.country)
        else:
            countries = list()
            countries.append(video.country)
        if self.__is_trending_video(video) and self.__is_trending_video_in_all_countries(video):
            self.trending_videos.append(video)

    def __is_trending_video(self, video):
         return len(self.trending_dates_by_video.get(video.id)) >= TRENDING_DAYS_COUNT

    def __is_trending_video_in_all_countries(self, video):
        return len(self.countries_by_video.get(video.id)) >= self.total_countries


    def __next_stage(self, trending_filter_message: Message):
        self.middleware_system_client.connect()
        init_message = Message(trending_filter_message.id, trending_filter_message.request_id, trending_filter_message.source_id,
                                        START_PROCESS_OP_ID, trending_filter_message.destination_id, "")
        self.middleware_system_client.call_storage_data(init_message)
        for trending_video in self.trending_videos:
            trending_video_message = Message(trending_filter_message.id, trending_filter_message.request_id, trending_filter_message.source_id,
                                        PROCESS_DATA_OP_ID, trending_filter_message.destination_id, json.dumps(trending_video.__dict__))
            self.middleware_system_client.call_storage_data(trending_video_message)
        end_message = Message(trending_filter_message.id, trending_filter_message.request_id, trending_filter_message.source_id,
                                        END_PROCESS_OP_ID, trending_filter_message.destination_id, "")
        self.middleware_system_client.call_storage_data(end_message)
        self.middleware_system_client.close()
