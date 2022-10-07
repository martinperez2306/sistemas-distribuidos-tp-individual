from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.middlewaresys_client.work_caller import WorkCaller

class MaxCaller(WorkCaller):
    def __init__(self, config_params):
        super().__init__(MAX_QUEUE)
        self.total_routes = int(config_params["service_instances"])
        self.callings = 0
    
    def get_max(self, message: Message):
        self.callings += 1
        if not self.connection or not self.connection.is_open:
                self.connect()
        max_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, MAX_WORKER_ID, message.body)
        self.publish_data(max_message.to_string())
        if self.callings >= self.total_routes:
            self.close()