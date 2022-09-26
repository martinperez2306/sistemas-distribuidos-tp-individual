#!/usr/bin/env python3

import logging

from core.like_filter import LikeFilter

def main():
    initialize_log("INFO")
    logging.info("Initializing Like Filter")
    like_filter = LikeFilter()
    like_filter.run()

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