"""
Created on Jul 26, 2015

@author: J. Sanchez-Garcia
"""

import copy
import logging
import re
from operator import itemgetter
import networkx as nx
from gtk.keysyms import Prev_Virtual_Screen

logger = logging.getLogger(__name__)


def parser_wml(file_wml,node_x,node_y):

    file_0 = open(file_wml,'r')
    
    timestamp = -1
    node = 0
    node_counter = 0

    nodes_amount_t1 = 0
    
    aux_x = []
    aux_y = []
    
    for line in file_0:
        
        if line.startswith('\t\t\t<timestamp>'):
            # To skip the first time when no characters are read 
            if timestamp != -1:
                # We trust that the first timestamp will have all the nodes within the simulation area
                if timestamp == 0:
                    nodes_amount_t1 = max(len(aux_x),len(aux_y))
                                
                # Update the latest nodes if they are missing e.g. node 99 missing from 100 nodes
                if node_counter > nodes_amount_t1:
                    # TODO_1: Create a error file log to keep track of these errors 
                    # TODO_2: Update backwards the first positions of the list when a bigger amount of nodes are detected
                    logger.error('Error parsing wml file: the timestamp 0 has not all the nodes within simulation area')

                while node_counter < nodes_amount_t1:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # Insert in the matrix
                node_x.insert(timestamp, aux_x)
                node_y.insert(timestamp, aux_y)
                
                aux_x = []
                aux_y = []
                node_counter = 0
                
            i = 14
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                timestamp = int(float(line[14:i]))
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
            
        elif line.startswith('\t\t\t<node id'):
            i = 13
            while line[i]!='\"' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                # We assume that the first timestamp has all the nodes displayed within the simulation area of BonnMotion
                while int(line[13:i]) != node_counter:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # After inserting the missing node we have the current node and the node_counter updated    
                node = line[13:i]
                node_counter += 1
                
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'\"\' character')
        elif line.startswith('\t\t\t\t\t<x'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_x.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
        elif line.startswith('\t\t\t\t\t<y'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_y.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
                         
         
    node_x.insert(timestamp, aux_x)
    node_y.insert(timestamp, aux_y)
    
    file_0.close()

    return nodes_amount_t1,int(float(timestamp))



def parser_wml_boundaries(file_wml):
    """ Parse the .wml file and gets only the timestamps 0 and last """

    file_0 = open(file_wml,'r')
    
    node_x = []
    node_y = []
    
    timestamp = -1
    node = 0
    node_counter = 0

    nodes_amount_t1 = 0
    
    aux_x = []
    aux_y = []
    
    for line in file_0:
        
        if line.startswith('\t\t\t<timestamp>'):
            # To skip the first time when no characters are read 
            if timestamp != -1:
                # We trust that the first timestamp will have all the nodes within the simulation area
                if timestamp == 0:
                    nodes_amount_t1 = max(len(aux_x),len(aux_y))
                    
                    # Insert in the matrix only for the timestamp '0'
                    node_x.insert(timestamp, aux_x)
                    node_y.insert(timestamp, aux_y)
                                
                # Update the latest nodes if they are missing e.g. node 99 missing from 100 nodes
                if node_counter > nodes_amount_t1:
                    # TODO_1: Create a error file log to keep track of these errors 
                    # TODO_2: Update backwards the first positions of the list when a bigger amount of nodes are detected
                    logger.error('Error parsing wml file: the timestamp 0 has not all the nodes within simulation area')

                while node_counter < nodes_amount_t1:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # the rest of the timestamps are not inserted in the list but the last one, which is inserted outside the for loop
                aux_x = []
                aux_y = []
                node_counter = 0
                
            i = 14
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                timestamp = int(float(line[14:i]))
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
            
        elif line.startswith('\t\t\t<node id'):
            i = 13
            while line[i]!='\"' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                # We assume that the first timestamp has all the nodes displayed within the simulation area of BonnMotion
                while int(line[13:i]) != node_counter:
                    # The node is missing at this timestamp. We copy the values of the previous timestamp
                    # While loop in the case there are two or mode nodes missing consecutively
                    node = node_counter
                    node_counter += 1
                    
                    aux_x.insert(int(node), node_x[int(float(timestamp))-1][node])
                    aux_y.insert(int(node), node_y[int(float(timestamp))-1][node])
                
                # After inserting the missing node we have the current node and the node_counter updated    
                node = line[13:i]
                node_counter += 1
                
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'\"\' character')
        elif line.startswith('\t\t\t\t\t<x'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_x.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
        elif line.startswith('\t\t\t\t\t<y'):
            i = 8
            while line[i]!='<' and line[i]!='\n':
                i += 1    
            if line[i]!='\n':
                aux_y.insert(int(node), line[8:i])
            else:
                logger.error('Error: Bad parsing or .wml input file. EOF found and not the \'<\' character')
                         
    # insert the last timestamp information on the list 
    node_x.insert(timestamp, aux_x)
    node_y.insert(timestamp, aux_y)
    
    file_0.close()

    return node_x,node_y


def parser_video(filename,node_x,node_y):
    """Parser for the output 'values' drone file for creating the video application
    
    Parser for the output 'values' drone file for creating the video application.
    """
    t = 0
    drone = 0
    
    file_0 = open (filename,'r')
    
    node_x_aux=[]
    node_y_aux=[]
    
    for line in file_0:
    
        if line.startswith('time='):            
            if int(line[5:]) != 0:
                node_x.insert(t, node_x_aux) 
                node_y.insert(t, node_y_aux)
                
                node_x_aux = []
                node_y_aux = []
                
                t = int(line[5:])
                drone = 0 
            
        elif line.startswith('   drone_id='):
            drone = int(line[12:])
        
        elif line.startswith('\tpos_x='):
            node_x_aux.insert(drone, float(line[7:]))
        
        elif line.startswith('\tpos_y='):
            node_y_aux.insert(drone, float(line[7:]))
    
    # Final values to store in node_x and node_y, as there is no more lines to read 
    node_x.insert(t, node_x_aux) 
    node_y.insert(t, node_y_aux)
    
    # NOTE: The transposition is done outside, as it occurs with the parser of the wml "function"



# Parsers for plotting functions
#--------------------------------
def parser_discovered(in_file,drones_amount):
    """ Gets the nodes_in_range data from the file in order to be plot """
    discovered=[]      
        
    for i in range(drones_amount):
        discovered.append([])
    
    for line in in_file:
        if line.endswith('drone_id=0\n'):            
            drone_id=0 
        
        elif line.startswith('\tnodes_in_range_total='):
            discovered[drone_id].append(float(line[22:]))
            drone_id += 1
            
    return discovered  



def parser_acc_discovered(in_file):
    """ Gets the accumulated total amount of nodes discovered per time"""
    
    nodes_info=[]
    t_info = [] # store merged nodes_discovered information per each timestamp
    nodes_flag = False # True when reading nodes discovered list, False when read 'drone_id'
    
    # extracts and merges EACH timestamp nodes_discovered tables from all drones    
    for line in in_file:
        # parse only the last timestamp
        if line.startswith('timestamp='):    
            timestamp = int(line[10:].strip('\n'))
            
            if timestamp == 0:
                # first timestamp
                pass 
            else:     
                nodes_info.append(t_info)
                t_info = [] 
                nodes_flag = False # avoids reading other information when a timestamp finishes
                
        if line.startswith('   drone_id='):            
            nodes_flag = False # avoids reading other information from drones
            
        if line.startswith('\t\tnode_id'):
            nodes_flag = True # activates reading the nodes_discovered table
        
        elif nodes_flag == True:
            if line != '\t[]\n':
                # if nodes_discovered table is not empty
                aux = line[2:]
                aux = aux.strip('\n')
                aux = aux.replace('\t\t\t','\t\t')
                aux = aux.split('\t\t')                    
                
                if not t_info:
                    # if t_info is empty (no nodes discovered before)
                    aux[0] = int(aux[0])
                    aux[2] = int(aux[2])
                    aux[3] = int(aux[3])
                    
                    t_info.append(copy.deepcopy(aux)) # positions are copied without any transformation
                else:
                    aux[0] = int(aux[0])
                    aux[2] = int(aux[2])
                    aux[3] = int(aux[3])
                    
                    if aux[0] in zip(*t_info)[0]:
                        for node_i in range(len(t_info)):
                            if aux[0] == t_info[node_i][0]:
                                if aux[3] > t_info[node_i][3]:                                                                    
                                    t_info[node_i] = copy.deepcopy(aux)
                                else:
                                    # do nothing, as the node is in its most updated time
                                    pass
                    else:                        
                        t_info.append(copy.deepcopy(aux))
    
    # last timestamp append
    nodes_info.append(t_info)
    
    # after everything is merged we can sort and extract the info per each timestamp
    total_nodes_time = []
    
    for time_i in nodes_info:        
        
        # total number of nodes
        total_nodes_time.append(len(time_i))            
    
    return total_nodes_time



def parser_discovered_per_time(in_file):
    """ Gets the nodes discovered per time stamp.
        
    Parameters
    ----------
    in_file : file
        Plain text file containing the values of the simulation.
        
    Returns
    -------
    total_discovered_time : list
        list containing the unique number of nodes discovered each time stamp

    
    """
    total_discovered_time=[]
    discovered_time=[]
    nodes_t=[]
    
    
    for line in in_file:
        if line.startswith('timestamp='):    
            timestamp = int(line[10:].strip('\n'))
            
            if timestamp == 0:
                # first timestamp
                pass 
            else:     
                discovered_time.append(copy.deepcopy(nodes_t))
                del nodes_t[:] 
        
        if line.startswith('\tnodes_in_range='):
            # if there are nodes discovered by this drone at this time stamp
            if not line.startswith('\tnodes_in_range=[]'):
                
                aux = line.strip('\tnodes_in_range=[')
                aux_list = re.split(r'\]\,\[',aux,re.S) 
    
                # save nodes id's discovered in a specific time stamp by a specific drone
                for i,item in enumerate(aux_list):
                    # if nodes_t is empty
                    if not nodes_t:
                        node_str=item.split(',')
                        nodes_t.append(copy.deepcopy(node_str[0])) # the first element is the node id
                    else:
                        # check if node id is already in node_t
                        del node_str[:]
                        node_str=item.split(',')
                        
                        if node_str[0] in zip(*nodes_t):
                            # do nothing, as the node is in its most updated time
                            pass
                        else:                        
                            nodes_t.append(copy.deepcopy(node_str[0]))

            # empty nodes_in_range
            else:
                pass

    # append the latest read values
    discovered_time.append(copy.deepcopy(nodes_t))
    del nodes_t[:] 
    
    total_discovered_time=[len(time_i) for time_i in discovered_time]
            
    return total_discovered_time  



def parser_nodes_statistics(in_file,nodes_amount,duration):
    """ Gets the nodes update time frequency and other statistics.
    
    NOTE: nodes ids start at the id = 0
        
    Parameters
    ----------
    in_file : file
        Plain text file containing the values of the simulation.
        
    Returns
    -------
    total_discovered_time : list
        list containing the unique number of nodes discovered each time stamp

    
    """    
    nodes_events=[]
    
    # nodes ids start at the id=0
    for i in range(nodes_amount):
        empty_list=[]
        nodes_events.append(copy.deepcopy(empty_list))
        del empty_list
        
    
    for line in in_file:
        if line.startswith('timestamp='):    
            timestamp = int(line[10:].strip('\n'))
        
        if line.startswith('\tnodes_in_range='):
            # if there is not any node discovered by this drone at this time stamp
            if not line.startswith('\tnodes_in_range=[]'):

                aux = line.strip('\tnodes_in_range=[')            
                aux_list = re.split(r'\]\,\[',aux,re.S) 
                
                # get nodes id's discovered in a specific time stamp by a specific drone
                for i,item in enumerate(aux_list):
                    
                    # get node id
                    node_id=int(item.split(',')[0])
                    
                    # the first time this node was discovered by a drone
                    if len(nodes_events[node_id]) == 0:                   
                        # create the node sublist as a list with the time stamp
                        nodes_events[node_id].append(timestamp)
                    
                    # the node was discovered in a previous time stamp
                    else:
                        # check if another drone connected to the same node in the same time stamp
                        if nodes_events[node_id][-1] == timestamp:
                            pass
                        else:
                            # the first time this node is discovered in this time stamp
                            nodes_events[node_id].append(timestamp)
            
            # empty nodes_in_range
            else:
                pass
    
    # calculate the number of connections of nodes for creating a histogram
    nodes_frequency=[len(node_i) for node_i in nodes_events]
    
    # calculate nodes time interval between consecutive connections
    nodes_time_btw_conn=[]
        
    del node_i[:] # clear previous use of this variable
    
    for node_i in nodes_events:
        # there is no connections with this node
        if len(node_i) == 0:
            # we store the entire duration of the experiment as the time between connections
            nodes_time_btw_conn.append(duration)
        
        else:
            
            for i,connection_i in enumerate(node_i):
                if i == 0:
                    # store the first connection
                    prev = node_i[0]
                
                else:
                    time_diff = connection_i - prev
                    nodes_time_btw_conn.append(time_diff)
                    
                    prev = connection_i
                    
    
            
    return nodes_events,nodes_frequency,nodes_time_btw_conn 



def parser_positions(in_file,drones_amount):
    """ Gets the pos_x and posy_ data from the file in order to be plot """
    positions=[]
        
    for i in range(drones_amount):
        positions.append([])
    
    for line in in_file:
        if line.endswith('drone_id=0\n'):            
            drone_id=0 
        
        elif line.startswith('\tpos_x='):
            aux_x = float(line[7:])
            
        elif line.startswith('\tpos_y='):
            aux_y = float(line[7:])
            positions[drone_id].append((aux_x,aux_y))
            drone_id += 1
            
    return positions


def parser_localbest(in_file,drones_amount):
    """ Gets the local_best from the file in order to be plot """
    localbest_total=[]
    localbest_pos=[]      
        
    for i in range(drones_amount):
        localbest_total.append([])
        localbest_pos.append([])
    
    for line in in_file:
        if line.endswith('drone_id=0\n'):            
            drone_id=0 
        
        elif line.startswith('\tlocal_best='):
            aux = line[12:]
            aux = aux.replace('[','').replace(']','')
            aux = aux.split(",")
            
            total = int(aux[0])
            x_pos = float(aux[1])
            y_pos = float(aux[2])
            
            localbest_total[drone_id].append(total)
            localbest_pos[drone_id].append((x_pos,y_pos))
            drone_id += 1
            
    return localbest_total,localbest_pos


def parser_neighborsbest(in_file,drones_amount):
    """ Gets the neighbors_best from the file in order to be plot """
    neighbest_discoverer=[]
    neighbest_total=[]
    neighbest_pos=[]
          
    for i in range(drones_amount):
        neighbest_discoverer.append([])
        neighbest_total.append([])
        neighbest_pos.append([])
        
    for line in in_file:
        if line.endswith('drone_id=0\n'):            
            drone_id=0 
        
        elif line.startswith('\tneighbor_best='):
            aux = line[15:]
            aux = aux.replace('[','').replace(']','')
            aux = aux.split(",")
            
            discoverer = int(aux[0])
            total = int(aux[1])
            x_pos = float(aux[2])
            y_pos = float(aux[3])
            
            neighbest_discoverer[drone_id].append(discoverer)
            neighbest_total[drone_id].append(total)
            neighbest_pos[drone_id].append((x_pos,y_pos))
            drone_id += 1
            
    return neighbest_discoverer,neighbest_total,neighbest_pos


def parser_update_time(in_file,drones_amount,duration):
    """ Gets the nodes' update time from the file in order to be plot """
    
    nodes_info=[]
    
    nodes_flag = False # True when reading nodes discovered list, False when read 'drone_id'
    final_timestamp = int(duration)-1    
    final_time_flag = False
    
    # extracts and merges the last timestamp nodes_discovered tables from all drones    
    for line in in_file:
        # parse only the last timestamp
        if line.startswith('timestamp='+str(final_timestamp)):
            # detects when the nodes list finished for one drone
            final_time_flag = True
            
        if final_time_flag == True:
            if line.startswith('   drone_id='):            
                nodes_flag = False
                
            if line.startswith('\t\tnode_id'):
                nodes_flag = True
            
            elif nodes_flag == True:
                if line != '\t[]\n':
                    aux = line[2:]
                    aux = aux.strip('\n')
                    aux = aux.replace('\t\t\t','\t\t')
                    aux = aux.split('\t\t')                    
                    
                    if not nodes_info:
                        # nodes_info is empty
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        nodes_info.append(copy.deepcopy(aux))
                    else:
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        if aux[0] in zip(*nodes_info)[0]:
                            for node_i in range(len(nodes_info)):
                                if aux[0] == nodes_info[node_i][0]:
                                    if aux[3] > nodes_info[node_i][3]:                                                                    
                                        nodes_info[node_i] = copy.deepcopy(aux)
                                    else:
                                        # do nothing, as the node is in its most updated time
                                        pass
                        else:                        
                            nodes_info.append(copy.deepcopy(aux))
    
    # sort the nodes_info table according to the timestamp
    sorted_nodes = sorted(nodes_info, key=itemgetter(3))
    
    # total number of nodes
    total_nodes = len(sorted_nodes)
    
    # counts the number of nodes per each timestamp
    nodes_per_time = []
    update_times = zip(*sorted_nodes)[3]
    
    for timestamp in range(duration):
        amount = update_times.count(duration-1-timestamp)
        nodes_per_time.append(amount)
    
    # nodes positions and their update time in a colormap-shape
    positions_per_time = []
    positions = zip(*sorted_nodes)[1]
    
    for i,node in enumerate(positions):
        aux = node.strip('[]')
        aux = aux.replace(' ','')
        aux = aux.split(',')
        x_aux = float(aux[0])
        y_aux = float(aux[1])
        update_t = duration-1-update_times[i]
        positions_per_time.append((x_aux,y_aux,update_t))
            
    
    return nodes_per_time,positions_per_time,total_nodes


def parser_update_time_intermediate(in_file,drones_amount,intermediate_time):
    """ Gets the nodes' update time from the file in order to be plot """
    
    nodes_info=[]
    
    nodes_flag = False # True when reading nodes discovered list, False when read 'drone_id'
    final_timestamp = int(intermediate_time)-1    
    final_time_flag = False
    
    # extracts and merges the last timestamp nodes_discovered tables from all drones    
    for line in in_file:
        # parse only the last timestamp
        if line.startswith('timestamp='+str(final_timestamp)):
            # detects when the nodes list finished for one drone
            final_time_flag = True
        
        if line.startswith('timestamp='+str(final_timestamp+1)):
            # detects when the specific timestamp of interest finished
            final_time_flag = False
            
        if final_time_flag == True:
            if line.startswith('   drone_id='):            
                nodes_flag = False
                
            if line.startswith('\t\tnode_id'):
                nodes_flag = True
            
            elif nodes_flag == True:
                if line != '\t[]\n':
                    aux = line[2:]
                    aux = aux.strip('\n')
                    aux = aux.replace('\t\t\t','\t\t')
                    aux = aux.split('\t\t')                    
                    
                    if not nodes_info:
                        # nodes_info is empty
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        nodes_info.append(copy.deepcopy(aux))
                    else:
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        if aux[0] in zip(*nodes_info)[0]:
                            for node_i in range(len(nodes_info)):
                                if aux[0] == nodes_info[node_i][0]:
                                    if aux[3] > nodes_info[node_i][3]:                                                                    
                                        nodes_info[node_i] = copy.deepcopy(aux)
                                    else:
                                        # do nothing, as the node is in its most updated time
                                        pass
                        else:                        
                            nodes_info.append(copy.deepcopy(aux))
    
    # sort the nodes_info table according to the timestamp
    sorted_nodes = sorted(nodes_info, key=itemgetter(3))
    
    # total number of nodes
    total_nodes = len(sorted_nodes)
    
    # counts the number of nodes per each timestamp
    nodes_per_time = []
    update_times = zip(*sorted_nodes)[3]
    
    for timestamp in range(intermediate_time):
        amount = update_times.count(intermediate_time-1-timestamp)
        nodes_per_time.append(amount)
    
    # nodes positions and their update time in a colormap-shape
    positions_per_time = []
    positions = zip(*sorted_nodes)[1]
    
    for i,node in enumerate(positions):
        aux = node.strip('[]')
        aux = aux.replace(' ','')
        aux = aux.split(',')
        x_aux = float(aux[0])
        y_aux = float(aux[1])
        update_t = intermediate_time-1-update_times[i]
        positions_per_time.append((x_aux,y_aux,update_t))
            
    
    return nodes_per_time,positions_per_time,total_nodes



def parser_update_time_interval(in_file,drones_amount,duration):
    """ Gets the nodes' update time from the file at specific time intervals of 60 seconds.
    
    Creates tables of the nodes update time each 60 seconds. The 60 seconds interval is a fixed interval: 
    
    Parameters
    ----------
    in_file : file
        Plain text file containing the values of the simulation.
    drones_amount : int 
        Number of drones
    duration : int
        Duration of the simulation
        
    Returns
    -------
    nodes_per_time_t : list
        list of lists containing the nodes update time at different intervals
    """
    tables_interval=[] # for storing the different tables generated each interval
    nodes_info=[]
    nodes_per_time_t=[]
    total_nodes_t=[]
    interval = 60
    nodes_flag = False # True when reading nodes discovered list, False when read 'drone_id'
    interval_list = range(0,duration,interval) # list of intervals to be parsed
    interval_iter=iter(interval_list)
    interval = next(interval_iter)
    interval_time_flag = False
    appended_flag = False
    
    # extracts and merges the last time stamp nodes_discovered tables from all drones    
    for line in in_file:
        # parse all the time stamp in the timestamp_list
        if line.startswith('timestamp='):
            
            nodes_flag=False
            
            if line.startswith('timestamp='+str(interval)):
                # detects if the timestamp belongs to an interval of interest
                interval_time_flag = True       
                appended_flag = False
                
                try:
                    interval=next(interval_iter)
                except StopIteration:
                    logger.error('Reached last interval in update_time_interval charts')
                    
            else:
                # a new timestamp line was read but it does not correspond an interval
                interval_time_flag = False
                
                if appended_flag == False:
                    tables_interval.append(copy.deepcopy(nodes_info))
                    appended_flag = True
                else:
                    # the nodes_info table of interest was already appended to tables_interval 
                    pass
            
        if interval_time_flag == True:
            if line.startswith('   drone_id='):            
                nodes_flag = False
                
            if line.startswith('\t\tnode_id'):
                nodes_flag = True
            
            elif nodes_flag == True:
                if line != '\t[]\n':
                    aux = line[2:]
                    aux = aux.strip('\n')
                    aux = aux.replace('\t\t\t','\t\t')
                    aux = aux.split('\t\t')                    
                    
                    if not nodes_info:
                        # nodes_info is empty
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        nodes_info.append(copy.deepcopy(aux))
                    else:
                        aux[0] = int(aux[0])
                        aux[2] = int(aux[2])
                        aux[3] = int(aux[3])
                        
                        if aux[0] in zip(*nodes_info)[0]:
                            for node_i in range(len(nodes_info)):
                                if aux[0] == nodes_info[node_i][0]:
                                    if aux[3] > nodes_info[node_i][3]:                                                                    
                                        nodes_info[node_i] = copy.deepcopy(aux)
                                    else:
                                        # do nothing, as the node is in its most updated time
                                        pass
                        else:                        
                            nodes_info.append(copy.deepcopy(aux))
    
    
    # generate again the timestamp intervals list        
    interval_iter=iter(interval_list)
    
    for nodes_info_i in tables_interval:
        
        interval=next(interval_iter)
        
        # sort the nodes_info table according to the timestamp
        sorted_nodes = sorted(nodes_info_i, key=itemgetter(3))
        
        # total number of nodes
        total_nodes_t.append(len(sorted_nodes))
        
        # counts the number of nodes per each timestamp
        nodes_per_time = []
        if sorted_nodes:
            update_times = zip(*sorted_nodes)[3]
        else:
            update_times=[]
        
        for timestamp in range(interval):
            amount = update_times.count(interval-1-timestamp)
            nodes_per_time.append(amount)
                
        nodes_per_time_t.append(copy.deepcopy(nodes_per_time))
        
    return nodes_per_time_t,interval_list,total_nodes_t



def parser_encounters(in_file,drones_amount):
    """ Parse drones_in_range """
    
    drones_in_range=[]
    encounters=[] # encounters per time (all drones)
        
    for i in range(drones_amount):
        drones_in_range.append([])
    
    for line in in_file:
        if line.endswith('drone_id=0\n'):            
            drone_id=0 
        
        elif line.startswith('\tdrones_in_range='):
            aux = line[17:]
            aux = aux.strip('\n')
            aux = aux.strip('[]')
            
            if aux == '':
                aux = []
            else:
                aux = aux.split(',')
                aux[:] = [int(i) for i in aux] # convert to int
                
            drones_in_range[drone_id].append(copy.deepcopy(aux))
            drone_id += 1
    
    # calculate encounters per time
    drones_transp = zip(*drones_in_range)
    
    for timestamp in drones_transp:
        drones_graph = nx.Graph()
        
        for drone_i,dr_in_range in enumerate(timestamp):
            if dr_in_range:
                edges = [(drone_i,i) for i in dr_in_range]
                drones_graph.add_edges_from(edges) # nodes ids correspond to drones ids
            else:               
                # empty list, the drone is not connected to any other drone but we add the node
                # to the graph as a not connected node so far
                drones_graph.add_node(drone_i)
        
        encounters.append(drones_graph.number_of_edges())
    
    total_encounters = sum(encounters)
    
    last_graph = drones_graph
    
    return encounters, total_encounters, last_graph
    
