#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log

from ingestion_service.ingestion_service import IngestionService

CONFIG_PATH = "/root/ingestion_service/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Server configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Ingestion Service")
    ingestion_service = IngestionService()
    ingestion_service.run()

if __name__ == "__main__":
    main()