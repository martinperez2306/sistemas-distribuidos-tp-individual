from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.propagation import Propagation
from dependencies.commons.work_service import WorkService

class Max(WorkService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.propagations = dict()
        self.max_views = 0
        self.trending_date_with_max_views = None
        super().__init__(id, group_id, MAX_QUEUE)

    def work(self, ch, method, properties, body):
        max_message = self.middleware_system_client.parse_message(body)
        self.__process_max(max_message)
        self.__check_next_stage(max_message)

    def __check_next_stage(self, max_message: Message):
        request_id = max_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        propagation.inc_end()
        if propagation.ends_count == self.total_routes:
            self.__next_stage(max_message)
        self.propagations[str(request_id)] = propagation

    def __process_max(self, max_message: Message):
        views_by_date: dict() = eval(max_message.body)
        for trending_date in views_by_date:
            if self.max_views < views_by_date[trending_date]:
                self.max_views = views_by_date[trending_date]
                self.trending_date_with_max_views = trending_date
    
    def __next_stage(self, max_message: Message):
        self.middleware_system_client.connect()
        result_message: Message = Message(max_message.id, max_message.request_id, 
                                        max_message.source_id, max_message.operation_id,
                                        max_message.destination_id, self.trending_date_with_max_views)
        self.middleware_system_client.call_storage_data(result_message)
        self.middleware_system_client.close()
        