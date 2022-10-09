import json
import logging

from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video
from dependencies.commons.propagation import Propagation
from dependencies.commons.routing_serivce import RoutingService

TRENDING_DAYS_COUNT = 21

class TrendingFilter(RoutingService):
    def __init__(self, config_params):
        super().__init__(config_params, TRENDING_FILTER_EXCHANGE)
        self.total_countries = 0
        self.trending_dates_by_video = dict()
        self.countries_by_video = dict()
        self.trending_videos = list()
        self.propagations = dict()

    def work(self, ch, method, properties, body):
        trending_filter_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == trending_filter_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == trending_filter_message.operation_id:
            self.__process_trending(trending_filter_message)
        elif END_PROCESS_OP_ID == trending_filter_message.operation_id:
            self.__check_next_stage(trending_filter_message)
        elif LOAD_TOTAL_COUNTRIES == trending_filter_message.operation_id:
            self.__storage_total_countries(trending_filter_message)
        else:
            pass

    def __storage_total_countries(self, trending_filter_message: Message):
        logging.info("Total Countries [{}]".format(trending_filter_message.body))
        self.total_countries = int(trending_filter_message.body)

    def __process_trending(self, like_filter_message: Message):
        video = Video.from_json(like_filter_message.body)
        logging.debug("Video {}".format(str(video)))
        if self.trending_dates_by_video.get(video.id):
            trending_dates: list = self.trending_dates_by_video.get(video.id)
            self.__add_unique(trending_dates, video.trending_date)
            self.trending_dates_by_video[video.id] = trending_dates
        else:
            trending_dates = list()
            trending_dates.append(video.trending_date)
            self.trending_dates_by_video[video.id] = trending_dates

        if self.countries_by_video.get(video.id):
            countries: list = self.countries_by_video.get(video.id)
            self.__add_unique(countries, video.country)
            self.countries_by_video[video.id] = countries
        else:
            countries = list()
            countries.append(video.country)
            self.countries_by_video[video.id] = countries
  
        if self.__is_trending_video(video) and self.__is_trending_video_in_all_countries(video):
            logging.info("Video is trending in all countries: [{}]".format(str(video)))
            unique = True
            for trending_video in self.trending_videos:
                if video.id == trending_video.id:
                    unique = False
            if unique:             
                self.trending_videos.append(video)

    def __add_unique(self, list: 'list', value):
        if value not in list:
            list.append(value)

    def __is_trending_video(self, video: Video):
         return len(self.trending_dates_by_video.get(video.id)) >= TRENDING_DAYS_COUNT

    def __is_trending_video_in_all_countries(self, video: Video):
        return len(self.countries_by_video.get(video.id)) >= self.total_countries

    def __check_next_stage(self, trending_filter_message: Message):
        request_id = trending_filter_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        propagation.inc_end()
        if propagation.ends_count == self.total_routes:
            self.__next_stage(trending_filter_message)
        self.propagations[str(request_id)] = propagation
    
    def __next_stage(self, trending_filter_message: Message):
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
