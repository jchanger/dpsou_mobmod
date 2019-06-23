"""
Created on April 26, 2017

@author: J. Sanchez-Garcia
"""

import copy
from functions import parsers


def parser_update_time_avg(value_files, CONFIG):
    """ Parse the update time of a list of files """
    
    update = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        # the following parser returns a tuple: nodes_per_time, pos_per_time, total_nodes
        aux = parsers.parser_update_time(val_file, CONFIG['drones_amount'], CONFIG['duration'])
        update.append(aux)
        
        val_file.close()

    # separate the different variables
    nodes_per_time_l = zip(*update)[0] 
    pos_per_time_l = zip(*update)[1]
    total_nodes_l = zip(*update)[2]
    
    return nodes_per_time_l, pos_per_time_l, total_nodes_l 


def parser_acc_discovered_avg(value_files, CONFIG):
    """ Parse the accumulated nodes discovered """

    discovered_l = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux = parsers.parser_acc_discovered(val_file)
        discovered_l.append(aux)
        
        val_file.close()
    
    return discovered_l


def parser_discovered_per_time_avg(value_files):
    """ Parse the discovered nodes per time """

    discovered_per_time_l = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux = parsers.parser_discovered_per_time(val_file)
        discovered_per_time_l.append(aux)
        
        val_file.close()
    
    return discovered_per_time_l



def parser_nodes_statistics_avg(value_files,nodes_amount,duration):
    """ Gets the nodes update time frequency and other statistics."""

    nodes_events_l=[]
    nodes_frequency_l=[]
    nodes_time_btw_conn_l=[]
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux_0,aux_1,aux_2 = parsers.parser_nodes_statistics(val_file,nodes_amount,duration)
        nodes_events_l.append(aux_0)
        nodes_frequency_l = copy.deepcopy(nodes_frequency_l + aux_1)           # concatenate because this is used to represent an histogram
        nodes_time_btw_conn_l = copy.deepcopy(nodes_time_btw_conn_l + aux_2)   # concatenate because this is used to represent an histogram
        
        val_file.close()
    
    return nodes_events_l,nodes_frequency_l,nodes_time_btw_conn_l
    
    
    
def parser_encounters_avg(value_files, CONFIG):
    """ Parse drones encounters and drones in range """
    
    drone_enc_l = []
    drone_enc_total_l = []
    drone_last_gr_l = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux = parsers.parser_encounters(val_file,CONFIG['drones_amount'])
        drone_enc_l.append(aux[0])
        drone_enc_total_l.append(aux[1])
        drone_last_gr_l.append(aux[2])
        
        val_file.close()
    
    return drone_enc_l, drone_enc_total_l, drone_last_gr_l



def parser_positions_avg(value_files, CONFIG):
    """ Parse the drones positions """
    
    drone_pos_l = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux = parsers.parser_positions(val_file,CONFIG['drones_amount'])
        drone_pos_l.append(aux)
        
        val_file.close()
    
    return drone_pos_l


def parser_neighborsbest_avg(value_files, CONFIG):
    """ Parse the drones neighbors final positions """
    
    nb_pos_l = []
    
    for file_i in value_files:        
        val_file = open(file_i,'r')
    
        aux_nb_disc,aux_nb_total,aux_nb_pos = parsers.parser_neighborsbest(val_file,CONFIG['drones_amount'])
        nb_pos_l.append(aux_nb_pos) # we are interested only in the position
        
        val_file.close()
    
    return nb_pos_l
    
    
    
    
    
    