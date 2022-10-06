from dependencies.commons.constants import *
from dependencies.commons.work_service import WorkService

class IngestionService(WorkService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        super().__init__(id, group_id, INGESTION_SERVICE_QUEUE)

    def work(self, ch, method, properties, body):
        ingestion_message = self.middleware_system_client.parse_message(body)
        if START_PROCESS_OP_ID == ingestion_message.operation_id:
            self.middleware_system_client.connect()
            self.middleware_system_client.call_filter_by_likes(ingestion_message)
            self.middleware_system_client.call_filter_by_trending(ingestion_message)
        elif PROCESS_DATA_OP_ID == ingestion_message.operation_id:
            self.middleware_system_client.call_filter_by_likes(ingestion_message)
            self.middleware_system_client.call_filter_by_trending(ingestion_message)
        elif END_PROCESS_OP_ID == ingestion_message.operation_id:
            self.middleware_system_client.call_filter_by_likes(ingestion_message)
            self.middleware_system_client.call_filter_by_trending(ingestion_message)
            self.middleware_system_client.close()
        
    
    