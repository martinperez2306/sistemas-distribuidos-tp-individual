#!/usr/bin/env python3

import logging
from dependencies.commons.base_app import initialize_config, initialize_log

from reporting_service.reporting_service import ReportingService

CONFIG_PATH = "/root/reporting_service/config/config.ini"

def main():
    config_params = initialize_config(CONFIG_PATH)
    initialize_log(config_params["logging_level"])

    # Log config parameters at the beginning of the program to verify the configuration
    # of the component
    logging.debug("Reporting Service configuration: {}".format(config_params))

    # Initialize service
    logging.info("Initializing Reporting Service")
    reporting_service = ReportingService(config_params)
    reporting_service.run()

if __name__ == "__main__":
    main()