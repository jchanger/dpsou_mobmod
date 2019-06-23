"""
Created on Mar 14, 2017

@author: J. Sanchez-Garcia
"""

from random import randint
from functions import geometry


def random_algo(self_drone):
    """ Calculate a random next destination for a drone movement""" 
    
    # Define a random point that will determine the direction for the first movement
    point = []
    point.append(randint(0, self_drone.area_dimens[0]))
    point.append(randint(0, self_drone.area_dimens[1]))
    
    # Calculate the next destination point
    closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, point, self_drone.max_speed)

    return closer_p
    

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



def only_localbest(self_drone):
    """ Calculate the next destination for a drone movement with a local best attraction point"""
    
    # random move if we are in the first timesteps
    if self_drone.drone_time==0:
        aux_pos = random_algo(self_drone)
    
    # for the rest of the timesteps
    else:
        # first simulation stage with only inertia
        if self_drone.drone_time <= self_drone.pso_params[3]:
            # inertia
            #--------
            inertia_weight =  self_drone.pso_params[0][0]
            inertia_pos = get_inertia_p(self_drone, inertia_weight)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, inertia_pos)
                            
        # second simulation stage with local_best effects increasing 
        elif self_drone.drone_time <= self_drone.pso_params[4]:
            # TODO: make these calculations on the drone objects in order to avoid doing it each time here
            # difference between the max and min values of local_best effect
            lb_walk = self_drone.pso_params[1][1] - self_drone.pso_params[1][0]
            lb_walk_duration = self_drone.pso_params[4] - self_drone.pso_params[3]
            lb_step = lb_walk/lb_walk_duration
            
            lb_weight = lb_step*(self_drone.drone_time-self_drone.pso_params[3])
            
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia
            #--------
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
                
            # local best
            #-----------
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos) 
                    
        # third stage where local_best reaches its max value
        else:
            lb_weight = self_drone.pso_params[1][1]
            inertia_weight =  self_drone.pso_params[0][0]-lb_weight
        
            # inertia
            #--------
            inertia_pos = get_inertia_p(self_drone,inertia_weight)
                
            # local best
            #-----------
            l_best_pos = get_localbest_p(self_drone,lb_weight)
                
            # add inertia_final and local_best_final
            added_pos = geometry.add_vectors(self_drone.position,inertia_pos,l_best_pos)
            
            # check if the drone is out and recalculate inertia
            aux_pos = get_pos_from_out(self_drone, added_pos,l_best_pos) 
            
    
    return aux_pos       
        
