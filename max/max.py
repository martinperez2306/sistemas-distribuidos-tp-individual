from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.work_service import WorkService

class Max(WorkService):
    def __init__(self, config_params):
        id = config_params["service_id"]
        group_id = config_params["group_id"]
        self.total_routes = int(config_params["service_instances"])
        self.eof_count = 0
        WorkService.__init__(self, id, group_id, MAX_QUEUE)

    def work(self, ch, method, properties, body):
        max_message = self.middleware_system_client.parse_message(body)
        if END_PROCESS_OP_ID == max_message.operation_id:
            self.eof_count += 1
            self.__process_max(ch, method, properties, body, max_message)
        else:
            self.__propagate_message(ch, method, properties, body, max_message)

    def __process_max(self, ch, method, properties, body, max_message: Message):
        if self.__is_eof():
            days_grouped: dict() = eval(max_message.body)
            max = 0
            max_trend_date = None
            for trending_date in days_grouped:
                if max < days_grouped[trending_date]:
                    max = days_grouped[trending_date]
                    max_trend_date = trending_date
            result_message: Message = Message(max_message.id, max_message.request_id, 
                                                max_message.source_id, max_message.operation_id,
                                                max_message.destination_id, max_trend_date)
            self.__propagate_message(ch, method, properties, body, result_message)

    def __propagate_message(self, ch, method, properties, body, max_message: Message):
        self.middleware_system_client.call_storage_data(max_message)

    def __is_eof(self):
        return (self.eof_count == self.total_routes)