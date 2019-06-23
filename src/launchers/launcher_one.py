#!/usr/bin/python

""" Launches the sim_core with specific parameters

--------------------------
Created on Apr 4, 2017

@author: J. Sanchez-Garcia
"""

import time
import subprocess
import logging
import settings
import sim_core
from functions import timing
from functions import file_helper
from charts import avg_charts
from algorithms import lawn_mower



def launcher_local_scen(LAUNCH_CONFIG,input_file_local):
    
    logger = logging.getLogger(__name__)

    # Configuration flags
    # -------------------
    pso_flag = LAUNCH_CONFIG['pso']
    lawn_mower_flag = LAUNCH_CONFIG['lawn']
    pso_iterations = LAUNCH_CONFIG['pso_iter']
    lawn_iterations = LAUNCH_CONFIG['lawn_iter']
    
    logger.info('Reading local scenario from: '+input_file_local)
    settings.INPUT_FILE = input_file_local
    
    t_start = time.time()
    
    # Generate lawn mower trajectories (run this wit debug to know the duration of an entire sweep with lawn_mower, 
    # then generate the scenario manually, copy it to ./scenarios folder within this project, copy the path to settings
    # and also the new duration and run an entire simulation for getting the results)
    #---------------------------------
    logger.info('Calculating the duration of the simulation from lawn_mower algo')
    
    CONFIG = settings.update_CONFIG()
    traj_per_drone = lawn_mower.gen_lawnmower_traj(CONFIG)
    settings.lm_trajectories = traj_per_drone
     
    duration = len(traj_per_drone[0])
    logger.info('Duration: '+str(duration))
    
    if CONFIG['f_duration'] == 0:
        settings.DURATION = duration
    else:
        # Leave the duration specified on the settings file
        pass
    
    
    #  SIM_CORE calls
    #-----------------
    
    timestamp_main = timing.timestamp_gen()
                
    main_output_folder = './outputs/'+str(timestamp_main)
    command = ['mkdir', main_output_folder]
    subprocess.call(command)
    
    settings.MAIN_OUTPUT_FOLDER = main_output_folder    
    
    # PSO
    #-----
    if pso_flag == 1:
        pso_folder = main_output_folder+'/pso'
        command = ['mkdir', pso_folder]
        subprocess.call(command)
        
        settings.ALGORITHM = 'pso'

        
        for i in range(pso_iterations):   
            sub_timestamp = timing.timestamp_gen()
            sub_folder = pso_folder+'/'+str(sub_timestamp)
            command = ['mkdir', sub_folder]
            subprocess.call(command)
            
            settings.OUTPUT_FOLDER = sub_folder
            settings.CURRENT_ITERATION = i
            logger.info(str(settings.ALGORITHM)+' algorithm: iteration '+str(i))
            
            logger.info('Calling sim_core')
            sim_core.simulator()        
        
        #  Create averaged charts and maps
        #-----------------------------------
        logger.info('Generating average charts for: '+settings.ALGORITHM)
        settings.TIMESTAMP =  timestamp_main # averaged charts will be generated with main timestamp
        CONFIG = settings.update_CONFIG()
        avg_charts.plot_all(settings.FILES, CONFIG)
        logger.info('Average charts generated for: '+settings.ALGORITHM)
    
    # Clean state after pso simulation
    settings.FILES = []
    
    
    # Lawn mower
    #------------
    if lawn_mower_flag == 1:
        lawn_folder = main_output_folder+'/lawn'
        command = ['mkdir', lawn_folder]
        subprocess.call(command)
        
        settings.ALGORITHM = 'lawn_mower'
        
        for i in range(lawn_iterations): #range(iterations) will be used in the loop when there is random variables in the lawn mower algo  
            sub_timestamp = timing.timestamp_gen()
            sub_folder = lawn_folder+'/'+str(sub_timestamp)
            command = ['mkdir', sub_folder]
            subprocess.call(command)
            
            settings.OUTPUT_FOLDER = sub_folder
            settings.CURRENT_ITERATION = i
            logger.info(str(settings.ALGORITHM)+' algorithm: iteration '+str(i))
            
            logger.info('Calling sim_core')
            sim_core.simulator()        
        
        #  Create averaged charts and maps
        #-----------------------------------
        logger.info('Generating average charts for: '+settings.ALGORITHM)
        settings.TIMESTAMP =  timestamp_main # averaged charts will be generated with main timestamp
        CONFIG = settings.update_CONFIG()
        avg_charts.plot_all(settings.FILES, CONFIG)
        logger.info('Average charts generated for: '+settings.ALGORITHM)
    
    
    # Close files
    #-------------
    logger.info('All simulations terminated')
    
    t_end = time.time()
    sim_duration = (t_end - t_start) # simulation total duration 
    mins = int(sim_duration/60) # (minutes)
    secs = int(sim_duration%60)
    
    logger.info('Simulation duration: '+str(mins)+' mins '+str(secs)+' secs \n')
