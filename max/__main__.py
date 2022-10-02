#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log
from max.max import Max

CONFIG_PATH = "/root/max/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Max configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Max")

    max = Max(config_params)
    max.run()

if __name__ == "__main__":
    main()