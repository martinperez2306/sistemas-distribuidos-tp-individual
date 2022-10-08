import pika
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.work_caller import WorkCaller

class StorageServiceCaller(WorkCaller):
    def __init__(self, config_params):
        super().__init__(REPORTING_SERVICE_QUEUE)
        self.total_routes = int(config_params["service_instances"])

    def storage_categories(self, categories_message: Message):
        if not self.connection or not self.connection.is_open:
            self.connect()
        self.publish_data(categories_message.to_string())
        self.close()
    
    def storage_data(self, message: Message):
        storage_message = Message(SERVICE_MESSAGE_ID, message.request_id, message.source_id, message.operation_id, STORAGE_DATA_WORKER_ID, message.body)
        if START_PROCESS_OP_ID == message.operation_id:
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

    def get_results(self, result_message: Message, properties:pika.BasicProperties):
        if not self.connection or not self.connection.is_open:
            self.connect()
        self.publish_data_with_props(result_message.to_string(), properties)
        self.close()

    def download_thumbnail(self, download_message: Message, props: pika.BasicProperties):
        if not self.connection or not self.connection.is_open:
                self.connect()
        self.publish_data_with_props(download_message.to_string(), props)
        self.close()