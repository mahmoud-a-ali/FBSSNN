
"""
Created on Sat May 26 17:30:15 2018

@author: mali
"""

import numpy as np
import spynnaker8 as sim 

#import spynnaker7 as sim 
#import pyNN.spiNNaker as sim
#import pyNN.brian as sim
from pyNN.space import Grid2D

#import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

from pylab import *
import seaborn as sns; sns.set()



def prnt_pop_chs(pop):
    print '---------------------------------- {} ch\'s --------------------------------------'.format(pop.label)
    #print 'positions                       :        {}'.format(L_rtna._positions)
    print 'size                            :        {}'.format(pop.size)
    print 'local_size                      :        {}'.format(pop.local_size)
    print 'structure                       :        {}'.format(pop.structure)
    print 'label                           :        {}'.format(pop.label)
    print 'length                          :        {}'.format(len(pop))
    print 'length__                        :        {}'.format(pop.__len__())
    print 'first_id                        :        {}'.format(pop._first_id) 
    print 'last_id                         :        {}'.format(pop._last_id)
    print 'index of first id               :        {}'.format(pop.id_to_index(pop._first_id))
    print 'all_ids                         :        {} '.format(pop._all_ids)
    print '--------------------------------------------------------------------------------------'
    
def prnt_gb_wghts(gb):
    print 'gb wght by wght'
    for i in range( len(gb) ):
        print '##gb[{}]: {}'.format(i, gb[i])
        
def draw_gb_wghts(gb, idx):
    ax = sns.heatmap(gb[idx])
    plt.show()

def prnt_conn_lst(conn_lst, n_conn):
#    print '\nconn_lst: conn by conn '
    conn_len = len(conn_lst)  # or out1_sz * out2_sz * k1_sz * k2_sz
    for conn in range(n_conn):
        print '##conn:  {}'.format(conn_lst[conn])
        
        
        
def prnt_proj( proj ):
    all_conn = len(proj)
    for prj in range(all_conn):
        print proj[prj]
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
