class Message:
    def __init__(self, id, request_id, client_id, operation_id, body):
        self.id = id
        self.request_id = request_id
        self.client_id = client_id
        self.operation_id = operation_id
        self.body = body

    def to_string(self) -> str:
        return "MESSAGE_ID[{}]REQUEST_ID[{}]CLIENT_ID[{}]OPERATION_ID[{}]BODY[{}]"\
            .format(self.id, self.request_id, self.client_id, self.operation_id, self.body)