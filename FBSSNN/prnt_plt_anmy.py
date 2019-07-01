#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May 29 13:04:50 2018

@author: mali
"""
import time
import comn_conversion as cnvrt
import numpy  as np
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.animation as animation









################################################################################################################
def anmy_rtna_rf_orn(  batch_spk_trns, rtna_hght, rtna_wdth, n_rtna, krnl_sz, strt_tm , stop_tm):
    """ takes lst of rtna_rf_spk_trns (batch_spk_trns) in the form of:
        [Lrtna, Rrtna, Lrf0.....Lrf_n, Rrf0.....Rrf_n] or [rtna, rf0.....rf_n], 
        each spk_trn is in 1D and 2D form:
        [T, 1D, X2D, Y2D] which called TDXY lst
        ex: batch_spk_trns[0][0] is T vector of Lrtna,
            batch_spk_trns[0][3] is Y vector of Lrtna"""
    print '============================ FUNC_start: anmy_rtna_rf_orn ==========================='
    n_spk_trns = len(batch_spk_trns) 
    if n_rtna ==1:
        n_orn = n_spk_trns  - 1 
    elif n_rtna == 2:
        n_orn =  (n_spk_trns / 2) - 1 
    else: 
        print '### error: n_rtna should be 1 or 2 ' 
    rf_w   = rtna_wdth - krnl_sz + 1
    rf_h   = rtna_hght - krnl_sz + 1
    subplt_rws = n_rtna
    subplt_cls = n_orn+1
    print '### n_rtna x n_orn:  {}'.format( n_rtna,  n_orn ) 
    print '### subplt_rws x subplt_cls  : {} x {}'.format( subplt_rws, subplt_cls )
    print '### rf_w x rf_h:  {}'.format( rf_w,  rf_h ) 
    print '### rtna_w x rtna_h:  {}'.format( rtna_wdth,  rtna_hght ) 
    ######################################## animy_start #########################################
    def animate(i):
        if i < stop_tm: # length of T vector of Lrtna , -1 to remove added events
            print 'i = {}'.format(i, subplt_rws)
            for row in xrange(subplt_rws):
                for col in xrange(subplt_cls):
                    axs[row][col].clear()
                    init_axs = init_fig_mxn_sbplt_wxh_res (fig, axs, rtna_hght, rtna_wdth, rf_w,  rf_h )
            for row in xrange(subplt_rws):
                for col in xrange(subplt_cls):
#                    init_axs[row][col].scatter( batch_spk_trns[5][X_2D][i], batch_spk_trns[5][Y_2D][i] )
                    if n_rtna ==1:
                        print '### one rtna_one one_row  '
                        init_axs[row][col].scatter( batch_spk_trns[col][2][i], batch_spk_trns[col][3][i] ) 
                    else:
                        if col==0:
#                            print '###########col = 0 '
                            if row ==0:
                                init_axs[row][col].scatter( batch_spk_trns[0][2][i], batch_spk_trns[0][3][i] )
                            else: # row==1:
                                init_axs[row][col].scatter( batch_spk_trns[1][2][i], batch_spk_trns[1][3][i] )
                        else:
                            if row ==0:
                                init_axs[row][col].scatter( batch_spk_trns[col+1][2][i+1], batch_spk_trns[col+1][3][i+1] )
#                                print 'row==0, col={} --> {}'.format(col, col+1)
                            else: # row==1:
                                init_axs[row][col].scatter( batch_spk_trns[(n_orn+1)+col][2][i], batch_spk_trns[(n_orn+1)+col][3][i] )
#                                print 'row==1, col={} --> {}'.format(col, 5*row+col)
            plt.suptitle('t= {}'.format( batch_spk_trns[0][0][i] ) )
            if i==0 or i==4000 or i==9000:
                 print'loooooooooooooooooooooooooooooooooook'
                 time.sleep(10)
        else:
#            time.sleep(.1)
#            plt.close(fig) 
            print 'animation finish!'
    ######################################## animy_start #########################################

    fig, axs = plt.subplots(subplt_rws, subplt_cls, sharex=False,  sharey=False)  #, figsize=(12,5))
    init_axs = init_fig_mxn_sbplt_wxh_res (fig, axs, rtna_hght, rtna_wdth, rf_w,  rf_h )
    plt.grid(True)
    interval = strt_tm - stop_tm
    animy = animation.FuncAnimation(fig, animate,interval=0.01)
    plt.show()
    print '======================== FUNC_end: anmy_rtna_rf_orn, return True ========================= '

    return True
################################################################################################################
def st_sbttle(row, col):
    if row==0:
        ch = 'L'
    else:
        ch='R'
    if col==0:
        sbttle = '{}_rtna'.format(ch)
    else:
        sbttle = '{}_rf_{}'.format(ch, col-1)
    return sbttle
################################################################################################################
def set_axs(ax, rtna_hght, rtna_wdth, rf_w,  rf_h, col):
     if col >0:
         xtcks = range(0, rf_w) 
         ytcks = range(0, rf_h)
         ax.set_xlim(-1,rf_w)
         ax.set_ylim(-1,rf_h)
         ax.set_xticks(xtcks)
         ax.set_yticks(ytcks)
        #                 print 'col==0, xtcks: {}'.format(xtcks)
     elif col==0 :
         xtcks = range(0, rtna_wdth) 
         ytcks = range(0, rtna_hght)
         ax.set_xlim(-1,rtna_wdth)
         ax.set_ylim(-1,rtna_hght)
         ax.set_xticks(xtcks)
         ax.set_yticks(ytcks)
        #                 print 'col!=0, xtcks: {}'.format(xtcks)
################################################################################################################
def init_fig_mxn_sbplt_wxh_res (fig, axs, rtna_hght, rtna_wdth, rf_w,  rf_h, sbplt_rws, sbplt_cls):
#    print '======================== FUNC_start: init_fig_mxn_sbplt_wxh_res ========================= '
    mngr = plt.get_current_fig_manager()
#    mngr.window.setGeometry(0,0,1500, 1000)  #size of window: (x0, y0 , xf, yf) (0,0) top left 
    if sbplt_rws==2:
        for row in xrange(sbplt_rws):
            for col in xrange(sbplt_cls):
                 ax = axs[row][col]
                 set_axs(ax, rtna_hght, rtna_wdth, rf_w,  rf_h, col)
                 ttle = st_sbttle(row, col)
                 ax.set_title(ttle)
                 ax.grid(color='k', linestyle='-', linewidth=.1)
                 ax.invert_yaxis()
    elif sbplt_rws==1:
        for col in xrange(sbplt_cls):
            print 'col2 here: {} '.format(col)
            ax = axs[col]
            set_axs(ax, rtna_hght, rtna_wdth, rf_w,  rf_h, col)
            ttle = st_sbttle(0, col)
            ax.set_title(ttle)
            ax.grid(color='k', linestyle='-', linewidth=.1)
            ax.invert_yaxis()
    else:
        print'error, no subtitle'

    plt.show

#    mngr = plt.get_current_fig_manager()
#    mngr.window.setGeometry(0,0,1250, 500)  #size of window: (x0, y0 , xf, yf) (0,0) top left
#    print '======================== FUNC_end: init_fig_mxn_sbplt_wxh_res, return axs ========================= '
    return axs
################################################################################################################



################################################################################################################
def plt_rtna_rf_spk_v (rtna_spks, rf_v, rf_spks, orn,  vrjn, LR='L' ):
    img_pth = 'fgrs/spn/{}_{}'.format(vrjn, orn)
    sim_time = int(rtna_spks[0].t_stop)
   
    plot.Figure(
            #plot voltage for first ([0]) neuron
            plot.Panel( rtna_spks, yticks=True, xlim=(0, sim_time)), 
#            plot.Panel( rf_v, yticks=True, xticks=True, markersize=5, xlim=(0, sim_time)),
            plot.Panel( rf_spks, yticks=True, xticks=True, markersize=5, xlim=(0, sim_time)),
            title= '{}_rtna_rf_{}'.format(LR, orn) #"3by3 pxl to RF"
    #        annotations = "Simulated with {}".format(sim.name())
            )
#    plt.grid(True) 
    plt.savefig( img_pth )
    plt.show()

################################################################################################################











































#def anmy_rf_orn(X_2D, Y_2D, rtna_hght, rtna_wdth, n_rtna=2, n_orn=8):
#    def animate(i):
#        if i< len(X_2D):
#            print 'i = {}'.format(i)
#            for col in xrange(sub_cls):
#                for row in xrange(sub_rws):
#                    axs[row][col].clear()
#            init_axs = init_fig_mxn_sbplt_wxh_res (fig, axs, n_rows, n_cols )
#            for col in xrange(sub_cls):
#                for row in xrange(sub_rws):
#                    init_axs[row][col].scatter(X_2D[i],Y_2D[i]) 
#        else:
#            time.sleep(.1)
#    #        plt.close(fig) 
#            print 'animation finish!'
#   #-----------------------------------
#    n_rows = rtna_hght
#    n_cols = rtna_wdth
#    sub_rws = n_rtna
#    sub_cls = n_orn
#    fig, axs = plt.subplots(sub_rws, sub_cls,sharex=True,  sharey=True)        #, figsize=(12,5))
#    init_axs = init_fig_mxn_sbplt_wxh_res (fig, axs, n_rows, n_cols )
#    print '### n_rtna x n_orn  : {} x {}'.format( len(init_axs), len(init_axs[0]) )
#    print '### width x height  : {} x {}'.format( n_rows, n_cols)
#    plt.grid(True)
#    animy = animation.FuncAnimation(fig, animate, interval=10000)
#    plt.show()
#    print 'done'
#    return True


#################### example to call : ####################
#        import pickle
#        #spks_file = 'L_rf_2_spks_rslts_2.pickle'
#        spks_file = 'L_rtna_spks_rslts_2.pickle'
#        print '\n###### loading the spk_rslts_file',spks_file,' .... '
#        with open(spks_file , 'rb') as pop_spks:
#            spks = pickle.load(pop_spks)
#        #    print '### spks_file : (', spks_file,') is loaded !' 
#        #    print '### spks_file\'s spk_trns : \n'
#        #    print spks.segments[0].spiketrains 
#        n_col_x = 4
#        n_row_y = 4   
#        T_1D_X_Y = cnvrt.frm_spk_trns_to_1D_2D(spks, n_col_x, n_row_y)    
#        time_idxs   = T_1D_X_Y[0]
#        idxs_1D  = T_1D_X_Y[1]
#        X_2D        = T_1D_X_Y[2]
#        Y_2D        = T_1D_X_Y[3]
#        print '\n### idxs_1D : \n{}'.format(idxs_1D) # dimension 4 x t_stp x depend 
#        print '\n### time_idxs : \n{}'.format(time_idxs) # dimension 4 x t_stp x depend 
#        print '\n### X_2D : \n{}'.format(X_2D) # dimension 4 x t_stp x depend 
#        print '\n### Y_2D : \n{}'.format(Y_2D) # dimension 4 x t_stp x depend 
#        
#        
#        anmy_rf_orn(X_2D, Y_2D, n_row_y, n_col_x, n_rtna=2, n_orn=4)
################################################################################################################











































