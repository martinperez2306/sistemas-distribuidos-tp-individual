import constants
import logging
import pika
from .message import Message

class ClientService:
    def __init__(self):
        self.request_count = 0

    def start_data_process(self, ch, method, props, message: Message):
        logging.info("Starting data process")
        self.request_count += 1
        response = Message(constants.MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, self.request_count)
        self.__respond(response)

    def process_data(self, ch, method, props, message: Message):
        logging.info("Processing Data [{}]".format(message.to_string()))
        response = Message(constants.MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, "ACK")
        self.__respond(response)

    def end_data_process(self, ch, method, props, message: Message):
        logging.info("Ending data process")
        response = Message(constants.MIDDLEWARE_MESSAGE_ID, message.request_id, message.client_id, message.operation_id, "ACK")
        self.__respond(response)

    def __respond(self, ch, method, props, request: Message, response: Message):
        logging.info("Respond to client [{}] with [{}]".format(request.client_id, response.to_string()))
        ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = props.correlation_id),
                     body=str(response.to_string()))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
