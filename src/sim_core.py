#!/usr/bin/python

""" Core module of the simulator

--------------------------
Created on May 31, 2016

@author: J. Sanchez-Garcia
"""

import logging
import time
import sys
import settings

from functions import initialize
from functions import file_helper
from functions import output
from functions import timing
from functions import inputs
from classes import networking
from charts import drone_charts

def simulator():
    
    logger = logging.getLogger(__name__)
    
    #    INPUTS VALUES
    ########################    
     
    settings.TIMESTAMP = timing.timestamp_gen() # modifies only local CONFIG
    CONFIG = settings.update_CONFIG()
    
    #    Input checking
    ###########################
    
    # Checking that inputs values have proper values. If the inputs are not correct values
    # for the simulation, the program exits with 'sys.exit()'
    logger.info('Checking input values')
    inputs.check_algo_name(CONFIG['algorithm'])
    inputs.check_drones_amount(CONFIG['drones_amount'])
    inputs.check_initial_pos_mode(CONFIG['init_distrib'])
    
    #   Start counting time
    ##########################
    
    # Time variable for controlling simulation duration
    t_sim_START = time.time()
    
    #   Files creation
    #####################
    logger.info('Creating simulation files')
    param_file,output_file = file_helper.create_files(CONFIG)
    output.param_file_write(CONFIG, param_file)
    
    out_filename=output_file.name # get the name for the chart at the end of the module
    settings.FILES.append(out_filename) # appends to the list of '_values' files in settings
    
    #   Objects creation
    ###############################
    logger.info('Creating simulation objects: drones, nodes and sim_network')
    
    # Networking object/server creation
    #----------------------------------
    sim_network = networking.Network(CONFIG)
    
    # Scenario loading process
    #-------------------------
    nodes = initialize.create_scenario(CONFIG, sim_network)
    
    # Drones objects generation
    #--------------------------
    drones = initialize.create_drones(CONFIG, sim_network)
    
    # if lawn mower,  trajectories are generated and set within 'initialize' module        
    
    logger.info('Starting simulation main loop')
    
    
    #     Sim. Loop        
    #---------------------
     
    # The for loop runs until the simulation time has finished
    for t_current in range(0,int(CONFIG['duration'])):   
        
        # Printing simulation progress (each 10 seconds for avoiding excessive messages)
        if t_current%10 == 0:
            logger.info('Current time = '+str(t_current)+'; Progress = %d%% ' % (100*t_current/int(CONFIG['duration'])))
    
        
        # Communications
        #---------------
        #logger.debug('Drones communicate')
        for drone_i in drones:
            drone_i.communicate()
        
        #logger.debug('Nodes communicate')           
        for node_i in nodes:
            node_i.communicate()
    
        # Algorithm call for calculating the next position
        #-------------------------------------------------
        #logger.debug('Drones calculate next destination')
        for drone_i in drones:
            drone_i.calc_next_destination()
    
        # Logging drones information to output file
        #------------------------------------------
        #logger.debug('Drones logging to file')
        for drone_i in drones:
            drone_i.drone_logging(t_current,output_file,CONFIG)
    
        # Move to next position
        #----------------------
        #logger.debug('Drones move')
        for drone_i in drones:
            drone_i.move()
            
        #logger.debug('Nodes move')
        for node_i in nodes:
            node_i.move()                        
         
        # Update drones and nodes time
        #-----------------------------
        #logger.debug('Drones update time')
        for drone_i in drones:
            drone_i.update_time()

        #logger.debug('Nodes update time')
        for node_i in nodes:
            node_i.update_time()
                
        
    #   Closing section      
    ##########################
    
    logger.info('Main iteration loop finished')

    # Calculate simulation time
    t_sim_TOTAL = timing.get_sim_duration(t_sim_START)
    
    # Write the simulation time on the parameters file
    output.param_file_write(None,param_file,t_sim_TOTAL)
    
    # Final message print on screen
    output.param_screen(None, t_sim_TOTAL)
    
    file_helper.close_files(param_file, output_file)
    
    
    #   Plotting section
    ######################

    if CONFIG['individual_charts'] == 1:
        logger.info('Generating individual graphics')
            
        # Create charts after files are closed
        drone_charts.plot_all(out_filename, CONFIG)
       
        logger.info('Sim_core iteration terminated')
    
                   
# Enables the module being executed as a script and also by the launcher calling the 'simulator' function        
if __name__ == "__main__":
    simulator()   
    

