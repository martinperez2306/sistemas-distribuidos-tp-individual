#!/usr/bin/env python3

import logging
from max.max import Max

def main():
    initialize_log("INFO")
    logging.info("Initializing Ingestion Service")
    max = Max()
    max.run()

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