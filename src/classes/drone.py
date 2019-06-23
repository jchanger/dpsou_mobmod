"""
Created on Jun 3, 2016

@author: J. Sanchez-Garcia
"""

from functions import communications
from functions import output
from algorithms import pso
from algorithms import lawn_mower
import copy


class Drone():
       
    def __init__(self, drone_id, CONFIG, init_pos, sim_network,first_inertia=None,trajectory=None):
                
        self.drone_id = drone_id
        self.coverage = CONFIG['coverage']
        self.max_speed = CONFIG['max_speed']
        self.drones_amount = CONFIG['drones_amount']
        self.area_dimens = CONFIG['area_dimens']
        self.pso_params = CONFIG['pso_params']
        self.force_inertia = self.pso_params[7]
        self.algorithm = CONFIG['algorithm']
        self.init_distrib = CONFIG['init_distrib']
        self.first_inertia = first_inertia
        
        # time related variable
        self.drone_time = 0
        self.drone_duration = CONFIG['duration']
        
        # Position related variables
        #    position: current position at the time of starting the loop
        #    next_position: next position to occupy at the next time step
        #    prev_position: positions corresponding to the previous time step
        self.position = [0.0,0.0]
        self.position[0] = init_pos[0][drone_id]
        self.position[1] = init_pos[1][drone_id]
        
        # for lawn_mower mobility
        if self.algorithm == 'lawn_mower':
            self.trajectory = trajectory
        
        self.next_position = [0.0,0.0]        
        self.prev_position = [0.0,0.0]
        
        # nodes and drones in range list of the current timestamp (after communicate function)    
        self.nodes_in_range = []  
        self.drones_in_range = []
        
        # Discovered nodes table and timestamps associated, this will be exchanged by drones
        # The 'nodes_discovered' table refers to the entire simulation time, i.e. it stores nodes discovered in different timestamps 
        self.nodes_discovered = []
        self.neighbors_discovered = [] # stores the nodes_discovered tables received from other drones
        self.neighbors_localbest = [] # stores the local_best received from other drones
        self.neighbors_neighbest = [] # stores the neighbors_best received from other drones
        
        # attraction points. The max_serviced_values refers to a 1 specific position occupied by 1 drone at a specific timestamp
        self.local_best = [0,[0.0,0.0]] # [max_serviced_nodes, [position_of_the_max_value]]
        self.neighbors_best = [0,0,[0.0,0.0]] # : [drone_best,max_serviced_nodes,[position_of_the_max_value]] 
        
        # network emulator object
        self.network = sim_network
            
    
    def communicate(self):
        communications.send_receive(self)


    def update_nodes_table(self):
        """ Update the nodes_discovered table with the current_discoveries tables""" 
        # merge with other drones nodes_discoveries tables (received at time=t, updated per each drone at time=t-1)
        # TODO: IMPORTANT revise we do not miss any node discovered in this loops (specifically when the tables are empty at the beginning)
        for neighb_id,table in self.neighbors_discovered:
            for node_new in table:
                if self.nodes_discovered: # an empty list is evaluated a 'false'
                    if node_new[0] in zip(*self.nodes_discovered)[0]:
                        for node_info in self.nodes_discovered:
                            if node_new[0] == node_info[0]:
                                # update info if more recent
                                if node_new[3] > node_info[3]:
                                    # node_info[0] id the node_id
                                    node_info[1] = copy.deepcopy(node_new[1]) # node_position
                                    node_info[2] = copy.deepcopy(neighb_id) # drone that discovered the node 
                                    node_info[3] = copy.deepcopy(node_new[3]) # timestamp
                                else:
                                    pass # the node info is not more recent, do not update 
                    else:
                        self.nodes_discovered.append(copy.deepcopy(node_new))
                else:
                    self.nodes_discovered.append(copy.deepcopy(node_new))

            
        # merge with self.nodes_in_range table (updated at time=t)
        for node_new in self.nodes_in_range:
            if self.nodes_discovered: # an empty list is evaluated a 'false'
                if node_new[0] in zip(*self.nodes_discovered)[0]: # transpose and take the first row
                    for node_info in self.nodes_discovered:
                        if node_new[0] == node_info[0]:
                            # update node info
                            # node_info[0] id the node_id
                            node_info[1] = copy.deepcopy(node_new[1]) # node_position
                            node_info[2] = copy.deepcopy(self.drone_id)
                            node_info[3] = copy.deepcopy(self.drone_time)
                        else:
                            pass
                else:
                    # add the new node discovered. We use deepcopy bcs if not the drone_time will vary as the simulation goes on
                    aux_new = []
                    aux_new.append(copy.deepcopy(node_new[0]))
                    aux_new.append(copy.deepcopy(node_new[1]))
                    aux_new.append(copy.deepcopy(self.drone_id))
                    aux_new.append(copy.deepcopy(self.drone_time))
                    
                    self.nodes_discovered.append(aux_new)
            else:
                # add to nodes_discovered when this list is empty
                aux_new = []
                aux_new.append(copy.deepcopy(node_new[0]))
                aux_new.append(copy.deepcopy(node_new[1]))
                aux_new.append(copy.deepcopy(self.drone_id))
                aux_new.append(copy.deepcopy(self.drone_time))
                
                self.nodes_discovered.append(aux_new)
                
    
    def evaluate_local_best(self):
        """Calculate the local best from the nodes_in_range variable"""
        
        # IMPORTANT to work with shallow copies in this function, if not we will lose
        # the info when updating the 'nodes_in_range' in the networking module 
        if self.drone_time == 0:
            # first timestamp, save the first local best from nodes_in_range            
            self.local_best[0] = copy.deepcopy(len(self.nodes_in_range))
            self.local_best[1] = copy.deepcopy(self.position)
        
        else:
            # compare with previous local best, save if it is improved
            if len(self.nodes_in_range) > self.local_best[0]:
                self.local_best[0] = copy.deepcopy(len(self.nodes_in_range))
                self.local_best[1] = copy.deepcopy(self.position)
            else:
                # we keep the previous local best
                pass
        
        
    def evaluate_neighbors_best(self):
        """Calculate the local best from the nodes_in_range variable"""
        
        # IMPORTANT to work with shallow copies in this function, if not we will lose
        # the info when updating the 'nodes_in_range' in the networking module 
        
        if self.drone_time == 0:
            # first timestamp, save the first local best as neighbors best            
            self.neighbors_best[0] = copy.deepcopy(self.drone_id)
            self.neighbors_best[1] = copy.deepcopy(len(self.nodes_in_range))
            self.neighbors_best[2] = copy.deepcopy(self.position)
            
        else:
            # check if the current position is better than the neighbors_neighbest, update if it is improved
            if self.neighbors_best[1] < len(self.nodes_in_range):
                self.neighbors_best[0] = copy.deepcopy(self.drone_id)
                self.neighbors_best[1] = copy.deepcopy(len(self.nodes_in_range))
                self.neighbors_best[2] = copy.deepcopy(self.position)
            
            # compare with received neighbors_neighbest, update if it is improved
            for neighbor in self.neighbors_neighbest:
                if neighbor[1] > self.neighbors_best[1]:
                    self.neighbors_best[0] = copy.deepcopy(neighbor[0])
                    self.neighbors_best[1] = copy.deepcopy(neighbor[1])
                    self.neighbors_best[2] = copy.deepcopy(neighbor[2])
                else:
                    pass # the received neighbest is not better than the current one
    
    
    def calc_next_destination(self):
        """ Calculates the next destination of the drone according to the events and the drone current position """        
        
        if self.algorithm == 'pso':
            self.evaluate_local_best()
            self.evaluate_neighbors_best()
            self.update_nodes_table() # this function has to be called after the evaluate_local_best
            
            if self.force_inertia == 0:
                self.next_position = pso.pso_algo(self) 
            else:
                self.next_position = pso.pso_algo_force_inertia(self)
        
        else:
            self.evaluate_local_best()
            self.evaluate_neighbors_best()
            self.update_nodes_table() # this function has to be called after the evaluate_local_best
            
            self.next_position = lawn_mower.lawnmower_algo(self)
    
    def move(self): 
        """ The function responsible for moving the drone to its next position  
        """    
        # Move the drone to its next position (the position and next_position variables
        # will have the same values until the next execution of this function)
        self.prev_position = self.position
        self.position = self.next_position     
    
    
    def update_time(self):
        # update drone time
        self.drone_time += 1    
        
        
    def drone_logging(self, t_current, output_file, CONFIG):
        if self.drone_id == 0:
            # We print the time stamp only before the drone number 0
            output_file.write('timestamp='+str(t_current)+'\n')
            output.drone_write(self, output_file)
        else:
            output.drone_write(self, output_file)

