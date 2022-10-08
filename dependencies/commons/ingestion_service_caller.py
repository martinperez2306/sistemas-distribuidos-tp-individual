from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video
from dependencies.commons.video_input import VideoInput
from dependencies.commons.routing_caller import RoutingCaller

class IngestionServiceCaller(RoutingCaller):
    def __init__(self, config_params):
        super().__init__(INGESTION_SERVICE_EXCHANGE)
        self.total_routes = int(config_params["service_instances"])
    
    def ingest_data(self, message: Message):
        ingest_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, INGEST_DATA_GROUP_ID, message.body)
        if START_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(ingest_message)
        elif PROCESS_DATA_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            video_input = VideoInput.from_json(ingest_message.body)
            video = Video.from_input(video_input)
            video_id = video.id
            routing_key = INGEST_DATA_GROUP_ID + "_" + str((hash(video_id) % self.total_routes) + 1)
            self.publish_data(ingest_message.to_string(), str(routing_key))
        elif END_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.__broadcast(ingest_message)
            self.close()
        else:
            pass

    def __broadcast(self, message):
        for route in range(self.total_routes):
            routing_key = routing_key = INGEST_DATA_GROUP_ID + "_" + str((route + 1))
            self.publish_data(message.to_string(), str(routing_key))
        