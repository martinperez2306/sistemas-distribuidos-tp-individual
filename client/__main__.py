#!/usr/bin/env python3

import pathlib
import logging
from itertools import islice

from dependencies.commons.message import Message
from dependencies.middleware_client.middleware_client import MiddlewareClient

VIDEOS = "/root/client/videos"
CHUNKSIZE = 1

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"

RESULTS_PENDING = "PENDING"

def main():
    initialize_log("INFO")
    middleware_client = initialize_middleware_client()
    total_countries = get_total_countries()
    request_id = process_videos(middleware_client, total_countries)
    results: Message = get_results(middleware_client, request_id)
    while RESULTS_PENDING == results.body:
        results = get_results(middleware_client, request_id)
    shutdown_middleware_client(middleware_client)
    show_results(results)

def initialize_log(logging_level):
    """
    Python custom logging initialization

    Current timestamp is added to be able to identify in docker
    compose logs the date when the log has arrived
    """
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging_level,
        datefmt='%Y-%m-%d %H:%M:%S',
    )

def initialize_middleware_client():
    logging.info("Initializing Middleware Client")
    return MiddlewareClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE)
    
def get_total_countries():
    logging.info("Getting total countries")
    countries = 0
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            countries += 1
    logging.info("Total Countries = {}".format(countries))
    return countries

def process_videos(middleware_client: MiddlewareClient, total_countries):
    logging.info("Processing Videos")
    middleware_client.connect()
    message: Message = middleware_client.call_start_data_process()
    request_id = message.body
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            process_in_chunks(path, CHUNKSIZE, middleware_client, request_id)
    middleware_client.call_end_data_process(request_id)
    return request_id
    

def process_in_chunks(path, chunk_size, middleware_client, request_id):
    with open(path, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            for line in lines:
                process_video(line, middleware_client, request_id)
            if not lines:
                break

def process_video(video: str, middleware_client: MiddlewareClient, request_id:int ):
    logging.info("Processing Video: [{}] in Request with ID [{}]".format(video, request_id))
    middleware_client.call_process_data(request_id, video)

def get_results(middleware_client: MiddlewareClient, request_id):
    logging.info("Getting Results for Request with ID [{}]".format(request_id))
    results_message: Message = middleware_client.wait_get_results(request_id)
    logging.info("Results for Request with ID [{}]: [{}]".format(request_id, results_message.to_string()))
    return results_message

def show_results(results):
    print(results.to_string())

def shutdown_middleware_client(middleware_client: MiddlewareClient):
    middleware_client.close()

if __name__ == "__main__":
    main()