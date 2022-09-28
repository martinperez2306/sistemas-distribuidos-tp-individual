class Request:
    def __init__(self, request_id, correlation_id, client_id, client_queue):
        self.request_id = request_id
        self.correlation_id = correlation_id
        self.client_id = client_id
        self.client_queue = client_queue