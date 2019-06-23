"""
Created on Mar 14, 2017

@author: J. Sanchez-Garcia
"""

from functions import geometry
from random import randint
from math import sqrt


# Initial drones positions functions definitions
#-----------------------------------------------

def init_pos_centroid(centroid,num_points,dist):
    """ Calculates the initial position of the drones from the centroid of the scenario
    
    Calculates the initial position of the drones from the centroid of the scenario and the number 
    of drones used in the simulation.
    
    Input
    -----
    centroid: tuple of floats 
        The scenario centroid as a tuple centroid = (cx,cy)
    
    num_points: integer 
        The number of drones
        
    dist: float
        The distance to keep between some of the points (e.g. in a triangle means the
        the triangle's sides
    
    Returns
    -------
    positions: list of tuples
        List of tuples in which each tuple is a initial position for one drone. The first tuple
        corresponds to drone_0, the second to drone_1 and so on and so forth.

    Notes
    -----
    - The letter 'G' is used in some comments to represent the controid G: (Gx,Gy) 
    """
    if num_points == 1:
        # If only one drone, its initial position will be the scenario centroid
        d_0 = [None]*2
        
        d_0[0] = centroid[0]
        d_0[1] = centroid[1]
        
        return d_0[0],d_0[1]
    
    elif num_points == 2: # Line configuration
        #
        #    A:d_0 ----- G ----- B:d_1
        #
        
        d_0 = [None]*2
        d_1 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-(dist/2)
        d_1[0] = centroid[0]+(dist/2)
        
        # y coordinates for all drones
        d_0[1] = centroid[1]
        d_1[1] = centroid[1]
        
        coords = zip(d_0,d_1)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 3: # Triangle configuration
        # centroid is a tuple (inmutable object) thus if we would do 'c=centroid' we won't we changing 
        # 'centroid' values, we will change only 'c' and 'centroid' will maintain its value. The problem
        # is with mutable objects
        
        # The correspondence with the triangle vertices are
        #        A: d_0
        #        /\
        #       /__\
        #  C:d_2    B: d_1
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]
        d_1[0] = centroid[0]+(dist/2)
        d_2[0] = centroid[0]-(dist/2)
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+(dist*(1/sqrt(3)))
        d_1[1] = centroid[1]-(dist*sqrt(1/12))
        d_2[1] = centroid[1]-(dist*sqrt(1/12))
        
        coords = zip(d_0,d_1,d_2)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 4: # Square configuration
        # The correspondence with the square vertices are
        #        
        #     A: d_0 ___ B: d_1
        #           |   |
        #           |___|
        #      D:d_3     C: d_2    
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-(dist/2)
        d_1[0] = centroid[0]+(dist/2)
        d_2[0] = centroid[0]+(dist/2)
        d_3[0] = centroid[0]-(dist/2)
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+(dist/2)
        d_1[1] = centroid[1]+(dist/2)
        d_2[1] = centroid[1]-(dist/2)
        d_3[1] = centroid[1]-(dist/2)
        
        coords = zip(d_0,d_1,d_2,d_3)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 5: # Star configuration
        # The correspondence with the star vertices are
        #        
        #     A: d_0 ___________B: d_1
        #           |           |
        #           |           |
        #           |     x     |
        #           |    G:d_4  |
        #           |___________|
        #      D:d_3             C: d_2    
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        d_4 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-(dist/2)
        d_1[0] = centroid[0]+(dist/2)
        d_2[0] = centroid[0]+(dist/2)
        d_3[0] = centroid[0]-(dist/2)
        d_4[0] = centroid[0]
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+(dist/2)
        d_1[1] = centroid[1]+(dist/2)
        d_2[1] = centroid[1]-(dist/2)
        d_3[1] = centroid[1]-(dist/2)
        d_4[1] = centroid[1]
        
        coords = zip(d_0,d_1,d_2,d_3,d_4)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 6: # Rectangle configuration
        # The correspondence with the star vertices are
        #        
        #    A: d_0 x___________x B: d_1
        #           |           |
        #           |           |
        #           |           |
        #   F: d_5  x     .G    x C: d_2
        #           |           |
        #           |           |
        #           |___________|
        #    E:d_4  x           x D: d_3    
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        d_4 = [None]*2
        d_5 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-(dist/2)
        d_1[0] = centroid[0]+(dist/2)
        d_2[0] = centroid[0]+(dist/2)
        d_3[0] = centroid[0]+(dist/2)
        d_4[0] = centroid[0]-(dist/2)
        d_5[0] = centroid[0]-(dist/2)
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+dist
        d_1[1] = centroid[1]+dist
        d_2[1] = centroid[1]
        d_3[1] = centroid[1]-dist
        d_4[1] = centroid[1]-dist
        d_5[1] = centroid[1]
        
        coords = zip(d_0,d_1,d_2,d_3,d_4,d_5)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 7:
        # The correspondence with the star vertices are
        #        
        #    A: d_0 x___________x B: d_1
        #           /           \
        #          /             \
        #         /               \
        # F:d_5  x        x G      x C: d_2
        #         \      H:d_6    /
        #          \             /
        #           \ __________/
        #     E:d_4  x          x D: d_3    
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        d_4 = [None]*2
        d_5 = [None]*2
        d_6 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-(dist/2)
        d_1[0] = centroid[0]+(dist/2)
        d_2[0] = centroid[0]+dist
        d_3[0] = centroid[0]+(dist/2)
        d_4[0] = centroid[0]-(dist/2)
        d_5[0] = centroid[0]-dist
        d_6[0] = centroid[0]
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+((dist/2)*sqrt(3))
        d_1[1] = centroid[1]+((dist/2)*sqrt(3))
        d_2[1] = centroid[1]
        d_3[1] = centroid[1]-((dist/2)*sqrt(3))
        d_4[1] = centroid[1]-((dist/2)*sqrt(3))
        d_5[1] = centroid[1]
        d_6[1] = centroid[1]
        
        coords = zip(d_0,d_1,d_2,d_3,d_4,d_5,d_6)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    elif num_points == 8:
        # The correspondence with the star vertices are
        #            
        #                B: d_1
        # A: d_0 x________x________x C: d_2
        #        |        |        |
        #        |        |        |
        #        |        |        |
        #  H:d_6 x--------x G------x D: d_3
        #         \      I:d_7    /
        #          \             /
        #           \ __________/
        #     F:d_5  x          x E:d_4     
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        d_4 = [None]*2
        d_5 = [None]*2
        d_6 = [None]*2
        d_7 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-dist
        d_1[0] = centroid[0]
        d_2[0] = centroid[0]+dist
        d_3[0] = centroid[0]+dist
        d_4[0] = centroid[0]+(dist/2)
        d_5[0] = centroid[0]-(dist/2)
        d_6[0] = centroid[0]-dist
        d_7[0] = centroid[0]
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+dist
        d_1[1] = centroid[1]+dist
        d_2[1] = centroid[1]+dist
        d_3[1] = centroid[1]
        d_4[1] = centroid[1]-((dist/2)*sqrt(3))
        d_5[1] = centroid[1]-((dist/2)*sqrt(3))
        d_6[1] = centroid[1]
        d_7[1] = centroid[1]
        
        coords = zip(d_0,d_1,d_2,d_3,d_4,d_5,d_6,d_7)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    
    elif num_points == 9:
        # The correspondence with the star vertices are
        #            
        #                B: d_1
        # A: d_0 x________x________x C: d_2
        #        |        |        |
        #        |        |        |
        #        |        |        |
        #  I:d_7 x--------x G------x D: d_3
        #        |       J:d_8     |
        #        |        |        |
        #        |________|________|
        #  H:d_6 x        x        x E:d_4     
        #                 F:d_5
                        
        d_0 = [None]*2
        d_1 = [None]*2
        d_2 = [None]*2
        d_3 = [None]*2
        d_4 = [None]*2
        d_5 = [None]*2
        d_6 = [None]*2
        d_7 = [None]*2
        d_8 = [None]*2
        
        # x coordinates for all drones
        d_0[0] = centroid[0]-dist
        d_1[0] = centroid[0]
        d_2[0] = centroid[0]+dist
        d_3[0] = centroid[0]+dist
        d_4[0] = centroid[0]+dist
        d_5[0] = centroid[0]
        d_6[0] = centroid[0]-dist
        d_7[0] = centroid[0]-dist
        d_8[0] = centroid[0]
        
        # y coordinates for all drones
        d_0[1] = centroid[1]+dist
        d_1[1] = centroid[1]+dist
        d_2[1] = centroid[1]+dist
        d_3[1] = centroid[1]
        d_4[1] = centroid[1]-dist
        d_5[1] = centroid[1]-dist
        d_6[1] = centroid[1]-dist
        d_7[1] = centroid[1]
        d_8[1] = centroid[1]
        
        coords = zip(d_0,d_1,d_2,d_3,d_4,d_5,d_6,d_7,d_8)
        coords_x = list(coords[0])
        coords_y = list(coords[1])
        
        return coords_x,coords_y
    
    


def init_drone_pos(CONFIG):
    """Creates a list with the drones initial positions according to different configurations
    
    Creates a list with the drones initial positions according to different configurations. These
    configurations may be:
        regular: in formation, positioning the drones at the vertices (ONLY UP TO 9 DRONES)
        centered: all the drones start at the center of the scenario
        random: the drones start at random positions within the scenario
        corner_bottom_left: the drones start at the corner [0,0]
        corner_bottom_right: the drones start at the corner [area_dimension[0],0]
        corner_top_left: the drones start at the corner [0,area_dimension[1]]
        corner_top_right: the drones start at the corner [area_dimension[0],area_dimension[1]]
    """

    drones_amount = CONFIG['drones_amount']
    mode = CONFIG['init_distrib']
    area_dimens = CONFIG['area_dimens']
    coverage = CONFIG['coverage']
    
    
    init_x = []
    init_y = []
    
    centroid = [float(area_dimens[0]/2),float(area_dimens[1]/2)]
    
    array_xy = []
    
    # The regular mode is designed for a maximum number of 9 drones. This can be extended in the future
    if mode == 'regular':
        init_x[:] = init_pos_centroid(centroid, drones_amount, coverage/4)[0]
        init_y[:] = init_pos_centroid(centroid, drones_amount, coverage/4)[1]
        
    elif mode == 'centered':
        for i in range(drones_amount):
            init_x.append(centroid[0]) 
            init_y.append(centroid[1])
        
    elif mode == 'random':
        # The random positions are chosen from a squared area of (area_dimens/3 x area_dimens/3)
        # Using a third of the width of the scenario it has been a decision taken but other 
        # quantities could be chosen 1/2,1/4...
        for i in range(drones_amount):
            init_x.append(randint(float(area_dimens[0]/3),float(2*area_dimens[0]/3)))
            init_y.append(randint(float(area_dimens[0]/3),float(2*area_dimens[0]/3)))

    elif mode == 'corner_bottom_left':
        # select a random position close to a corner 
        for i in range(drones_amount):
            init_x.append(randint(0, coverage))
            init_y.append(randint(0, coverage))        
    
    elif mode == 'corner_bottom_right':
        # select a random position close to a corner
        for i in range(drones_amount):
            init_x.append(area_dimens[0]-randint(0, coverage))
            init_y.append(randint(0, coverage))
    
    elif mode == 'corner_top_left':
        # select a random position close to a corner
        for i in range(drones_amount):
            init_x.append(randint(0, coverage))
            init_y.append(area_dimens[1]-randint(0, coverage))
            
    elif mode == 'corner_top_right':
        # select a random position close to a corner
        for i in range(drones_amount):
            init_x.append(area_dimens[0]-randint(0, coverage))
            init_y.append(area_dimens[1]-randint(0, coverage))
            
    else:
        # in the case we do not select a valid initial_position model this is checked in 'inputs' module
        pass
    
    array_xy.append(init_x)
    array_xy.append(init_y)
        
    return array_xy


def get_first_inertia(CONFIG):
    """ Calculate the first inertia points to be evenly distributed somehow over the scenario diagonal line 
    
    Parameters
    ----------
    CONFIG : dictionary
        The configuration parameters dictionary.

    Returns
    -------
    list
        List containing the points that defines the drones direction
        for the inertia stage at the first part of the simulation.
    
    """
    
    if CONFIG['init_distrib'] == 'corner_bottom_left':
        corner_1 = (0,CONFIG['area_dimens'][1])
        corner_2 = (CONFIG['area_dimens'][0],0)
        
        points_list = geometry.get_points_distributed_line(corner_1,corner_2,CONFIG['coverage'],CONFIG['drones_amount'])     
            
    elif CONFIG['init_distrib'] == 'corner_top_right':
        corner_1 = (0,CONFIG['area_dimens'][1])
        corner_2 = (CONFIG['area_dimens'][0],0)
        
        points_list = geometry.get_points_distributed_line(corner_1,corner_2,CONFIG['coverage'],CONFIG['drones_amount'])
    
    elif CONFIG['init_distrib'] == 'corner_top_left':
        # other corners
        corner_1 = (0,0)
        corner_2 = (CONFIG['area_dimens'][0],CONFIG['area_dimens'][1])
        
        points_list = geometry.get_points_distributed_line(corner_1,corner_2,CONFIG['coverage'],CONFIG['drones_amount'])
    
    else:
        # other corners
        corner_1 = (0,0)
        corner_2 = (CONFIG['area_dimens'][0],CONFIG['area_dimens'][1])
        
        points_list = geometry.get_points_distributed_line(corner_1,corner_2,CONFIG['coverage'],CONFIG['drones_amount'])
            
    return points_list

