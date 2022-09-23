#!/usr/bin/env python3

import pathlib
import logging
import os

def main():
    initialize_log("INFO")
    logging.info("Hi! Im am the client")
    print (os.getcwd())
    initial_count = 0
    for path in pathlib.Path("videos").iterdir():
        if path.is_file():
            initial_count += 1

    logging.info("Files count = {}".format(initial_count))

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

if __name__ == "__main__":
    main()