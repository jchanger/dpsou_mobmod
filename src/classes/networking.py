""" This module acts as an object emulating a future server for the network simulator

-----------------------
Created on Mar 19, 2017

@author: J. Sanchez-Garcia
"""

import drone
import node
from functions import geometry


class Network():
    
    def __init__(self, CONFIG):
        
        self.drones_am = CONFIG['drones_amount']
        self.nodes_am = CONFIG['nodes_amount']
        
        # the following variables counts simulated call from drones and victims
        self.drone_calls = 0
        self.node_calls = 0
        
        # variables for storing the drones and victims list
        self.drone_list = []
        self.node_list = []
        
    
    def comm_request(self, obj_i):
        """This module will receive all objects (drones and victims) requests for exchanging messages with other modules"""
        
        # if the object is of drone type
        # TODO: at each timestep all the objects are appended to list, this should be changed to do it only the first time for efficiency reasons 
        if isinstance(obj_i,drone.Drone):
            self.drone_list.append(obj_i)
            
            # count the number of calls received
            self.drone_calls +=1
        
        # when the obj_i is a node (victim)
        else:
            self.node_list.append(obj_i)
            
            # count the number of calls received
            self.node_calls +=1
            
        if self.drone_calls == self.drones_am and self.node_calls == self.nodes_am:
            # call to drones_in_range()
            self.nodes_in_range()
        
            # call to nodes_in_range
            self.drones_in_range()
            
            # empty drones and nodes lists for the next timestamp calls
            self.drone_calls = 0
            self.node_calls = 0
            
            self.drone_list = []
            self.node_list = []
        else:
            # do nothing and wait to other drones and nodes calls to exchange messages
            pass
            
        
        
    def nodes_in_range(self):
        """Calculate the nodes that are within range for each drone"""
               
        for drone_i in self.drone_list:
            coverage_dist = drone_i.coverage
            
            # empty the previous timestamp list
            drone_i.nodes_in_range = []
            
            for node_j in self.node_list:
                distance = geometry.get_distance(drone_i.position, node_j.position)
                
                if distance <= coverage_dist:
                    # the node is under coverage, create a list with the nodes id's and their positions
                    drone_i.nodes_in_range.append([node_j.node_id,node_j.position])
                    
                else:
                    pass
    
    
    def drones_in_range(self):
        """Euclidean distance between drones and security distance by using this function"""
        
        for drone_i in self.drone_list:
            # empty previous timestamp lists of all drones
            drone_i.drones_in_range = []
            drone_i.neighbors_discovered = []
            drone_i.neighbors_localbest = []
            drone_i.neighbors_neighbest = []
            
        # Loop for the encounters. We consider the coverage_i as the ability of a drone to send a message
        # to other drone. In the case they have different coverage, it may occur that one receives a message
        # but it is not able to send its message due to the lack of transmission power
        # TODO: Check the concept of above
        for i in range(0,len(self.drone_list)):
            for j in range(0,len(self.drone_list)):
                # we take into account the coverage of the drones that can reach us (we detect them when we receive a message from them)
                coverage_j = self.drone_list[j].coverage
                                
                if i != j:
                    distance = geometry.get_distance(self.drone_list[i].position, self.drone_list[j].position)
                    
                    if distance <= coverage_j:
                        # update drones_in_range
                        self.drone_list[i].drones_in_range.append(self.drone_list[j].drone_id)
                        
                        # receive the nodes_discovered table of the drones who has drone_i in range, with the first field being the node_id of the sender
                        self.drone_list[i].neighbors_discovered.append([self.drone_list[j].drone_id,self.drone_list[j].nodes_discovered])
                        
                        # receive the local_best of other drones
                        self.drone_list[i].neighbors_localbest.append([self.drone_list[j].drone_id,self.drone_list[j].local_best])
                        # receive the neigh_best of other drones
                        self.drone_list[i].neighbors_neighbest.append(self.drone_list[j].neighbors_best)
                else:
                    # the case when the drone_i check its coverage with itself
                    pass    

