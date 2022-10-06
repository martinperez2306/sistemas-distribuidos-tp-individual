from dependencies.commons.constants import *
from middleware.base_caller import BaseCaller
from dependencies.commons.message import Message

class StorageServiceCaller(BaseCaller):
    def __init__(self, config_params):
        super().__init__(REPORTING_SERVICE_QUEUE)
        self.total_routes = int(config_params["service_instances"])
        self.popular_and_funny_eofs = 0
        self.trending_eofs = 0
        self.most_liked_eof = 0
    
    def storage_data(self, message: Message):
        storage_message = Message(MIDDLEWARE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, STORAGE_DATA_WORKER_ID, message.body)
        if LOAD_CATEGORIES_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.publish_data(storage_message.to_string())
            self.close()
        elif START_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
        elif PROCESS_DATA_OP_ID == message.operation_id:
            self.publish_data(storage_message.to_string())
        elif END_PROCESS_OP_ID == message.operation_id:
            self.__increment_eofs(message)
            self.publish_data(storage_message.to_string())
            if self.__all_eof():
                self.close()
        else:
            pass

    def __increment_eofs(self, message: Message):
        if FUNNY_FILTER_GROUP_ID == message.source_id:
            self.popular_and_funny_eofs += 1
        elif TRENDING_FILTER_GROUP_ID:
            self.trending_eofs += 1
        elif MAX_WORKER_ID == message.source_id:
            self.most_liked_eof += 1
        else:
            pass

    def __all_eof(self):
        return (self.popular_and_funny_eofs >= self.total_routes and self.trending_eofs >= self.total_routes and self.most_liked_eof >= self.total_routes)