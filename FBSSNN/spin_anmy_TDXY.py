#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:00:59 2018

@author: mali
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 13:09:55 2018

@author: mali
"""

#import time
import pickle
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import comn_conversion as cnvrt
import prnt_plt_anmy as ppanmy
from __main__ import *

# file and folder names =======================================================

rtna_w = 65
rtna_h = 65
krnl_sz = 5
jmp =2
n_rtna  = 2
rf_orn_vect = [  2 ]
n_orn  = len ( rf_orn_vect)
rf_w = (rtna_w - krnl_sz)/jmp +1
rf_h = (rtna_h - krnl_sz)/jmp +1
n_lyrs = rf_h




subplt_rws= 2 
subplt_cls= n_orn+1

spks_fldr  = 'real_dataset/'
rslts_fldr = 'rslts/{}'.format(   spks_fldr  )
print '#rslts_fldr: {}'.format(rslts_fldr )   

print '##### required variables: \n n_rtna={}, n_orn={}, rtna_w={}, rtna_h={}, krnl_sz={}, jmp={} rf_w={} , rf_h={}'.format(
 n_rtna , n_orn, rtna_w, rtna_h, krnl_sz, jmp,  rf_w , rf_h  )

#---------------------------------------------------------------------------   
print '##rtnas files'
pickle_filename = 'TDXY_L_rtna.pickle'
file_pth    = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
with open(file_pth , 'rb') as tdxy:
    tdxy_l_rtna    = pickle.load( tdxy )
pickle_filename = 'TDXY_R_rtna.pickle'
file_pth    = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
with open(file_pth , 'rb') as tdxy:
    tdxy_r_rtna    = pickle.load( tdxy )


L_rf_files   = []
L_rf_fpath  = []
R_rf_files   = []
R_rf_fpath  = []
for orn in range(n_orn):
    L_rf_files.append(  'TDXY_L_rf_{}f{}.pickle'.format(    rf_orn_vect[orn], n_orn-1      )   )
    L_rf_fpath.append(  cnvrt.read_flenfldr_ncrntpth(  rslts_fldr, L_rf_files[orn]  )   )
    R_rf_files.append(  'TDXY_R_rf_{}f{}.pickle'.format(    rf_orn_vect[orn], n_orn-1      )   )
    R_rf_fpath.append(  cnvrt.read_flenfldr_ncrntpth(  rslts_fldr, R_rf_files[orn]  )    )

tdxy_l_rf=[]
tdxy_r_rf=[]
for orn in range(n_orn):
    print '##left files' 
    with open(L_rf_fpath[orn] , 'rb') as tdxy:
        tdxy_l_rf.append ( pickle.load( tdxy )  )
    print '##right files'    
    with open(R_rf_fpath[orn] , 'rb') as tdxy:
        tdxy_r_rf.append(   pickle.load( tdxy )  )

print len(tdxy_l_rf)
print len(tdxy_l_rf[0])
print len(tdxy_l_rf[0][2])
print tdxy_l_rf[0]


#animate the rtna_rf =========================================================
#print 'abplt_rw, sbplt_cl, rtna_w, rtna_h, rf_w, rf_h: {}, {}, {}, {}, {}, {} '.format(subplt_rws, subplt_cls, rtna_w, rtna_h, rf_w,  rf_h)
fig, axs = plt.subplots(subplt_rws, subplt_cls, sharex=False,  sharey=False)  #, figsize=(12,5))
axs = ppanmy.init_fig_mxn_sbplt_wxh_res (fig, axs, rtna_h, rtna_w, rf_w,  rf_h,  subplt_rws, subplt_cls)
plt.grid(True)
plt.show(block=False)
plt.pause(.01)

print '##### required variables: \n n_rtna={}, TDXY_len={}, rtna_w={}, rtna_h={}, krnl_sz={}, rf_w={} , rf_h={}'.format( 
n_rtna , 01010, rtna_w, rtna_h, krnl_sz, rf_w , rf_h  )


plt.show(block=False)
for i in range( len(tdxy_l_rtna[0]) -1  ): #t10u: 
    i = i*1
    print '\n\ni={}'.format(i)  
#    for cl in range( subplt_cls ):
#        for rw in range( subplt_rws ):
#            axs[rw][cl].cla()  
            #    axs = ppanmy.init_fig_mxn_sbplt_wxh_res (fig, axs, rtna_h, rtna_w, rf_w,  rf_h,  subplt_rws, subplt_cls)
            #    plt.suptitle('rtna_rf_orn:   t= {} usec'.format( i ) )
            #    axs[0][0].scatter(   tdxy_l_rtna[2][i],     tdxy_l_rtna[3][i], color='b' )
            #    axs[1][0].scatter(   tdxy_r_rtna[2][i],     tdxy_r_rtna[3][i], color='b' )
            #
            #    for orn in range(n_orn):
            #        axs[0][orn+1].scatter(   tdxy_l_rf[orn][2][i],      tdxy_l_rf[orn][3][i], color='b' )
            #        axs[1][orn+1].scatter(   tdxy_r_rf[orn][2][i],      tdxy_r_rf[orn][3][i], color='b' )
            #    plt.pause(.01)
    tdxy_l_rtna_x=[]
    tdxy_l_rtna_y=[]
    tdxy_r_rtna_x=[]
    tdxy_r_rtna_y=[]
#    
    tdxy_l_0f3_x=[]
    tdxy_l_0f3_y=[]
    tdxy_l_1f3_x=[]
    tdxy_l_1f3_y=[]
#    tdxy_l_2f3_x=[]
#    tdxy_l_2f3_y=[]
##    tdxy_l_3f3_x=[]
##    tdxy_l_3f3_y=[]
#    
#    
    tdxy_r_0f3_x=[]
    tdxy_r_0f3_y=[]
    tdxy_r_1f3_x=[]
    tdxy_r_1f3_y=[]
#    tdxy_r_2f3_x=[]
#    tdxy_r_2f3_y=[]
##    tdxy_r_3f3_x=[]
##    tdxy_r_3f3_y=[]
#
#    
    for wndw in range (10):
        tdxy_l_rtna_x= tdxy_l_rtna_x +  tdxy_l_rtna[2][i+wndw]
        tdxy_l_rtna_y= tdxy_l_rtna_y + tdxy_l_rtna[3][i+wndw]  
        tdxy_r_rtna_x= tdxy_r_rtna_x + tdxy_r_rtna[2][i+wndw]  
        tdxy_r_rtna_y= tdxy_r_rtna_y + tdxy_r_rtna[3][i+wndw]  

        tdxy_l_0f3_x= tdxy_l_0f3_x +  tdxy_l_rf[0][2][i+wndw]   
        tdxy_l_0f3_y= tdxy_l_0f3_y +  tdxy_l_rf[0][3][i+wndw]   
#        tdxy_l_1f3_x= tdxy_l_1f3_x +  tdxy_l_rf[1][2][i+wndw]  
#        tdxy_l_1f3_y= tdxy_l_1f3_y +  tdxy_l_rf[1][3][i+wndw]  
#        tdxy_l_2f3_x= tdxy_l_2f3_x +  tdxy_l_2f3[2][i+wndw]   
#        tdxy_l_2f3_y= tdxy_l_2f3_y +  tdxy_l_2f3[3][i+wndw]   
##        tdxy_l_3f3_x= tdxy_l_3f3_x +  tdxy_l_3f3[2][i+wndw]  
##        tdxy_l_3f3_y= tdxy_l_3f3_y +  tdxy_l_3f3[3][i+wndw]    
#        
        tdxy_r_0f3_x= tdxy_r_0f3_x +  tdxy_r_rf[0][2][i+wndw]   
        tdxy_r_0f3_y= tdxy_r_0f3_y +  tdxy_r_rf[0][3][i+wndw]   
#        tdxy_r_1f3_x= tdxy_r_1f3_x +  tdxy_r_rf[1][2][i+wndw]  
#        tdxy_r_1f3_y= tdxy_r_1f3_y +  tdxy_r_rf[1][3][i+wndw]  
#        tdxy_r_2f3_x= tdxy_l_2f3_x +  tdxy_r_2f3[2][i+wndw]   
#        tdxy_r_2f3_y= tdxy_l_2f3_y +  tdxy_r_2f3[3][i+wndw]   
##        tdxy_r_3f3_x= tdxy_l_3f3_x +  tdxy_r_3f3[2][i+wndw]  
##        tdxy_r_3f3_y= tdxy_l_3f3_y +  tdxy_r_3f3[3][i+wndw]   
#        
    print 'tdxy_l_rtna_x= {}'.format(tdxy_l_rtna_x)
    print len(tdxy_l_rtna_x)    
    print 'tdxy_l_rtna_y = {}'.format(tdxy_l_rtna_y)
    print len(tdxy_l_rtna_y)  
    
    print 'tdxy_l_0f3_x= {}'.format(tdxy_l_0f3_x)
    print len(tdxy_l_0f3_x)    
    print 'tdxy_l_0f3_y = {}'.format(tdxy_l_0f3_y)
    print len(tdxy_l_0f3_y)  

    print 'tdxy_r_0f3_x= {}'.format(tdxy_r_0f3_x)
    print len(tdxy_r_0f3_x)    
    print 'tdxy_r_0f3_y = {}'.format(tdxy_r_0f3_y)
    print len(tdxy_r_0f3_y)  

    axs[0][0].scatter(   tdxy_l_rtna_x,    tdxy_l_rtna_y, color='b' )
    axs[1][0].scatter(   tdxy_r_rtna_x,    tdxy_r_rtna_y, color='b' )
    axs[0][1].scatter(   tdxy_l_0f3_x,     tdxy_l_0f3_y,  color='b' )
#    axs[0][2].scatter(   tdxy_l_1f3_x,     tdxy_l_1f3_y,  color='b' )
    axs[1][1].scatter(   tdxy_r_0f3_x,     tdxy_r_0f3_y,  color='b' )
#    axs[1][2].scatter(   tdxy_r_1f3_x,     tdxy_r_1f3_y,  color='b' )
    plt.pause(0.01)
plt.pause(5)















