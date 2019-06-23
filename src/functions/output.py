"""
Created on Jul 30, 2015

@author: J. Sanchez-Garcia
"""

import logging

# Global variable for printing decimals 
DECIMALS = 4
NUMBER_FORMAT = '%.'+str(DECIMALS)+'f'

logger = logging.getLogger(__name__)

# Parameters file
#----------------

def param_file_write(CONFIG, param_file, t_sim_TOTAL=None):

    if t_sim_TOTAL == None:
        # Writes the simulation initial parameters on the file
                
        param_file.write('Simulation parameters\n')
        param_file.write('---------------------\n')
        param_file.write('Input filename: '+CONFIG['input_file']+'\n')
        param_file.write('Output filename: '+param_file.name+'\n')
        param_file.write('\n')
        
        param_file.write('Scenario size (m): '+str(CONFIG['area_dimens'])+'\n')
        param_file.write('Number of clusters: '+str(len(CONFIG['clusters']))+'\n')
        for i in range(len(CONFIG['clusters'])):   
            param_file.write('\tCluster_'+str(i+1)+': origin '+str(CONFIG['clusters'][i][0])+'; dimension '+str(CONFIG['clusters'][i][1])+'\n')
        param_file.write('Number of nodes: '+str(CONFIG['nodes_amount'])+'\n')
        param_file.write('Duration (s): '+str(CONFIG['duration'])+'\n')
        param_file.write('\n')
        
        param_file.write('Number of Drones: '+str(CONFIG['drones_amount'])+'\n')
        param_file.write('Drones coverage (m): '+str(CONFIG['coverage'])+'\n')
        param_file.write('Drones maximum speed (m/s): '+str(CONFIG['max_speed'])+'\n')
        param_file.write('Drones initial distribution: '+CONFIG['init_distrib']+'\n')
        param_file.write('\n')
        
        param_file.write('Algorithm: '+CONFIG['algorithm']+'\n')
        
        if CONFIG['algorithm']=='pso':
            param_file.write('parameters:\n')
            param_file.write('\tinertia weight (start value,final value): '+str(CONFIG['pso_params'][0])+'\n')
            param_file.write('\tlocal best weight (start value,final value): '+str(CONFIG['pso_params'][1])+'\n')
            param_file.write('\tglobal best weight (start value,final value): '+str(CONFIG['pso_params'][2])+'\n')
            
            param_file.write('\tlocal best start time (s): '+str(CONFIG['pso_params'][3])+'\n')
            param_file.write('\tlocal best top time (s): '+str(CONFIG['pso_params'][4])+'\n')
            param_file.write('\tneighbors best start time (s): '+str(CONFIG['pso_params'][5])+'\n')
            param_file.write('\tneighbors best final time (s): '+str(CONFIG['pso_params'][6])+'\n')
        
        elif CONFIG['algorithm']=='lawn_mower': 
            param_file.write('parameters:\n')
            param_file.write('\tinter-drone distance (m): '+str(CONFIG['lawnmower_params'][0])+'\n')
            param_file.write('\tdistance to scenario edge (m): '+str(CONFIG['lawnmower_params'][1])+'\n')
            param_file.write('\tinter-region time (s): '+str(CONFIG['lawnmower_params'][2])+'\n')        
        
        param_file.flush()
        
        return param_file
    else:
        # Writes the simulation time on the file
        param_file.write('\nSimulation time (s): '+str(t_sim_TOTAL)+'\n')
        

# Main output values file 
#------------------------


# For writing the drone output file
def drone_write(drone_self, out_file):
    out_file.write('   drone_id='+str(drone_self.drone_id)+'\n')
    out_file.write('     drone_time='+str(drone_self.drone_time)+'\n')
    out_file.write('\tpos_x='+str(drone_self.position[0])+'\n')
    out_file.write('\tpos_y='+str(drone_self.position[1])+'\n')
    out_file.write('\tprev_pos='+str(drone_self.prev_position).replace(' ', '')+'\n')
    out_file.write('\tnext_pos='+str(drone_self.next_position).replace(' ', '')+'\n')
    
    out_file.write('\tnodes_in_range_total='+str(len(drone_self.nodes_in_range))+'\n')
    out_file.write('\tnodes_in_range='+str(drone_self.nodes_in_range).replace(' ', '')+'\n')
    out_file.write('\tdrones_in_range_total='+str(len(drone_self.drones_in_range))+'\n')
    out_file.write('\tdrones_in_range='+str(drone_self.drones_in_range).replace(' ', '')+'\n')
     
    out_file.write('\tlocal_best='+str(drone_self.local_best).replace(' ', '')+'\n')
    out_file.write('\tneighbor_best='+str(drone_self.neighbors_best).replace(' ', '')+'\n')
    
    out_file.write('\tnodes_discovered_total='+str(len(drone_self.nodes_discovered))+'\n')
    out_file.write('\t\tnode_id\t\tnode_pos\t\t\t\tdrone_discoverer\ttimestamp\n') 
    
    if drone_self.nodes_discovered:
        for n_discovered in drone_self.nodes_discovered:
            out_file.write('\t\t'+str(n_discovered[0]))
            out_file.write('\t\t'+str(n_discovered[1]))
            out_file.write('\t\t'+str(n_discovered[2]))
            out_file.write('\t\t\t'+str(n_discovered[3])+'\n')
    else:
        out_file.write('\t[]\n')
    
    # force writing buffer to actually write the file
    out_file.flush()
    
    

# Screen functions        
#-----------------
    
# Screen output at the beginning of the simulation
def param_screen(CONFIG,t_sim_TOTAL=None):
    
    if t_sim_TOTAL == None:
        
        logger.info('Simulation parameters:'\
                    +'\n\t Input filename: '+str(CONFIG['input_file'])\
                    +'\n\t Number of nodes: '+str(CONFIG['nodes_amount']) \
                    +'\n\t Duration (seconds): '+str(CONFIG['duration'])\
                    +'\n\t Number of Drones: '+str(CONFIG['drones_amount'])\
                    +'\n\t Drones max_speed: '+str(CONFIG['max_speed'])\
                    +'\n\t Initial distribution: '+str(CONFIG['init_distrib'])\
                    +'\n\t Area dimension: '+str(CONFIG['area_dimens'])\
                    +'\n\t Algorithm: '+str(CONFIG['algorithm'])\
                    +'\n\t Current iteration: '+str(CONFIG['current_iter']))
    else:
        logger.info('Simulation finished'\
                    +'\n\tAverage time spent in the algorithm: %.2f seconds' %(t_sim_TOTAL))
        

    