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
        WorkService.__init__(self, id, group_id, MAX_QUEUE)

    def work(self, ch, method, properties, body):
        max_message = self.middleware_system_client.parse_message(body)
        self.__propagate_message(ch, method, properties, body, max_message)

    def __propagate_message(self, ch, method, properties, body, max_message: Message):
        request_id = max_message.request_id
        propagation: Propagation = self.propagations.get(str(request_id))
        if not propagation:
            propagation = Propagation()
        if START_PROCESS_OP_ID == max_message.operation_id:
            propagation.inc_start()
            if propagation.starts_count == self.total_routes:
                self.middleware_system_client.call_storage_data(max_message)
        elif END_PROCESS_OP_ID == max_message.operation_id:
            propagation.inc_end()
            self.__process_max(max_message)
            if propagation.ends_count == self.total_routes:
                result_message: Message = Message(max_message.id, max_message.request_id, 
                                            max_message.source_id, max_message.operation_id,
                                            max_message.destination_id, self.trending_date_with_max_views)
                self.middleware_system_client.call_storage_data(result_message)
        else:
            pass
        self.propagations[str(request_id)] = propagation

    def __process_max(self, max_message: Message):
        views_by_date: dict() = eval(max_message.body)
        for trending_date in views_by_date:
            if self.max_views < views_by_date[trending_date]:
                self.max_views = views_by_date[trending_date]
                self.trending_date_with_max_views = trending_date
        