from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.middlewaresys_client.work_caller import WorkCaller

class MiddlewareCaller(WorkCaller):
    def __init__(self, config_params):
        super().__init__(MIDDLEWARE_QUEUE)
        self.total_routes = int(config_params["service_instances"])
    
    def send_results(self, result_message: Message):
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data(result_message.to_string())
        self.close()

    def upload_thumbnail(self, upload_message: Message):
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data(upload_message.to_string())
        self.close()

    def upload_complete(self, upload_message: Message):
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data(upload_message.to_string())
        self.close()