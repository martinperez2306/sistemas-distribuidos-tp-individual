from middleware.request import Request

class RequestRepository:
    def __init__(self):
        self.requests = dict()

    def add(self, request_id: int, request: Request):
        self.requests[str(request_id)] = request
    
    def delete(self, request_id: int):
        try:
            self.requests.pop(str(request_id))
        except KeyError:
            pass

    def get(self, request_id: int):
        return self.requests.get(str(request_id))