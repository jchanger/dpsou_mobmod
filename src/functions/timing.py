"""
Created on Jul 31, 2015

@author: J. Sanchez-Garcia
"""

import time
import datetime


def timestamp_gen():
    ts = time.time()
    
    t_stamp = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d-%H%M%S')
    t_stamp = t_stamp[2:]
    
    return t_stamp


def get_sim_duration(t_sim_START):
    t_sim_END = time.time()
    t_sim_TOTAL = t_sim_END - t_sim_START
    
    return t_sim_TOTAL
        
