""" This module initializes the data structures for the drones and nodes (victims) with input values

-----------------------
Created on Mar 17, 2017

@author: J. Sanchez-Garcia
"""

import parsers
import logging
import initial_positions
from classes import drone
from classes import node
from algorithms import lawn_mower

logger = logging.getLogger(__name__)


def create_nodes(CONFIG,nodes_xpos,nodes_ypos,sim_network):
    """ Creates the nodes (victims) objects and store them in a list"""
    nodes_list = []
    
    # matrix transpose for copying all the positions of a node into the object
    tr_nodes_xpos = zip(*nodes_xpos)
    tr_nodes_ypos = zip(*nodes_ypos)
    
    # len(nodes_xpos) is the number of nodes
    for i in range(0,len(tr_nodes_xpos)):
        aux_node = node.Node(i,CONFIG,tr_nodes_xpos[i],tr_nodes_ypos[i],sim_network)
        nodes_list.append(aux_node)
        
    return nodes_list


def create_scenario(CONFIG,sim_network):
    logger.info('Loading scenario...')
    nodes_xpos=[] 
    nodes_ypos=[]

    parsers.parser_wml(CONFIG['input_file'], nodes_xpos, nodes_ypos)  

    nodes_list = create_nodes(CONFIG,nodes_xpos,nodes_ypos,sim_network)          
    
    logger.info('Scenario loaded')


    return nodes_list


def create_drones(CONFIG,sim_network):
    # Drones list containing the drones objects
    drones = []
    
    if CONFIG['algorithm'] == 'pso':
        # Generate the initial positions of drones
        init_pos = initial_positions.init_drone_pos(CONFIG)
        
        first_inertia = initial_positions.get_first_inertia(CONFIG)

        # Create and initialize drones objects with __init__ method of the class Drone
        for i in range(0,CONFIG['drones_amount']):
            drones.append(drone.Drone(i, CONFIG, init_pos, sim_network,first_inertia))

    elif CONFIG['algorithm'] == 'lawn_mower':
        
        if CONFIG['lawnmower_params'][3] is not True:
            # Generate trajectories
            traj_per_drone = lawn_mower.gen_lawnmower_traj(CONFIG)
        
        else:
            # read the trajectories from settings.CONFIG (they were created in 'launcher' module)
            traj_per_drone = CONFIG['lawnmower_params'][3]
        
        # Extract the initial positions from trajectories
        aux_init_pos = zip(*traj_per_drone)[0]
        aux_x = zip(*aux_init_pos)[0]
        aux_y = zip(*aux_init_pos)[1]
        init_pos = [aux_x,aux_y]      
        
        # Assign the trajectories to each drone when creating the drones objects
        for i in range(0,CONFIG['drones_amount']):
            drones.append(drone.Drone(i, CONFIG, init_pos, sim_network,None,traj_per_drone[i]))        
        
        
    return drones
    
    
    