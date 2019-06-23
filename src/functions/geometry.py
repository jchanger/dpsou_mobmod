""" Geometry-related functions compilation

This module presents a compilation of functions related with geometry operations in a 2 dimensional
plane in order to hide the difficult implementation of these operations in the calling functions. 
 
----------------------------

Created on Jul 31, 2015

@author: J. Sanchez-Garcia
"""

from math import sqrt
from math import pow


def get_distance(a,b):
    """Calculates the distance between the point 'a' and the point 'b'. 
    
    Calculates the distance between the point 'a' and the point 'b'.
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        One of the points of the vector. 
        
    b: list of floats in the form [x,y]
        One of the points of the vector.          
        
    Returns
    -------
    <no_name>: float
        The distance between the points 'a' and 'b'.
    """
    return abs(sqrt(pow(b[0]-a[0],2)+pow(b[1]-a[1], 2)))



def get_unitary_vector(a):
    """Calculates the unitary vector from the vector 'a'. 
    
    Calculates the unitary vector from the vector 'a'. 
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        The vector 'a' is defined as follows:
       -->
        A = [x,y] 
         
    Returns
    -------
    <no_name>: list of floats in the form [x,y]
        The unitary vector in its form [x_coordinate,y_coordinate] and with unitary magnitude.
    """
    magnitude = abs(sqrt(pow(a[0],2)+pow(a[1],2)))
    
    if magnitude == 0:
        magnitude = 0.0000001
    
    return [a[0]/magnitude,a[1]/magnitude] 



# Return the vector from one point a to another point b. The input points are in the format a=[x,y]
def get_vector(a,b):
    """Calculates the vector from two points. 
    
    Calculates the vector going from point 'a' towards point 'b'. Thus the vector has its origin at point 'a'
    and its end at point 'b'. We can say that the vector is defined as
        -->
        AB=[x_b-x_a,y_b-y_a]
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        One of the points of the vector. 
        
    b: list of floats in the form [x,y]
        One of the points of the vector. 
        
    Returns
    -------
    <no_name>: list of floats in the form [x,y]
        The vector definition in its form [x_coordinate,y_coordinate] and starting at the coordinate
        system origin.
    """
    return [b[0]-a[0],b[1]-a[1]]



# get the slope of a line between two points
def get_slope(a,b):
    """Calculates the slope of a line.
    
    Calculates the slope of a line which joins the point 'a' and the point 'b'.
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        One of the points of the line. 
        
    b: list of floats in the form [x,y]
        One of the points of the line. 
        
    Returns
    -------
    <no_name>: float
        The slope of the line.
    """
    x_increment = b[0]-a[0]
    
    if x_increment == 0:
        x_increment = 0.0000001
        
    return (b[1]-a[1])/x_increment


def apply_vectors_to_point(current_point, *vectors):
    """ Applies movement defined by a variable number of vectors to a point"""
    
    x = current_point[0]
    y = current_point[1]
    
    for vector in vectors:
        x = x+vector[0]
        y = y+vector[1] 
    
    final_point = [x,y]
     
    return final_point 
    

def add_vectors(current_point, *other_points):
    """ Calculate the point that yields from adding vectors defined by  a source point"""
    vectors = []
       
    for point in other_points:
        vectors.append(get_vector(current_point, point))
    
    final_pos = apply_vectors_to_point(current_point, *vectors)

    return final_pos


def get_points_distributed_line(end_1,end_2,dist_from_ends,points_amount):
    """ Calculate evenly distributed points over a line defined by two given points """
    
    if points_amount == 1:
        # generate first point at a specific distance from the corner
        closer_p,further_p =  get_closer_and_further_points_v2(end_1,end_2,dist_from_ends)
        
        p1 = closer_p
        
        points_list = []
        
        points_list.append(p1) # if there is only one drone we create a list with only one point
        
    else:
        # generate first point at a specific distance from the corner
        closer_p,further_p =  get_closer_and_further_points_v2(end_1,end_2,dist_from_ends)
        
        p1 = closer_p
        
        # generate second point at a specific distance from the corner
        closer_p,further_p =  get_closer_and_further_points_v2(end_2,end_1,dist_from_ends)
            
        p2 = closer_p
        
        # get separation between the first inertia positions of drones
        separation = get_distance(p1,p2)/(points_amount-1)
        
        points_list = []
        
        for i in range(points_amount):
            if i == 0: 
                points_list.append(p1)
            else:
                if i != points_amount-1:    
                    prev_p = points_list[-1]
                    
                    closer_p,further_p = get_closer_and_further_points_v2(prev_p,end_2,separation)
                    
                    points_list.append(closer_p)
                    
                else:
                    # last point
                    points_list.append(p2)
    
    return points_list
    

def get_y_cross(point_a, point_b, x_value):
    """Calculates the cross of a line with an 'y' axis (vertical line).
    
    Returns the cross with an 'y' axis defined by its x value (e.g. x=0 line). 
    Takes as input one point of a line and the line slope. This is used to 
    calculate the line equation in its form point-slope.
        
    Inputs
    ------
    point: list of floats in the form [x,y]
        One of the points of the line. This is used to calculate the line equation in its form point-slope.
        
    point_b: list of floats in the form [x,y]
        This second point is used to calculate the slope of the line
        
    Returns
    -------
    y_cross: float
        The value of the 'y' coordinate when the line crosses the 'y' axis.
        
    Notes
    -----
    This function uses  the equation:  'y = y1 + m * (x - x1)'
    
    which after solving for x = x_value yields:  y = y1 + m * (x_value - x1)
    """
    slope = get_slope(point_a, point_b)
    
    y_cross = point_a[1]+slope*(x_value-point_a[0]) 
    
    return y_cross



def get_x_cross(point_a, point_b, y_value):
    """Calculates the cross of a line with an 'x' axis (horizontal line).
    
    Returns the cross with an 'x' axis defined by its y value (e.g. y=0 line). 
    Takes as input one point of a line and the line slope. This is used to 
    calculate the line equation in its form point-slope.
        
    Inputs
    ------
    point_a: list of floats in the form [x,y]
        One of the points of the line. This is used to calculate the line equation in its form point-slope.
        
    point_b: list of floats in the form [x,y]
        This second point is used to calculate the slope of the line
        
    Returns
    -------
    x_cross: float
        The value of the 'x' coordinate when the line crosses the 'x' axis.
        
    Notes
    -----
    This function uses  the equation:  'y = y1 + m * (x - x1)'
    
    which after solving for y = y_value yields:  x = x1 + (y_value - y1) / m
    
    """
    slope = get_slope(point_a, point_b)
    
    x_cross = point_a[0]+(y_value-point_a[1])/slope 
    
    return x_cross


 
def intersection_line_circumference(a,slope,radius):
    """Calculates the two points of the intersection of a generic circumference and a line
    
    Calculates the two points of the intersection of a generic circumference and a line and returns 
    these two points.
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        One of the points of the line. This is used to calculate the line equation in its form point-slope.
        This points is the position of the drone which is moving and thus is also the center of the circumference.
    
    slope: float
        The slope of the line.
        
    radius: float
        The radius of the circumference.
        
    Returns
    -------
    point_1: list of floats in the form [x,y]
        One of the two points from the intersection between the circumference and the line.
    
    point_2: list of floats in the form [x,y]
        One of the two points from the intersection between the circumference and the line.   
    """
    # We calculate the two possible x,y coordinates at a distance 'radius' of this current position
    if sqrt(1+(slope**2)) == 0:
        x = a[0]+(radius/0.0000001)
    else:
        x = a[0]+(radius/sqrt(1+(slope**2)))
    y = slope*(x-a[0])+a[1]
    point_1 = [x,y]

    if sqrt(1+(slope**2)) == 0:    
        x = a[0]-(radius/0.0000001)
    else:
        x = a[0]-(radius/sqrt(1+(slope**2)))
    y = slope*(x-a[0])+a[1]
    point_2 = [x,y]

    return point_1,point_2



def get_closer_and_further_points_v2(a, b, radius):
    """VERSION 2: Calculates the two points of the intersection of the circumference and the movement line
    
    Function that calculates the two possible points that are the intersection between a line that
    is defined by two points (a source and a destination or reference) and a circumference. The circumference
    represents the distance to move along the line between the two points. The two points can be considered as
    the position of a drone and the destination point that defines the movement direction of the drone.
    
    This function integrates the calculations of the slope and the distance between points within the function
    itself. It only needs as inputs the two points (source and destination) and the radius of the circumference.
        
    Inputs
    ------
    a: list of floats in the form [x,y]
        Receives one of the source point which is the current position of the drone which is calculating 
        its next movement.
    
    b: list of floats in the form [x,y]
        The position of the reference or next destination.
        
    radius: float
        The magnitude of the movement to be applied to the drone which is moving, i.e. the distance to move 
        along the line that join the points a and b. This describes the radius of the circumference for the
        intersection.
    
    Returns
    -------
    closer_p: list of floats in the form [x,y]
        The closest point to the destination point or point b, selected from the two intersections between the circumference
        and the line that joins the point a and the point b.
    
    further_p: list of floats in the form [x,y]
        The farthest point to the destination point or point b selected from the two intersections between the circumference
        and the line that joins the point a and the point b.
    """
    slope = get_slope(a, b)
    distance = get_distance(a, b)
    
    # Calculates the two intersection points
    next_p_plus,next_p_minus = intersection_line_circumference(a, slope, radius)
    dist_plus = get_distance(b, next_p_plus)
    
    # We determine which of the points is closer and which one is further of the drone with which we calculate forces
    if dist_plus >= distance:
        # next_p_plus is further from the point 'b'
        further_p = next_p_plus 
        closer_p = next_p_minus 
    else:
        # next_p_minus is further from the point 'b'
        further_p = next_p_minus 
        closer_p = next_p_plus
        
    return closer_p,further_p



def is_out_area(a, area_dimens):
    """ Check if point a is out of the area defined by area_dimens
    
    Check if point a is out of the area defined by area_dimens. It considers that a point
    is out of the area if IT HAS CROSSED the border, i.e. if it is IN a border the point
    is still considered as within the area. This means that we check this condition with
    strict inequalities (not >= or <=).
    
    Inputs
    ------
    a: list of floats in the form [x,y]
        Receives the point to check if is out the area.
         
    area_dimens: list of floats in the form [x,y]
        Receives the maximum values of the axis x and y. The area is defined as a square area starting at
        (0,0) and going to the corner (area_dimens[0],area_dimens[1])
        
     Returns
    -------
    out: binary variable
        1: the point a is out of the area
        0: the point is within the area
        
    """
    out = 0
    
    # The x axis limits x=0 and x=area_dimens[0]
    if a[0] < 0 or a[0] > area_dimens[0]:
        out = 1
    # The y axis limits y=0 and y=area_dimens[1]
    elif a[1] < 0 or a[1] > area_dimens[1]:
        out = 1
        
    return out
    
    
def is_within_area(pos,origin,dimension,margin):
    """ Checks if a certain point is within a specific area """
    
    if pos[0] > origin[0]-margin and pos[1] > origin[1]-margin and \
    pos[0] < origin[0]+dimension[0]+margin and pos[1] < origin[1]+dimension[1]+margin:
        return 1
    else:
        return 0
    
    