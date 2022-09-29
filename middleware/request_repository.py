import logging
from middleware.request import Request

class RequestRepository:
    def __init__(self):
        self.requests = dict()

    def add(self, request_id: int, request: Request):
        logging.info("Save request {}".format(request))
        self.requests[str(request_id)] = request
        logging.info("Requests {}".format(self.requests))
    
    def delete(self, request_id: int):
        try:
            self.requests.pop(str(request_id))
        except KeyError:
            pass

    def get(self, request_id: int):
        logging.info("Get request by id {}".format(request_id))
        return self.requests.get(str(request_id))