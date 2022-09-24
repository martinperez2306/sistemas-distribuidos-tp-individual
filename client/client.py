#!/usr/bin/env python3

import pathlib
import logging
from itertools import islice
from middleware_client.middleware_client import MiddlewareClient

VIDEOS = "./videos"
CHUNKSIZE = 1

RABBITMQ_HOST = "rabbitmq"
MIDDLEWARE_QUEUE = "middleware"

def main():
    initialize_log("INFO")
    middleware_client = initialize_middleware_client()
    logging.info("Hi! Im am the client")
    total_countries = get_total_countries()
    logging.info("Total Countries = {}".format(total_countries))
    process_videos(middleware_client, total_countries)
    middleware_client.close()

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
    return MiddlewareClient(RABBITMQ_HOST, MIDDLEWARE_QUEUE)
    
def get_total_countries():
    countries = 0
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            countries += 1
    return countries

def process_videos(middleware_client, total_countries):
    logging.info("Processing Videos")
    middleware_client.connect()
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            process_in_chunks(path, CHUNKSIZE, middleware_client)

def process_in_chunks(path, chunk_size, middleware_client):
    with open(path, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            for line in lines:
                process_video(line, middleware_client)
            if not lines:
                break

def process_video(video, middleware_client):
    logging.info("Processing Video: {}".format(video))
    middleware_client.request(video)

if __name__ == "__main__":
    main()