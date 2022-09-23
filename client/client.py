#!/usr/bin/env python3

import pathlib
import logging
import os
from itertools import islice

VIDEOS = "./videos"
CHUNKSIZE = 1

def main():
    initialize_log("INFO")
    logging.info("Hi! Im am the client")
    total_countries = get_total_countries()
    logging.info("Total Countries = {}".format(total_countries))
    process_videos(total_countries)

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
    
def get_total_countries():
    countries = 0
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            countries += 1
    return countries

def process_videos(total_countries):
    logging.info("Processing Videos")
    for path in pathlib.Path(VIDEOS).iterdir():
        if path.is_file():
            process_in_chunks(path, CHUNKSIZE)

def process_in_chunks(path, chunk_size):
    with open(path, 'r') as file:
        while True:
            lines = list(islice(file, chunk_size))
            for line in lines:
                process_video(line)
            if not lines:
                break

def process_video(video):
    logging.info("Processing Video: {}".format(video))

if __name__ == "__main__":
    main()