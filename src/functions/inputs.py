""" This module contains function definitions for checking that input values are correct for the simulation

--------------------------
Created on Mar 6, 2017

@author: J. Sanchez-Garcia
"""

import sys 
import logging

logger = logging.getLogger(__name__)

def check_algo_name(algo_name):
    if algo_name not in ['pso','lawn_mower']:
        
        logger.error('ALGORITHM must take values from the available algorithms: \
                    \n\t   1. pso: the drones move like pso particles \
                    \n\t   2. lawn_mower: the drones move following a typical lawn mower trajectory')

        sys.exit()
    else:
        pass
    
    
def check_drones_amount(drones_amount):
    # check not integer values
    if not float(drones_amount).is_integer():
        logger.error('The number of drones must be a positive integer > 1')
        sys.exit()
    # check not a small number of drones
    elif drones_amount < 1:
        logger.error('The number of drones must be a positive integer > 1')
        sys.exit()
    else:
        pass


def check_initial_pos_mode(init_distrib):
    """ Check that the INIT_DISTRIB parameter receives a valid mode"""
    possible_distrib=['regular','centered','random','corner_bottom_left','corner_bottom_right','corner_top_left','corner_top_right']
    
    if init_distrib not in possible_distrib:
        logger.error('INIT_DISTRIB must take values from the available initial distribution modes: \
                    \n\t 1. regular: in formation, positioning the drones at the vertices (ONLY UP TO 9 DRONES) \
                    \n\t 2. centered: all the drones start at the center of the scenario \
                    \n\t 3. random: the drones start at random positions within the scenario \
                    \n\t 4. corner_bottom_left: the drones start at the corner [0,0] \
                    \n\t 5. corner_bottom_right: the drones start at the corner [area_dimension[0],0] \
                    \n\t 6. corner_top_left: the drones start at the corner [0,area_dimension[1]] \
                    \n\t 7. corner_top_right: the drones start at the corner [area_dimension[0],area_dimension[1]]')

        sys.exit()
    else:
        pass    
    
    