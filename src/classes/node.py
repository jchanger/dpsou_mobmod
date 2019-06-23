"""
Created on Jun 3, 2016

@author: J. sanchez-garcia
"""

from functions import communications



class Node():
    
    def __init__(self, node_id, CONFIG, x_pos, y_pos, sim_network):
        
        self.node_id = node_id
        self.node_time = 0
        self.node_duration = CONFIG['duration']
        
        self.positions_list = zip(x_pos,y_pos)
        
        # stores the current position of the node
        self.position = [float(self.positions_list[0][0]),float(self.positions_list[0][1])] 
        
        # network emulator object
        self.network = sim_network


    def communicate(self):
        communications.send_receive(self)

    
    def move(self):
        # check if we are in the last position of the node positions list
        if self.node_time < self.node_duration-1:
            # updates the node position to the next timestamp one
            aux_x =  float(self.positions_list[self.node_time+1][0])
            aux_y =  float(self.positions_list[self.node_time+1][1])
            self.position = [aux_x,aux_y]
            
        else:
            # in the last timestep the nodes position is not updated as we run out of nodes positions
            pass
        
        
    def update_time(self):
        # update drone time
        self.node_time += 1 
        
    
    