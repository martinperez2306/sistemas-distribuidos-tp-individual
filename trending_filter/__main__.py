#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log

from trending_filter.trending_filter import TrendingFilter

CONFIG_PATH = "/root/trending_filter/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Trending Filter configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Trending Filter")
    trending_filter = TrendingFilter(config_params)
    trending_filter.run()

if __name__ == "__main__":
    main()