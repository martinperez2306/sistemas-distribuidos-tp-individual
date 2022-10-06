import re
import json
import logging
from dependencies.commons.constants import *
from dependencies.commons.message import Message
from dependencies.commons.video import Video

def to_json(jsoneable):
    return json.dumps(jsoneable)

def parse_message(body: str) -> Message:
    logging.debug("Parsing message: {}".format(body))
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

def json_to_video(video_json: str):
    parsed = json.loads(video_json)
    video = Video(parsed["id"], parsed["title"], parsed["published_at"], parsed["channel_id"], parsed["channel_title"], parsed["category_id"], 
                    parsed["trending_date"], parsed["tags"], parsed["view_count"], parsed["likes"], parsed["dislikes"], parsed["comment_count"], 
                    parsed["thumbnail_link"], parsed["comments_disabled"], parsed["ratings_disabled"], parsed["description"], parsed["country"])
    return video

def unique(list):
    # intilize a null list
    unique_list = []

    if list:
        # traverse for all elements
        for video in list:
            # check if exists in unique_list or not
            unique = True
            for unique_video in unique_list:    
                if video.id == unique_video.id and video.title == unique_video.title and video.category_id == unique_video.category_id:
                    unique = False
            if unique:
                unique_list.append(video)

    return unique_list