# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 21:57:11 2018

@author: mali
"""

"""
Created on Tue Jul 10 20:11:33 2018

@author: mali
"""


"""
Created on Tue Jul  3 09:35:59 2018

@author: mali
"""

import sys 
#print sys.path

print sys.path
import time 
import os
import logging
import numpy as np
import pickle
import spynnaker8 as sim 

from pyNN.space import Grid2D
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import print_chs as prnt
import Gabor_weights as GB
import comn_conversion as cnvrt
import c_rtna_cls as RTNA
import c_rf_cls as RF
import c_cnet_cls_v5 as cnet
#logger = logging.getLogger(__file__)



# ================== functin to print chs of cnet =============================
def prnt_cnet_rw_cl_dsp_x_info ( n_lyrs, c_net):    
    print '\n \n################## number of layers: {}'.format(n_lyrs)
    for lyr in range( n_lyrs ):
        print'#### lyr_{} :: \n   ##nrns_in_rows = {} \n   ##nrns_in_cols= {}'.format(lyr, c_net[lyr]._row_nrns, c_net[lyr]._col_nrns)
        print'   ##_L_nrns = {} \n   ##_R_nrns= {}'.format( c_net[lyr]._L_nrns, c_net[lyr]._R_nrns)
    print ' '
    for lyr in range( n_lyrs ):
        print'\n#### lyr_{} :: '.format( lyr )        
        print'   ##_L_nrns = {} \n   ##_R_nrns = {}'.format( c_net[lyr]._L_nrns, c_net[lyr]._R_nrns)
        for rw in range ( c_net[lyr]._n_rows ):
            print'   ##nrns_in_row [{}]      = {}'.format(rw, c_net[lyr]._row_nrns[rw])
        for cl in range ( c_net[lyr]. _n_cols ):
            print'   ##nrns_in_col [{}]      = {}'.format(cl, c_net[lyr]._col_nrns[cl])        
        for dsp in range ( c_net[lyr]._min_dsp,  c_net[lyr]._max_dsp+1):   
            print'   ##nrns_wth_dsp_vlu[{}] = {}'.format(dsp, c_net[lyr]._dsp_nrns[dsp])
        for x in range ( c_net[lyr]._min_x, c_net[lyr]._max_x+1 ): 
            print'   ##nrns_wth_x_vlu [{}]  = {}'.format(x, c_net[lyr]._x_nrns[x])
#==============================================================================

step_t= 1
sim_t= 10.2
get_plt= 2

rtna_w = 65
rtna_h = 65
krnl_sz = 5
jmp     = 2
n_rtna  = 2
rf_orn_vect = [   2 ]
n_orn  = len ( rf_orn_vect)
rf_w = (rtna_w - krnl_sz)/jmp +1
rf_h = (rtna_h - krnl_sz)/jmp +1
n_lyrs = rf_h

# ============================== sim setup ====================================
sim.setup(timestep = step_t, min_delay=1*step_t, max_delay=10*step_t)
sim.set_number_of_neurons_per_core(sim.IF_curr_exp, 500)

#sim.setup(timestep=step_t, min_delay=1*step_t)

#sim.setup(timestep=1.0)
print '\n############################################ sim param:'
print '## get_time_step:  {}'.format ( sim.get_time_step() )
print '## get_min_delay:  {}'.format ( sim.get_min_delay() )
print '## get_max_delay:  {}'.format ( sim.get_max_delay() )



# ================= read spikes and associated variables ======================
print '\n##### loading the spike_times.pickle file as list of list of list .... '
print ' =================== real data ======================='

spks_fldr  = 'real_dataset/'
L_spk_fle  = 'pendulum_lft_20_21_10ur_lft.pickle'
R_spk_fle  = 'pendulum_rght_20_21_10ur_rght.pickle'
rslts_fldr = 'rslts/{}'.format(   spks_fldr  )
#spks_fldr  = 'lines_6/'
#L_spk_fle  = 'lines6_90_20_lft_lft.pickle'
#R_spk_fle  = 'lines6_90_20_rght_rght.pickle'
#rslts_fldr = 'rslts/{}'.format(   spks_fldr  )



#================== nrn variables and connection parameters ===================    
rf_scan_jmp= jmp

dly_rtna2rf= step_t
G_rtna2rf= 10.0
rf_lif_param = {'cm': 0.06,           'i_offset': 0.0,      'tau_m': 1.8, 
                'tau_refrac': 1.0,    'tau_syn_E': 1.5,    'tau_syn_I': 1.1,
                'v_reset': -65.0,     'v_rest': -65.0,      'v_thresh': -62.0}
# for cnet --------------------------------------------------------------------
dly_rf2cnet= 2*step_t
G_rf2cnet= 15.0  # it is in th elist generated by spin_generate
cnet_lif_param = {'cm': 0.08,           'i_offset': 0.0,      'tau_m': 0.2,  
                'tau_refrac': 2.0,    'tau_syn_E': 0.8,    'tau_syn_I': 1.0,
                'v_reset': -65.0,     'v_rest': -65.0,      'v_thresh': -61.0}
#======================= instantiate populations ==============================    
# rtna paths
L_spks_pth = cnvrt.read_flenfldr_ncrntpth( 'pkl_spk_tms/{}'.format(spks_fldr),  L_spk_fle)
R_spks_pth = cnvrt.read_flenfldr_ncrntpth( 'pkl_spk_tms/{}'.format(spks_fldr),   R_spk_fle)

# instaniate rtna -------------------------------------------------------------
L_rtna = RTNA.create_rtna( L_spks_pth , rtna_w , rtna_h, label_='L_rtna')
R_rtna = RTNA.create_rtna( R_spks_pth , rtna_w , rtna_h, label_='R_rtna')
# instantiate rf --------------------------------------------------------------
L_rf= []
R_rf= []
for rf_orn_vlu in rf_orn_vect :
    L_rf.append ( RF.create_rf( L_rtna, krnl_sz, jmp, rf_orn_vlu,  n_orn, rf_lif_param, label_='L_rf' )  )
    R_rf.append ( RF.create_rf( R_rtna, krnl_sz, jmp, rf_orn_vlu,  n_orn, rf_lif_param, label_='R_rf' )  )
# create weights as gabor filter and make connection accordingly:
c_net = []
max_dsp_=30
min_dsp_=0
for orn in range( n_orn ):
    L_rf[orn].create_gb_wghts()
    R_rf[orn].create_gb_wghts()
    
    L_rf[orn].drw_gb_wghts()
    R_rf[orn].drw_gb_wghts()
    
    L_rf[orn].conect2rtna_gb_fltr (rf_scan_jmp, dly_rtna2rf, G_rtna2rf )
    R_rf[orn].conect2rtna_gb_fltr (rf_scan_jmp, dly_rtna2rf, G_rtna2rf )   
    # instantiate cnet -----------------------------------------------------------
    c_net.append( cnet.create_cnet_lyr(L_rf[orn],  R_rf[orn], cnet_lif_param, dly_rf2cnet, G_rf2cnet,  max_dsp_, min_dsp_, label_='cnet_{}f{}'.format(rf_orn_vect[orn], n_orn-1)   )   )
#                         



#============================ characteistics ==================================    
L_rtna.prnt_chs()
R_rtna.prnt_chs()
#for orn in range( n_orn):
#    L_rf[orn].prnt_chs()
#    L_rf[orn].prnt_gb_wghts()
#    L_rf[orn].drw_gb_wghts()
#    L_rf[orn].prnt_rtna2rf_proj()
#    R_rf[orn].prnt_chs()
#    R_rf[orn].prnt_gb_wghts()
#    R_rf[orn].drw_gb_wghts()
#    R_rf[orn].prnt_rtna2rf_proj()
#for lyr in range( n_lyrs ):
#    c_net[lyr].prnt_chs()
    
#============================ Record spk,v ====================================  
# only spks ------------------------------------------------------------------
#L_rtna._pop.record(["spikes"] ) 
#R_rtna._pop.record(["spikes"] ) 

if get_plt == 1:
    for orn in range( n_orn):
        print 'record : orn_{}'.format(orn)
        L_rf[orn]._pop.record(["spikes","v"] ) #["spikes","v"]  
        R_rf[orn]._pop.record(["spikes","v"] ) #["spikes","v"]  
        print 'record : lyr_{}'.format(orn)
        c_net[orn]._pop.record(["spikes","v"] ) #["spikes","v"]  

elif get_plt == 2:
    for orn in range( n_orn):
#        print 'record : orn_{}'.format(orn)
#        L_rf[orn]._pop.record(["spikes"] ) #["spikes","v"]  
#        R_rf[orn]._pop.record(["spikes"] ) #["spikes","v"]  
        print 'record : cnet_{}'.format(orn)
        c_net[orn]._pop.record(["spikes"] ) #["spikes","v"]  


print '=========================== start simulation ==========================='      
simtime= sim_t #for neuron voltage make it small ..... for spiking extraction make more than the dataset time 
sim.run(simtime) # bet run and end ===> write_data and get_data================

# rtna to rf projection chs [weights and delays]
#for orn in range( n_orn):
#    L_rf[orn].prnt_rtna2rf_proj_chs()
#    R_rf[orn].prnt_rtna2rf_proj_chs()
#    c_net[orn].prnt_chs()
orn=0
#print c_net[orn]._Lrf2cnet_proj 
#print c_net[orn]._Lrf2cnet_proj.get('weight', format='array') 
##print c_net[orn]._Lrf2cnet_proj.get('delay', format='array')
#
#print c_net[orn]._Rrf2cnet_proj
#print c_net[orn]._Rrf2cnet_proj.get('weight', format='array') 

#print c_net[orn]._minh_proj0
#print c_net[orn]._minh_proj0.get('weight', format='array') 
#
#print c_net[orn]._minh_proj00
#print c_net[orn]._minh_proj00.get('weight', format='array') 
# ==============================  write data ==================================
if get_plt ==2:
    print '### storing data in folder:{}'.format(rslts_fldr)
#    L_rtna.write_data(  cnvrt.write_flenfldr_ncrntpth(rslts_fldr, 'L_rtna.pickle')  )
#    R_rtna.write_data(  cnvrt.write_flenfldr_ncrntpth(rslts_fldr, 'R_rtna.pickle')  )
    for orn in range( n_orn):
#        print '### storing RF data in folder: {}'.format(rslts_fldr)
#        L_rf[orn].write_data( rslts_fldr )    
#        R_rf[orn].write_data( rslts_fldr )    
        print '### storing CNET data in folder: {}'.format(rslts_fldr)
        c_net[orn]._pop.write_data(  cnvrt.write_flenfldr_ncrntpth(rslts_fldr, '{}.pickle'.format(c_net[orn]._label) )   )

if get_plt ==1:
    print '### rtnas get data: ............... '
    L_rtna.get_spks( )
    R_rtna.get_spks()
    for orn in range( n_orn):
        print '### rfs get data: orn_{}'.format( rf_orn_vect[orn] )
        L_rf[orn].get_spks()
        R_rf[orn].get_spks()
        L_rf[orn].get_v()
        R_rf[orn].get_v()
        print '### cnets get data: orn_{}'.format(  rf_orn_vect[orn]  )
        c_net[orn].get_spks()
        c_net[orn].get_v()

sim.end()
print '=========================== simulation done ============================'      


 

if get_plt ==1:
    print '### plot rtnas .............. '
#    L_rtna.plt_spks( )
    plt.show()
    for orn in range( n_orn):
        print '### rfs plot orn_{}'.format( rf_orn_vect[orn] )
        L_rf[orn].plt_spks(  L_rtna, v=1, wth_param=0)
        plt.show()
        R_rf[orn].plt_spks(  R_rtna, v=1, wth_param=0)
        plt.show()
    for orn in range( n_orn):
        print '### cnets plot orn_{}'.format(  rf_orn_vect[orn]  )
        c_net[orn].plt_spks(  L_rtna,  R_rtna, v=1, wth_param=0)
        plt.show()


    
        
        
        
        
        
        
        
