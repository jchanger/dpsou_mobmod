#!/usr/bin/python

""" Launches the sim_core with specific parameters

--------------------------
Created on Apr 4, 2017

@author: J. Sanchez-Garcia
"""

import sys
import json
import time
import subprocess
import logging
import settings
import sim_core
import client_socket
from subprocess import PIPE, Popen
from functions import timing
from functions import file_helper
from charts import avg_charts
from algorithms import lawn_mower
from algorithms import pso


def launcher_characterization(LAUNCH_CONFIG):
    
    logger = logging.getLogger(__name__)
    
    # Configuration flags
    # -------------------
    pso_flag = LAUNCH_CONFIG['pso']
    lawn_mower_flag = LAUNCH_CONFIG['lawn']
    exception_flag = LAUNCH_CONFIG['exception']
    pso_iterations = LAUNCH_CONFIG['pso_iter']
    lawn_iterations = LAUNCH_CONFIG['lawn_iter']
    
    t_start = time.time()
    
    # Generate lawn mower trajectories for defining the duration
    #-----------------------------------------------------------
    logger.info('Calculating the duration of the simulation from lawn_mower algo')
    
    CONFIG = settings.update_CONFIG()
    traj_per_drone = lawn_mower.gen_lawnmower_traj(CONFIG)
    settings.lm_trajectories = traj_per_drone
    
    duration = len(traj_per_drone[0])
    logger.info('Duration: '+str(duration))
    
    # Generate scenario
    #------------------
    # call to scenario_builder through socket
    logger.info('Using socket to get the scenario_builder generating the scenario')
    
    message = client_socket.get_scenario(duration)
    
    js_obj = json.loads(message)
    folder_path = js_obj['scenario']
    clusters = js_obj['clusters']
    settings.NODES_AMOUNT = js_obj['nodes_amount']
    
    folder = folder_path[-13:]
    relative_folder = './scenarios/'+folder+'/'
    command = ['mkdir',relative_folder]
    subprocess.call(command)
    
    # save new scenario from /scenario_builder folder to /scenario folder
    logger.info('Moving the new scenario to /scenarios folder')
    
    command = ['find',folder_path,'-maxdepth','1','-type','f']
    popen_proc = Popen(command,stdout=PIPE)
    files_to_copy = popen_proc.stdout.read()
    files_to_copy = files_to_copy.split('\n')
    del files_to_copy[-1]
    
    for file_i in files_to_copy:
        command = ['cp', file_i, relative_folder]
        subprocess.call(command)
    
    # get .wml filename
    logger.info('Finding the main .wml file')
    
    command = ['ls', relative_folder]
    popen_proc = Popen(command,stdout=PIPE)
    filename_l = popen_proc.stdout.read()
    
    # get '.wml' file name
    filename_l = filename_l.split('\n')
    for file_i in filename_l:
        if file_i.endswith('.wml'):
            wml_filename = file_i
        else:
            pass
    
    wml_full_path = relative_folder+wml_filename
    
    # save the scenario path in settings
    logger.info('Saving scenario path in settings file')
    settings.INPUT_FILE = wml_full_path
    
    CONFIG = settings.update_CONFIG()
    
    if CONFIG['f_duration'] == 0:
        settings.DURATION = duration
    else:
        # Leave the duration specified on the settings file
        pass
    
    settings.CLUSTERS = clusters
    
    
    timestamp_main = timing.timestamp_gen()
                
    main_output_folder = './outputs/'+str(timestamp_main)
    command = ['mkdir', main_output_folder]
    subprocess.call(command)
            
            
    # Generate pso parameters
    #------------------------
    logger.info('Generating sets of pso parameters values')
    pso_vals = pso.generate_pso_params()
    
    for pso_mode_i in pso_vals:
    
        mode = pso_mode_i[0]
        lb_vals = pso_mode_i[1]
        nb_vals = pso_mode_i[2]
        
        for val_i in range(len(lb_vals)):
         
            # inertia weight has not to be set
            settings.beta = (0,lb_vals[val_i])      # local best weight
            settings.gamma = (0,nb_vals[val_i])     # global best weight        
            logger.info('Parameter set: mode='+str(mode)+'\t lb='+str(settings.beta)+'\t nb='+str(settings.gamma))

            
            #  SIM_CORE calls
            #-----------------
            logger.info('Creating output folder')
            
            charac_folder = main_output_folder+'/'+str(mode)+'_'+str(lb_vals[val_i])+'_'+str(nb_vals[val_i])
            command = ['mkdir', charac_folder]
            subprocess.call(command)      
            
            settings.MAIN_OUTPUT_FOLDER = charac_folder
                        
            
            # create pso params file
            CONFIG = settings.update_CONFIG()
            
            report_file = file_helper.create_pso_vals(timestamp_main,charac_folder)
            report_file.write('PSO values:\n')
            report_file.write('mode: '+mode+'\n')
            report_file.write('inertia final val: '+str(1-lb_vals[val_i]-nb_vals[val_i])+'\n')
            report_file.write('local best final val: '+str(lb_vals[val_i])+'\n')
            report_file.write('global best final val: '+str(nb_vals[val_i])+'\n')
            
            report_file.write('inertia only time: [0,'+str(CONFIG['pso_params'][3])+']\n')
            report_file.write('lb time: ['+str(CONFIG['pso_params'][3])+','+str(CONFIG['pso_params'][5])+']\n')
            report_file.write('nb time: ['+str(CONFIG['pso_params'][5])+','+str(CONFIG['duration'])+']\n')
            
            
            # PSO
            #-----
            if pso_flag == 1:
                pso_folder = charac_folder+'/pso'
                command = ['mkdir', pso_folder]
                subprocess.call(command)
                
                settings.ALGORITHM = 'pso'
                CONFIG = settings.update_CONFIG()
                
                for i in range(pso_iterations):   
                    sub_timestamp = timing.timestamp_gen()
                    sub_folder = pso_folder+'/'+str(sub_timestamp)
                    command = ['mkdir', sub_folder]
                    subprocess.call(command)
                    
                    settings.OUTPUT_FOLDER = sub_folder
                    settings.CURRENT_ITERATION = i 
                    logger.info(str(settings.ALGORITHM)+' algorithm: iteration '+str(i))
                    
                    if exception_flag == 1:
                        try:
                            logger.info('Calling sim_core')
                            sim_core.simulator()
                        except (BaseException,KeyboardInterrupt):
                            logger.debug('pso iteration: '+str(i)+' -- Exception caught:' \
                                 +'\n\tfilename: '+sys.exc_info()[2].tb_frame.f_code.co_filename \
                                 +'\n\tlineno: '+str(sys.exc_info()[2].tb_lineno) \
                                 +'\n\tname: '+sys.exc_info()[2].tb_frame.f_code.co_name \
                                 +'\n\ttype: '+sys.exc_info()[0].__name__ \
                                 +'\n\tmessage: '+sys.exc_info()[1].message)

                    else:
                        logger.info('Calling sim_core')
                        sim_core.simulator()

                
                #  Create averaged charts and maps
                #-----------------------------------
                logger.info('Generating average charts for: '+settings.ALGORITHM)
                
                settings.TIMESTAMP =  timestamp_main # averaged charts will be generated with main timestamp
                CONFIG = settings.update_CONFIG()
                avg_charts.plot_all(settings.FILES, CONFIG, report_file)

                logger.info('Average charts generated for: '+settings.ALGORITHM)
            
            # Clean state after pso simulation
            report_file.close()
            settings.FILES = []
            logger.info('PSO sims terminated')

    # Lawn mower
    #------------
    if lawn_mower_flag == 1:
        lawn_sim_folder = main_output_folder+'/x_lawn_sim'
        command = ['mkdir', lawn_sim_folder]
        subprocess.call(command)
        
        settings.MAIN_OUTPUT_FOLDER = lawn_sim_folder
    
        lawn_folder = lawn_sim_folder+'/lawn'
        command = ['mkdir', lawn_folder]
        subprocess.call(command) 
        
        settings.ALGORITHM = 'lawn_mower'
        CONFIG = settings.update_CONFIG()
        
        report_file = file_helper.create_pso_vals(timestamp_main,lawn_sim_folder)
        report_file.write('Lawn_mower values:\n')       
        report_file.write('entire sweep duration: '+str(CONFIG['duration'])+'\n')
        
        for i in range(lawn_iterations): #range(iterations) will be used in the loop when there is random variables in the lawn mower algo  
            sub_timestamp = timing.timestamp_gen()
            sub_folder = lawn_folder+'/'+str(sub_timestamp)
            command = ['mkdir', sub_folder]
            subprocess.call(command)
            
            settings.OUTPUT_FOLDER = sub_folder
            settings.CURRENT_ITERATION = i
            logger.info(str(settings.ALGORITHM)+' algorithm: iteration '+str(i))

            if exception_flag == 1:
                try:
                    logger.info('Calling sim_core')
                    sim_core.simulator()
                except (BaseException,KeyboardInterrupt):
                    logger.debug('lawn_mower iteration: '+str(i)+' -- Exception caught:' \
                         +'\n\tfilename: '+sys.exc_info()[2].tb_frame.f_code.co_filename \
                         +'\n\tlineno: '+str(sys.exc_info()[2].tb_lineno) \
                         +'\n\tname: '+sys.exc_info()[2].tb_frame.f_code.co_name \
                         +'\n\ttype: '+sys.exc_info()[0].__name__ \
                         +'\n\tmessage: '+sys.exc_info()[1].message)

            else:
                logger.info('Calling sim_core')
                sim_core.simulator()
        
        #  Create averaged charts and maps
        #-----------------------------------
        logger.info('Generating average charts for: '+settings.ALGORITHM)
        
        settings.TIMESTAMP =  timestamp_main # averaged charts will be generated with main timestamp
        CONFIG = settings.update_CONFIG()
        avg_charts.plot_all(settings.FILES, CONFIG, report_file)
        
        logger.info('Average charts generated for: '+settings.ALGORITHM)
    
    
    # Close files
    #-------------
    logger.info('All simulations terminated')
    
    report_file.close()

    t_end = time.time()
    sim_duration = (t_end - t_start) # simulation total duration 
    mins = int(sim_duration/60) # (minutes)
    secs = int(sim_duration%60)
    
    logger.info('Simulation duration: '+str(mins)+' mins '+str(secs)+' secs \n')
    
    # Clean state after pso simulation
    # Necessary when running the characterization for avoiding last lawn_mower being plot with the next pso 
    settings.FILES = []
