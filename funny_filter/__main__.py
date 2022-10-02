#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log

from funny_filter.funny_filter import FunnyFilter

CONFIG_PATH = "/root/funny_filter/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Funny Filter configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Funny Filter")
    like_filter = FunnyFilter(config_params)
    like_filter.run()

if __name__ == "__main__":
    main()