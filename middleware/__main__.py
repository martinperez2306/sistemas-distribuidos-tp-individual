#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log

from middleware.middleware import Middleware

CONFIG_PATH = "/root/middleware/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Server configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Middleware")
    middleware = Middleware()
    middleware.run()

if __name__ == "__main__":
    main()