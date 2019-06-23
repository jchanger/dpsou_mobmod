"""
Created on Mar 13, 2017

@author: J. Sanchez-Garcia
"""


# TODO: together with the networking module, in the future this module can be programmed as part of a client-server
# where, the drones and victims send communications requests and the networking module act as a server. This 'communications'
# module simply redirects the drone communication request to the networking module. The aim of this 'communications' module 
# is to represent a common communications functions definitions that all drones may share in the future. However, for now it only
# calls to the networking module, which means that the networking module could be called from the drone class direcly. If no more 
# communication functions definitions are defined in the future, the drone class will call directly the networking module and this
# module could be deleted.


def send_receive(obj_i):    
    """ This function represents the communication channel of all the calls of the objects to the network module"""
    # The Network object is stored in each object and is called from them
    obj_i.network.comm_request(obj_i)


