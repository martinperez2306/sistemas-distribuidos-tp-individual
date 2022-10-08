import json
import logging
import os
import pathlib
import pika
from dependencies.commons.message import Message
from dependencies.commons.constants import *
from dependencies.commons.utils import json_to_video
from dependencies.commons.video import Video
from dependencies.commons.work_service import WorkService
from reporting_service.reporting_check import ReportingCheck
from reporting_service.result_repository import ResultRepository
from reporting_service.results import Results
from reporting_service.thumbnail_downlader import ThumbnailDownloader
from reporting_service.video_result import VideoResult

class ReportingService(WorkService):
    def __init__(self, config_params):
        super().__init__(config_params, REPORTING_SERVICE_QUEUE)
        self.reply_to = None
        self.total_routes = int(config_params["service_instances"])
        self.result_repository = ResultRepository()
        self.reporting_check = ReportingCheck(self.total_routes)
        self.categories_by_country = dict()
        self.thumbnail_downloader = ThumbnailDownloader()

    def work(self, ch, method, properties, body):
        reporting_message = self.middleware_system_client.parse_message(body)
        if LOAD_CATEGORIES_OP_ID == reporting_message.operation_id:
            self.__storage_categories(reporting_message, properties)
        elif START_PROCESS_OP_ID == reporting_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == reporting_message.operation_id:
            self.__storage_video(reporting_message)
        elif END_PROCESS_OP_ID == reporting_message.operation_id:
            self.__check_end_stage(reporting_message)
        elif SEND_RESULTS_OP_ID == reporting_message.operation_id:\
            self.__save_reply_to(reporting_message, properties)
        elif DOWNLOAD_THUMBNAILS == reporting_message.operation_id:
            self.__upload_thumbnails_to_client(reporting_message)
        else:
            pass

    def __storage_categories(self, reporting_message: Message, properties: pika.BasicProperties):
        self.categories_by_country = json.loads(reporting_message.body)
        logging.info("Categories by Country [{}] for reply to queue [{}]".format(self.categories_by_country, self.reply_to))

    def __storage_video(self, reporting_message: Message):
        logging.info("Storaging video")
        video = json_to_video(reporting_message.body)
        request_id = reporting_message.request_id
        if FUNNY_FILTER_GROUP_ID == reporting_message.source_id:
            self.result_repository.save_popular_and_funny_video(request_id, video)
        elif TRENDING_FILTER_GROUP_ID == reporting_message.source_id:
            self.result_repository.save_trending_video(request_id, video)
        else:
            pass

    def __check_end_stage(self, message: Message):
        logging.info("Checking end stage")
        if FUNNY_FILTER_GROUP_ID == message.source_id:
            self.reporting_check.eof_funny()
        elif TRENDING_FILTER_GROUP_ID == message.source_id:
            self.reporting_check.eof_trending()
        elif MAX_WORKER_ID == message.source_id:
            self.result_repository.save_most_viewed_day(message.body)
            self.reporting_check.eof_max()
        else:
            pass
        if self.reporting_check.check_eofs():
            self.__end_stage(message)
        
    def __end_stage(self, message: Message):
        logging.info("Ending stage and sending results for client")
        trending_videos = self.result_repository.get_trending_videos(message.request_id)
        filtered_videos = self.result_repository.get_filtered_videos(message.request_id)
        categorized_videos = self.__get_categorized_filtered_videos(filtered_videos)
        most_viewed_day = self.result_repository.get_most_viewed_day()
        results = Results(categorized_videos, most_viewed_day)
        self.__download_thumnbails(trending_videos)
        self.middleware_system_client.call_send_results(message.request_id, self.reply_to, str(results))
        self.__upload_thumbnails_to_client(message)
        
    def __save_reply_to(self, message: Message, properties: pika.BasicProperties):
        logging.info("Saving replying queue for client [{}]".format(properties.reply_to))
        self.reply_to = properties.reply_to
         
    def __get_categorized_filtered_videos(self, filtered_videos: 'list[Video]'):
        categorized_filtered_videos = list()
        for filtered_video in filtered_videos:
            category = self.categories_by_country[filtered_video.country][filtered_video.category_id]
            categorized_video = VideoResult(filtered_video.id, filtered_video.title, category)
            categorized_filtered_videos.append(categorized_video)
        return categorized_filtered_videos

    def __download_thumnbails(self, trending_videos: 'list[Video]'):
        logging.info("Download thumbnails into system")
        if trending_videos:
            for trendind_video in trending_videos:
                self.thumbnail_downloader.download(trendind_video)

    def __upload_thumbnails_to_client(self, message: Message):
        logging.info("Uploading thumbnails to client")
        request_id = message.request_id
        for path in pathlib.Path(THUMBNAILS_STORAGE).iterdir():
            if path.is_file():
                basename = str(os.path.basename(path))
                with open(path, 'rb') as thumbnail:
                    file = thumbnail.read()
                    self.middleware_system_client.call_upload_thumbnail(request_id, self.reply_to, basename, file)
        self.middleware_system_client.call_upload_complete(request_id, self.reply_to)