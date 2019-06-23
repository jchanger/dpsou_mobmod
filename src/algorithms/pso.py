"""
Created on Mar 14, 2017

@author: J. Sanchez-Garcia
"""

import numpy as np
from random import randint,uniform
from functions import geometry


def random_algo(self_drone):
    """ Calculate a random next destination for a drone movement""" 
    
    # Define a random point that will determine the direction for the first movement
    # the destination is chosen from within the scenario, no possibility to be out the first time 
    point = []
    point.append(randint(0, self_drone.area_dimens[0]))
    point.append(randint(0, self_drone.area_dimens[1]))
    
    # Calculate the next destination point
    closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, point, self_drone.max_speed)

    return closer_p



def generate_pso_params():
    """ Generate sequences of numbers for pso parameters """

    pso_vals = []
     
    # inertia final value has not to be generated as it is calculated as the difference with lb and nb
     
    # only local best: local best increases and global best is zero
    mode = 'inertia-local'
    lb_vals = np.arange(0.0,1.2,0.25) # the value of 1.2 is set for getting lb_vals=1 as the last element
    nb_vals = np.zeros(5)
     
    pso_vals.append([mode,lb_vals.tolist(),nb_vals.tolist()])
     
    # only global best: global best increases and local best is zero
    mode = 'inertia-global'
    lb_vals = np.zeros(5)
    nb_vals = np.arange(0.0,1.2,0.25) # the value of 1.2 is set for getting lb_vals=1 as the last element
     
    pso_vals.append([mode,lb_vals.tolist(),nb_vals.tolist()])
 
    # residual local best: local best residual constant value and global best increases
    mode = 'residual-local'
    lb_vals = np.empty(4)
    lb_vals.fill(0.2)
    nb_vals = np.arange(0.2,1.0,0.2)
     
    pso_vals.append([mode,lb_vals.tolist(),nb_vals.tolist()])
     
    # residual global best: global best residual constant value and local best increases
    mode = 'residual-global'
    lb_vals = np.arange(0.2,1.0,0.2)
    nb_vals = np.empty(4)
    nb_vals.fill(0.2)
     
    pso_vals.append([mode,lb_vals.tolist(),nb_vals.tolist()])
     
    # equal local-global
    mode = 'equal_local-global'
    lb_vals = np.arange(0.2,0.6,0.1)
    nb_vals = np.arange(0.2,0.6,0.1)
     
    pso_vals.append([mode,lb_vals.tolist(),nb_vals.tolist()])
     
    return pso_vals


def get_inertia_p(self_drone,inertia_weight):
    """ Calculate the next inertia point """
    
    # inertia weight calculation
    inertia_displacement = self_drone.max_speed * inertia_weight

    # calculate inertia next point
    closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, self_drone.prev_position, inertia_displacement)
    
    # we select the further_p because we use the direction defined by the previous position and current position 
    return further_p


def get_localbest_p(self_drone, lb_weight):
    """ Calculate the next local best point """
    # calculate difference between current position and local best
    l_best_distance = geometry.get_distance(self_drone.position, self_drone.local_best[1])
    
    if l_best_distance > self_drone.max_speed:
        # local best weight calculation with the drone max_speed
        l_best_displacement = self_drone.max_speed * lb_weight
    else:
        # local best weight calculation
        l_best_displacement = l_best_distance * lb_weight
    
    # calculate local_best next point
    closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, self_drone.local_best[1], l_best_displacement)
    
    # we select closer_p because it is the point closer to the local best attraction point
    return closer_p
    

def get_neighbest_p(self_drone, neigh_weight):
    """ Calculate the next neighbor best point """
    # calculate difference between current position and neigh best position (neighbors_best[2])
    n_best_distance = geometry.get_distance(self_drone.position, self_drone.neighbors_best[2]) 
    
    if n_best_distance > self_drone.max_speed:
        # neighbors best weight calculation with the drone max_speed
        n_best_displacement = self_drone.max_speed * neigh_weight
    else:
        # neigh best weight calculation
        n_best_displacement = n_best_distance * neigh_weight
    
    # calculate neighbors_best next point
    closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, self_drone.neighbors_best[2], n_best_displacement)
    
    # we select closer_p because it is the point closer to the local best attraction point
    return closer_p


def get_pos_from_out(self_drone, added_pos, *vectors):
    """ If the drone next position is out of the scenario boundaries recalculates the inertia component"""
    # check if the drone is out of the area dimension
    # This is calculated after the local_best and inertia addition in order to see if 
    # the addition avoids that the inertia gets out of the scenario area
    out = geometry.is_out_area(added_pos, self_drone.area_dimens)
    
    if out:
        while out:
            inertia_pos = random_algo(self_drone)
            out = geometry.is_out_area(inertia_pos, self_drone.area_dimens)
        
        # depending on the case, add the vectors (local_best and neigh_best to the new  random-inertia point) 
        if len(vectors) == 0:
            # only inertia case
            aux_pos = inertia_pos
        elif len(vectors) == 1:
            # inertia and local_best case
            aux_pos = geometry.add_vectors(self_drone.position,inertia_pos,vectors[0])
        else:
            # inertia, local_best and neigh_best case
            aux_pos = geometry.add_vectors(self_drone.position,inertia_pos,vectors[0],vectors[1])
    else:
        aux_pos = added_pos
        
    return aux_pos
    



def pso_algo(self_drone):
    """ Calculate the next destination for a drone movement with fixed values of inertia,
    local best (lb) and neighbor best (nb),and also time values, i.e. the start time of
    lb and nb. The weight values depend on and change for each time step"""
    
    # random move if we are in the first timesteps
    if self_drone.drone_time == 0:
        if self_drone.first_inertia == None:
            # the first_inertia points were not calculated (the initial movement of drones is entirely random)
            aux_pos = random_algo(self_drone)   
        else:
            # the self_drone.next_position can be generated from the first inertia values
            # the first_inertia target positions are assigned in order no  matter the random initial position of the drone
            target_pos = self_drone.first_inertia[self_drone.drone_id]
            
            closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position,target_pos,self_drone.max_speed)
            
            # select the closer point to the first inertia target
            aux_pos = closer_p
    
    # for the rest of the timesteps
    else:
        # first simulation stage with only inertia
        if self_drone.drone_time <= self_drone.pso_params[3]:
            # inertia
            inertia_weight =  self_drone.pso_params[0][0]
            inertia_pos = get_inertia_p(self_drone, inertia_weight)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, inertia_pos)
                
        # second simulation stage with local_best effects increasing 
        elif self_drone.drone_time <= self_drone.pso_params[4]:
            # weights calculation
            lb_walk = self_drone.pso_params[1][1] - self_drone.pso_params[1][0] # difference between the max and min values of local_best effect
            lb_walk_duration = self_drone.pso_params[4] - self_drone.pso_params[3]
            lb_step = lb_walk/lb_walk_duration
            lb_weight = lb_step*(self_drone.drone_time - self_drone.pso_params[3])
            
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia and local best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos)
        
        # third stage where local_best reaches its max value and neighbors_best has not started yet
        elif self_drone.drone_time <= self_drone.pso_params[5]:       
        # weights calculation
            lb_weight = self_drone.pso_params[1][1]
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia and local best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos)   
        
        # fourth stage where neighbors_best starts having effects
        elif self_drone.drone_time <= self_drone.pso_params[6]:
            # weights calculation
            nb_walk = self_drone.pso_params[2][1] - self_drone.pso_params[2][0] # difference between the max and min values of neighbors_best effect
            nb_walk_duration = self_drone.pso_params[6] - self_drone.pso_params[5]
            nb_step = nb_walk/nb_walk_duration
            nb_weight = nb_step*(self_drone.drone_time-self_drone.pso_params[5])
                        
            lb_weight = self_drone.pso_params[1][1] # lb_weight is at its max value
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight-nb_weight
                        
            # inertia, local_best and neighbor best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
            n_best_pos = get_neighbest_p(self_drone,nb_weight)
            
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos,n_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone,added_pos,l_best_pos,n_best_pos)
        
        # after the neighbors_best reached its maximum
        else:
            nb_weight = self_drone.pso_params[2][1]
            lb_weight = self_drone.pso_params[1][1]
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight-nb_weight
            
            # inertia, local_best and neighbor best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
            n_best_pos = get_neighbest_p(self_drone,nb_weight)
            
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos,n_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone,added_pos,l_best_pos,n_best_pos)
            
    return aux_pos       
    


def pso_algo_force_inertia(self_drone):
    """ Calculate the next destination for a drone movement with fixed values of inertia,
    local best (lb) and neighbor best (nb),and also time values, i.e. the start time of
    lb and nb. The weight values depend on and change for each time step. It makes a drone
    to keep searching if no node was found """
    
    # random move if we are in the first timesteps
    if self_drone.drone_time == 0:
        if self_drone.first_inertia == None:
            # the first_inertia points were not calculated (the initial movement of drones is entirely random)
            aux_pos = random_algo(self_drone)   
        else:
            # the self_drone.next_position can be generated from the first inertia values
            # the first_inertia target positions are assigned in order no  matter the random initial position of the drone
            target_pos = self_drone.first_inertia[self_drone.drone_id]
            
            closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position,target_pos,self_drone.max_speed)
            
            # select the closer point to the first inertia target
            aux_pos = closer_p
    
    # for the rest of the timesteps
    else:
        # we maintain the inertia if nodes_discovered is empty
        if not self_drone.nodes_discovered: 
            # inertia
            inertia_weight =  self_drone.pso_params[0][0]
            inertia_pos = get_inertia_p(self_drone, inertia_weight)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, inertia_pos)
            
        # after the previous condition, we move to only inertia if we are still in that time
        elif self_drone.drone_time <= self_drone.pso_params[3]:
            # inertia
            inertia_weight =  self_drone.pso_params[0][0]
            inertia_pos = get_inertia_p(self_drone, inertia_weight)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, inertia_pos)
                
        # second simulation stage with local_best effects increasing 
        elif self_drone.drone_time <= self_drone.pso_params[4]:
            # weights calculation
            lb_walk = self_drone.pso_params[1][1] - self_drone.pso_params[1][0] # difference between the max and min values of local_best effect
            lb_walk_duration = self_drone.pso_params[4] - self_drone.pso_params[3]
            lb_step = lb_walk/lb_walk_duration
            lb_weight = lb_step*(self_drone.drone_time - self_drone.pso_params[3])
            
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia and local best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos)
        
        # third stage where local_best reaches its max value and neighbors_best has not started yet
        elif self_drone.drone_time <= self_drone.pso_params[5]:       
        # weights calculation
            lb_weight = self_drone.pso_params[1][1]
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia and local best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos)   
        
        # fourth stage where neighbors_best starts having effects
        elif self_drone.drone_time <= self_drone.pso_params[6]:
            # weights calculation
            nb_walk = self_drone.pso_params[2][1] - self_drone.pso_params[2][0] # difference between the max and min values of neighbors_best effect
            nb_walk_duration = self_drone.pso_params[6] - self_drone.pso_params[5]
            nb_step = nb_walk/nb_walk_duration
            nb_weight = nb_step*(self_drone.drone_time-self_drone.pso_params[5])
                        
            lb_weight = self_drone.pso_params[1][1] # lb_weight is at its max value
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight-nb_weight
                        
            # inertia, local_best and neighbor best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
            n_best_pos = get_neighbest_p(self_drone,nb_weight)
            
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos,n_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone,added_pos,l_best_pos,n_best_pos)
        
        # after the neighbors_best reached its maximum
        else:
            nb_weight = self_drone.pso_params[2][1]
            lb_weight = self_drone.pso_params[1][1]
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight-nb_weight
            
            # inertia, local_best and neighbor best
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
            l_best_pos = get_localbest_p(self_drone,lb_weight)
            n_best_pos = get_neighbest_p(self_drone,nb_weight)
            
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos,n_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone,added_pos,l_best_pos,n_best_pos)
            
    return aux_pos  

