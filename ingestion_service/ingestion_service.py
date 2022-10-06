from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.utils import to_json
from dependencies.commons.video import Video
from dependencies.commons.video_input import VideoInput
from dependencies.commons.work_service import WorkService

class IngestionService(WorkService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        super().__init__(id, group_id, INGESTION_SERVICE_QUEUE)
        self.ingested_videos = list()

    def work(self, ch, method, properties, body):
        ingestion_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == ingestion_message.operation_id:
            pass
        elif PROCESS_DATA_OP_ID == ingestion_message.operation_id:
            video_input = VideoInput.from_json(ingestion_message.body)
            video = Video.from_input(video_input)
            self.ingested_videos.append(video)
        elif END_PROCESS_OP_ID == ingestion_message.operation_id:
            self.middleware_system_client.connect()
            self.__process_ingested_videos(ingestion_message)
            self.middleware_system_client.call_filter_by_likes_and_trending(ingestion_message)
            self.middleware_system_client.close()
            self.ingested_videos.clear()

    def __process_ingested_videos(self, ingestion_message: Message):
        for ingested_video in self.ingested_videos:
            ingested_video_message = Message(ingestion_message.id, ingestion_message.request_id, ingestion_message.source_id,
                                        PROCESS_DATA_OP_ID, ingestion_message.destination_id, to_json(ingested_video.__dict__))
            self.middleware_system_client.call_filter_by_likes_and_trending(ingested_video_message)
        pass
        
    
    