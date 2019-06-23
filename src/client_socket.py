""" Launches the a client for requesting a scenario from scenario_builder application

--------------------------
Created on May 9, 2017

@author: J. Sanchez-Garcia
"""

import logging
import socket
import time
import settings
import json
from _socket import SHUT_RDWR

HOST = 'localhost' # 127.0.0.1 can be also used
PORT = 10000
BUFFER_SIZE = 1024


def get_scenario(duration):
    """ Call to scenario_builder for generating a new scenario and receive the file where the new scenario is saved """
    
    logger = logging.getLogger(__name__)
        
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect the socket to the port where the server is listening
    server_address = (HOST,PORT)
    logger.info('Connecting to %s port %s' % server_address)
    sock.connect(server_address)
    
    
    # The protocol is implemented by sending the message lenght before sending the message itself
    CONFIG = settings.update_CONFIG()

    js_obj = {"duration":duration,"clusters_amount":str(CONFIG['clusters_amount']),'area_dimens':CONFIG['area_dimens']}
    message = json.dumps(js_obj)       
    data_size = len(message)  
    sock.sendall(str(data_size)) # Send data size 
    
    # wait for ACK
    data = sock.recv(BUFFER_SIZE)
    
    if data == 'ACK':
        sock.sendall(message) # send the actual message
        
        # wait for response size
        data_size = sock.recv(BUFFER_SIZE)
        data = sock.recv(int(data_size))
        
    else:        
        pass
    
    logger.info('Closing socket to %s port %s' % server_address)

    sock.shutdown(SHUT_RDWR)
    sock.close()
        
    return data

