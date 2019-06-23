#!/usr/bin/python

""" Starting point of the simulator application, gathering the launcher main configuration and selecting
which launcher is called.

--------------------------
Created on Oct 19, 2017

@author: J. Sanchez-Garcia
"""

from launchers import launcher_one
from launchers import launcher_two
from launchers import launcher_three
from launchers import launcher_four
from launchers import launcher_five

import logging
from log_helpers import log_module

log_module.setup_logging()  
logger = logging.getLogger(__name__)

# Exceptions
#-----------
exception_flag = 0

# Launcher flags
#---------------
# This does not calls scenario_builder, it needs an scenario previously created and stored in scenarios folder
launch_local = 0
# In the case launch_local = 1 the parameters from below must have the specific information of the scenario saved locally within scenarios folder
INPUT_FILE = "scenarios/170526-124252/170526-124314_main.wml"       # wml file containing the scenario nodes movements

# This calls scenario_builder for calculating the duration of the simulation. It runs pso with only 1 set of parameter values and also runs lawn mower 
launch_create_scen = 0

# This calls scenario_builder for calculating the duration of the simulation. It runs pso with various sets of parameter values  and also runs lawn mower
launch_characterization = 0

# This calls the launcher that runs the sim core four times per iteration, one making the drones start from each corner
first_dr_pos = ['corner_bottom_left', 'corner_bottom_right', 'corner_top_left', 'corner_top_right']
launch_fourcorners = 1

# This calls the launcher that characterizes the pso algo and also runs the sim core four times per iteration, one making the drones start from each corner
launch_fourcorners_and_char = 0


# Algorithms flags
#-----------------
pso_flag = 1
lawn_mower_flag = 0

pso_iterations = 20
lawn_mower_iterations = 1


LAUNCH_CONFIG = {'pso':pso_flag, 'lawn':lawn_mower_flag, \
                 'pso_iter':pso_iterations, 'lawn_iter':lawn_mower_iterations,\
                 'first_drones_pos': first_dr_pos, 'exception':exception_flag} 

# Launcher selection
# -------------------
if launch_local == 1:
    
    logger.info('Calling launcher_one:')
    logger.info(str(LAUNCH_CONFIG))
    
    # Calling launcher simple
    launcher_one.launcher_local_scen(LAUNCH_CONFIG,INPUT_FILE)
    
    
elif launch_create_scen == 1:
   
    logger.info('Calling launcher_two:')
    logger.info(str(LAUNCH_CONFIG))
    
    # Calling launcher simple
    launcher_two.launcher_create_scen(LAUNCH_CONFIG)
    
    
elif launch_characterization == 1:
    
    logger.info('Calling launcher_three:')
    logger.info(str(LAUNCH_CONFIG))
    
    # Calling launcher simple
    launcher_three.launcher_characterization(LAUNCH_CONFIG)


elif launch_fourcorners == 1:
    
    logger.info('Calling launcher_four:')
    logger.info(str(LAUNCH_CONFIG))
    
    # Calling launcher simple
    launcher_four.launch_fourcorners(LAUNCH_CONFIG)

elif launch_fourcorners_and_char == 1:
    
    logger.info('Calling launcher_five:')
    logger.info(str(LAUNCH_CONFIG))
    
    # Calling launcher simple
    launcher_five.launch_fourcorners_and_char(LAUNCH_CONFIG)
    