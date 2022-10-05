import json
import logging
from dependencies.commons.message import Message
from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from dependencies.commons.video import Video
from dependencies.commons.work_service import WorkService
from reporting_service.reporting_check import ReportingCheck
from reporting_service.result_repository import ResultRepository
from reporting_service.results import Results
from reporting_service.video_result import VideoResult

class ReportingService(WorkService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.result_repository = ResultRepository()
        self.reporting_check = ReportingCheck(self.total_routes)
        self.categories_by_country = dict()
        super().__init__(id, group_id, REPORTING_SERVICE_QUEUE)

    def work(self, ch, method, properties, body):
        reporting_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == reporting_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == reporting_message.operation_id:
            self.__storage_video(reporting_message)
        elif END_PROCESS_OP_ID == reporting_message.operation_id:
            self.__check_end_stage(reporting_message)
        elif LOAD_CATEGORIES_OP_ID == reporting_message.operation_id:
            self.__storage_categories(reporting_message)
        else:
            pass

    def __storage_categories(self, reporting_message: Message):
        self.categories_by_country = json.loads(reporting_message.body)
        logging.info("Categories by Country [{}]".format(self.categories_by_country))

    def __storage_video(self, reporting_message: Message):
        video = json_to_video(reporting_message.body)
        request_id = reporting_message.request_id
        self.result_repository.save_filtered_video(request_id, video)

    def __check_end_stage(self, message: Message):
        if FUNNY_FILTER_GROUP_ID == message.source_id:
            self.reporting_check.check_filter()
        elif MAX_WORKER_ID in message.source_id:
            self.result_repository.save_most_viewed_day(message.body)
            self.reporting_check.check_grouper()
        else:
            pass
        if self.reporting_check.check():
            self.__end_stage(message)
        
    def __end_stage(self, message: Message):
        self.middleware_system_client.connect()
        filtered_videos = self.result_repository.get_filtered_videos(message.request_id)
        categorized_videos = self.__get_categorized_filtered_videos(filtered_videos)
        most_viewed_day = self.result_repository.get_most_viewed_day()
        results = Results(categorized_videos, most_viewed_day)
        self.middleware_system_client.call_send_results(message.request_id, str(results))
        self.middleware_system_client.close()

    def __get_categorized_filtered_videos(self, filtered_videos: 'list[Video]'):
        categorized_filtered_videos = list()
        for filtered_video in filtered_videos:
            category = self.categories_by_country[filtered_video.country][filtered_video.category_id]
            categorized_video = VideoResult(filtered_video.id, filtered_video.title, category)
            categorized_filtered_videos.append(categorized_video)
        return categorized_filtered_videos
            
    