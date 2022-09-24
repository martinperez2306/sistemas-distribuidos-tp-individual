import constants
import pika
from .message import Message

class ClientService:
    def __init__(self):
        self.request_count = 0

    def start_data_process(self, ch, method, props, message: Message):
        self.request_count += 1
        response = Message(constants.MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, self.request_count)
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response.to_string()))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
