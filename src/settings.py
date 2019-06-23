""" Stores the input values for the sim_core with specific parameters

--------------------------
Created on Apr 4, 2017

@author: J. Sanchez-Garcia
"""

#  Arguments from CLI:
#----------------------
#     - input_file
#     - duration:
#            3600s = 1h; 1800s = 30 min; 900s  = 15 min; 600s = 10 min; 300s = 5 min
#     - nodes_amount: 
#            defined by the wml input file
#     - drones_amount: 
#            [1,9] for 'regular' initial distribution
#            no limitations for other cases
#     - coverage:
#            usually working with 250 meters
#     - drones maximum speed (m/s)
#            usually working with 15 m/s (equivalent to 55 km/h approx)
#     - drones initial distribution:
#            regular: drones start in formation within the scenario center
#            centered: drones start in the scenario center-point
#            random: drones start at randomly generated positions
#            corner_bottom_left: drones start at a small region in the bottom-left corner
#            corner_bottom_right: drones start at a small region in the right-left corner
#            corner_top_left: drones start at a small region in the top-left corner
#            corner_top_right: drones start at a small region in the top-right corner
#     - scenario area dimensions:
#            [x_meters,y_meters]
#     - movement algorithm:
#            random: drones decide random positions to go at each time step
#            linear: drones follow linear trajectories until they reach a border
#            pso: drones move like particles in the particle swarm optimization algorithm

# NOTE: variables with a comment that says 'DYNAMIC' are those that can be changed during the program execution


# SIMULATION PARAMETERS
#---------------------------

INPUT_FILE = ''
DURATION = 1370
FORCE_DURATION = 0                                                  # Force the previous DURATION over the lawn mower entire sweep duration
ALGO_DURATION = DURATION                                            # The duration of the algorithm, that is used for the algorithm phases calculations. 
                                                                    # If it has set a specific value this is independent of the time spent in one iteration duration. 
                                                                    # If we desire an entire simulation of full duration with the pso phases related to it, give it 
                                                                    # the value of DURATION
CLUSTERS = []                                                       # number of clusters, to be received from launcher
CLUSTERS_AMOUNT = 1
NODES_AMOUNT = 200                                                  # number of nodes in the scenarios
DRONES_AMOUNT = 6                                                   # number of drones
COVERAGE = 250                                                      # drones circular coverage (meters)
MAX_SPEED = 15                                                      # drones maximum speed (m/s)
INIT_DISTRIB = 'corner_bottom_left'                                 # initial positions of the drones 
AREA_DIMENS = [5000,5000]                                           # scenario dimensions (x,y)
ALGORITHM = 'pso'                                                   # movement algorithm
CURRENT_ITERATION = 0                                               # Number of simulation runs per each algorithm
INDIVIDUAL_CHARTS = 1                                               # Plot each iteration charts when it is equal to 1  

# Plot intermediate charts in the iterations, corresponding to each phase of the PSO algo.
    # 1st pos - flag, in which the 1= plots intermediate charts
    # 2nd pos - offset (the time added to lb_start and nb_start to calculate the timestamp in which the intermediate char will be plot)
INTERMEDIATE_CHARTS = (0, 200)                                             

# PSO parameters in the form (initial_value,final_value) (these not depending on other settings variables)
alpha = (1,)                        # inertia weight, its final_value comes from the values of local and neighbors_best
beta = (0,0.2)                      # local best weight: example (0,0.4)
gamma = (0,0.6)                     # neighbour best weight: example (0,0.6)
FORCE_INERTIA = 1                   # Maintains the inertia component if a drone did not discovered any victim, not was informed of victims by other drone                       

# Lawn_mower parameters (the ones that not depend on other settings variables)
lm_trajectories = [] # DYNAMIC: It will be filled if it is called from the 'launcher' module

# Cluster external region to determine drones belonging to a cluster
cluster_edgewidth = 50                  # in meters

# folder for storing the simulation results, will be modified by 'launcher'
CHARACTERIZATION_FOLDER = '' # DYNAMIC
MAIN_OUTPUT_FOLDER = '' # DYNAMIC 
OUTPUT_FOLDER = '' # DYNAMIC 

# timestamp of each sim_core. It will be filled in each 'sim_core' call
TIMESTAMP = '' # DYNAMIC

# List for storing the '_values' file of each sim_core
FILES = [] # DYNAMIC



# PARAMETERS GROUPING 
# -------------------

def update_CONFIG():
    
    # PSO parameters in the form (initial_value,final_value)
    lb_start = int(ALGO_DURATION/3)             # timestamp from which the local_best is considered
    lb_top = lb_start+10                        # timestamp from which the local_best effect is at its max value
    nb_start = 2*int(ALGO_DURATION/3)           # timestamp from which the neighbors_best is considered
    nb_top = nb_start+10                        # timestamp from which the neighbors_best effect is at its max value
    
    # Lawn mower parameters (these depending on other settings variables)
    interdrone_dist = COVERAGE
    dist_to_edge = COVERAGE-10
    # the time needed for the drones to move from the last position on a lawn_mover last point of a subsection and the next point where
    #the drone will start the next sweep (see the lawn_mower module for gaining more insights on this) 
    intersection_distance = interdrone_dist*(DRONES_AMOUNT-1)+dist_to_edge
    interregion_time = int(intersection_distance/MAX_SPEED)
    
    # PSO parameters in the form [initial_value,final_value]
    PSO_PARAMS = (alpha, beta, gamma, lb_start, lb_top, nb_start, nb_top, FORCE_INERTIA)
    
    # Lawn mower parameters
    LAWNMOWER_PARAMS = (interdrone_dist,dist_to_edge,interregion_time,lm_trajectories)
        
    
    # CONFIG is a dictionary to group parameters and ease the initial values passing to functions
    CONFIG = {'input_file':INPUT_FILE, 'nodes_amount':NODES_AMOUNT, 'duration':DURATION, 'f_duration':FORCE_DURATION, 'algo_duration':ALGO_DURATION,\
              'current_iter':CURRENT_ITERATION,'individual_charts':INDIVIDUAL_CHARTS,'intermediate_charts':INTERMEDIATE_CHARTS,'clusters':CLUSTERS,'clusters_amount':CLUSTERS_AMOUNT,\
              'drones_amount':DRONES_AMOUNT, 'coverage':COVERAGE,'max_speed':MAX_SPEED,'init_distrib':INIT_DISTRIB, 'area_dimens':AREA_DIMENS, 'algorithm':ALGORITHM,\
              'pso_params':PSO_PARAMS,'main_output_folder':MAIN_OUTPUT_FOLDER, 'output_folder':OUTPUT_FOLDER, 'timestamp':TIMESTAMP, 'lawnmower_params':LAWNMOWER_PARAMS,\
              'cluster_edgewidth':cluster_edgewidth, 'charac_output_folder':CHARACTERIZATION_FOLDER}
    
    return CONFIG
    
