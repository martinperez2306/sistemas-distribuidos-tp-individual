class Message:
    def __init__(self, id, request_id, client_id, operation_id):
        self.id = id
        self.request_id = request_id
        self.client_id = client_id
        self.operation_id = operation_id