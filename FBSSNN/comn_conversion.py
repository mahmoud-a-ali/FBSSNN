#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat May 26 17:38:46 2018

@author: mali
"""
import pickle 
import numpy as np
import os 





######################### function ############################################
def cnvrt_cmra_evts_to_spk_tms(evts,  start_time,  simtime,   dataset_name,   camera,
                               rtna_w, rtna_h, ch_idx, t_idx, pol_idx, x_idx, y_idx ):
    ### start_time and simtime should passed cause in case of events from both R and L, need them to be synchronous    

    #print 'data set is {}'.format(evts)
    n_nrns = rtna_w * rtna_h
    n_evts = len(evts)  
    print '\n##### converting',camera,'events to spike_times ... '
    print 'n_{}_evts :  {}'.format(camera, n_evts)
    rtna = []
    
    for nrn in range(n_nrns):
        print nrn
        nrn_row_y,  nrn_col_x = frm_nrn_indx_to_2D_grd(nrn, rtna_w, rtna_h)
        nrn_spks =[] 
        if nrn==0:  # just to overcome of problem of listoflist vs ndarray type 
            nrn_spks.append( simtime  ) # APPEND ZERO OR AT LAST EVENT TIME                
        for evnt in range(n_evts):
            if evts[evnt][x_idx]== nrn_col_x and evts[evnt][y_idx]== nrn_row_y:
                nrn_spks.append(  (evts[evnt][t_idx]-start_time)   )   #/1000
        rtna.append(nrn_spks)  
#        print '# convert: ({},{})   -->    {}'.format(nrn_row_y, nrn_col_x,nrn_spks)
    spk_tms= np.array(rtna)
#    print '### type(rtna): {},  type(rtna[0]): {},  rtna : \n{}'.format( type(rtna), type(rtna[0]), rtna)
#    print '### type(spk_tms): {}, type(spk_tms[0]): {}, spk_tms: \n{}'.format( type(spk_tms), type(spk_tms[0]), spk_tms)


    print 'done!' 
    
    print '\n###### deleting repeated spike_times .... '
    for nrn in range(n_nrns):
        if len(spk_tms[nrn]) > 1:
            for each in spk_tms[nrn]: 
                count = spk_tms[nrn].count(each)  
                if count > 1: 
                    spk_tms[nrn].remove(each)
#                    print '({},{})   -->    {}'.format(nrn_row_y, nrn_col_x,spk_tms[nrn])    
    
#    print spk_tms               
    print 'done!' 
    
    print '\n###### add spikes at zero or at (last_time_instant+1) for all nodes to solve get_data problem  ... '          
    for nrn in range(n_nrns):
        nrn_row_y,  nrn_col_x = frm_nrn_indx_to_2D_grd(nrn, rtna_w, rtna_h)
        # if you want to shift all spks by 1, so we keep real spk at zeros to be at one otherwise they will be lost
    #    for spk in range( len(spk_tms[nrn]) ):
    #        spk_tms[nrn][spk] = spk_tms[nrn][spk] +1
#        print '### append error here, spk_tms = {}'.format(spk_tms[nrn])
#        print '### 1st dim of spk_tms : {}'.format( len(spk_tms) )
#        print '### 2nd dim of spk_tms : {} '.format( len(spk_tms[nrn]) )
#        print '### 3rd dim of spk_tms  !!! '.format( len(spk_tms[nrn][0]) )

        spk_tms[nrn].append( simtime  ) # or at zero 
        spk_tms[nrn].sort()
#        print '({},{})   -->    {}'.format(nrn_row_y, nrn_col_x,spk_tms[nrn])
         
    print spk_tms  
    return spk_tms

###############################################################################   
    








###############################################################################
def write_flenfldr_ncrntpth(fldr, fle):
    crnt_dir     = os.path.dirname(os.path.abspath(__file__))
    fldr_pth     = os.path.join( crnt_dir, fldr)
    if not os.path.exists(fldr_pth):
        os.makedirs(fldr_pth)   
    return os.path.join( fldr_pth, fle )

def read_flenfldr_ncrntpth(fldr, fle):
#    print fldr
#    print fle
    crnt_dir     = os.path.dirname(os.path.abspath(__file__))
    fldr_pth     = os.path.join( crnt_dir, fldr)
    if not os.path.exists(fldr_pth):
        print '\n ================ERROR=============  \nfolder {} is not exist !!!'.format(fldr_pth)
    else: 
#        print '### file exist'
        return  os.path.join( fldr_pth, fle )




###############################################################################
# conn formula  is ( (y_pre, x_pre),  (y_post, x_post),  w, d  )
def translate_grid2D_to_1D (x, y, row_size):
    return(x + y*row_size) 
    
def translate_grid2D_to_1D (x, y, row_size):
    return(x + y*row_size) 
    
    
def grid2D_conn_lst_to_1D (conn_lst, pre_w , post_w ):    
    conn_len = len(conn_lst)
    pre_nrn_idx =[]
    post_nrn_idx =[]
    for conn in range(conn_len):
        x_pre = conn_lst[conn][0][1]
        y_pre = conn_lst[conn][0][0]
        x_post = conn_lst[conn][1][1]
        y_post = conn_lst[conn][1][0]
        pre_nrn =  translate_grid2D_to_1D (x_pre, y_pre, pre_w)
        post_nrn =  translate_grid2D_to_1D (x_post, y_post , post_w)
        pre_nrn_idx.append(pre_nrn)
        post_nrn_idx.append(post_nrn)
#        print '### {}th conn: ({}, {}) ,  ({}, {})  to  {},  {} '.format(conn, y_pre, x_pre,  y_post, x_post,  pre_nrn, post_nrn)
    conn_lst_by_nrn_idx = []
    for conn in range(conn_len):
        conn_lst_by_nrn_idx.append( (pre_nrn_idx[conn] , post_nrn_idx[conn] , conn_lst[conn][2] ,  conn_lst[conn][3])  )
        
    return conn_lst_by_nrn_idx
# #############################################################################
    

def frm_nrn_indx_to_2D_grd ( nrn_indx, n_col_x, n_row_y):
    """ retuns 2D coordinate of nrn in form (nrn_row_n_y,  nrn_col_n_x) """
    nrn_row_n_y = nrn_indx / n_col_x
    nrn_col_n_x = nrn_indx % n_row_y
    nrn_in_2D = (nrn_row_n_y,  nrn_col_n_x)
    return nrn_in_2D
#for i in range(9):
#    print frm_nrn_indx_to_2D_grd (i,3,3 )
    
###############################################################################
def frm_spk_trns_to_1D_2D(spk_trns, n_col_x, n_row_y): 
    print ' \n======= FUNC_start: frm_nrn_indx_to_2D_grd ========================= ' 
    cnvr2usec = 100
    print ' cnvr2usec: {}'.format( cnvr2usec)    
    spk_trns_usec = [ x*cnvr2usec for x in spk_trns]
    spks_strt_tm = int (spk_trns[0].t_start * cnvr2usec)
    spks_stop_tm  = int (spk_trns[0].t_stop * cnvr2usec)
    spks_step_tm = int(  ( float(spk_trns[0].t_stop)  - int(spk_trns[0].t_stop) ) * cnvr2usec )
    
#    print '### incoming spk_trns: \n{}'.format(spk_trns)
        #    print '### spk_trns_usec: \n{}'.format(spk_trns_usec)
    print '\n### start_time  : {}  ----  type: {}'.format(spks_strt_tm,  type(spks_strt_tm))
    print '### stop_time     : {}  ----   type: {} '.format(spks_stop_tm,  type(spks_stop_tm))
    print '### step_time     : {}  ----   type: {}'.format( spks_step_tm, type(spks_step_tm) )
    print '### n_nrns        : {}'.format(len(spk_trns))
    T=[]
    spks_1D = []
    for t in range(spks_strt_tm, spks_stop_tm+spks_step_tm ):#- 300): #
#        print '\n###### For t :  {}'.format(t)
        T.append(t)
        n_nrns = len(spk_trns)
        spks_at_t=[]
        for nrn_id in range(n_nrns):
#            print '\n### spks of nrn {} :  {}'.format( nrn_id, spk_trns[nrn_id] )
            if len(spk_trns_usec[nrn_id]) > 0: #is not None:
#                print 't = {} ... spk_trns_usec[{}] = {} is not [] '.format(t, nrn_id, spk_trns_usec[nrn_id] )
                for spk_tm in range( len(spk_trns_usec[nrn_id]) ):
#                    print '### t={}     spk_tms :  {}'.format( t,  spk_trns_usec[nrn_id][spk_tm] ) 
#                    print 'spk_trns_usec ...: {}'.format(int (spk_trns_usec[nrn_id][spk_tm]) )
#                    print 't ...............: {}'.format(t)
                    if int (spk_trns_usec[nrn_id][spk_tm]) == t:
                        print 'nrn_id [{}]            t= {}'.format(nrn_id, t)
                        spks_at_t.append(nrn_id)
    #    print 'at t= {}, spkng_nrns are: {}'.format(t, spks_at_t)
        spks_1D.append(spks_at_t)

    X_2d=[]
    Y_2d=[]
    for t in range( len(spks_1D) ):
        t_Xs =[]
        t_Ys =[]
        if spks_1D[t] is not None:  
            if spks_1D[t] !=[] :  # len() >=1 
                for nrn in range( len(spks_1D[t]) ):
                    row_y, col_x = frm_nrn_indx_to_2D_grd ( spks_1D[t][nrn], n_col_x, n_row_y)
    #                T.append(t)
                    t_Xs.append(col_x)
                    t_Ys.append(row_y)
#                print nrn    
                X_2d.append(t_Xs)
                Y_2d.append(t_Ys)
            else:
    #             T.append(t)
                 X_2d.append(spks_1D[t])
                 Y_2d.append(spks_1D[t])
#    chk_tm = 540    
#    print '### T [{}] : {}' .format(chk_tm, T[chk_tm]) #test at certain time at which you know which nrn spikes
#    print '### 1D[{}] : {}' .format(chk_tm, spks_1D[chk_tm])
#    print '### X [{}] : {}' .format(chk_tm, X_2d[chk_tm])
#    print '### Y [{}] : {}' .format(chk_tm, Y_2d[chk_tm])
    T_1D_X_Y = []
    T_1D_X_Y.append(T)
    T_1D_X_Y.append(spks_1D)
    T_1D_X_Y.append(X_2d)
    T_1D_X_Y.append(Y_2d) 
#    print '\n### T_X_Y_2D : \n{}'.format(T_1D_X_Y) # dimension 4 x t_stp x depend 
    print '======== FUNC_end: frm_nrn_indx_to_2D_grd, return: T_1D_X_Y ============= '
    return T_1D_X_Y

    # calling example:---------------------------------------------------------------
#            spks_file = 'L_rtna_spks_rslts_2.pickle'
#            print '\n###### loading the spk_rslts_file',spks_file,' .... '
#            with open(spks_file , 'rb') as pop_spks:
#                spks = pickle.load(pop_spks)
#            n_col_x = 4
#            n_row_y = 4   
#            T_1D_X_Y = cnvrt.frm_spk_trns_to_1D_2D(spks, n_col_x, n_row_y)    
#            time_idxs   = T_1D_X_Y[0]
#            idxs_1D  = T_1D_X_Y[1]
#            X_2D        = T_1D_X_Y[2]
#            Y_2D        = T_1D_X_Y[3]
#            print '\n### idxs_1D : \n{}'.format(idxs_1D) # dimension 4 x t_stp x depend 
#            print '\n### time_idxs : \n{}'.format(time_idxs) # dimension 4 x t_stp x depend 
#            print '\n### X_2D : \n{}'.format(X_2D) # dimension 4 x t_stp x depend 
#            print '\n### Y_2D : \n{}'.format(Y_2D) # dimension 4 x t_stp x depend 
    

#########################################################################################################



    
        
    
























