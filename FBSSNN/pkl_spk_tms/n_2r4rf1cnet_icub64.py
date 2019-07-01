#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 19:17:15 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 17:28:21 2018

@author: mali
"""



import time 
import os
import logging
import numpy as np
import pickle
#import spynnaker8 as sim 
#import pyNN.spiNNaker as sim


import pyNN.neuron as sim 
from pyNN.space import Grid2D
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
#from pylab import *
import seaborn as sns; sns.set()
import print_chs as prnt
import manch_gaussian as manch
import comn_conversion as cnvrt
import n_rtna_cls as RTNA
import n_rf_cls as RF
import n_cnet_cls as cnet
#logger = logging.getLogger(__file__)


# sim setup
step_tm = 0.01
sim.setup(timestep = step_tm, min_delay=0.1, max_delay=1.0)
#sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 120)
print '\n############################################ sim param:'
print '## get_time_step:  {}'.format ( sim.get_time_step() )
print '## get_min_delay:  {}'.format ( sim.get_min_delay() )
print '## get_max_delay:  {}'.format ( sim.get_max_delay() )



# load spikes times from pickle file 
print '\n###### loading the spike_times.pickle file as list of list of list .... '
#file to read
spks_fldr  = 'pkl_spk_tms/icub64x64_nsy/'
L_spk_fle  = 'icub64x64_12-8-45_lft_lft.pickle' 
R_spk_fle  = 'icub64x64_12-8-45_rght_rght.pickle'


#spks_fldr  = 'pkl_spk_tms/cnet_2lnes/'
#L_spk_fle  = 'cnet_2lnes_6x6_3-2_lft_lft.pickle' 
#R_spk_fle  = 'cnet_2lnes_6x6_3-2_rght_rght.pickle'

L_spks_pth = cnvrt.read_flenfldr_ncrntpth(spks_fldr, L_spk_fle)
R_spks_pth = cnvrt.read_flenfldr_ncrntpth(spks_fldr, R_spk_fle)

# file store
rslts_fldr =  'rslts/rtna2rf2cnet_icub_64x64/'



# instaniate rtna
L_rtna = RTNA.create_rtna( L_spks_pth , wdth_ =64, hght_=64, label_='L_rtna')
R_rtna = RTNA.create_rtna( R_spks_pth , wdth_ =64, hght_=64, label_='R_rtna')
# instantiate rf
n_orn=4
rf_scan_jmp=1
dly_rtna2rf=0.01
G_rtna2rf= 66
lif_param = {'cm': 0.2,           'i_offset': 0.0,      'tau_m': 1.1, 
                'tau_refrac': 0.1,    'tau_syn_E': 0.01,    'tau_syn_I': 01.01,
                'v_reset': -65.0,     'v_rest': -65.0,      'v_thresh': -63.0
                   }
L_rf = RF.create_rf( L_rtna, krnl_sz_=3, n_orn_=n_orn, lif_param_=lif_param, label_='L_rf' )
R_rf = RF.create_rf( R_rtna, krnl_sz_=3, n_orn_=n_orn, lif_param_=lif_param, label_='R_rf' )
#print '### to check the connection: \n{}'.format(L_rf[2]._pop)

# instantiate cnet
dly_rf2cnet= 0.01 
G_rf2cnet= 15
c_net = cnet.create_cnet_lyr(L_rf[2],  R_rf[2], lif_param, dly_rf2cnet, G_rf2cnet, label_='cnet')
n_lyrs = len(c_net)
print '\n \n################## number of layers: {}'.format(n_lyrs)
for lyr in range( n_lyrs ):
    print'#### lyr_{} :: \n   ##nrns_in_rows = {} \n   ##nrns_in_cols= {}'.format(lyr, c_net[lyr]._row_nrns, c_net[lyr]._col_nrns)
    print'   ##_L_nrns = {} \n   ##_R_nrns= {}'.format( c_net[lyr]._L_nrns, c_net[lyr]._R_nrns)

print ' '
for lyr in range( n_lyrs ):
    print'\n#### lyr_{} :: '.format( lyr )        
#    print'   ##_L_nrns = {} \n   ##_R_nrns = {}'.format( c_net[lyr]._L_nrns, c_net[lyr]._R_nrns)
#    for rw in range ( c_net[lyr]._n_rows ):
#        print'   ##nrns_in_row [{}]      = {}'.format(rw, c_net[lyr]._row_nrns[rw])
#    for cl in range ( c_net[lyr]. _n_cols ):
#        print'   ##nrns_in_col [{}]      = {}'.format(cl, c_net[lyr]._col_nrns[cl])        
    for dsp in range ( c_net[lyr]._min_dsp,  c_net[lyr]._max_dsp+1):   
        print'   ##nrns_wth_dsp_vlu[{}] = {}'.format(dsp, c_net[lyr]._dsp_nrns[dsp])
    for x in range ( c_net[lyr]._min_x, c_net[lyr]._max_x+1 ): 
        print'   ##nrns_wth_x_vlu [{}]  = {}'.format(x, c_net[lyr]._x_nrns[x])

for lyr in range( n_lyrs ):
    c_net[lyr].prnt_chs()







#chs
#L_rtna.prnt_chs()

#record rtna spks
L_rtna.record_data()
R_rtna.record_data()


for orn in range( n_orn):
#    L_rf[orn].prnt_chs()
    L_rf[orn].record_data()
#    R_rf[orn].prnt_chs()
    R_rf[orn].record_data()

    L_rf[orn].create_gb_wghts()
#    L_rf[orn].prnt_gb_wghts()
#    L_rf[orn].drw_gb_wghts()
    R_rf[orn].create_gb_wghts()
#    R_rf[orn].prnt_gb_wghts()
#    R_rf[orn].drw_gb_wghts()

    L_rf[orn].conect2rtna_gb_fltr (rf_scan_jmp, dly_rtna2rf, G_rtna2rf )
#    L_rf[orn].prnt_rtna2rf_proj()
    R_rf[orn].conect2rtna_gb_fltr (rf_scan_jmp, dly_rtna2rf, G_rtna2rf )
#    R_rf[orn].prnt_rtna2rf_proj()
for lyr in range( n_lyrs):
    c_net[lyr].record_data()   
    
    
    
#param = L_rf.get_crnt_lif_param( )
#print 'parammmmmmmmmmmmmmmmm :\n{}'.format(param)
lif_param = {'cm': 0.05,           'i_offset': 0.0,      'tau_m': 0.06, 
                'tau_refrac': 0.01,    'tau_syn_E': 0.05,    'tau_syn_I': 0.05,
                'v_reset': -65.0,     'v_rest': -65.0,      'v_thresh': -63.0}
lif_param_1 = {'cm': 0.05,           'i_offset': 0.0,      'tau_m': 0.06, 
                'tau_refrac': 0.01,    'tau_syn_E': 0.05,    'tau_syn_I': 0.05,
                'v_reset': -65.0,     'v_rest': -65.0,      'v_thresh': -63.0}

for orn in range( n_orn):
    L_rf[orn].set_lif_param_of_pop( lif_param)
#    L_rf[orn].prnt_crnt_lif_param()
    R_rf[orn].set_lif_param_of_pop( lif_param)
#    R_rf[orn].prnt_crnt_lif_param()




#run simulation ==============================================================
simtime= 1.1 #for neuron voltage make it small ..... for spiking extraction make more than the dataset time 
sim.run(simtime) # bet run and end ===> write_data and get_data================

#for orn in range( n_orn):
#    L_rf[orn].prnt_rtna2rf_proj_chs()
#    R_rf[orn].prnt_rtna2rf_proj_chs()
#



# store data
L_rtna.write_data(  cnvrt.write_flenfldr_ncrntpth(rslts_fldr, 'rslts_L_rtna.pickle')  )
R_rtna.write_data(  cnvrt.write_flenfldr_ncrntpth(rslts_fldr, 'rslts_R_rtna.pickle')  )

for orn in range( n_orn):
    L_rf[orn].write_data( rslts_fldr )    
    R_rf[orn].write_data( rslts_fldr )   
    
for lyr in range( n_lyrs):
    c_net[lyr].write_data(rslts_fldr)
    
    
# get spks, v, stop_tm
L_rtna_spks =  L_rtna.get_spks()
R_rtna_spks =  R_rtna.get_spks()
stop_time   =  L_rtna._stop_tm

L_rf_spks =[]
L_rf_v    =[]
for orn in range( n_orn):
    L_rf_spks.append(  L_rf[orn].get_spks()  )
    L_rf_v.append(     L_rf[orn].get_v()     )

R_rf_spks =[]
R_rf_v    =[]
for orn in range( n_orn):
    R_rf_spks.append(  R_rf[orn].get_spks()  )
    R_rf_v.append(     R_rf[orn].get_v()     )
    
c_net_spks =[]    
c_net_v    =[]
for lyr in range( n_lyrs):
    c_net_spks.append(  c_net[lyr].get_spks()  )
    c_net_v.append(     c_net[lyr].get_v()     )


sim.end()
#end simulation ==============================================================

        #L_rtna.prnt_chs()
        #L_rtna.plt_spks( )
for orn in range( n_orn):
    print 'plot {}'.format(L_rf[orn]._pop.label)
    L_rf[orn].plt_spks( L_rtna )
    plt.show()
for orn in range( n_orn):
    print 'plot {}'.format(R_rf[orn]._pop.label)
    R_rf[orn].plt_spks( R_rtna )
    plt.show()

for lyr in range( n_lyrs):#n_lyrs
    print '\n============================ plot {} =========================='.format(L_rf[lyr]._pop.label)
    c_net[lyr].plt_spks( )
    plt.show()
    
    
c_net[0].prnt_proj_chs()
print'\n'
c_net[1].prnt_proj_chs()
print'\n'
c_net[2].prnt_proj_chs()        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        