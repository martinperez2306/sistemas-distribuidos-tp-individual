#!/usr/bin/env python3

import os
import signal
import logging
from configparser import ConfigParser

class BaseApp:
    def __init__(self, app_name):
        self.running = False
        self.app_name = app_name
    
    # graceful shutdown
    def exit_gracefully(self, *args):
        logging.info("Proceed to shutdown {} gracefully".format(self.app_name))
        self.running = False

    def run(self):
        self.running = True

def initialize_config(config_path):
    """ Parse env variables or config file to find program config params

    Function that search and parse program configuration parameters in the
    program environment variables first and the in a config file. 
    If at least one of the config parameters is not found a KeyError exception 
    is thrown. If a parameter could not be parsed, a ValueError is thrown. 
    If parsing succeeded, the function returns a ConfigParser object 
    with config parameters
    """

    config = ConfigParser(os.environ)
    # If config.ini does not exists original config object is not modified
    config.read(config_path)
    config_params = {}
    try:
        for key in config["DEFAULT"]:  
            config_params[key] = config["DEFAULT"][key]
    except KeyError as e:
        raise KeyError("Key was not found. Error: {} .Aborting server".format(e))
    except ValueError as e:
        raise ValueError("Key could not be parsed. Error: {}. Aborting server".format(e))

    return config_params

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
