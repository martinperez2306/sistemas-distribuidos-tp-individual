#!/usr/bin/env python3

import logging
from day_grouper.day_grouper import DayGrouper
from dependencies.commons.base_app import initialize_config, initialize_log

CONFIG_PATH = "/root/day_grouper/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Day Grouper configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Day Grouper")
    day_grouper = DayGrouper(config_params)
    day_grouper.run()

if __name__ == "__main__":
    main()