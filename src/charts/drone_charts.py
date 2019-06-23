""" Function definitions for plotting results

--------------------------
Created on Apr 5, 2017

@author: J. Sanchez-Garcia
"""

import sys
import copy
import logging
import subprocess
import matplotlib   
import networkx as nx
from matplotlib.testing.jpl_units.Duration import Duration
from IPython.core.magic_arguments import argument
# from pandas._libs.index import Timestamp
matplotlib.use('Agg')   # for running the script on the server without graphics system up

import matplotlib.pylab as plt
# import matplotlib.colors as colors
from functions import parsers
from functions import geometry
from itertools import cycle

logger = logging.getLogger(__name__)


def plot_settings():
    """ Creates lists with available line markers and colors for easing plotting """
    
    #colors = matplotlib.colors.cnames.keys() # not used as some colors are very clear for a blank background
    colors = ['green','blue','red','cyan','magenta','black','orange','maroon','lime','gold','crimson','deeppink','purple','olive']
    
    colors_cycler = cycle(colors)
    
    return colors_cycler
 
 
def plot_discovered(discovered, CONFIG): 
    """ Plot discovered nodes per drone during all the simulation time """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for drone_i in range(len(discovered)):
        ax.plot(range(CONFIG['duration']),discovered[drone_i],label='drone '+str(drone_i),color=next(colors_cycler))
        
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Discovered Nodes")
    ax.set_title("Discovered nodes per time\n\n")
    x_dimension = CONFIG['duration']
    ax.set_xlim([0,x_dimension])
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_discovered.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    
    

def plot_acc_discovered(accum_discovered, CONFIG):
    """ Plot accumulated discovered nodes for all drones per time stamp """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    
    ax.plot(range(CONFIG['duration']),accum_discovered,color=next(colors_cycler))
        
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Number of nodes (accumulated)")
    ax.set_title("Discovered nodes per time (accumulated)\n\n")
    x_dimension = CONFIG['duration']
    ax.set_xlim([0,x_dimension])
    ax.grid(True)
    
    # text
    percent = float(accum_discovered[-1])*100/CONFIG['nodes_amount']
    percent_text = 'Total discovered: '+format(percent, '.2f')+' %'    
    total_text = 'Total: '+str(accum_discovered[-1])+' nodes'
    ax.text(x_dimension+7,0,percent_text+'\n'+total_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_discovered_acc.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')


def plot_discovered_per_time(total_discovered_time, CONFIG):
    """ Plot discovered nodes for all drones per time stamp """
     
    colors_cycler = plot_settings() 
     
    fig = plt.figure()
    ax = fig.add_subplot(111)
         
    ax.plot(range(CONFIG['duration']),total_discovered_time,color=next(colors_cycler))
         
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Discovered nodes per time\n\n")
    x_dimension = CONFIG['duration']
    ax.set_xlim([0,x_dimension])
    ax.grid(True)
     
    # text
    percent = float(total_discovered_time[-1])*100/CONFIG['nodes_amount']
    percent_text = 'Total discovered: '+format(percent, '.2f')+' %'    
    total_text = 'Total: '+str(total_discovered_time[-1])+' nodes'
    ax.text(x_dimension+7,0,percent_text+'\n'+total_text)
     
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_discovered_per_time.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')


def plot_discovery_rate(accum_discovered,CONFIG):
    """ Plot discovery rate """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # finite differentiation method
    derivative = []
    
    for i in range(len((accum_discovered))):
        if i != len(accum_discovered)-1:
            diff = accum_discovered[i+1] - accum_discovered[i]
            derivative.append(diff)
        else:
            # not defined for the last element of the list
            pass
    
    # reduce the x axis to 'duration'-1 because the derivative is not defined for the last value
    x_values = range(CONFIG['duration'])
    del x_values[-1]
    
    ax.plot(x_values,derivative,color=next(colors_cycler))
        
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Discovery rate")
    ax.set_title("Nodes discovery rate\n\n")
    ax.grid(True)
    ax.set_xlim([0,CONFIG['duration']])
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_discovery_rate.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_acc_quartile(accum_discovered,CONFIG):
    """ Plot accumulated discovered nodes quartile """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    q_1 = int(CONFIG['nodes_amount']/4)
    q_2 = int(CONFIG['nodes_amount']/2)
    q_3 = int(3*CONFIG['nodes_amount']/4)
    
    values = [None,None,None,None]
    
    for i,val in enumerate(accum_discovered):
        if  val >= q_1 and values[0] == None:
            values[0] = i
        if  val >= q_2 and values[1] == None:
            values[1] = i
        if  val >= q_3 and values[2] == None:
            values[2] = i
        if  val >= CONFIG['nodes_amount'] and values[3] == None:
            values[3] = i
    
    for i,val in enumerate(values):
        if val == None:
            values[i] = CONFIG['duration']
    
    y_vals = values
    x_vals = range(len(y_vals))
    width = 0.8
    
    ax.bar(x_vals,y_vals,width,color='green')
        
    ax.set_xlabel("Percentage of nodes discovered")
    ax.set_ylabel("Time (s)")
    ax.set_title("Time up to discovery\n\n")
    ax.grid(True)
    
    xtick_pos = x_vals
    ax.set_xticks(xtick_pos)
    ax.set_xticklabels(('25 %','50 %','75 %','100 %'))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_acc_quartile.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    
    
    
def plot_local_best(total_lb,pos_lb, CONFIG):
    """ Plot the local best per drone during all the simulation time """
    
    colors_cycler = plot_settings()
    fig_1 = plt.figure()
    splot_1 = fig_1.add_subplot(111)
    
    # Plot the local best positions
    for drone_i in range(len(pos_lb)):
        drone_pos = pos_lb[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        curr_color = next(colors_cycler)
        
        splot_1.plot(x_pos,y_pos,marker='+',label='drone '+str(drone_i),color=curr_color,linestyle='--')
        splot_1.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        splot_1.plot(x_pos[0],y_pos[0],marker='.',color=curr_color)
        
    splot_1.set_xlabel("x coordinate (m)")
    splot_1.set_ylabel("y coordinate (m)")
    splot_1.set_title("Drones' local best positions\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    splot_1.axis([0,x_dimension,0,y_dimension])
    splot_1.grid(True)
    splot_1.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig_1.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_localbest_pos.svg',format='svg',dpi=1200,bbox_inches='tight')
    
    
    colors_cycler = plot_settings() # called again to print with the same color-linestyle sequence for each drone
    fig_2 = plt.figure()
    splot_2 = fig_2.add_subplot(111)
    
    # Plot the nodes discovered in the local best positions
    for drone_i in range(len(total_lb)):
        splot_2.plot(range(CONFIG['duration']),total_lb[drone_i],label='drone '+str(drone_i),color=next(colors_cycler))
        
    splot_2.set_xlabel("Time(s)")
    splot_2.set_ylabel("Discovered nodes")
    splot_2.set_title("Discovered nodes in local best positions\n\n")
    x_dimension = CONFIG['duration']
    splot_2.set_xlim([0,x_dimension])
    splot_2.grid(True)
    splot_2.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig_2.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_localbest_total.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    
    
def plot_neighbor_best(discoverer,total_nb,pos_nb,CONFIG):
    """ Plot the neighbors best per drone during all the simulation time"""
    
    colors_cycler = plot_settings()
    
    fig_1 = plt.figure()
    splot_1 = fig_1.add_subplot(111)
    
    # Plot the neighbor best positions
    for drone_i in range(len(pos_nb)):
        drone_pos = pos_nb[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        curr_color = next(colors_cycler)
        
        splot_1.plot(x_pos,y_pos,marker='+',label='drone '+str(drone_i),color=curr_color,linestyle='--')
        splot_1.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        splot_1.plot(x_pos[0],y_pos[0],marker='.',color=curr_color)
        
    splot_1.set_xlabel("x coordinate (m)")
    splot_1.set_ylabel("y coordinate (m)")
    splot_1.set_title("Drones' neighbors best positions\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    splot_1.axis([0,x_dimension,0,y_dimension])
    splot_1.grid(True)
    splot_1.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig_1.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_neighbest_pos.svg',format='svg',dpi=1200,bbox_inches='tight')

    colors_cycler = plot_settings() # called again to print with the same color-linestyle sequence for each drone
    fig_2 = plt.figure()
    splot_2 = fig_2.add_subplot(111)
    
    # Plot the nodes discovered in the local best positions
    for drone_i in range(len(total_nb)):
        splot_2.plot(range(CONFIG['duration']),total_nb[drone_i],label='drone '+str(drone_i),color=next(colors_cycler))            
        
    splot_2.set_xlabel("Time(s)")
    splot_2.set_ylabel("Discovered nodes")
    splot_2.set_title("Discovered nodes in neighbors best positions\n\n")
    x_dimension = CONFIG['duration']
    splot_2.set_xlim([0,x_dimension])
    splot_2.grid(True)
    splot_2.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig_2.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_neighbest_total.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_final_neighbor_best(pos_nb,CONFIG):
    """ Plot the final neighbors best for each drone """
    
    colors_cycler = plot_settings()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # Plot the neighbor best positions
    for drone_i in range(len(pos_nb)):
        drone_pos = pos_nb[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        curr_color = next(colors_cycler)
        
        ax.scatter(x_pos[-1],y_pos[-1],label='drone '+str(drone_i),marker='x',color=curr_color)
        
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Drones' final neighbors best positions\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.axis([0,x_dimension,0,y_dimension])
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_neighbest_pos_final.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    
    
def plot_trajectory(pos_drones,CONFIG):
    """ Plot the drones' trajectories during all the simulation time """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        curr_color = next(colors_cycler)
        ax.plot(x_pos,y_pos,label='drone '+str(drone_i),color=curr_color,linestyle='--')
        ax.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        ax.plot(x_pos[0],y_pos[0],marker='.',color=curr_color)
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Drones' trajectories\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_trajectories.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_final_positions(pos_drones,CONFIG):
    """ Plot the drones' final positions """
    
    colors_cycler = plot_settings() 
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    text = []
    
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        curr_color = next(colors_cycler)
        ax.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        
        aux_text = (x_pos[-1],y_pos[-1])
        text.append(aux_text)
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Drones' final positions\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.grid(True)
    
    # text
    all_text = 'Final positions:'
    
    for i in range(len(text)):
        dr_text = '\nDrone '+str(i)+': ['+format(text[i][0], '.2f')+','+format(text[i][1], '.2f')+']'
        all_text = all_text+dr_text
    
    ax.text(x_dimension+20,0,all_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_final_positions.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    
        
    
def plot_update_time(nodes_per_time, total_nodes,CONFIG):
    """ Plot the nodes update time """   
    
    # nodes amount per time
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # generate the columns locations
    bars_loc = range(CONFIG['duration']) 
    
    ax.bar(bars_loc, nodes_per_time, width=2, edgecolor='green', color='green') 
    
    ax.set_xlabel("Time since last connection (s)")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Number of nodes discovered 't' seconds ago\n\n")
    x_dimension = CONFIG['duration']
    ax.set_xlim([-20,x_dimension])
    y_min_val = max(nodes_per_time)*0.05 # patch for making lawn_mower and pso charts with similar distance below y=0 line
    ax.set_ylim(ymin=-y_min_val) # avoids the text to appear below the figure when the y axis does not have values in '0'
    ax.grid(True)
    
    # text
    percent = float(total_nodes)*100/CONFIG['nodes_amount']
    percent_text = 'Total discovered: '+format(percent, '.2f')+' %'    
    total_text = 'Total: '+str(int(total_nodes))+' nodes'
    ax.text(x_dimension+7,-y_min_val,percent_text+'\n'+total_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_update.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_update_time_interval(nodes_per_time_t, interval_list, total_nodes_t, CONFIG):
    """ Plot the nodes update time tables within a folder"""   
    
    interval_folder = CONFIG['output_folder']+'/update_intervals'
    command = ['mkdir',interval_folder]
    subprocess.call(command)
    
    interval_iter=iter(interval_list)
    
    for i in range(len(nodes_per_time_t)):
        
        total_nodes=total_nodes_t[i]                  
        nodes_per_time = nodes_per_time_t[i]
        
        while len(nodes_per_time) < CONFIG['duration']:
            nodes_per_time.append(0)
        
        interval=next(interval_iter)
        
        # nodes amount per time
        fig = plt.figure()
        ax = fig.add_subplot(111)
        
        # generate the columns locations
        bars_loc = range(CONFIG['duration']) 
        
        ax.bar(bars_loc, nodes_per_time, width=2, edgecolor='green', color='green') 
        
        ax.set_xlabel("Time since last connection (s)")
        ax.set_ylabel("Number of nodes")
        ax.set_title("Nodes discovered 't' seconds ago - interval: "+str(interval)+"\n\n")
        x_dimension = CONFIG['duration']
        ax.set_xlim([-20,x_dimension])
        y_min_val = max(nodes_per_time)*0.05 # patch for making lawn_mower and pso charts with similar distance below y=0 line
        ax.set_ylim(ymin=-y_min_val) # avoids the text to appear below the figure when the y axis does not have values in '0'
        ax.grid(True)
        
        # text
        percent = float(total_nodes)*100/CONFIG['nodes_amount']
        percent_text = 'Total discovered: '+format(percent, '.2f')+' %'    
        total_text = 'Total: '+str(int(total_nodes))+' nodes'
        ax.text(x_dimension+7,-y_min_val,percent_text+'\n'+total_text)
        
        # save images into the simulation folder
        # SAVE INTO OTHER IMAGE FORMATS: eps,png...
        fig.savefig(interval_folder+'/'+str(i).zfill(2)+'_update_interval_'+str(interval)+'.svg',format='svg',dpi=1200,bbox_inches='tight')
        plt.close('all')


def plot_nodes_statistics(nodes_events,nodes_frequency,nodes_time_btw_conn,CONFIG):
    """ Plot several nodes statistics """   
    
    # nodes connections per time
    #############################
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # generate the columns locations
    nodes_ids = range(len(nodes_events))
    
    try:
        ax.eventplot(nodes_events, orientation='horizontal', lineoffsets=nodes_ids) 
    
    except AttributeError,argument:
        # in the case that the bug of matplotlib for the horizontal attribute of eventplot arises
        # more information about this bug at: https://github.com/matplotlib/matplotlib/issues/6412
        logger.warning("AttributeError exception caught: "+str(argument) \
                       +"\n\tscatter plot will be used instead of event plot")
      
        plt.close('all') # close the previous figure object
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
    
        for i,events in enumerate(nodes_events):
            
            y = [i]*len(events) # generation of y axis with the node id
                
            ax.scatter(events,y, color='blue', s=5, edgecolor='none') 
 
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Node id")
    ax.set_title("Nodes connection events between nodes and UAVs per time\n") 
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_nodes_connection_events.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    
    # nodes connections frequency
    #############################
    
    # normal scale
    #-------------
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration'])
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_frequency, bins, normed=False)
    
    ax.set_xlabel("Number of nodes connections events")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Frequency of the number of nodes connection to UAVs\n")
    
    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])

    ocurrences_zero=nodes_frequency.count(0)
    text_pos_x=50
    text_pos_y=ocurrences_zero
    ax.annotate('Value: '+str(ocurrences_zero), xy=(0,ocurrences_zero),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_nodes_connection_hist.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    # logarithmic scale
    #------------------
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration'])
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_frequency, bins, normed=False, log=True)
    
    ax.set_xlabel("Number of nodes connections events")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Frequency of the number of nodes connection to UAVs\n\n")
    
    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])
    
    ocurrences_zero=nodes_frequency.count(0)
    text_pos_x=50
    text_pos_y=ocurrences_zero+1
    ax.annotate('Value: '+str(ocurrences_zero), xy=(0,ocurrences_zero),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_nodes_connection_hist_log.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    
    
    # time between consecutive nodes connections to UAVs
    ####################################################
    
    # normal scale
    #-------------

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration']) # duration is the max time between connections
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_time_btw_conn, bins, normed=False)
    
    ax.set_xlabel("Time between consecutive nodes connections events")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Time between consecutive nodes connections to UAVs\n\n")
  
    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])
        
    xticks_fix = ax.xaxis.get_majorticklocs()      
    xticks_fix = [1. if x==0. else x for x in xticks_fix] # change the tick '0' to '1' as visually it represent better the results 
    xticks_fix[0] = -10.0
    
    ax.set_xticks(xticks_fix)
    ax.xaxis.get_major_ticks()[0].label1.set_visible(False)
    
    ocurrences_one=nodes_time_btw_conn.count(1)
    text_pos_x=50
    text_pos_y=ocurrences_one+10
    ax.annotate('Value: '+str(ocurrences_one), xy=(1,ocurrences_one),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    ocurrences_duration=nodes_time_btw_conn.count(CONFIG['duration'])
    text_pos_x=CONFIG['duration']-50
    text_pos_y=ocurrences_duration+2000
    ax.annotate('Value: '+str(ocurrences_duration), xy=(CONFIG['duration'],ocurrences_duration),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_nodes_time_between_connections.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    
    # logarithmic scale
    #------------------

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration']) # duration is the max time between connections
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_time_btw_conn, bins, normed=False, log=True)
    
    ax.set_xlabel("Time between consecutive nodes connections events")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Time between consecutive nodes connections to UAVs\n\n")
  
    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])
        
    xticks_fix = ax.xaxis.get_majorticklocs()      
    xticks_fix = [1. if x==0. else x for x in xticks_fix] # change the tick '0' to '1' as visually it represent better the results 
    xticks_fix[0] = -10.0
    
    ax.set_xticks(xticks_fix)
    ax.xaxis.get_major_ticks()[0].label1.set_visible(False)

    ocurrences_one=nodes_time_btw_conn.count(1)
    text_pos_x=50
    text_pos_y=ocurrences_one+10
    ax.annotate('Value: '+str(ocurrences_one), xy=(1,ocurrences_one),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    ocurrences_duration=nodes_time_btw_conn.count(CONFIG['duration'])
    text_pos_x=CONFIG['duration']-50
    text_pos_y=ocurrences_duration+100
    ax.annotate('Value: '+str(ocurrences_duration), xy=(CONFIG['duration'],ocurrences_duration),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_nodes_time_between_connections_log.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_colormap(pos_per_time, CONFIG):
    
    # nodes positions colormap
    fig = plt.figure()
    ax = fig.add_subplot(111)
        
    x_pos = list(zip(*pos_per_time)[0])
    y_pos = list(zip(*pos_per_time)[1]) 
    z_pos = list(zip(*pos_per_time)[2]) # this represents the color intensity
    
    cm = plt.cm.get_cmap('YlOrRd_r')
    scat = ax.scatter(x_pos,y_pos,c=z_pos,vmin=0,vmax=CONFIG['duration'],s=50,cmap=cm)
        
    fig.colorbar(scat)
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Nodes discovered latest positions\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_colormap.svg',format='svg',dpi=1200)
    plt.close('all')
           
           

def plot_colormap_and_traj(pos_per_time, pos_drones,CONFIG,values_file):
    """ Plot the nodes update map and drones trajectories together """
    
    colors_cycler = plot_settings()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
     
    # drones trajectories
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
          
        curr_color = next(colors_cycler)
        ax.plot(x_pos,y_pos,label='drone '+str(drone_i),color=curr_color,linestyle='--')
        ax.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        ax.plot(x_pos[0],y_pos[0],marker='.',color=curr_color)
    
    # nodes positions colormap    
    x_pos = list(zip(*pos_per_time)[0])
    y_pos = list(zip(*pos_per_time)[1]) 
    z_pos = list(zip(*pos_per_time)[2]) # this represents the color intensity
    
    cm = plt.cm.get_cmap('YlOrRd_r')
    scat = ax.scatter(x_pos,y_pos,c=z_pos,vmin=0,vmax=CONFIG['duration'],s=50,cmap=cm)
        
    fig.colorbar(scat)
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Nodes discovered color map\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.legend(bbox_to_anchor=(1.25,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_updatemapandtraj.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')

    # if intermediate charts have to be plot
    if CONFIG['intermediate_charts'][0] == 1:
        
        offset = CONFIG['intermediate_charts'][1]
        
        in_timestamp = offset
        # taking lb_start and nb_start as the timestamp plus an offset
        lb_timestamp = CONFIG['pso_params'][3]+offset
        nb_timestamp = CONFIG['pso_params'][5]+offset 
    
        # inertia intermediate plot
        # parse the nodes update time with the timestamp as if it were the final duration 
        nodes_per_time_aux, pos_per_time_aux, total_nodes_aux = parsers.parser_update_time_intermediate(values_file, CONFIG['drones_amount'], in_timestamp)
        values_file.seek(0)        
        plot_colormap_and_traj_timet(pos_per_time_aux, pos_drones,CONFIG,in_timestamp,'in')
        
        # local best intermediate plot
        nodes_per_time_aux, pos_per_time_aux, total_nodes_aux = parsers.parser_update_time_intermediate(values_file, CONFIG['drones_amount'], lb_timestamp)
        values_file.seek(0)
        plot_colormap_and_traj_timet(pos_per_time_aux, pos_drones,CONFIG,lb_timestamp,'lb')

        # neighbor best intermediate plot
        nodes_per_time_aux, pos_per_time_aux, total_nodes_aux = parsers.parser_update_time_intermediate(values_file, CONFIG['drones_amount'], nb_timestamp)
        values_file.seek(0)
        plot_colormap_and_traj_timet(pos_per_time_aux, pos_drones,CONFIG,nb_timestamp,'nb')
        
    else:
        pass
     

def plot_colormap_and_traj_timet(pos_per_time, pos_drones,CONFIG,intermediate_time,id):
    """ Plot the nodes update map and drones trajectories together at a specific time within the simulation duration"""
    
    colors_cycler = plot_settings()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
     
    # drones trajectories
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        # remove drones positions that are beyond the intermediate time that we want to plot
        x_pos = x_pos[0:intermediate_time]
        y_pos = y_pos[0:intermediate_time]
          
        curr_color = next(colors_cycler)
        ax.plot(x_pos,y_pos,label='drone '+str(drone_i),color=curr_color,linestyle='--')
        ax.plot(x_pos[-1],y_pos[-1],marker='x',color=curr_color)
        ax.plot(x_pos[0],y_pos[0],marker='.',color=curr_color)
    
    # nodes positions colormap    
    x_pos = list(zip(*pos_per_time)[0])
    y_pos = list(zip(*pos_per_time)[1]) 
    z_pos = list(zip(*pos_per_time)[2]) # this represents the color intensity
    
    # remove nodes positions that are beyond the intermediate time that we want to plot
#     x_pos = x_pos[0:intermediate_time]
#     y_pos = y_pos[0:intermediate_time]
#     z_pos = z_pos[0:intermediate_time]
    
    cm = plt.cm.get_cmap('YlOrRd_r')
    scat = ax.scatter(x_pos,y_pos,c=z_pos,vmin=0,vmax=intermediate_time,s=50,cmap=cm)
        
    fig.colorbar(scat)
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Nodes discovered color map\n\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.legend(bbox_to_anchor=(1.25,1.02), loc='upper left')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_updatemapandtraj_'+id+'.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_encounters(encounters,total_encounters, CONFIG):
    """ Plot drones encounters per time and total """ 
  
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(range(CONFIG['duration']),encounters)
        
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Number of drones encounters")
    ax.set_title("Drones encounters per time\n\n")
    ax.grid(True)
    ax.set_xlim([0,CONFIG['duration']])
    ax.set_ylim(ymin=0) # avoids the text to appear below the figure when the y axis does not have values in '0'
    
    x_dimension = CONFIG['duration']
    encounters_text = 'Total encounters: '+str(total_encounters)
    ax.text(x_dimension+7,0,encounters_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_encounters.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    
    
  
def plot_graph(drones_graph, pos_drones, CONFIG):
    """ Plot drones encounters per time and total """ 
  
    colors_cycler = plot_settings()
  
    fig = plt.figure()
    axes_fig = fig.add_subplot(111)
    
    # calculate drones final positions
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = copy.deepcopy(drone_pos[0][-1])
        y_pos = copy.deepcopy(drone_pos[1][-1])
        
        # add position attribute to drones nodes in the graph
        drones_graph.add_node(drone_i, x=x_pos,y=y_pos)
       
    # generate drones positions as a dictionary
    if nx.__version__ == '1.7rc1':
        
        drones_positions={}
        
        for node in drones_graph.nodes(data=True):
            key_val = str(node[0])
            x_val=node[1]['x']
            y_val=node[1]['y']
            drones_positions[key_val]=(x_val,y_val)
        
    else: 
        # this case assumes a networkx version 2.0
        drones_positions={node[0]: (node[1]['x'],node[1]['y']) for node in drones_graph.nodes(data=True)}    
    
    axes_fig.set_xlabel("x coordinate (m)")
    axes_fig.set_ylabel("y coordinate (m)")
    axes_fig.set_title("Drones graph\n")
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    axes_fig.set_xlim([0,x_dimension])
    axes_fig.set_ylim([0,y_dimension])    
    
    # draw each subgraph with a different color
    for subgraph_i in nx.connected_component_subgraphs(drones_graph):
        # draw each subgrpah with a different color
        nx.draw_networkx(subgraph_i, pos=drones_positions, with_labels=False, ax=axes_fig, node_size=100, node_color=next(colors_cycler))
        
        # create a label for the subgraph        
        aux = [node[0] for node in subgraph_i.nodes(data=True)]
        
        for i,node_id in enumerate(aux):
            if len(aux) == 1:
                sub_label=str(node_id)
            else:
                if i != len(aux)-1:
                    sub_label=str(node_id)+','
                else:
                    sub_label=sub_label+str(node_id)
        
        # get one of the nodes position of subgraph e.g. the last node_id
        x_label_offset = 100
        y_label_offset = 0
        
        if nx.__version__ == '1.7rc1':
            x_pos_node = float(subgraph_i.nodes(data=True)[node_id][1]['x']) + x_label_offset
            y_pos_node = float(subgraph_i.nodes(data=True)[node_id][1]['y']) + y_label_offset
        else: 
            # this case assumes a networkx version 2.0
            x_pos_node = float(subgraph_i.nodes()[node_id]['x']) + x_label_offset
            y_pos_node = float(subgraph_i.nodes()[node_id]['y']) + y_label_offset
        
        axes_fig.annotate(sub_label,xy=(x_pos_node,y_pos_node))
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_drones_graph.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
  
  
    
def plot_drones_in_cluster(pos_drones,CONFIG):
    """ Plot the final neighbor best position of each drone in relation with a cluster"""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # If the cluster membership were based in the neighbor best even lawn_mower interprets 
    # that drones are finally flying around a cluster
   
    # Get drones latest positions
    final_pos = []
    
    for drone_i in range(len(pos_drones)):
        drone_pos = pos_drones[drone_i]
        drone_pos = zip(*drone_pos)
        x_pos = drone_pos[0]
        y_pos = drone_pos[1]
        
        final_pos.append([x_pos[-1],y_pos[-1]])
        
    
    # get clusters 
    clusters = CONFIG['clusters']
    total_clusters = len(clusters)
    drone_per_cluster = []
     
    for cluster_i in clusters:
        origin = cluster_i[0]
        dimension = cluster_i[1]
        margin = CONFIG['cluster_edgewidth']
        
        drone_count = 0
        
        for pos in final_pos:
            if geometry.is_within_area(pos,origin,dimension,margin): 
                drone_count += 1
            else:
                pass
        
        drone_per_cluster.append(drone_count)
    
    # generate the columns locations
    bars_loc = range(total_clusters)
    width = 0.8
    
    ax.bar(bars_loc,drone_per_cluster,width,color='green')
    
    ax.set_xlabel("Clusters")
    ax.set_ylabel("Number of drones")
    ax.set_title("Drones per cluster\n\n")
    ax.grid(True)
    
    y_dimension = CONFIG['drones_amount']+1
    ax.set_ylim([0,y_dimension])
    
    xtick_pos = bars_loc
    ax.set_xticks(xtick_pos)
    ticks = []
    
    for i in bars_loc:
        ticks.append('cluster '+str(int(i+1-0.2))) 
        
    ax.set_xticklabels(tuple(ticks))
    
    # text
    x_dimension = total_clusters
    all_text = 'Total clusters: '+str(total_clusters)
    ax.annotate(all_text, xy=(1.05,0), xycoords='axes fraction')

    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_drone_per_cluster.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')



def plot_time_to_cluster(pos_drones,CONFIG):
    """ Plots the time needed for the drones to converge flying within a cluster"""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    
    drones_convergence = []
    clusters = CONFIG['clusters']
    margin = CONFIG['cluster_edgewidth'] 
    
    # Check convergence for each drone    
    for drone_i in range(len(pos_drones)):
        
        drone_pos = pos_drones[drone_i]
        
        time_cluster = [] # time at which the drone remains at each cluster
        
        # for each position we check if the drone is within a cluster
        for t,pos_i in enumerate(drone_pos):
            
            # we check all the clusters
            for i,cluster_i in enumerate(clusters):
                origin = cluster_i[0]
                dimension = cluster_i[1]
                
                # initialize the time_cluster
                if t == 0:
                    time_cluster.append(0)
                    
                elif geometry.is_within_area(pos_i,origin,dimension,margin):
                    # not update time, keep he last value
                    pass 
                else:
                    time_cluster[i] = t
        
        # select the cluster in which the drone converges (the one with less time)        
        drones_convergence.append(min(time_cluster))
    
    # generate the columns locations
    bars_loc = range(CONFIG['drones_amount']) 
    width = 0.8
    
    ax.bar(bars_loc, drones_convergence, width, color='green')
    
    ax.set_xlabel("Drones")
    ax.set_ylabel("Time")
    ax.set_title("Convergence time in a cluster\n\n")
    ax.grid(True)
    
    y_dimension = CONFIG['duration']
    ax.set_ylim([0,y_dimension])
    
    xtick_pos = bars_loc
    ax.set_xticks(xtick_pos)
    ticks = []
    
    for i in bars_loc:
        ticks.append('drone '+str(int(i-0.2))) 
        
    ax.set_xticklabels(tuple(ticks))
    
    # text
    x_dimension = CONFIG['drones_amount']
    all_text = 'Max convergence time: '+str(max(drones_convergence))+'\n'
    all_text = all_text+'Min convergence time: '+str(min(drones_convergence))
    ax.text(int(x_dimension)-0.3,0,all_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['output_folder']+'/'+CONFIG['timestamp']+'_convergence.svg',format='svg',dpi=1200,bbox_inches='tight')
    plt.close('all')
    

def plot_all(filename, CONFIG):
    values_file = open(filename,'r')
    
    # check first if there are any nodes discovered
    accum_discovered = parsers.parser_acc_discovered(values_file)
    values_file.seek(0)
    
    if accum_discovered[-1] == 0:
        # none nodes were discovered, plot only charts that have information avaialable
        pass
    
    else:
        # parsing functions calls
        discovered = parsers.parser_discovered(values_file,CONFIG['drones_amount'])
        values_file.seek(0) # returns the file pointer to the beginning
                
        total_discovered_time = parsers.parser_discovered_per_time(values_file)
        values_file.seek(0)
         
        pos_drones = parsers.parser_positions(values_file, CONFIG['drones_amount'])
        values_file.seek(0)
         
        total_lb,pos_lb = parsers.parser_localbest(values_file, CONFIG['drones_amount'])
        values_file.seek(0)
         
        discoverer,total_nb,pos_nb = parsers.parser_neighborsbest(values_file, CONFIG['drones_amount'])
        values_file.seek(0)  
        
        nodes_per_time, pos_per_time, total_nodes = parsers.parser_update_time(values_file, CONFIG['drones_amount'], CONFIG['duration'])
        values_file.seek(0)
        
    #     nodes_per_time_t,interval_list,total_nodes_t = parsers.parser_update_time_interval(values_file, CONFIG['drones_amount'], CONFIG['duration'])
    #     values_file.seek(0)
        
        nodes_events,nodes_frequency,nodes_time_btw_conn = parsers.parser_nodes_statistics(values_file,CONFIG['nodes_amount'],CONFIG['duration'])
        values_file.seek(0)
    
        encounters,total_encounters, last_graph = parsers.parser_encounters(values_file, CONFIG['drones_amount']) 
        values_file.seek(0)
        
        # plotting functions calls
        plot_discovered(discovered,CONFIG)
        plot_acc_discovered(accum_discovered,CONFIG)
        plot_discovered_per_time(total_discovered_time,CONFIG)
        plot_discovery_rate(accum_discovered,CONFIG)
        plot_acc_quartile(accum_discovered,CONFIG)
          
        plot_trajectory(pos_drones,CONFIG)
        plot_final_positions(pos_drones,CONFIG)
         
        plot_local_best(total_lb,pos_lb,CONFIG)
        plot_neighbor_best(discoverer,total_nb,pos_nb,CONFIG)
        plot_final_neighbor_best(pos_nb,CONFIG)
         
        plot_update_time(nodes_per_time, total_nodes, CONFIG)
    #     plot_update_time_interval(nodes_per_time_t, interval_list, total_nodes_t, CONFIG)
        plot_nodes_statistics(nodes_events,nodes_frequency,nodes_time_btw_conn,CONFIG)
     
        plot_colormap(pos_per_time, CONFIG)
        plot_colormap_and_traj(pos_per_time, pos_drones, CONFIG, values_file)
         
        plot_encounters(encounters,total_encounters, CONFIG)
        
        if nx.__version__ == '1.7rc1':
            logger.info('Networkx version 1.7rc1 - not plotting the drones graph')
        else:
            plot_graph(last_graph, pos_drones, CONFIG)
        
        plot_drones_in_cluster(pos_drones,CONFIG)
        plot_time_to_cluster(pos_drones,CONFIG)
    
    values_file.close()
    
    