'''
Created on 21 Oct 2017

@author: jesus
'''


import os
import json
import logging
import logging.config


def setup_logging():
    
    MAIN_APP_PATH='/home/jesus/Develop/uav_ns'
    
    file_path = MAIN_APP_PATH+'/auav/src/log_helpers/debug.log'
    config_path = MAIN_APP_PATH+'/auav/src/log_helpers/log_config.json'

    # remove previous simulations debug messages
    if os.path.exists(file_path):
        os.remove(file_path)
  
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            logging.config.dictConfig(config)
    else:
        print 'log_config.json file does not exists. Using generic logging'
        logging.basicConfig(level=logging.DEBUG)

