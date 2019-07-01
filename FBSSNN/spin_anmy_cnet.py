#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 10:41:45 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 09:40:29 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 23:59:05 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 20:41:29 2018

@author: mali
"""

import pickle
import comn_conversion as cnvrt 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from __main__ import *


#if you have the path directly
#pth = '/home/mali/thesis/spiNNaker/tst_bnchmrk/rslts/tst4orn_krnl3_dft500_tres0/rslts_L_rtna.pickle'
  
rtna_w = 65
rtna_h = 65
krnl_sz = 5
jmp     = 2
n_rtna  = 2
rf_orn_vect = [  2 ]
n_orn  = len ( rf_orn_vect)
rf_w = (rtna_w - krnl_sz)/jmp +1
rf_h = (rtna_h - krnl_sz)/jmp +1
n_lyrs = rf_h


#file to read 
spks_fldr  = 'real_dataset/'
rslts_fldr = 'rslts/{}'.format(   spks_fldr  )
print '#rslts_fldr: {}'.format(rslts_fldr ) 
  
pickle_filename = 'TDXY_cnet_{}f{}.pickle'.format( rf_orn_vect[0] , len(rf_orn_vect)-1 )
file_pth    = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, pickle_filename )


print '##### required variables: \n n_rtna={}, n_orn={}, rtna_w={}, rtna_h={}, krnl_sz={}, jmp={} rf_w={} , rf_h={}'.format(
 n_rtna , n_orn, rtna_w, rtna_h, krnl_sz, jmp,  rf_w , rf_h  )


T_idx = 0
D_idx = 1
X_idx = 2
Y_idx = 3



with open(file_pth , 'rb') as pkl:
    data = pickle.load(pkl)
############################################# copy from original 
###############################################func############################
    def set_axs(ax, rf_h, rf_w): #============================================
         mngr = plt.get_current_fig_manager()
#         mngr.window.setGeometry(0,0,1000, 1000)  #size of window: (x0, y0 , xf, yf) (0,0) top left 
         xtcks = range(0, rf_w ) 
         ytcks = range(0, rf_w )
         ztcks = range(0, rf_h )
         ax.set_xlim(-1,rf_w+1)
         ax.set_ylim(-1,rf_w+1)
         ax.set_zlim(-1,rf_h+1)
         ax.set_xticks(xtcks)
         ax.set_yticks(ytcks)
         ax.set_zticks(ztcks)
#         ax.set_title('coincidence network')
         ax.invert_yaxis()
         ax.invert_zaxis()
         
###############################################################################             

n_lyrs = len(data)
simtime = len(data[0][0])
print '## lngth of TDXY (n_lyrs): {}'.format( n_lyrs )
print '## simtime : {} usec'.format( simtime )
smpls= range (0,simtime,1)
smpls.append( simtime )
n_smpls = len(smpls) 
print '## n_smpls = {}'.format(n_smpls)


nrns_ID=[]
tt=[]
X=[]
Y=[]
Z=[]
for smpl in range (n_smpls -1):
    t_strt = smpls[smpl]
    t_end = smpls[smpl + 1]
    print '\n####### smpl {}: [{}:{}]'.format(smpl, t_strt, t_end)
    print '## strt_tm : {}'.format( t_strt)
    print '## strt_tm : {}'.format( t_end)
    nrns_at_smpl=[]
    x_at_smpl=[]
    y_at_smpl=[]
    z_at_smpl=[]
    t_at_smpl=[]
    for lyr in range ( n_lyrs ):
#        print '## lyr[{}] : '.format(lyr)
        for t in range ( t_strt, t_end ):
            if data[lyr][D_idx][t] !=[]:
                for nrn in data[lyr][D_idx][t] :   
                    nrns_at_smpl.append( nrn  )
                    z_at_smpl.append( lyr )
                    t_at_smpl.append(t)
#                    print 't= {}  --> nrn_id = {}'.format(t, nrn)
                for x in data[lyr][X_idx][t] :                
                    x_at_smpl.append( x  )
                for y in data[lyr][Y_idx][t] :                
                    y_at_smpl.append( y  )
                    
    nrns_ID.append( nrns_at_smpl  )
    X.append( x_at_smpl  )
    Y.append( y_at_smpl  )
    Z.append( z_at_smpl  )
    tt.append(t_at_smpl)
#    print '## tt[]               : {}'.format( smpl,    t_at_smpl   )
#    print '## nrns_at_smpl[{}] : {}'.format( smpl,         nrns_at_smpl       )
#    print '## x_at_smpl[{}]    : {}'.format( smpl,  x_at_smpl     )
#    print '## y_at_smpl[{}]    : {}'.format( smpl,   y_at_smpl    )
#    print '## z_at_smpl[{}]    : {}'.format( smpl,   z_at_smpl    )
#    print '## note that time is repeates according to n_lyrs that has spiking nrns !!! '   
    
zdsp= range(0,31)   
############ working one smpl by smpl:-----------------------------------------    
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
set_axs(ax, rf_h, rf_w)  
plt.show(block = False)
raw_input(" choose the suitable 3D view to continue...")
for smpl in range(n_smpls -1 ): 
#    if smpl ==0:
#    raw_input("  continue...")
    print '============================ sample : {} ==========================='.format(smpl)
    print '## tt      : {}'.format(  tt[smpl]  )
    print '## nrns_ID : {}'.format(  nrns_ID[smpl]  )
    print '## X       : {}'.format(  X[smpl]  )
    print '## Y       : {}'.format(  Y[smpl]  )
    print '## Z       : {}'.format(  Z[smpl]  )
    print '## note that time is repeates according to n_lyrs that has spiking nrns !!! ' 
    plt.cla()
    set_axs(ax, rf_h, rf_w) 
    ax.scatter(X[smpl], Y[smpl], Z[smpl], c='r', marker='o')
    ax.scatter(zdsp, zdsp, zdsp[0]*30, c='b', marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
#    ax.set_title( 'coincidence network, G, dly  , param \n sample{} '.format(  smpl )  )#  cnet_lif_param ) ) # G_rf2cnet, dly_rf2cnet, 
    ax.set_title( 'coincidence network:, sample={} , G={}, dly={} ,\n {} '.format(smpl, 0,   0, 0 )       )
    plt.pause(3)
plt.pause(15)
#raw_input(" choose the suitable 3D view to continue...")





        
        
        
        
        
        
        


