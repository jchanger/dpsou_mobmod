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
    
    
def linear_algo(self_drone):
    """ Calculate the next destination for a drone movement"""
    # In the case the drone is at its initial position. If we do not use this random movement at the beginning,
    # all drones start with the same direction as the prev_position=[0,0] at start is equal for all of them 
    if self_drone.drone_time==0:
        aux_pos = random_algo(self_drone)
    
    # in the case it has moved before i.e. prev_position!=[0,0]
    else:
        # check if the drone is out of the area dimension
        out = geometry.is_out_area(self_drone.position, self_drone.area_dimens)
            
        if out:
            while out:
                # calling to random_algo() returns the random next position (not the destination)
                aux_pos = random_algo(self_drone)
                out = geometry.is_out_area(aux_pos, self_drone.area_dimens)    
        else:
            # when we have a linear trajectory defined and we keep following that direction
            closer_p,further_p = geometry.get_closer_and_further_points_v2(self_drone.position, self_drone.prev_position, self_drone.max_speed)
            # we select the further_p because we use the direction defined by the previous position and current position 
            aux_pos = further_p
        
    return aux_pos


