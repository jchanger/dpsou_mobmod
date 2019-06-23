""" Function definitions for plotting results

--------------------------
Created on Apr 5, 2017

@author: J. Sanchez-Garcia
"""

import matplotlib   
matplotlib.use('Agg')   # for running the script on the server without graphics system up

import subprocess
import numpy as np
import matplotlib.pylab as plt
import networkx as nx
# import matplotlib.colors as colors
from functions import parsers
from functions import parsers_avg
from functions import geometry
from itertools import cycle
from subprocess import PIPE, Popen
from collections import Counter


def get_algo_params(CONFIG):
    """ Get the algorithm parameters to be plotted on the figure"""
    
    if CONFIG['algorithm'] == 'pso':
        str_aux = CONFIG['main_output_folder'].split("/")
        fig_params = 'pso: '+str_aux[-1]
    else:
        fig_params = "lawn mower"
    
    return fig_params


def plot_settings():
    """ Creates lists with available line markers and colors for easing plotting """
    
    #colors = matplotlib.colors.cnames.keys() # not used as some colors are very clear for a blank background
    colors = ['green','blue','red','cyan','magenta','black','orange','maroon','lime','gold','crimson','deeppink','purple','olive']
    
    colors_cycler = cycle(colors)
    
    return colors_cycler

     
    
# def plot_update_time_avg(nodes_per_time, total_nodes,CONFIG):
#     """ Plot the nodes update time """   
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     # generate the columns locations
#     bars_loc = range(CONFIG['duration']) 
#     
#     ax.bar(bars_loc, nodes_per_time, width=2, edgecolor='green', color='green') 
#     
#     ax.set_xlabel("Time since last connection (s)")
#     ax.set_ylabel("Number of nodes")
#     ax.set_title("Number of nodes discovered 't' seconds ago [avg]\n"+get_algo_params(CONFIG))
#     x_dimension = CONFIG['duration']
#     x_min_val = x_dimension*0.02
#     ax.set_xlim([-x_min_val,x_dimension])
#     y_min_val = max(nodes_per_time)*0.05 # patch for making lawn_mower and pso charts with similar distance below y=0 line
#     ax.set_ylim(ymin=-y_min_val)
#     ax.grid(True)
#     
#     # text
#     percent = float(total_nodes)*100/CONFIG['nodes_amount']
#     percent_text = 'Total discovered: '+format(percent, '.2f')+' %'    
#     total_text = 'Total (avg): '+format(total_nodes, '.2f')+' nodes'
#     ax.text(x_dimension+7,-y_min_val,percent_text+'\n'+total_text)
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_update_avg.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')
# 
# 
# 
# def plot_update_time_std(nodes_time_avg, nodes_time_std, total_nodes_avg, total_nodes_std, CONFIG):
#     """ Plot the nodes update time mean and standard deviation """   
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     # generate the columns locations
#     x = range(CONFIG['duration']) 
#     y_mean = nodes_time_avg
#     err = nodes_time_std
#     
#     y_top = [y_val+err_val for y_val,err_val in zip(y_mean,err)]
#     y_bottom = [y_val-err_val for y_val,err_val in zip(y_mean,err)]
# 
#     ax.fill_between(x,y_top,y_bottom,color='greenyellow')
#     ax.plot(x,y_mean,color='green')
#     ax.plot(x[0],y_mean[0],color='green',marker='.')
#     
#     ax.set_xlabel("Time since last connection (s)")
#     ax.set_ylabel("Number of nodes")
#     ax.set_title("Number of nodes discovered 't' seconds ago [avg-std]\n"+get_algo_params(CONFIG))
#     x_dimension = CONFIG['duration']
#     x_min_val = x_dimension*0.02
#     ax.set_xlim([-x_min_val,x_dimension])
#     y_min_val = max(y_top)*0.05 # patch for making lawn_mower and pso charts with similar distance below y=0 line
#     ax.set_ylim(ymin=-y_min_val)
#     ax.grid(True)
#     
#     # text
#     percent = float(total_nodes_avg)*100/CONFIG['nodes_amount']
#     percent_text = 'Total discovered: '+format(percent, '.2f')+' %'
#     total_text = 'Total (avg): '+format(total_nodes_avg, '.2f')+' nodes'
#     total_std_text = 'dev : '+format(total_nodes_std, '.2f')+' nodes'
#     ax.text(x_dimension+7,-y_min_val,percent_text+'\n'+total_text+'\n'+total_std_text)
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_update_std.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')
    
    

def plot_acc_discovered_avg(discovered_avg,discovered_std,CONFIG, file_report):
    """ Plot the accumulated discovered nodes mean and standard deviation """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # generate the columns locations
    x = range(CONFIG['duration']) 
    y_mean = discovered_avg
    err = discovered_std
    
    y_top = [y_val+err_val for y_val,err_val in zip(y_mean,err)]
    y_bottom = [y_val-err_val for y_val,err_val in zip(y_mean,err)]

    ax.fill_between(x,y_top,y_bottom,color='greenyellow')
    ax.plot(x,y_mean,color='green')
    
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Number of nodes (accumulated)")
    ax.set_title("Discovered nodes per time (accumulated) [avg]\n"+get_algo_params(CONFIG))
    x_dimension = CONFIG['duration']
    ax.set_xlim([0,x_dimension])
    y_dimension = CONFIG['nodes_amount']
    ax.set_ylim([0,y_dimension])
    ax.grid(True)
    
    # text
    percent = float(y_mean[-1])*100/CONFIG['nodes_amount']
    percent_text = '% discovered (avg): '+format(percent, '.2f')+' %'    
    total_text = 'Total discovered (avg): '+str(y_mean[-1])
    deviation_text = 'dev: '+format(err[-1],'.2f')
    ax.annotate(percent_text+'\n'+total_text+'\n'+deviation_text, xy=(1.05,0), xycoords='axes fraction')

    if file_report != None:
        file_report.write("\nDiscovered nodes per time (accumulated) [avg]\n")
        file_report.write('\t'+percent_text+'\n\t'+total_text+'\n\t'+deviation_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_discovered_std.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



def plot_discovered_per_time_avg(discovered_per_time_avg,discovered_per_time_std,CONFIG, file_report):
    """ Plot the discovered nodes per time mean and standard deviation """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # generate the columns locations
    x = range(CONFIG['duration']) 
    y_mean = discovered_per_time_avg
    err = discovered_per_time_std
    
    y_top = [y_val+err_val for y_val,err_val in zip(y_mean,err)]
    y_bottom = [y_val-err_val for y_val,err_val in zip(y_mean,err)]

    ax.fill_between(x,y_top,y_bottom,color='greenyellow')
    ax.plot(x,y_mean,color='green')
    
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Number of nodes")
    ax.set_title("Discovered nodes per time [avg]\n"+get_algo_params(CONFIG))
    x_dimension = CONFIG['duration']
    ax.set_xlim([0,x_dimension])
    y_dimension = CONFIG['nodes_amount']
    ax.set_ylim([0,y_dimension])
    ax.grid(True)

    # text
    y_sublist = y_mean[0:CONFIG['pso_params'][3]].tolist() # 3 corresponds to lb_start
    in_max_val = max(y_sublist)
    in_max_index = [i for i,j in enumerate(y_sublist) if j == in_max_val] # get all max values occurrences 
    in_max_pos = x[in_max_index[-1]] # take the last max value of the range
    if CONFIG['algorithm'] == 'pso':
        in_max_text = 'inertia max (x,y): ('+format(in_max_pos, '.1f')+',  '+format(in_max_val, '.1f')+')'
    else:
        in_max_text = '1st stage max (x,y): ('+format(in_max_pos, '.1f')+',  '+format(in_max_val, '.1f')+')'

    y_sublist = y_mean[CONFIG['pso_params'][3]:CONFIG['pso_params'][5]].tolist() # 5 corresponds to nb_start
    lb_max_val = max(y_sublist)
    lb_max_index = [i for i,j in enumerate(y_sublist) if j == lb_max_val] # get all max values occurrences
    lb_max_pos = x[lb_max_index[-1]+CONFIG['pso_params'][3]]  # add the start of the lb range
    if CONFIG['algorithm'] == 'pso':
        lb_max_text = 'lb max (x,y): ('+format(lb_max_pos, '.1f')+',  '+format(lb_max_val, '.1f')+')'
    else:
        lb_max_text = '2nd stage max (x,y): ('+format(lb_max_pos, '.1f')+',  '+format(lb_max_val, '.1f')+')'
        
    y_sublist = y_mean[CONFIG['pso_params'][5]:CONFIG['duration']].tolist()
    nb_max_val = max(y_sublist)
    nb_max_index = [i for i,j in enumerate(y_sublist) if j == nb_max_val] # get all max values occurrences
    nb_max_pos = x[nb_max_index[-1]+CONFIG['pso_params'][5]]
    if CONFIG['algorithm'] == 'pso':
        nb_max_text = 'nb max (x,y): ('+format(nb_max_pos, '.1f')+',  '+format(nb_max_val, '.1f')+')'
    else:
        nb_max_text = '3rd stage max (x,y): ('+format(nb_max_pos, '.1f')+',  '+format(nb_max_val, '.1f')+')'   
    
    discov_mean_text = 'Mean of discovered per time: '+format(np.mean(y_mean), '.1f')
    
    ax.annotate(in_max_text+'\n'+lb_max_text+'\n'+nb_max_text+'\n'+discov_mean_text, xy=(1.05,0), xycoords='axes fraction')
    
    if file_report != None:
        file_report.write("\nDiscovered nodes per time [avg]\n")
        file_report.write('\t'+in_max_text+'\n\t'+lb_max_text+'\n\t'+nb_max_text+'\n\t'+discov_mean_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_discovered_per_time_std.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')


def plot_nodes_statistics_avg(nodes_events_l,nodes_frequency_l,nodes_time_btw_conn_l,CONFIG, file_report):
    """ Plot several nodes statistics """   

    # nodes connections per time
    #############################

    # TODO: The events for all the iterations of the simulation will be represented in the future


    # nodes connections frequency
    #############################
    
    # normal scale
    #-------------
# LIGHT_SIM
#     fig = plt.figure(figsize=(20,10))
#     ax = fig.add_subplot(111)
#     
#     bins=range(CONFIG['duration'])
#     bins.append(CONFIG['duration'])
#     
#     ax.hist(nodes_frequency_l, bins, normed=False, color='green')
#     
#     ax.set_xlabel("Nodes connections events")
#     ax.set_ylabel("Number of nodes (frequency)")
#     ax.set_title("Number of nodes connection to UAVs\n"+get_algo_params(CONFIG))
#     ax.grid(False)
#
#     x_dimension_min = -10
#     x_dimension_max = CONFIG['duration']+10
#     ax.set_xlim([x_dimension_min,x_dimension_max])
#         
#     ocurrences_zero=nodes_frequency_l.count(0)
#     text_pos_x=50
#     text_pos_y=ocurrences_zero+1
#     ax.annotate('Value: '+str(ocurrences_zero), xy=(0,ocurrences_zero),xytext=(text_pos_x,text_pos_y),\
#                 arrowprops=dict(arrowstyle="->"))
#      
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_nodes_connection_hist_all.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')


    # logarithmic scale
    #------------------
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration'])
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_frequency_l, bins, normed=False, log=True, color='green')
    
    ax.set_xlabel("Nodes connections events")
    ax.set_ylabel("Number of nodes (frequency)")
    ax.set_title("Number of nodes connection to UAVs\n"+get_algo_params(CONFIG))
    ax.grid(False)

    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])
        
    ocurrences_zero=nodes_frequency_l.count(0)
    text_pos_x=50
    text_pos_y=ocurrences_zero+1
    ax.annotate('Value: '+str(ocurrences_zero), xy=(0,ocurrences_zero),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))

    # get max value
    max_tuples = Counter(nodes_frequency_l).most_common()
    max_pos = max_tuples[0][0]
    max_val = max_tuples[0][1]
    max_y_text = 'Max val (x,y): '+format(max_pos, '.2f')+', '+format(max_val, '.2f')
    
    if len(max_tuples) == 1:
        # There is not a second maximum
        sec_max_y_text = 'Second max val (x,y): None'
    else:
        sec_max_pos = max_tuples[1][0]
        sec_max_val = max_tuples[1][1]
        sec_max_y_text = 'Second max val (x,y): '+format(sec_max_pos, '.2f')+', '+format(sec_max_val, '.2f')
    
    max_x_text = 'Max connections events (x axis): '+str(max(nodes_frequency_l))
    ocurrences_zero_text = 'Freq in x=0: '+str(ocurrences_zero)
    
    hist_y_vals = np.histogram(nodes_frequency_l, bins,normed=False)[0]
    conn_mean_text = 'Mean of connections bars: '+format(np.mean(hist_y_vals), '.1f')
    
    ax.annotate(ocurrences_zero_text+'\n'+max_x_text+'\n'+max_y_text+'\n'+sec_max_y_text+'\n'+conn_mean_text, xy=(1.02,0), xycoords='axes fraction')

    if file_report != None:
        file_report.write("\nNumber of nodes connection to UAVs\n")
        file_report.write('\t'+ocurrences_zero_text+'\n\t'+max_x_text+'\n\t'+max_y_text+'\n\t'+sec_max_y_text+'\n\t'+conn_mean_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_nodes_connection_hist_log_all.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')
    
    
    # time between consecutive nodes connections to UAVs
    ####################################################
    
    # normal scale
    #-------------
#    LIGHT_SIM
#     fig = plt.figure(figsize=(20,10))
#     ax = fig.add_subplot(111)
#     
#     bins=range(CONFIG['duration']) # duration is the max time between connections
#     bins.append(CONFIG['duration'])
#     
#     ax.hist(nodes_time_btw_conn_l, bins, normed=False, color='green')
#     
#     ax.set_xlabel("Time between consecutive nodes connections events")
#     ax.set_ylabel("Number of nodes (frequency)")
#     ax.set_title("Time between consecutive nodes connections to UAVs\n"+get_algo_params(CONFIG))
#     ax.grid(False)
#  
#     x_dimension_min = -10
#     x_dimension_max = CONFIG['duration']+10
#     ax.set_xlim([x_dimension_min,x_dimension_max])
#         
#     xticks_fix = ax.xaxis.get_majorticklocs()      
#     xticks_fix = [1. if x==0. else x for x in xticks_fix] # change the tick '0' to '1' as visually it represent better the results 
#     xticks_fix[0] = -10.0
#     
#     ax.set_xticks(xticks_fix)
#     ax.xaxis.get_major_ticks()[0].label1.set_visible(False)
#     
#     ocurrences_one=nodes_time_btw_conn_l.count(1)
#     text_pos_x=50
#     text_pos_y=ocurrences_one+10
#     ax.annotate('Value: '+str(ocurrences_one), xy=(1,ocurrences_one),xytext=(text_pos_x,text_pos_y),\
#                 arrowprops=dict(arrowstyle="->"))
#     
#     ocurrences_duration=nodes_time_btw_conn_l.count(CONFIG['duration'])
#     text_pos_x=CONFIG['duration']-50
#     text_pos_y=ocurrences_duration+2000
#     ax.annotate('Value: '+str(ocurrences_duration), xy=(CONFIG['duration'],ocurrences_duration),xytext=(text_pos_x,text_pos_y),\
#                 arrowprops=dict(arrowstyle="->"))
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_nodes_time_between_connections_all.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')
    
    # logarithmic scale
    #------------------
    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    
    bins=range(CONFIG['duration']) # duration is the max time between connections
    bins.append(CONFIG['duration'])
    
    ax.hist(nodes_time_btw_conn_l, bins, normed=False, log=True, color='green')
    
    ax.set_xlabel("Time between consecutive nodes connections events")
    ax.set_ylabel("Number of nodes (frequency)")
    ax.set_title("Time between consecutive nodes connections to UAVs\n"+get_algo_params(CONFIG))
    ax.grid(False)
  
    x_dimension_min = -10
    x_dimension_max = CONFIG['duration']+10
    ax.set_xlim([x_dimension_min,x_dimension_max])
        
    xticks_fix = ax.xaxis.get_majorticklocs()      
    xticks_fix = [1. if x==0. else x for x in xticks_fix] # change the tick '0' to '1' as visually it represent better the results 
    xticks_fix[0] = -10.0
    
    ax.set_xticks(xticks_fix)
    ax.xaxis.get_major_ticks()[0].label1.set_visible(False)
    
    ocurrences_one=nodes_time_btw_conn_l.count(1)
    text_pos_x=50
    text_pos_y=ocurrences_one+10
    ax.annotate('Value: '+str(ocurrences_one), xy=(1,ocurrences_one),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))
    
    ocurrences_duration=nodes_time_btw_conn_l.count(CONFIG['duration'])
    text_pos_x=CONFIG['duration']-100
    text_pos_y=ocurrences_duration+200
    ax.annotate('Value: '+str(ocurrences_duration), xy=(CONFIG['duration'],ocurrences_duration),xytext=(text_pos_x,text_pos_y),\
                arrowprops=dict(arrowstyle="->"))

    # get second maximum value
    max_tuples = Counter(nodes_time_btw_conn_l).most_common()
    max_pos = max_tuples[0][0]
    max_val = max_tuples[0][1]
    max_y_text = 'Max val (x,y): '+format(max_pos, '.2f')+', '+format(max_val, '.2f')
    
    if len(max_tuples) == 1:
        # There is not a second maximum
        sec_max_y_text = 'Second max val (x,y): None'
    else:
        sec_max_pos = max_tuples[1][0]
        sec_max_val = max_tuples[1][1]
        sec_max_y_text = 'Second max val (x,y): '+format(sec_max_pos, '.2f')+', '+format(sec_max_val, '.2f')
    
    sorted_l = sorted(nodes_time_btw_conn_l, reverse=True)
    
    for i,val in enumerate(sorted_l):
        if i == 0:
            second_max = val
        else:
            if second_max == val:
                pass
            else:
                # the first value that is not the maximum
                second_max = val
                break
         
    second_max_text =  'Second max time btw conn (x axis): '+str(second_max)
    ocurrences_one_text = 'Freq in x=1: '+str(ocurrences_one)
    ocurrences_duration_text = 'Freq in x=duration: '+str(ocurrences_duration)
    
    hist_y_vals = np.histogram(nodes_time_btw_conn_l, bins,normed=False)[0]
    tbtw_conn_mean_text = 'Mean of time btw conn bars: '+format(np.mean(hist_y_vals), '.1f')
    
    ax.annotate(ocurrences_one_text+'\n'+ocurrences_duration_text+'\n'+second_max_text+'\n'+max_y_text+'\n'+sec_max_y_text+'\n'+tbtw_conn_mean_text,\
                 xy=(1.02,0), xycoords='axes fraction')

    if file_report != None:
        file_report.write("\nTime between consecutive nodes connections to UAVs\n")
        file_report.write('\t'+ocurrences_one_text+'\n\t'+ocurrences_duration_text+'\n\t'+second_max_text+'\n\t'+max_y_text+'\n\t'+sec_max_y_text\
                          +'\n\t'+tbtw_conn_mean_text)
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_nodes_time_between_connections_log_all.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')
    
    

# def plot_derivative_avg(derivative_avg,derivative_std,CONFIG):
#     """ Plot the derivative of the accumulated discovery nodes """
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     # generate the columns locations
#     x = range(CONFIG['duration']) 
#     del x[-1] 
#     y_mean = derivative_avg
#     err = derivative_std
#     
#     y_top = [y_val+err_val for y_val,err_val in zip(y_mean,err)]
#     y_bottom = [y_val-err_val for y_val,err_val in zip(y_mean,err)]
# 
#     ax.fill_between(x,y_top,y_bottom,color='greenyellow')
#     ax.plot(x,y_mean,color='green')
#     
#     ax.set_xlabel("Time (s)")
#     ax.set_ylabel("Discovery rate")
#     ax.set_title("Nodes discovery rate [avg]\n"+get_algo_params(CONFIG))
#     x_dimension = CONFIG['duration']
#     ax.set_xlim([0,x_dimension])
#     ax.grid(True)
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_discovery_rate_std.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')
    
    
    
# def plot_final_positions_avg(drone_pos_l,CONFIG):
#     """ Plot the drones final positions """
#     
#     colors_cycler = plot_settings()
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     drone_ordered = zip(*drone_pos_l)
#             
#     for drone_i in range(len(drone_ordered)):
#         last_pos = []
#         
#         for sim_i in drone_ordered[drone_i]:
#             last_pos.append(sim_i[-1]) # take only the final position of each simulation
#         
#         drone_i_pos = zip(*last_pos)
#         x_pos = drone_i_pos[0]
#         y_pos = drone_i_pos[1]
#         
#         curr_color = next(colors_cycler)
#         ax.scatter(x_pos,y_pos,label='drone '+str(drone_i),marker='x',color=curr_color)
# 
#     
#     ax.set_xlabel("x coordinate (m)")
#     ax.set_ylabel("y coordinate (m)")
#     ax.set_title("Drones' final positions [all iterations]\n"+get_algo_params(CONFIG))
#     x_dimension = CONFIG['area_dimens'][0]
#     y_dimension = CONFIG['area_dimens'][1]
#     ax.set_xlim([0,x_dimension])
#     ax.set_ylim([0,y_dimension])
#     ax.grid(True)
#     ax.legend(bbox_to_anchor=(1.02,1.02), loc='upper left')
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_final_positions_avg.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')
    
    

def plot_final_positions_2_avg(drone_pos_l,CONFIG, file_report):
    """ Plot the drones final positions coloring each simulation with a different color """
    
    colors_cycler = plot_settings()
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
                
    for i in range(len(drone_pos_l)):
        last_pos = []
        
        for drone_i in drone_pos_l[i]:
            last_pos.append(drone_i[-1]) # take only the final position of each simulation
         
        sim_i_pos = zip(*last_pos)
        x_pos = sim_i_pos[0]
        y_pos = sim_i_pos[1]
        
        curr_color = next(colors_cycler)
        ax.scatter(x_pos,y_pos,label='simulation '+str(i),marker='x',color=curr_color)

    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Drones' final positions [all iterations]\n"+get_algo_params(CONFIG))
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.grid(True)

    # text
    # calculate number of drones within cluster
    clusters = CONFIG['clusters']
    margin = CONFIG['cluster_edgewidth'] 
    
    dr_in = 0
    dr_out = 0
    
    for pos_drones in drone_pos_l:
        
        # Check final position for each drone    
        for drone_i in range(len(pos_drones)):
            
            drone_pos = pos_drones[drone_i]
            pos_last = drone_pos[-1]
            any_in = 0
            
            # we check all the clusters
            for i,cluster_i in enumerate(clusters):
                origin = cluster_i[0]
                dimension = cluster_i[1]
                
                if geometry.is_within_area(pos_last,origin,dimension,margin):
                    any_in = 1
                
            if any_in:
                dr_in = dr_in+1
            else:
                dr_out = dr_out+1
    
    percent_in = 100*float(dr_in)/(dr_in+dr_out)
    percent_out = 100*float(dr_out)/(dr_in+dr_out)
    
    dr_in_text = 'Within cluster: '+str(dr_in)
    in_percent_text = 'Within cluster (%): '+format(percent_in, '.2f')
    dr_out_text = 'Out of cluster: '+str(dr_out)
    out_percent_text = 'Out of cluster (%): '+format(percent_out, '.2f')
    
    ax.annotate(dr_in_text+'\n'+in_percent_text+'\n'+dr_out_text+'\n'+out_percent_text, xy=(1.05,0), xycoords='axes fraction')

    if file_report != None:
        file_report.write("\nDrones' final positions [all iterations]\n")
        file_report.write('\t'+dr_in_text+'\n\t'+in_percent_text+'\n\t'+dr_out_text+'\n\t'+out_percent_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_final_positions_2_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



# def plot_nb_final_avg(nb_pos_l,CONFIG):
#     """ Plot the final positions of the neighbors best per each simulation """
#     
#     colors_cycler = plot_settings()
#     
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     
#     for i in range(len(nb_pos_l)):
#         nb_last_pos = []
#         
#         for drone_i in nb_pos_l[i]:
#             nb_last_pos.append(drone_i[-1]) # take only the final position of each simulation
#          
#         sim_i_pos = zip(*nb_last_pos)
#         x_pos = sim_i_pos[0]
#         y_pos = sim_i_pos[1]
#         
#         curr_color = next(colors_cycler)
#         ax.scatter(x_pos,y_pos,label='simulation '+str(i),marker='x',color=curr_color)
# 
#     
#     ax.set_xlabel("x coordinate (m)")
#     ax.set_ylabel("y coordinate (m)")
#     ax.set_title("Drones' neighbors best final positions [all iterations]\n"+get_algo_params(CONFIG))
#     x_dimension = CONFIG['area_dimens'][0]
#     y_dimension = CONFIG['area_dimens'][1]
#     ax.set_xlim([0,x_dimension])
#     ax.set_ylim([0,y_dimension])
#     ax.grid(True)
#     #ax.legend(bbox_to_anchor=(1.02,1.02), loc='upper left') # commented bcs the legend is too big for a high number of sims
#     
#     # save images into the simulation folder
#     # SAVE INTO OTHER IMAGE FORMATS: eps,png...
#     fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_neighbest_pos_final_avg.svg',format='svg',dpi=600,bbox_inches='tight')
#     plt.close('all')

        
        
def plot_acc_quartile_avg(quartile_avg,quartile_std,CONFIG, file_report):
    """ Plot the accumulated discovery quartile average """
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    q_1 = int(CONFIG['nodes_amount']/4)
    q_2 = int(CONFIG['nodes_amount']/2)
    q_3 = int(3*CONFIG['nodes_amount']/4)
    
    y_mean = quartile_avg
    err = quartile_std
    
    x_vals = range(len(y_mean))
    width = 0.8
    
    ax.bar(x_vals,y_mean,width,color='greenyellow',yerr=err)
        
    ax.set_xlabel("Percentage of nodes discovered")
    ax.set_ylabel("Time (s)")
    ax.set_title("Time up to discovery [avg]\n"+get_algo_params(CONFIG))
    ax.grid(True)
    
    if matplotlib.__version__ == '2.0.2':
        xtick_pos = x_vals
    else:
        xtick_pos = [val+(width/2) for val in x_vals]

    ax.set_xticks(xtick_pos)
    ax.set_xticklabels(('25 %','50 %','75 %','100 %'))
    
    #text 
    y_sublist = y_mean.tolist() 
    y_sublist_e = err.tolist() 
    q_1_text = '25%: '+format(y_sublist[0], '.1f')+'   dev: '+format(y_sublist_e[0], '.1f')
    q_2_text = '50%: '+format(y_sublist[1], '.1f')+'   dev: '+format(y_sublist_e[1], '.1f')
    q_3_text = '75%: '+format(y_sublist[2], '.1f')+'   dev: '+format(y_sublist_e[2], '.1f')
    q_4_text = '100%: '+format(y_sublist[3], '.1f')+'   dev: '+format(y_sublist_e[3], '.1f')
    
    # bars mean for sim analysis
    qs_mean_text = 'Mean of q-bars: '+format(np.mean(y_mean), '.1f')
        
    ax.annotate(q_1_text+'\n'+q_2_text+'\n'+q_3_text+'\n'+q_4_text+'\n'+qs_mean_text, xy=(1.05,0), xycoords='axes fraction')
     
    if file_report != None:
        file_report.write("\nTime up to discovery [avg]\n")
        file_report.write('\t'+q_1_text+'\n\t'+q_2_text+'\n\t'+q_3_text+'\n\t'+q_4_text+'\n\t'+qs_mean_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_acc_quartile_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



def plot_encounters_avg(drone_enc_avg, drone_enc_std, total_enc_avg, total_enc_std, CONFIG, file_report):
    """ Plot average drones encounters"""

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    # generate the columns locations
    x = range(CONFIG['duration']) 
    y_mean = drone_enc_avg
    err = drone_enc_std
     
    y_top = [y_val+err_val for y_val,err_val in zip(y_mean,err)]
    y_bottom = [y_val-err_val for y_val,err_val in zip(y_mean,err)]
 
    ax.fill_between(x,y_top,y_bottom,color='greenyellow')
    ax.plot(x,y_mean,color='green')
        
    ax.set_xlabel("Time(s)")
    ax.set_ylabel("Number of drone encounters")
    ax.set_title("Drone encounters per time [avg]\n"+get_algo_params(CONFIG))
    ax.grid(True)
    x_max = CONFIG['duration']
    y_min=-1
    ax.set_xlim([0,x_max])
    ax.set_ylim(ymin=y_min) # avoids the text to appear below the figure when the y axis does not have values in '0'
    
    # text
    y_sublist = y_mean[0:CONFIG['pso_params'][3]].tolist() # 3 corresponds to lb_start
    in_max_val = max(y_sublist)
    in_max_index = [i for i,j in enumerate(y_sublist) if j == in_max_val] # get all max values occurrences 
    in_max_pos = x[in_max_index[-1]] # take the last max value of the range
    if CONFIG['algorithm'] == 'pso':
        in_max_text = 'inertia max (x,y): ('+format(in_max_pos, '.1f')+',  '+format(in_max_val, '.1f')+')'
    else:
        in_max_text = '1st stage max (x,y): ('+format(in_max_pos, '.1f')+',  '+format(in_max_val, '.1f')+')'

    y_sublist = y_mean[CONFIG['pso_params'][3]:CONFIG['pso_params'][5]].tolist() # 5 corresponds to nb_start
    lb_max_val = max(y_sublist)
    lb_max_index = [i for i,j in enumerate(y_sublist) if j == lb_max_val] # get all max values occurrences
    lb_max_pos = x[lb_max_index[-1]+CONFIG['pso_params'][3]]  # add the start of the lb range
    if CONFIG['algorithm'] == 'pso':
        lb_max_text = 'lb max (x,y): ('+format(lb_max_pos, '.1f')+',  '+format(lb_max_val, '.1f')+')'
    else:
        lb_max_text = '2nd stage max (x,y): ('+format(lb_max_pos, '.1f')+',  '+format(lb_max_val, '.1f')+')'
    
    y_sublist = y_mean[CONFIG['pso_params'][5]:CONFIG['duration']].tolist()
    nb_max_val = max(y_sublist)
    nb_max_index = [i for i,j in enumerate(y_sublist) if j == nb_max_val] # get all max values occurrences
    nb_max_pos = x[nb_max_index[-1]+CONFIG['pso_params'][5]]
    if CONFIG['algorithm'] == 'pso':
        nb_max_text = 'nb max (x,y): ('+format(nb_max_pos, '.1f')+',  '+format(nb_max_val, '.1f')+')'
    else:
        nb_max_text = '3rd stage max (x,y): ('+format(nb_max_pos, '.1f')+',  '+format(nb_max_val, '.1f')+')'
    
    total_text = 'Total encounters (avg): '+str(total_enc_avg)
    deviation_text = 'dev : '+format(total_enc_std, '.2f')
    
    encounters_mean_text = 'Mean of encounters: '+format(np.mean(y_mean), '.1f') 
    
    ax.annotate(in_max_text+'\n'+lb_max_text+'\n'+nb_max_text+'\n'+total_text+'\n'+deviation_text+'\n'+encounters_mean_text, xy=(1.05,0), xycoords='axes fraction')
    
    if file_report != None:
        file_report.write("\nDrone encounters per time [avg]\n")
        file_report.write('\t'+in_max_text+'\n\t'+lb_max_text+'\n\t'+nb_max_text+'\n\t'+total_text+'\n\t'+deviation_text+'\n\t'+encounters_mean_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_encounters_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



def plot_graph_stats(drone_last_gr_l, CONFIG, file_report):
    """ Plot drones graph statistics"""

    # number of subgraphs
    # -------------------
    fig = plt.figure()
    ax = fig.add_subplot(111)
       
    # get number of subgraphs
    sgraph_num_l =  [len(sorted(nx.connected_components(graph_i))) for graph_i in drone_last_gr_l]
    max_sgr_num = max(sgraph_num_l)
    bins_vals = range(CONFIG['drones_amount']+2) # we add 2 more units to the bins_vals list, later we remove the last 2 bins_edges of the ticks
    
#     if max_sgr_num == 1:
#         bins_vals = range(12) 
#     else:
#         bins_vals = range(max_sgr_num+2) # we add 2 more units to the bins_vals list, later we remove the last 2 bins_edges of the ticks
        
    ax.hist(sgraph_num_l, bins=bins_vals, normed=False, color='greenyellow')
    
    ax.grid(True)
    xtick_pos = [ bin_ledge+0.5 for i,bin_ledge in enumerate(bins_vals) ]
    xtick_pos = xtick_pos[0:-1] # remove two last ticks
    ax.set_xticks(xtick_pos)
    
    ticks = []
    for i,pos_i in enumerate(xtick_pos):
        ticks.append(str(i)) # pos_i is not used, we only are interested in the label here
            
    ax.set_xticklabels(tuple(ticks))
    
    ax.set_xlabel("Drone subgraphs")
    ax.set_ylabel("Frequency")
    ax.set_title("Number of drone subgraphs\n"+get_algo_params(CONFIG))
    x_limits = ax.get_xlim()
    x_dimension = bins_vals[-1]+0.5
    ax.set_xlim([x_limits[0],x_dimension])
    
    # calculate average and standard deviation
    np_sgraph_num = np.asarray(sgraph_num_l)
    sgraph_num_avg = np.mean(np_sgraph_num)
    sgraph_num_std = np.std(np_sgraph_num) 
    
    # text  
    sorted_l = sorted(sgraph_num_l, reverse=True)
    max_pos = sorted_l[0]
    max_val = sgraph_num_l.count(sorted_l[0])
    
    # get second maximum value
    second_max_pos = 0
    for i,val in enumerate(sorted_l):
        if i == 0:
            # if there is no second max, the second max will equal to the max
            second_max_pos = val
        else:
            if second_max_pos == val:
                pass
            else:
                # the first value that is not the maximum
                second_max_pos = val
                break
    
    second_max_val = sgraph_num_l.count(second_max_pos)
    
    max_text = 'Max val: '+format(max_pos, '.1f')+'   Freq: '+format(max_val, '.1f') 
    second_max_text =  'Second max: '+format(second_max_pos, '.1f')+'   Freq: '+format(second_max_val, '.1f')
    
    total_text = 'Total number of drone subgraphs (avg): '+format(sgraph_num_avg, '.1f')
    deviation_text = 'dev : '+format(sgraph_num_std, '.1f')
    
    hist_y_vals = np.histogram(sgraph_num_l,bins=bins_vals,normed=False)[0]
    drsubgraph_mean_text = 'Mean of dr-subgraph bars: '+format(np.mean(hist_y_vals), '.1f')
    
    ax.text(x_dimension+0.1,0,max_text+'\n'+second_max_text+'\n'+total_text+'\n'+deviation_text+'\n'+drsubgraph_mean_text)
    
    if file_report != None:
        file_report.write("\nNumber of drone subgraphs\n")
        file_report.write('\t'+max_text+'\n\t'+second_max_text+'\n\t'+total_text+'\n\t'+deviation_text+'\n\t'+drsubgraph_mean_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_subgraphs_num_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')
    
    
    # number of drones per subgraphs
    # ------------------------------
    fig = plt.figure()
    ax = fig.add_subplot(111)
     
    # get number of drones per subgraphs
    sgraph_nodes_num_l =  [len(sgraph_i) for graph_i in drone_last_gr_l for sgraph_i in nx.connected_component_subgraphs(graph_i)]
    max_sgr_nodes_num = max(sgraph_nodes_num_l)
    bins_vals = range(CONFIG['drones_amount']+2) # we add 2 more units to the bins_vals list, later we remove the last 2 bins_edges of the ticks
    
#     if max_sgr_nodes_num == 1:
#         bins_vals = range(12) 
#     else:
#         bins_vals = range(max_sgr_nodes_num+2) # we add 2 more units to the bins_vals list, later we remove the last 2 bins_edges of the ticks
         
    ax.hist(sgraph_nodes_num_l, bins=bins_vals, normed=False, edgecolor='black', color='green')
     
    xtick_pos = [ bin_ledge+0.5 for i,bin_ledge in enumerate(bins_vals) ]
    xtick_pos = xtick_pos[0:-1] # remove two last ticks
    ax.set_xticks(xtick_pos)
     
    ticks = []
    for i,pos_i in enumerate(xtick_pos):
        ticks.append(str(i)) # pos_i is not used, we only are interested in the label here
             
    ax.set_xticklabels(tuple(ticks))
     
    ax.set_xlabel("Number of drones per subgraph")
    ax.set_ylabel("Frequency")
    ax.set_title("Number of drones per subgraph\n"+get_algo_params(CONFIG))
    x_limits = ax.get_xlim()
    x_dimension = bins_vals[-1]+0.5
    ax.set_xlim([x_limits[0],x_dimension])
     
    # calculate average and standard deviation
    np_sgraph_nodes_num = np.asarray(sgraph_nodes_num_l)
    sgraph_nodes_num_avg = np.mean(np_sgraph_nodes_num)
    sgraph_nodes_num_std = np.std(np_sgraph_nodes_num) 
     
    # text
    counter_dict = Counter(sgraph_nodes_num_l)
    tuple_l = sorted(zip(counter_dict.values(),counter_dict.keys()), reverse=True)
    max_val,max_pos = tuple_l[0]
    if len(tuple_l) >= 2:
        second_max_val,second_max_pos = tuple_l[1]
    else:
        second_max_val,second_max_pos = tuple_l[0]
    
    max_text = 'Max val: '+format(max_pos, '.1f')+'   Freq: '+format(max_val, '.1f') 
    second_max_text =  'Second max: '+format(second_max_pos, '.1f')+'   Freq: '+format(second_max_val, '.1f')
    
    total_text = 'Total number of drones per subgraph (avg): '+format(sgraph_nodes_num_avg, '.1f')
    deviation_text = 'dev : '+format(sgraph_nodes_num_std, '.1f')
    
    hist_y_vals = np.histogram(sgraph_nodes_num_l,bins=bins_vals,normed=False)[0]
    dr_per_sgraph_mean_text = 'Mean of drones per subgraph bars: '+format(np.mean(hist_y_vals), '.1f')

    ax.text(x_dimension+0.1,0,max_text+'\n'+second_max_text+'\n'+total_text+'\n'+deviation_text+'\n'+dr_per_sgraph_mean_text)
    
    if file_report != None:
        file_report.write("\nNumber of drone per subgraphs\n")
        file_report.write('\t'+max_text+'\n\t'+second_max_text+'\n\t'+total_text+'\n\t'+deviation_text+'\n\t'+dr_per_sgraph_mean_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_drones_per_subgraph_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')
    
    

def plot_drones_in_cluster_avg(drone_pos_l,CONFIG, file_report):
    """ Plot the final position average of each drone in relation with a cluster"""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)    
    
    # get clusters 
    clusters = CONFIG['clusters']
    total_clusters = len(clusters)
    margin = CONFIG['cluster_edgewidth']
    drone_per_cluster_l = []
     
    # For each simulation 
    for i in range(len(drone_pos_l)):
        final_pos = []
        
        aux_drone_per_cluster = []
        
         # Get drones latest positions
        for drone_i in drone_pos_l[i]:
            final_pos.append(drone_i[-1]) # take only the final position of each simulation

        # check the drones in each cluster
        for cluster_i in clusters:
            origin = cluster_i[0]
            dimension = cluster_i[1]
            
            drone_count = 0
            
            for pos in final_pos:
                if geometry.is_within_area(pos,origin,dimension,margin): 
                    drone_count += 1
                else:
                    pass
            
            aux_drone_per_cluster.append(drone_count)
        
        drone_per_cluster_l.append(aux_drone_per_cluster)
        
    
    # statistics calculations
    drone_per_cluster_l_zip = zip(*drone_per_cluster_l)
    np_drone_per_cluster = np.asarray(drone_per_cluster_l_zip)
    drone_per_cluster_avg = np.mean(np_drone_per_cluster, axis=1) 
    drone_per_cluster_std = np.std(np_drone_per_cluster, axis=1)
    
    y_mean = drone_per_cluster_avg
    err = drone_per_cluster_std

    bars_loc = range(total_clusters)
    width = 0.8
    
    ax.bar(bars_loc,y_mean,width,color='greenyellow',yerr=err)
        
    ax.set_xlabel("Clusters")
    ax.set_ylabel("Number of drones")
    ax.set_title("Drones per cluster [avg]\n"+get_algo_params(CONFIG))
    ax.grid(True)

    if matplotlib.__version__ == '2.0.2':
        xtick_pos = bars_loc
    else:
        xtick_pos = [val+(width/2) for val in bars_loc]

    ax.set_xticks(xtick_pos)
    ticks = []
    
    for i in bars_loc:
        ticks.append('cluster '+str(int(i+1-0.2))) 
        
    ax.set_xticklabels(tuple(ticks))
    
    # text
    y_sublist = y_mean.tolist() 
    y_sublist_e = err.tolist() 
    
    clusters_text = ''
    
    for i in range(total_clusters):
        ci_text = 'cluster'+str(i)+': '+format(y_sublist[i], '.1f')+'   dev: '+format(y_sublist_e[i], '.1f')
        clusters_text = clusters_text+ci_text+'\n'
    
    
    drcluster_mean_text = 'Mean of drones per cluster: '+format(np.mean(y_mean), '.1f')
    
    x_dimension = total_clusters
    all_text = 'Total clusters: '+str(total_clusters)    
    ax.annotate(clusters_text+all_text+'\n'+drcluster_mean_text, xy=(1.05,0), xycoords='axes fraction')

    if file_report != None:
        file_report.write("\nDrones per cluster [avg]\n")
        c_report_text=clusters_text[:-1].replace('\n','\n\t')

        file_report.write('\t'+c_report_text+'\n\t'+all_text+'\n\t'+drcluster_mean_text)

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_drone_per_cluster_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



def plot_time_to_cluster_avg(drone_pos_l,CONFIG, file_report):
    """ Plots the time needed for the drones to converge flying within a cluster"""
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    convergence_l = []
    clusters = CONFIG['clusters']
    margin = CONFIG['cluster_edgewidth'] 
    
    for pos_drones in drone_pos_l:
        
        drones_convergence = []
        
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
        
        convergence_l.append(drones_convergence)
    
    # statistics calculations
    convergence_l_zip = zip(*convergence_l)
    np_convergence = np.asarray(convergence_l_zip)
    convergence_avg = np.mean(np_convergence, axis=1) 
    convergence_std = np.std(np_convergence, axis=1)
    
    y_mean = convergence_avg
    err = convergence_std   
    
    # generate the columns locations
    bars_loc = range(CONFIG['drones_amount']) 
    width = 0.8
    
    ax.bar(bars_loc, y_mean, width, color='greenyellow',yerr=err)

    ax.set_xlabel("Drones")
    ax.set_ylabel("Time")
    ax.set_title("Convergence time in a cluster [avg]\n"+get_algo_params(CONFIG))
    ax.grid(True)
    
    if matplotlib.__version__ == '2.0.2':
        xtick_pos = bars_loc
    else:
        xtick_pos = [val+(width/2) for val in bars_loc]

    ax.set_xticks(xtick_pos)
    ticks = []
    
    for i in bars_loc:
        ticks.append('drone '+str(int(i-0.2))) 
        
    ax.set_xticklabels(tuple(ticks))
    
    # text
    y_sublist = y_mean.tolist() 
    y_sublist_e = err.tolist() 
    
    for i,val in enumerate(y_sublist):
        if i == 0:
            dr_text = 'dr0: '+format(y_sublist[0], '.1f')+'   dev: '+format(y_sublist_e[0], '.1f')
        else:
            dr_text = dr_text+'\ndr'+str(i)+': '+format(y_sublist[i], '.1f')+'   dev: '+format(y_sublist_e[i], '.1f')
      
    x_dimension=CONFIG['drones_amount']
    dr_mean_text = 'Mean of dr-convergence bars: '+format(np.mean(y_sublist), '.1f')+'\n'
    all_text = dr_mean_text+'dev: '+format(np.std(np_convergence),'.2f')
    ax.text(x_dimension+0.05,0,dr_text+'\n'+all_text)
    
    if file_report != None:
        file_report.write("\nConvergence time in a cluster [avg]\n")
        dr_text_2 = dr_text.replace('\n','\n\t')
        all_text_2 = all_text.replace('\n','\n\t')
        file_report.write('\t'+dr_text_2+'\n\t'+all_text_2)
        file_report.write('\n')

    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_convergence_avg.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')



def plot_scenario(nodes_xpos,nodes_ypos,CONFIG):
    """ Plots a snapshot of the scenario at timestamps 0 and the last """
    
    fig = plt.figure()
    
    # timestamp 0
    ax = fig.add_subplot(121)
    
    ax.plot(nodes_xpos[0],nodes_ypos[0],linestyle='None',marker='.',color='green')
    
    ax.set_xlabel("x coordinate (m)")
    ax.set_ylabel("y coordinate (m)")
    ax.set_title("Nodes map at time=0\n"+get_algo_params(CONFIG))
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.set_aspect('equal')
    
    # last timestamp
    ax = fig.add_subplot(122)
    
    ax.plot(nodes_xpos[1],nodes_ypos[1],linestyle='None',marker='.',color='green')
    
    ax.set_xlabel("x coordinate (m)")
#     #ax.set_ylabel("y coordinate (m)") # y_label is equal for both subplots
    ax.set_title("Nodes map at last time="+str(CONFIG['duration'])+"\n"+get_algo_params(CONFIG))
    x_dimension = CONFIG['area_dimens'][0]
    y_dimension = CONFIG['area_dimens'][1]
    ax.set_xlim([0,x_dimension])
    ax.set_ylim([0,y_dimension])
    ax.set_aspect('equal')
    
    # save images into the simulation folder
    # SAVE INTO OTHER IMAGE FORMATS: eps,png...
    fig.savefig(CONFIG['main_output_folder']+'/'+CONFIG['algorithm']+'_'+CONFIG['timestamp']+'_nodes_map.svg',format='svg',dpi=600,bbox_inches='tight')
    plt.close('all')




def plot_all(value_files, CONFIG, report_file=None):   



    # UPDATE TIME
    # -----------
#     LIGHT_SIM
#     nodes_per_time_l, pos_per_time_l, total_nodes_l = parsers_avg.parser_update_time_avg(value_files, CONFIG)  
#     
#     nodes_time = zip(*nodes_per_time_l) # now first dimension corresponds to time
#     np_nodes_time = np.asarray(nodes_time)    
#     nodes_time_avg = np.mean(np_nodes_time, axis=1) 
#     nodes_time_std = np.std(np_nodes_time, axis=1)
#       
#     np_total_nodes = np.asarray(total_nodes_l)
#     total_nodes_avg = np.mean(np_total_nodes)
#     total_nodes_std = np.std(np_total_nodes)
#     
#     plot_update_time_avg(nodes_time_avg, total_nodes_avg, CONFIG)
#     plot_update_time_std(nodes_time_avg, nodes_time_std, total_nodes_avg, total_nodes_std, CONFIG)


    # ACCUMULATED DISCOVERED
    # ----------------------
    discovered_l = parsers_avg.parser_acc_discovered_avg(value_files, CONFIG)
    
    # statistics calculations
    discovered_l_zip = zip(*discovered_l)
    np_discovered = np.asarray(discovered_l_zip)
    discovered_avg = np.mean(np_discovered, axis=1) 
    discovered_std = np.std(np_discovered, axis=1)
    
    plot_acc_discovered_avg(discovered_avg,discovered_std,CONFIG, report_file)    
    
    # DISCOVERED PER TIME
    #--------------------
    discovered_per_time_l = parsers_avg.parser_discovered_per_time_avg(value_files)
    
    # statistics calculations
    discovered_per_time_l_zip = zip(*discovered_per_time_l)
    np_discovered_per_time = np.asarray(discovered_per_time_l_zip)
    discovered_per_time_avg = np.mean(np_discovered_per_time, axis=1) 
    discovered_per_time_std = np.std(np_discovered_per_time, axis=1)
    
    plot_discovered_per_time_avg(discovered_per_time_avg,discovered_per_time_std,CONFIG, report_file)
    
    
    # NODES STATISTICS
    #-----------------
    nodes_events_l,nodes_frequency_l,nodes_time_btw_conn_l = parsers_avg.parser_nodes_statistics_avg(value_files,CONFIG['nodes_amount'],CONFIG['duration'])
    plot_nodes_statistics_avg(nodes_events_l, nodes_frequency_l, nodes_time_btw_conn_l, CONFIG, report_file)


    # DISCOVERY RATE
    # --------------
    # using the 'parser_acc_discovered_avg' of before
    
    # statistics calculations   
#    LIGHT_SIM
#     derivative_l = []
#     
#     for i in range(len((discovered_l))):
#         aux = []
#         for j in range(len(discovered_l[i])):
#             if j != len(discovered_l[i])-1:
#                 diff = discovered_l[i][j+1] - discovered_l[i][j]
#                 aux.append(diff)
#             else:
#                 # not defined for the last element of the list
#                 pass   
#         
#         derivative_l.append(aux) 
#     
#     
#     derivative_l_zip = zip(*derivative_l)
#     np_derivative = np.asarray(derivative_l_zip)
#     derivative_avg = np.mean(np_derivative, axis=1) 
#     derivative_std = np.std(np_derivative, axis=1)
#     
#     plot_derivative_avg(derivative_avg,derivative_std,CONFIG)
    
    
    # FINAL POSITIONS
    # --------------
    drone_pos_l = parsers_avg.parser_positions_avg(value_files, CONFIG)
    
#     plot_final_positions_avg(drone_pos_l,CONFIG) # LIGHT_SIM
    plot_final_positions_2_avg(drone_pos_l,CONFIG, report_file)
    
    
    # NEIGHBORS BEST FINAL POSITIONS
    #-------------------------------
#     LIGHT_SIM
#     nb_pos_l = parsers_avg.parser_neighborsbest_avg(value_files, CONFIG)
#     plot_nb_final_avg(nb_pos_l,CONFIG)
    
    
    # ACCUMULATED QUARTILE
    # ---------------------
    # discovered_l read before
    
    q_1 = int(CONFIG['nodes_amount']/4)
    q_2 = int(CONFIG['nodes_amount']/2)
    q_3 = int(3*CONFIG['nodes_amount']/4)
    
    quartile_l = []
    
    for sim_i in discovered_l:   
        
        values = [None,None,None,None]
    
        for i,val in enumerate(sim_i):
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
        quartile_l.append(y_vals)
    
    # statistics calculations
    quartile_l_zip = zip(*quartile_l)
    np_quartile = np.asarray(quartile_l_zip)
    quartile_avg = np.mean(np_quartile, axis=1) 
    quartile_std = np.std(np_quartile, axis=1)
    
    plot_acc_quartile_avg(quartile_avg,quartile_std,CONFIG, report_file)
    
    
    # DRONES ENCOUNTERS
    #------------------
    drone_enc_l, drone_enc_total_l, drone_last_gr_l = parsers_avg.parser_encounters_avg(value_files, CONFIG)
    
    # statistics calculations
    drone_enc_l_zip = zip(*drone_enc_l)
    np_drone_enc = np.asarray(drone_enc_l_zip)
    drone_enc_avg = np.mean(np_drone_enc, axis=1) 
    drone_enc_std = np.std(np_drone_enc, axis=1)   
    
    np_total_enc = np.asarray(drone_enc_total_l)
    total_enc_avg = np.mean(np_total_enc)
    total_enc_std = np.std(np_total_enc) 
    
    plot_encounters_avg(drone_enc_avg, drone_enc_std, total_enc_avg, total_enc_std, CONFIG, report_file)
    
    
    # GRAPH STATISTICS
    #-----------------
    drone_enc_l, drone_enc_total_l, drone_last_gr_l = parsers_avg.parser_encounters_avg(value_files, CONFIG)
    plot_graph_stats(drone_last_gr_l, CONFIG, report_file)
    
    
    # DRONES PER CLUSTER
    #--------------------
    drone_pos_l = parsers_avg.parser_positions_avg(value_files, CONFIG)
    plot_drones_in_cluster_avg(drone_pos_l,CONFIG, report_file)
    
    
    # Time to convergence in cluster
    #--------------------------------
    drone_pos_l = parsers_avg.parser_positions_avg(value_files, CONFIG)
    plot_time_to_cluster_avg(drone_pos_l,CONFIG, report_file)
    
    
    # Scenario nodes
    #-----------------
    # check if this figure was already created   
#     command = ['find',CONFIG['main_output_folder'],'-maxdepth','1','-name','*_nodes_map.svg']
#     popen_proc = Popen(command,stdout=PIPE) 
#     prev_figure = popen_proc.stdout.read()
#      
#     if not prev_figure:
#         nodes_xpos,nodes_ypos = parsers.parser_wml_boundaries(CONFIG['input_file'])
#     
#         plot_scenario(nodes_xpos,nodes_ypos,CONFIG) 
    
    

    