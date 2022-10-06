class Request:
    def __init__(self, request_id, client_id, client_queue):
        self.request_id = request_id
        self.client_id = client_id
        self.client_queue = client_queue

    def __str__(self):
        return "REQUEST_ID[{}] CLIENT_ID [{}] CLIENT_QUEUE[{}]"\
            .format(self.request_id, self.client_id, self.client_queue)