"""
Created on Mar 14, 2017

@author: J. Sanchez-Garcia
"""

import copy
import logging
from math import ceil

logger = logging.getLogger(__name__)


def gen_lawnmower_traj(CONFIG):
    """ Generates a graph with the positions of the drones following lawn mower trajectories """
    
    trajectories = []
    interdrone_dist = CONFIG['lawnmower_params'][0]
    dist_to_edge = CONFIG['lawnmower_params'][1]
    interregion_time = CONFIG['lawnmower_params'][2]
    init_distrib = CONFIG['init_distrib']
    
    
    if init_distrib == 'corner_bottom_left':
        
        # Calculate horizontal rectangles (sub-regions)
        # only 1 dist_to_edge, which means that the next sub region line division comes from the last y_position of the border drone
        vertical_drone_block = float((CONFIG['drones_amount']-1)*interdrone_dist+dist_to_edge) 
        subregions_amount = int(ceil(CONFIG['area_dimens'][1]/vertical_drone_block))
    
        # Calculate the vertical positions in which trajectories will be, for each sub region starting with the bottom sub region
        for i in range(subregions_amount):
            subregion_division = i*vertical_drone_block # the first division is with i=0 and is the y=0 axis
            
            aux = []
            
            for j in range(CONFIG['drones_amount']):
                if j == 0:            
                    dist = subregion_division+dist_to_edge
                    aux.append(copy.copy(dist))
                else:
                    dist = dist + interdrone_dist
                    aux.append(copy.copy(dist))

            # for each sub region we have a list of lines
            trajectories.append(aux)
            
        # create the drones positions from each line (all x coordinates are the same for each line) 
        x_coords = range(0,CONFIG['area_dimens'][0],CONFIG['max_speed'])
        
        for i in range(len(trajectories)):
            for j in range(len(trajectories[i])):
                points = [[x,trajectories[i][j]] for x in x_coords]
                trajectories[i][j] = copy.deepcopy(points)  
                    
        # order coordinates according to the initial positions            
        # first sub region start counting at 0
        for i,subregion_i in enumerate(trajectories):
            # even sub regions are travelled from left to right 
            if i % 2 == 0:
                pass # do nothing, let the coordinates as they are
            else:
                # reverse the lists order
                for line_i in subregion_i:
                    line_i.reverse()

        # Reorder the trajectories in one list per drone
        traj_per_drone = []
        
        for drone_i in range(0,CONFIG['drones_amount']):
            aux = []
                
            for subregion_i in trajectories:
                aux.append(subregion_i[drone_i])
            
            # create only one list concatenating all sub regions per each drone
            concat = []
            
            for subregion_i in aux:
                for item in subregion_i:
                    concat.append(item)
                
                # Add outer points close to the end point of each sub region as an 'interregion_time'
                # The outer drones' trajectories are not implemented, just a waiting time in the last external scenario position.
                if concat[-1][0] >= CONFIG['area_dimens'][0]- CONFIG['max_speed']:
                    # end of this sub region is close to the max value of x axis
                    point = [concat[-1][0]+CONFIG['max_speed'],concat[-1][1]]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                else:
                    # end of this sub region is close to x=0
                    point = [concat[-1][0]-CONFIG['max_speed'],concat[-1][1]]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                    
            traj_per_drone.append(concat)  
        
        # Remove the latest interregion_time added, as after the last sweep the simulation terminates when reaching the border
        for i in range(interregion_time):
            for drone_i in traj_per_drone:
                del drone_i[-1]
    
    
    elif init_distrib == 'corner_bottom_right':
        
        # Calculate vertical rectangles (sub-regions)
        # only 1 dist_to_edge, which means that the next sub region line division comes from the last y_position of the border drone
        horizontal_drone_block = float((CONFIG['drones_amount']-1)*interdrone_dist+dist_to_edge) 
        subregions_amount = int(ceil(CONFIG['area_dimens'][0]/horizontal_drone_block))
        
        # Calculate the horizontal positions in which trajectories will be, for each sub region starting with the bottom sub region
        for i in range(subregions_amount):
            subregion_division = i*horizontal_drone_block # the first division is with i=0 and is the y=0 axis
            
            aux = []
            
            # taking into account that we start from the x maximum towards x=0
            for j in range(CONFIG['drones_amount']):
                if j == 0:            
                    dist = CONFIG['area_dimens'][0]-subregion_division-dist_to_edge
                    aux.append(copy.copy(dist))
                else:
                    dist = dist-interdrone_dist
                    aux.append(copy.copy(dist))

            # for each sub region we have a list of lines
            trajectories.append(aux)
        
        # create the drones positions from each line (all y coordinates are the same for each line) 
        y_coords = range(0,CONFIG['area_dimens'][1],CONFIG['max_speed'])
        
        for i in range(len(trajectories)):
            for j in range(len(trajectories[i])):
                points = [[trajectories[i][j],y] for y in y_coords]
                trajectories[i][j] = copy.deepcopy(points)  
                    
        # order coordinates according to the initial positions            
        # first sub region start counting at 0
        for i,subregion_i in enumerate(trajectories):
            # even sub regions are travelled from bottom to top 
            if i % 2 == 0:
                pass # do nothing, let the coordinates as they are
            else:
                # reverse the lists order
                for line_i in subregion_i:
                    line_i.reverse() 
        
        # Reorder the trajectories in one list per drone
        traj_per_drone = []
        
        for drone_i in range(0,CONFIG['drones_amount']):
            aux = []
                
            for subregion_i in trajectories:
                aux.append(subregion_i[drone_i])
            
            # create only one list concatenating all sub regions per each drone
            concat = []
            
            for subregion_i in aux:
                for item in subregion_i:
                    concat.append(item)
                
                # Add outer points close to the end point of each sub region as an 'interregion_time'
                # The outer drones' trajectories are not implemented, just a waiting time in the last external scenario position.
                if concat[-1][1] >= CONFIG['area_dimens'][1]- CONFIG['max_speed']:
                    # end of this sub region is close to the max value of x axis
                    point = [concat[-1][0],concat[-1][1]+CONFIG['max_speed']]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                else:
                    # end of this sub region is close to x=0
                    point = [concat[-1][0],concat[-1][1]-CONFIG['max_speed']]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                    
            traj_per_drone.append(concat)  
        
        # Remove the latest interregion_time added, as after the last sweep the simulation terminates when reaching the border
        for i in range(interregion_time):
            for drone_i in traj_per_drone:
                del drone_i[-1]
    
    elif init_distrib == 'corner_top_right':
     
        # Calculate horizontal rectangles (sub-regions)
        # only 1 dist_to_edge, which means that the next sub region line division comes from the last y_position of the border drone
        vertical_drone_block = float((CONFIG['drones_amount']-1)*interdrone_dist+dist_to_edge) 
        subregions_amount = int(ceil(CONFIG['area_dimens'][1]/vertical_drone_block))
    
        # Calculate the vertical positions in which trajectories will be, for each sub region starting with the bottom sub region
        for i in range(subregions_amount):
            subregion_division = i*vertical_drone_block # the first division is with i=0 and is the y=0 axis
            
            aux = []
            
            for j in range(CONFIG['drones_amount']):
                if j == 0:            
                    dist = CONFIG['area_dimens'][1]-subregion_division-dist_to_edge
                    aux.append(copy.copy(dist))
                else:
                    dist = dist - interdrone_dist
                    aux.append(copy.copy(dist))

            # for each sub region we have a list of lines
            trajectories.append(aux)
            
        # create the drones positions from each line (all x coordinates are the same for each line) 
        x_coords = range(CONFIG['area_dimens'][0],0,-CONFIG['max_speed'])
        
        for i in range(len(trajectories)):
            for j in range(len(trajectories[i])):
                points = [[x,trajectories[i][j]] for x in x_coords]
                trajectories[i][j] = copy.deepcopy(points)  
                    
        # order coordinates according to the initial positions            
        # first sub region start counting at 0
        for i,subregion_i in enumerate(trajectories):
            # even sub regions are travelled from left to right 
            if i % 2 == 0:
                pass # do nothing, let the coordinates as they are
            else:
                # reverse the lists order
                for line_i in subregion_i:
                    line_i.reverse()

        # Reorder the trajectories in one list per drone
        traj_per_drone = []
        
        for drone_i in range(0,CONFIG['drones_amount']):
            aux = []
                
            for subregion_i in trajectories:
                aux.append(subregion_i[drone_i])
            
            # create only one list concatenating all sub regions per each drone
            concat = []
            
            for subregion_i in aux:
                for item in subregion_i:
                    concat.append(item)
                
                # Add outer points close to the end point of each sub region as an 'interregion_time'
                # The outer drones' trajectories are not implemented, just a waiting time in the last external scenario position.
                if concat[-1][0] >= CONFIG['area_dimens'][0]- CONFIG['max_speed']:
                    # end of this sub region is close to the max value of x axis
                    point = [concat[-1][0]+CONFIG['max_speed'],concat[-1][1]]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                else:
                    # end of this sub region is close to x=0
                    point = [concat[-1][0]-CONFIG['max_speed'],concat[-1][1]]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                    
            traj_per_drone.append(concat)  
        
        # Remove the latest interregion_time added, as after the last sweep the simulation terminates when reaching the border
        for i in range(interregion_time):
            for drone_i in traj_per_drone:
                del drone_i[-1] 
     
    elif init_distrib == 'corner_top_left':

        # Calculate vertical rectangles (sub-regions)
        # only 1 dist_to_edge, which means that the next sub region line division comes from the last y_position of the border drone
        horizontal_drone_block = float((CONFIG['drones_amount']-1)*interdrone_dist+dist_to_edge) 
        subregions_amount = int(ceil(CONFIG['area_dimens'][0]/horizontal_drone_block))
        
        # Calculate the horizontal positions in which trajectories will be, for each sub region starting with the bottom sub region
        for i in range(subregions_amount):
            subregion_division = i*horizontal_drone_block # the first division is with i=0 and is the y=0 axis
            
            aux = []
            
            # taking into account that we start from the x maximum towards x=0
            for j in range(CONFIG['drones_amount']):
                if j == 0:            
                    dist = subregion_division + dist_to_edge
                    aux.append(copy.copy(dist))
                else:
                    dist = dist + interdrone_dist
                    aux.append(copy.copy(dist))

            # for each sub region we have a list of lines
            trajectories.append(aux)
        
        # create the drones positions from each line (all y coordinates are the same for each line) 
        y_coords = range(CONFIG['area_dimens'][1],0,-CONFIG['max_speed'])
        
        for i in range(len(trajectories)):
            for j in range(len(trajectories[i])):
                points = [[trajectories[i][j],y] for y in y_coords]
                trajectories[i][j] = copy.deepcopy(points)  
                    
        # order coordinates according to the initial positions            
        # first sub region start counting at 0
        for i,subregion_i in enumerate(trajectories):
            # even sub regions are travelled from bottom to top 
            if i % 2 == 0:
                pass # do nothing, let the coordinates as they are
            else:
                # reverse the lists order
                for line_i in subregion_i:
                    line_i.reverse() 
        
        # Reorder the trajectories in one list per drone
        traj_per_drone = []
        
        for drone_i in range(0,CONFIG['drones_amount']):
            aux = []
                
            for subregion_i in trajectories:
                aux.append(subregion_i[drone_i])
            
            # create only one list concatenating all sub regions per each drone
            concat = []
            
            for subregion_i in aux:
                for item in subregion_i:
                    concat.append(item)
                
                # Add outer points close to the end point of each sub region as an 'interregion_time'
                # The outer drones' trajectories are not implemented, just a waiting time in the last external scenario position.
                if concat[-1][1] >= CONFIG['area_dimens'][1]- CONFIG['max_speed']:
                    # end of this sub region is close to the max value of x axis
                    point = [concat[-1][0],concat[-1][1]+CONFIG['max_speed']]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                else:
                    # end of this sub region is close to x=0
                    point = [concat[-1][0],concat[-1][1]-CONFIG['max_speed']]
                    concat.append(point)
                    
                    if interregion_time > 1:
                        for i in range(1,interregion_time):
                            point_copy = copy.deepcopy(point)
                            concat.append(point_copy)
                    
            traj_per_drone.append(concat)  
        
        # Remove the latest interregion_time added, as after the last sweep the simulation terminates when reaching the border
        for i in range(interregion_time):
            for drone_i in traj_per_drone:
                del drone_i[-1]


    else:
        logger.error('The drones initial distribution is not within the available patterns')   

    return traj_per_drone



def lawnmower_algo(self_drone):
    """ Returns the next destination for a drone movement with the lawn mover by reading from the trajectory that the drone knows"""
    
    # checks if we run out of positions to return
    if self_drone.drone_time < len(self_drone.trajectory)-2:
        next = self_drone.trajectory[self_drone.drone_time+1]
    
    else: # case for the last timestamp to avoid running out of positions
        next = self_drone.trajectory[-1]
    
    return next
    