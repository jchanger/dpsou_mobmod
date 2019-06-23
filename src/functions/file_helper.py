""" Store functions to open and close files for the simulator

-----------------------
Created on Mar 17, 2017

@author: root
"""

import timing
import output

#  Param filename
#------------------
def param_file_gen(CONFIG):
    """ Creates the parameters file and save it """
    
    param_filename = CONFIG['output_folder']+"/"+str(CONFIG['timestamp'])+"_param"
    param_file = open(param_filename, "w+")
        
    return param_file    


#  Output file
#---------------
def out_file_gen(CONFIG):
    out_filename = CONFIG['output_folder']+"/"+str(CONFIG['timestamp'])+"_values"
    output_file = open(out_filename, "w+") 
    
    return output_file


# PSO values file
#-------------
def create_pso_vals(timestamp,output_folder):
    pso_filename = output_folder+"/"+str(timestamp)+"_pso_vals"
    pso_file = open(pso_filename, "w+") 
    
    return pso_file



# Files wrappers
#-----------------
def create_files(CONFIG):
    """ Create output files: param and drones positions """

    # Generate and save the parameters file
    param_file = param_file_gen(CONFIG)
  
    # Print on the screen the simulation parameters
    output.param_screen(CONFIG)

    # Creates and opens output file
    output_file = out_file_gen(CONFIG)
    
    return param_file, output_file


def close_files(param_file,output_file):
    param_file.close()
    output_file.close()
    

    