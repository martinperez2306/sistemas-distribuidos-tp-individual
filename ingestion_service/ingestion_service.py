from dependencies.commons.constants import *
from dependencies.commons.work_service import WorkService
from dependencies.middlewaresys_client.middlewaresys_client import MiddlewareSystemClient

INGESTION_SERVICE_ID="ingestion_service"##TODO: Obtener de configuracion

class IngestionService(WorkService):
    def __init__(self):
        WorkService.__init__(self, INGESTION_SERVICE_ID, INGESTION_SERVICE_QUEUE)

    def work(self, ch, method, properties, body):
        ingestion_message = self.middleware_system_client.parse_message(body)
        self.middleware_system_client.call_filter_by_likes(ingestion_message)
    
    