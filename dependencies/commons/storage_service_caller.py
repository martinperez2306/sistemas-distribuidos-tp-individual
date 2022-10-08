from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.work_caller import WorkCaller

class StorageServiceCaller(WorkCaller):
    def __init__(self, config_params):
        super().__init__(REPORTING_SERVICE_QUEUE)
        self.total_routes = int(config_params["service_instances"])
    
    def storage_data(self, message: Message):
        storage_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, STORAGE_DATA_WORKER_ID, message.body)
        if LOAD_CATEGORIES_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.publish_data(storage_message.to_string())
            self.close()
        elif START_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
        elif PROCESS_DATA_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.publish_data(storage_message.to_string())
        elif END_PROCESS_OP_ID == message.operation_id:
            if not self.connection or not self.connection.is_open:
                self.connect()
            self.publish_data(storage_message.to_string())
            self.close()
        else:
            pass