import re
import logging
from dependencies.commons.constants import *
from dependencies.commons.message import Message

def parse_message(body: str) -> Message:
    logging.info("Parsing message: {}".format(body))
    message_id = -1
    try:
        msg_id = int(re.search(MESSAGE_ID_REGEX, body).group(1))
        message_id = msg_id
    except ValueError:
        pass
    request_id = re.search(MESSAGE_REQUEST_ID_REGEX, body).group(1)
    client_id = re.search(MESSAGE_SOURCE_ID_REGEX, body).group(1)
    operation_id = -1
    try:
        op_id = int(re.search(MESSAGE_OPERATION_ID_REGEX, body).group(1))
        operation_id = op_id
    except ValueError:
        pass
    destination_id = re.search(MESSAGE_DESTINATION_ID_REGEX, body).group(1)
    body = re.search(MESSAGE_BODY_REGEX, body).group(1)
    message = Message(message_id, request_id, client_id, operation_id, destination_id, body)
    logging.info("Message: {}".format(message.to_string()))
    return message

def unique(list):
    # intilize a null list
    unique_list = []

    # traverse for all elements
    for video in list:
        # check if exists in unique_list or not
        unique = True
        for unique_video in unique_list:    
            if video.id == unique_video.id and video.title == unique_video.title and video.category == unique_video.category:
                unique = False
        if unique:
            unique_list.append(video)

    return unique_list