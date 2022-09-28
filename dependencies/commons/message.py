class Message:
    def __init__(self, id: int, request_id: str, client_id: str, operation_id: int, destination_id :str, body: str):
        self.id = id
        self.request_id = request_id
        self.client_id = client_id
        self.operation_id = operation_id
        self.destination_id = destination_id
        self.body = body

    def to_string(self) -> str:
        return "MESSAGE_ID[{}]REQUEST_ID[{}]CLIENT_ID[{}]OPERATION_ID[{}]DESTINATION_ID[{}]BODY[{}]"\
            .format(self.id, self.request_id, self.client_id, self.operation_id, self.destination_id, self.body)