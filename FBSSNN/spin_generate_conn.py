
"""
Created on Sun Jun  3 23:49:20 2018

@author: mali
"""
import time 
import os
import logging
import pickle
import spynnaker8 as sim 
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt

import print_chs as prnt
import Gabor_weights as GB
import comn_conversion as cnvrt
import multiprocessing


label_ = 'cnet_conn'
rtna_w = 65
rtna_h = 65
krnl_sz = 5
jmp     = 2
rf_w = (rtna_w - krnl_sz)/jmp +1
rf_h = (rtna_h - krnl_sz)/jmp +1


    
rf2cnet_dly_   = 1
rf2cnet_G_     = 20

rwcl_minh_dly_ = 0 
rwcl_minh_G_   = 1 * rf2cnet_G_ 

x_minh_dly_    = 0 
x_minh_G_      = 1 * rf2cnet_G_ 

dsp_mext_dly_  = 0
dsp_mext_G_    = .1 * rf2cnet_G_

max_dsp_       = 40/jmp
min_dsp_       = - 40/jmp
n_out_lyrs_     = 1 


if rf_w != rf_h:
    print '## ERROR:  Lrf_._wdth != Rrf_._wdth or Lrf_._hght != Rrf_._hght'

       
self_rf_w = rf_w
self_rf_h = rf_h

self_min_dsp = min_dsp_   # -( self._Lrf._wdth - 1 )      # min_dsp_
self_max_dsp = max_dsp_  # ( self._Lrf._wdth - 1 )       # max_dsp_
self_min_x = 0
self_max_x = 2*( self_rf_w -1 )

self_n_lyrs  = self_rf_h
self_n_rows  = self_rf_w
self_n_cols  = self_rf_w 
self_n_dsps  = self_max_dsp - self_min_dsp
self_n_xs     = self_max_x - self_min_x 

self_n_nrns_lyr = self_n_rows * self_n_cols
self_n_nrns_row = self_n_cols 
self_n_nrns_col = self_n_rows 

self_label = label_
self_cnet_sz = self_n_rows * self_n_cols * self_n_lyrs 

self_rf2cnet_dly = rf2cnet_dly_ 
self_rf2cnet_G= rf2cnet_G_ 

self_inlyr_rowcol_minh_dly  = rwcl_minh_dly_
self_inlyr_rowcol_minh_G    = rwcl_minh_G_  
self_outlyr_rowcol_minh_dly = 1 * rwcl_minh_dly_
self_outlyr_rowcol_minh_G   = 1 * rwcl_minh_G_  

self_inlyr_xminh_dly  = x_minh_dly_ 
self_inlyr_xminh_G    = x_minh_G_    
self_outlyr_xminh_dly = 1 * x_minh_dly_ 
self_outlyr_xminh_G   = 1 * x_minh_G_  

self_inlyr_dsp_mext_dly  = dsp_mext_dly_
self_inlyr_dsp_mext_G    = dsp_mext_G_
self_outlyr_dsp_mext_dly = 1 * dsp_mext_dly_ 
self_outlyr_dsp_mext_G   = 1 * dsp_mext_G_       

#============================================================================================================        
# ============= converting neuron IDs to rows, columns, layers to be represented into 3D =======================
#============================================================================================================
# extract  nrns_idx for each lyr --------------------------------------
#    def extract_lyr_nrns(self): #return vector with all nrn idx will connect to that lyr 
print '\n### {} :: extract_lyr_nrns .... '.format(self_label)
lyr_nrns=[] 
for ilyr in range ( self_n_lyrs ):
    ilyr_nrns=[]
    for nrn_idx in range ( ilyr*self_n_nrns_lyr, ilyr*self_n_nrns_lyr +self_n_nrns_lyr ):
        ilyr_nrns.append( nrn_idx  )
    lyr_nrns.append( ilyr_nrns  )   
self_lyr_nrns = lyr_nrns 
lyr_nrns = []
print ' len of self_lyr_nrns: {}'.format( len(self_lyr_nrns) )  
#print '## self_lyr_nrns[0]: {}'.format( self_lyr_nrns[0] )      

# extract related nrns to L and R RFs_layer --------------------------------------
#    def extract_lyr_rf_nrns(self): #return vector with all nrn idx will connect to that lyr 
print '\n### {} :: extract_rltd_rf_nrns .... '.format(self_label)
lyr_rf_nrns=[] 
for ilyr in range ( self_n_lyrs ):
    ilyr_rf_nrns=[]
    for nrn_idx in range ( ilyr*self_n_rows, ilyr*self_n_rows +self_n_rows ):
        ilyr_rf_nrns.append( nrn_idx  )
    lyr_rf_nrns.append(ilyr_rf_nrns  )   
self_lyr_rf_nrns = lyr_rf_nrns
lyr_rf_nrns =[]
print ' len of self_lyr_rf_nrns: {}'.format( len(self_lyr_rf_nrns) )  
#print '## self_lyr_rf_nrns[0]: {}'.format( self_lyr_rf_nrns[0] )      



# extract lyr_row_nrn -----------------------------------------------------
#    def extract_lyr_row_nrns(self): 
print '\n### {} :: extract lyr_row_nrn .... '.format(self_label)
print 'self._min_dsp, self._max_dsp: {}, {}'.format(self_min_dsp, self_max_dsp)
lyr_row_nrns =[]
for ilyr in range ( self_n_lyrs ):
    ilyr_row_nrns =[]
    for irow in range ( self_n_rows ):
        ilyr_irow_nrns = []
        for inrn in range( self_n_nrns_row ):
            nrn_idx = ilyr* self_n_nrns_lyr + irow* self_n_nrns_row + inrn
            ilyr_irow_nrns.append( nrn_idx )
        ilyr_row_nrns.append( ilyr_irow_nrns )
    lyr_row_nrns.append( ilyr_row_nrns )
#limit disp to some given values: dsp_max, dsp_min    
lyr_row_nrns_r =[]
for ilyr in range ( self_n_lyrs ):
    ilyr_row_nrns_r =[]
    for irow in range ( self_n_rows ):
        ilyr_irow_nrns_r = []
        for inrn in lyr_row_nrns[ilyr][irow]:
#                    print inrn ,  lyr_row_nrns[ilyr][irow][irow]
            if inrn - lyr_row_nrns[ilyr][irow][irow] >= self_min_dsp and inrn - lyr_row_nrns[ilyr][irow][irow] <= self_max_dsp :
                ilyr_irow_nrns_r.append( inrn )
        ilyr_row_nrns_r.append( ilyr_irow_nrns_r )
    lyr_row_nrns_r.append( ilyr_row_nrns_r )

#        print lyr_row_nrns
#        print lyr_row_nrns_r
self_lyr_row_nrns = lyr_row_nrns_r
lyr_row_nrns = []
lyr_row_nrns_r = [] 
print ' len of self_lyr_row_nrns: {}'.format( len(self_lyr_row_nrns) )  
#print '## self_lyr_row_nrns[0]: {}'.format( self_lyr_row_nrns[0] )      
   
   
# extract lyr_col_nrns ----------------------------------------------------
#    def extract_lyr_col_nrns(self): 
print '\n### {} :: extract lyr_col_nrn .... '.format(self_label)
lyr_col_nrns =[]
for ilyr in range ( self_n_lyrs ):
    ilyr_col_nrns =[]
    for icol in range ( self_n_cols ):
        ilyr_icol_nrns = []
        for inrn in range( self_n_nrns_col ):
            nrn_idx = ilyr* self_n_nrns_lyr + icol + inrn* self_n_nrns_col
            ilyr_icol_nrns.append( nrn_idx )
        ilyr_col_nrns.append( ilyr_icol_nrns )
    lyr_col_nrns.append( ilyr_col_nrns )

lyr_col_nrns_r =[]
for ilyr in range ( self_n_lyrs ):
    ilyr_col_nrns_r =[]
    for icol in range ( self_n_cols ):
        ilyr_icol_nrns_r = []
        for inrn in lyr_col_nrns[ilyr][icol]:
            if any( inrn in sublist for sublist in self_lyr_row_nrns[ilyr] ):
#                        print inrn , lyr_col_nrns[ilyr][icol][icol], inrn , lyr_col_nrns[ilyr][icol][icol]
#                        print 'extist '
                ilyr_icol_nrns_r.append( inrn )
        ilyr_col_nrns_r.append( ilyr_icol_nrns_r )
    lyr_col_nrns_r.append( ilyr_col_nrns_r )
    
#        print lyr_col_nrns  
#        print lyr_col_nrns_r          
self_lyr_col_nrns = lyr_col_nrns_r
lyr_col_nrns   = []
lyr_col_nrns_r = []
print ' len of self_lyr_col_nrns: {}'.format( len(self_lyr_col_nrns) )  
#print '## self_lyr_col_nrns[0]: {}'.format( self_lyr_col_nrns[0] )      
   
# extract lyr_x_nrns  ---------------------------------
#    def extract_lyr_x_nrns(self): 
#    print '\n### {} :: extract lyr_x_nrns  .... '.format(self_label)
#    lyr_x_nrns =[]
#    for ilyr in range ( self_n_lyrs ):
#        ilyr_x_nrns =[]
#        for ix in range ( self_min_x, self_max_x  ):
#            ilyr_ix_nrns = []
#            for nrn_idx in self_lyr_nrns[ilyr] :
#                if any( nrn_idx in sublist for sublist in self_lyr_row_nrns[ilyr] ):
#                    prjctd_nrn_idx = nrn_idx - ilyr*self_n_nrns_lyr
#                    y_row, x_col = cnvrt.frm_nrn_indx_to_2D_grd( prjctd_nrn_idx, self_n_cols , self_n_rows  )
#                    if x_col + y_row == ix:
#                        print 'as'
#                        ilyr_ix_nrns.append( nrn_idx  )
#            ilyr_x_nrns.append( ilyr_ix_nrns )
#        lyr_x_nrns.append( ilyr_x_nrns )
#    self_lyr_x_nrns = lyr_x_nrns
#    print '\n## len of self_lyr_x_nrns: {}'.format( len(self_lyr_x_nrns) )  
#    print '## self_lyr_x_nrns[0]: {}'.format( self_lyr_x_nrns[0] )      
#       

# extract lyr_dsp_nrn  ---------------------------------
#    def extract_lyr_dsp_nrns(self): 
print '\n### {} :: extract lyr_dsp_nrn .... '.format(self_label)
lyr1_dsp_nrns=[] 
for idsp in range( 0, self_max_dsp+1 ):
    lyr1_idsp_nrns = []
    for nrn_idx in range ( self_n_nrns_lyr ):
        y_row, x_col = cnvrt.frm_nrn_indx_to_2D_grd( nrn_idx, self_n_cols , self_n_rows  )
        if x_col - y_row == idsp:
            lyr1_idsp_nrns.append( nrn_idx  )
    lyr1_dsp_nrns.append( lyr1_idsp_nrns )  
for idsp in range( self_min_dsp, 0 ):
    lyr1_idsp_nrns=[]
    for nrn_idx in range ( self_n_nrns_lyr):
        y_row, x_col = cnvrt.frm_nrn_indx_to_2D_grd( nrn_idx, self_n_cols , self_n_rows  )
        if x_col - y_row == idsp:
            lyr1_idsp_nrns.append( nrn_idx  )
    lyr1_dsp_nrns.append( lyr1_idsp_nrns )


lyr_dsp_nrns = [] 
lyr_dsp_nrns.append( lyr1_dsp_nrns  )   # lyr0 already computed
for ilyr in range( 1, self_n_lyrs ): 
    ilyr_dsp_nrns = []
    for idsp in range(   len(  lyr1_dsp_nrns )   ): 
        ilyr_idsp_nrns=[]
        for inrn in range(  len( lyr1_dsp_nrns[idsp] )     ):
            nrn_idx =   lyr1_dsp_nrns[idsp][inrn] + ilyr* self_n_nrns_lyr
            ilyr_idsp_nrns.append( nrn_idx  )
        ilyr_dsp_nrns.append( ilyr_idsp_nrns )
    lyr_dsp_nrns.append(  ilyr_dsp_nrns  )
self_lyr_dsp_nrns= lyr_dsp_nrns   
lyr1_dsp_nrns =[]       
lyr_dsp_nrns = []
print ' len of self_lyr_dsp_nrns: {}'.format( len(self_lyr_dsp_nrns) )  
#print '## self_lyr_dsp_nrns[0]: {}'.format( self_lyr_dsp_nrns[0] )      
   


#============================================================================================================
#====================================== projections rf2cnet  ================================================
#============================================================================================================
# Create  connlst_Lrf2cnet ---------------------------------
#    def create_Lrf2cnet_connlst (self):
 
def create_rf2cnet_connlst (p, self_label, self_rf_w, self_rf_h, self_rf2cnet_dly, self_rf2cnet_G,self_n_lyrs, self_n_rows, self_lyr_row_nrns, self_lyr_rf_nrns, self_lyr_col_nrns):
    print  '### ========================= {}============================== '.format(p)     
    print '\n### {} :: Create connlst_Lrf2cnet :: rf2cnet_dly={}, rf2cnet_G={}'.format( p ,self_rf2cnet_dly, self_rf2cnet_G )
    Lrf_conn_lst=[] 
    for ilyr in range ( self_n_lyrs ):
        for irow in range( self_n_rows ):
            for inrn in range ( len(self_lyr_row_nrns[ilyr][irow]) ):
                Lrf_conn_lst.append(   (  self_lyr_rf_nrns[ilyr][irow], self_lyr_row_nrns[ilyr][irow][inrn] )    )#, self_rf2cnet_G, self_rf2cnet_dly
    self_Lrf2cnet_connlst= Lrf_conn_lst   
    print ' len of self_Lrf2cnet_connlst: {}'.format( len(self_Lrf2cnet_connlst) )  
    print '## self_Lrf2cnet_connlst[0]: {}'.format( self_Lrf2cnet_connlst[0:20] )      
    #store TDXY as pkl file --------------------------------------------------
    rslts_fldr = 'connlsts/'
    pickle_filename = 'Lrf2cnet_connlsts_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_rf2cnet_dly, self_rf2cnet_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '#{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(self_Lrf2cnet_connlst, handle, protocol=pickle.HIGHEST_PROTOCOL)
    self_Lrf2cnet_connlst=[]

# Create  connlst_Rrf2cnet ---------------------------------
#    def create_Rrf2cnet_connlst (self):
    print '\n### {} :: Create connlst_Rrf2cnet :: rf2cnet_dly={}, rf2cnet_G={}'.format(self_label,self_rf2cnet_dly, self_rf2cnet_G)
    Rrf_conn_lst=[] 
    for ilyr in range ( self_n_lyrs ):
        for icol in range( self_n_rows ):
            for inrn in range ( len(self_lyr_col_nrns[ilyr][icol]) ):
                Rrf_conn_lst.append(   (  self_lyr_rf_nrns[ilyr][icol], self_lyr_col_nrns[ilyr][icol][inrn])    )#, self_rf2cnet_G, self_rf2cnet_dly 
    self_Rrf2cnet_connlst= Rrf_conn_lst   
    print ' len of self_Rrf2cnet_connlst: {}'.format( len(self_Rrf2cnet_connlst) )  
    print '## self_Rrf2cnet_connlst[0]: {}'.format( self_Rrf2cnet_connlst[0:20] )      
    #store TDXY as pkl file --------------------------------------------------
    rslts_fldr = 'connlsts/'
    pickle_filename = 'Rrf2cnet_connlsts_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_rf2cnet_dly, self_rf2cnet_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '#{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(self_Rrf2cnet_connlst, handle, protocol=pickle.HIGHEST_PROTOCOL)
    self_Rrf2cnet_connlst=[]
    print '#======================== {}:: done =========================\n '.format( p)       

    
        
        
        
#============================================================================================================        
# ====================================  Create self_connlst  =========================================
#============================================================================================================

# ====================================  Create rowcol_minh_connlst  =========================================
def create_rowcol_minh_connlst (p, klyrs, self_label, self_rf_w, self_rf_h, self_inlyr_rowcol_minh_dly, self_inlyr_rowcol_minh_G, self_n_cols, self_lyr_col_nrns, self_n_rows, self_lyr_row_nrns, self_n_lyrs ):
    print  '### ========================= {}============================== '.format(p)     
    print '### {} :: Create rowcol_minh_connlst :: inlyr_rowcol_minh_dly={}, inlyr_rowcol_minh_G ={}'.format(
    p, self_inlyr_rowcol_minh_dly , self_inlyr_rowcol_minh_G)
    #lyr0 inh itself ------------------------------------------------------------------------------------
    ilyr=0
    lyr0_minh_connlst=[]  
    for icol in range( self_n_cols ):        # for each col .... 
        for inrn in self_lyr_col_nrns[ilyr][icol]:   # for all nrn in same col
            for other_nrn in self_lyr_col_nrns[ilyr][icol]:
                if other_nrn != inrn: # for all nrn in that col but the concerned one
                    lyr0_minh_connlst.append(   ( inrn, other_nrn )    )#, self_inlyr_rowcol_minh_G, self_inlyr_rowcol_minh_dly
            
    for irow in range ( self_n_rows ):   # for each row
        for inrn in self_lyr_row_nrns[ilyr][irow]:   # for all nrn in same row
            for other_nrn in self_lyr_row_nrns[ilyr][irow]:
                if other_nrn != inrn: # for all nrn in that col but the concerned one
                    lyr0_minh_connlst.append(   ( inrn, other_nrn )    )#, self_inlyr_rowcol_minh_G, self_inlyr_rowcol_minh_dly                        
    #_n_inlyr_rowcol_minh_conn    
    self_n_inlyr_rowcol_minh_conn = len(lyr0_minh_connlst)         
    #print '## self._n_inlyr_rowcol_minh_conn  :{}'.format( self._n_inlyr_rowcol_minh_conn  )        
    #each lyr inh itself-----------------------------------------------------------------------------------
    self_lyr_inlyr_rowcol_minh_connlst =[]
    for ilyr in range( self_n_lyrs ): 
        ilyr_rowcol_inlyr_minh_connlst=[]
        for conn in range(   self_n_inlyr_rowcol_minh_conn   ): 
            ilyr_rowcol_inlyr_minh_connlst.append(     ( lyr0_minh_connlst[conn][0]+ilyr*self_n_nrns_lyr , 
                                          lyr0_minh_connlst[conn][1]+ilyr*self_n_nrns_lyr)   )#, self_inlyr_rowcol_minh_G, self_inlyr_rowcol_minh_dly
            self_lyr_inlyr_rowcol_minh_connlst.append( ilyr_rowcol_inlyr_minh_connlst )
    
    # each lyrinh other lyrs rowcol-----------------------------------------------------------------------
    self_lyr_outlyr_rowcol_minh_connlst =[]
    for ilyr in range( self_n_lyrs ):
        lwr_lyr=   ilyr-klyrs if (ilyr-klyrs > 0)  else 0
        upr_lyr=   ilyr+klyrs if (ilyr+klyrs < self_n_lyrs-1)  else  self_n_lyrs-1
        ilyr_rowcol_outlyr_minh_connlst=[]
        for klyr in range(lwr_lyr,  upr_lyr+1):
            #print '\n#########ilyr:{}, lwr_lyr, upr_lyr:  {} to {},     klyr:{}'.format(ilyr, lwr_lyr, upr_lyr, klyr)
            if klyr != ilyr:
                #print 'not equal'
                for conn in range(   self_n_inlyr_rowcol_minh_conn   ): 
                    ilyr_rowcol_outlyr_minh_connlst.append( (self_lyr_inlyr_rowcol_minh_connlst[ilyr][conn][0] , 
                                                   self_lyr_inlyr_rowcol_minh_connlst[ilyr][conn][1] + (klyr-ilyr)*self_n_nrns_lyr
                                                   )  )#  ,self_outlyr_rowcol_minh_G, self_outlyr_rowcol_minh_dly
        self_lyr_outlyr_rowcol_minh_connlst.append( ilyr_rowcol_outlyr_minh_connlst)
    print ' len of self_lyr_outlyr_rowcol_minh_connlst: {}'.format( len(self_lyr_outlyr_rowcol_minh_connlst) )  
#    print '## self_lyr_outlyr_rowcol_minh_connlst[0]: {}'.format( self_lyr_outlyr_rowcol_minh_connlst[0] )      


#store TDXY as pkl file --------------------------------------------------
    inlyr_rowcol_minh_connlst_1d = []
    for ilyr in range (self_n_lyrs):
#        print 'lyr {}'.format( ilyr)
        ilyr_conn = self_lyr_inlyr_rowcol_minh_connlst.pop( 0)
        for conn in range ( self_n_inlyr_rowcol_minh_conn ):
            inlyr_rowcol_minh_connlst_1d.append( ilyr_conn[conn] )
    rslts_fldr = 'connlsts/'
    pickle_filename = 'inlyr_rwcl_minh_connlsts_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_inlyr_rowcol_minh_dly, self_inlyr_rowcol_minh_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '##{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(inlyr_rowcol_minh_connlst_1d, handle, protocol=pickle.HIGHEST_PROTOCOL)
    inlyr_rowcol_minh_connlst_1d
    print '#{}:: inlyr_rwcl_minh_connlsts done, now oulyr \n '.format( p)

#store TDXY as pkl file --------------------------------------------------
    outlyr_rowcol_minh_connlst_1d = []
    for ilyr in range (self_n_lyrs):
        ilyr_conn = self_lyr_outlyr_rowcol_minh_connlst.pop( 0)
#        print ilyr, '   ', len(ilyr_conn)
        for conn in range ( len(ilyr_conn) ):
            outlyr_rowcol_minh_connlst_1d.append( ilyr_conn[conn] )
    rslts_fldr = 'connlsts/'
    pickle_filename = 'outlyr_rwcl_minh_connlsts_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_outlyr_rowcol_minh_dly, self_outlyr_rowcol_minh_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '#{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(outlyr_rowcol_minh_connlst_1d, handle, protocol=pickle.HIGHEST_PROTOCOL)
    outlyr_rowcol_minh_connlst_1d = []    
    print '#======================== {}:: done =========================\n '.format( p)       



## =========================================  Create x_minh_connlst   =========================================
#    def create_x_minh_connlst (self, klyrs):
#        print '\n### {} :: Create x_minh_connlst :: inlyr_x_minh_dly={}, inlyr_x_minh_G ={}'.format(
#        self._label, self._inlyr_xminh_dly , self._inlyr_xminh_G)       
#        #lyr0 inh itself -------------------------------------------------------------------------------------
#        ilyr=0
#        lyr0_xminh_connlst=[]  
#        for ix in range(self._min_x, self._max_x ):        # for each x value .... 
#            if len(self._lyr_x_nrns[ilyr][ix]) >0 : 
#                for inrn in self._lyr_x_nrns[ilyr][ix]:   # for each x_nrn in that x value ...
#                    for other_nrn in self._lyr_x_nrns[ilyr][ix]:   # for all nrn in same x_value
#    #                    print '## concerned_x_nrn: {}'.format(nrn )
#    #                    print '## other_x_nrn: {}'.format( x_nrn )
#                        if inrn != other_nrn: # for all other_x_nrn in that col but the concerned one
#                            lyr0_xminh_connlst.append(   (  inrn, other_nrn , self._inlyr_xminh_G, self._inlyr_xminh_dly )    )
#        #_n_inlyr_xminh_conn    
#        self._n_inlyr_xminh_conn = len(lyr0_xminh_connlst)         
##        print '## self._n_inlyr_xminh_conn  :{}'.format( self._n_inlyr_xminh_conn  )
#        #each lyr inh itself----------------------------------------------------------------------------------
#        self._lyr_inlyr_xminh_connlst =[]
#        for ilyr in range( self._n_lyrs ): 
#            ilyr_inlyr_xminh_connlst=[]
#            for conn in range(   self._n_inlyr_xminh_conn  ): 
#                ilyr_inlyr_xminh_connlst.append(     ( lyr0_xminh_connlst[conn][0]+ilyr*self._n_nrns_lyr , 
#                                              lyr0_xminh_connlst[conn][1]+ilyr*self._n_nrns_lyr, self._inlyr_xminh_G, self._inlyr_xminh_dly)   )
#            self._lyr_inlyr_xminh_connlst.append( ilyr_inlyr_xminh_connlst )
#        # each lyrinh other lyrs rowcol-----------------------------------------------------------------------
#        self._lyr_outlyr_xminh_connlst =[]
#        for ilyr in range( self._n_lyrs ):
#            lwr_lyr=   ilyr-klyrs if (ilyr-klyrs > 0)  else 0
#            upr_lyr=   ilyr+klyrs if (ilyr+klyrs < self._n_lyrs-1)  else  self._n_lyrs-1
#            ilyr_outlyr_xminh_connlst=[]
#            for klyr in range(lwr_lyr,  upr_lyr+1):
##                print '\n#########ilyr:{}, lwr_lyr, upr_lyr:  {} to {},     klyr:{}'.format(ilyr, lwr_lyr, upr_lyr, klyr)
#                if klyr != ilyr:
##                    print 'not equal'
#                    for conn in range(   self._n_inlyr_xminh_conn   ): 
#                        ilyr_outlyr_xminh_connlst.append( (self._lyr_inlyr_xminh_connlst[ilyr][conn][0] , 
#                                                       self._lyr_inlyr_xminh_connlst[ilyr][conn][1] + (klyr-ilyr)*self._n_nrns_lyr,
#                                                       self._outlyr_xminh_G, self._outlyr_xminh_dly)                                  )
#            self._lyr_outlyr_xminh_connlst.append( ilyr_outlyr_xminh_connlst)
#
#                for other_nrn in self_lyr_dsp_nrns[ilyr][idsp]:   # for all nrn in same x_value
#                    print inrn, other_nrn
## ======================================  Create x_dspmext_connlst  =========================================
def create_dsp_mext_connlst (p, klyrs,dsp_nghbors,  self_label,self_inlyr_dsp_mext_dly, self_inlyr_dsp_mext_G, self_lyr_dsp_nrns, self_n_lyrs  ):
    print  '### ========================= {}============================== '.format(p)         
    print '### {} :: Create dsp_mext_connlst :: inlyr_dsp_mext_dly={}, inlyr_dsp_mext_G ={}'.format(
    p, self_inlyr_dsp_mext_dly , self_inlyr_dsp_mext_G)         
    #lyr0 inh itself -----------------------------------------------------------------------------------
    ilyr=0
    lyr0_dsp_mext_connlst=[]  
    #print self._lyr_dsp_nrns[ilyr]
    for idsp in range( len(self_lyr_dsp_nrns[ilyr]) ):        # for each dsp value .... 
        if len(self_lyr_dsp_nrns[ilyr][idsp]) >0 : 
#            print '\n#### self_lyr_dsp_nrns[ilyr][idsp]: {}'.format(self_lyr_dsp_nrns[ilyr][idsp])
            for idx, inrn in enumerate( self_lyr_dsp_nrns[ilyr][idsp] ):   # for each x_nrn in that x value ...
#                for other_nrn in self_lyr_dsp_nrns[ilyr][idsp]:   # for all nrn in same x_value
                for klyr in range(1, dsp_nghbors+1):   # for all nrn in same x_value
#                    print 'idx: {}'.format(idx)
#                    print 'klyr: {}'.format(klyr)
#                    print 'self_lyr_dsp_nrns[idx]: {}'.format( self_lyr_dsp_nrns[ilyr][idsp][idx] )
#                    print 'self_lyr_dsp_nrns[idx-klyr]: {}'.format( self_lyr_dsp_nrns[ilyr][idsp][idx-klyr] )
#                    print 'self_lyr_dsp_nrns[idx+klyr]: {}'.format(self_lyr_dsp_nrns[ilyr][idsp][idx+klyr] )
                    if idx+klyr < len( self_lyr_dsp_nrns[ilyr][idsp] ): # for all other_x_nrn in that col but the concerned one
#                        print 'self_lyr_dsp_nrns[idx+klyr]: {}'.format(self_lyr_dsp_nrns[ilyr][idsp][idx+klyr] )
                        lyr0_dsp_mext_connlst.append(   (  inrn, self_lyr_dsp_nrns[ilyr][idsp][idx+klyr]) )# , self_inlyr_dsp_mext_G, self_inlyr_dsp_mext_dly
                   
                    if idx-klyr >= 0 : # for all other_x_nrn in that col but the concerned one
#                        print 'self_lyr_dsp_nrns[idx-klyr]: {}'.format(self_lyr_dsp_nrns[ilyr][idsp][idx-klyr] )
                        lyr0_dsp_mext_connlst.append(   (  inrn, self_lyr_dsp_nrns[ilyr][idsp][idx-klyr])  )#  , self_inlyr_dsp_mext_G, self_inlyr_dsp_mext_dly 

    self_n_inlyr_dsp_mext_conn = len(lyr0_dsp_mext_connlst)         
    
    #each lyr inh itself-------------------------------------------------------------------------------
    self_lyr_inlyr_dsp_mext_connlst =[]
    for ilyr in range( self_n_lyrs ): 
        ilyr_inlyr_dsp_mext_connlst=[]
        for conn in range(   self_n_inlyr_dsp_mext_conn  ): 
            ilyr_inlyr_dsp_mext_connlst.append(     ( lyr0_dsp_mext_connlst[conn][0]+ilyr*self_n_nrns_lyr , 
                                          lyr0_dsp_mext_connlst[conn][1]+ilyr*self_n_nrns_lyr)   )#, self_inlyr_dsp_mext_G, self_inlyr_dsp_mext_dly
        self_lyr_inlyr_dsp_mext_connlst.append( ilyr_inlyr_dsp_mext_connlst )
        
    # each lyr pre-ext other lyrs _dsp_mext-----------------------------------------------------------
    self_lyr_outlyr_dsp_mext_connlst =[]
    for ilyr in range( self_n_lyrs ):
        lwr_lyr=   ilyr-klyrs if (ilyr-klyrs > 0)  else 0
        upr_lyr=   ilyr+klyrs if (ilyr+klyrs < self_n_lyrs-1)  else  self_n_lyrs-1
        ilyr_outlyr_dsp_mext_connlst=[]
        for klyr in range(lwr_lyr,  upr_lyr+1):
            #print '\n#########ilyr:{}, lwr_lyr, upr_lyr:  {} to {},     klyr:{}'.format(ilyr, lwr_lyr, upr_lyr, klyr)
            if klyr != ilyr:
                #print 'not equal'
                for conn in range(   self_n_inlyr_dsp_mext_conn   ): 
                    ilyr_outlyr_dsp_mext_connlst.append( (self_lyr_inlyr_dsp_mext_connlst[ilyr][conn][0] , 
                                                   self_lyr_inlyr_dsp_mext_connlst[ilyr][conn][1] + (klyr-ilyr)*self_n_nrns_lyr,
                                                   )   )#self_outlyr_dsp_mext_G, self_outlyr_dsp_mext_dly    
        self_lyr_outlyr_dsp_mext_connlst.append( ilyr_outlyr_dsp_mext_connlst)
    print ' len of self_lyr_outlyr_dsp_mext_connlst: {}'.format( len(self_lyr_outlyr_dsp_mext_connlst) )  

#store TDXY as pkl file --------------------------------------------------
    inlyr_dsp_mext_connlst = []
    for ilyr in range (self_n_lyrs):
#        print 'lyr {}'.format( ilyr)
        ilyr_conn = self_lyr_inlyr_dsp_mext_connlst.pop( 0)
        for conn in range ( len(ilyr_conn) ):
            inlyr_dsp_mext_connlst.append( ilyr_conn[conn] )
    rslts_fldr = 'connlsts/'
    pickle_filename = 'inlyr_dsp_mext_connlst_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_inlyr_dsp_mext_dly, self_inlyr_dsp_mext_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '#{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(inlyr_dsp_mext_connlst, handle, protocol=pickle.HIGHEST_PROTOCOL)
    inlyr_dsp_mext_connlst =[]
    print '#{}:: inlyr_dsp_mext_connlsts done, now oulyr_dsp \n '.format( p)

#store TDXY as pkl file --------------------------------------------------
    outlyr_dsp_mext_connlst = []
    for dsp in range ( len(self_lyr_outlyr_dsp_mext_connlst) ):
#        print 'dsp {}'.format( disp_lyr)
        dsp_conn = self_lyr_outlyr_dsp_mext_connlst.pop( 0)
        for conn in range ( len(dsp_conn) ):
            outlyr_dsp_mext_connlst.append( dsp_conn[conn] )
    rslts_fldr = 'connlsts/'
    pickle_filename = 'outlyr_dsp_mext_connlst_{}x{}_{}w{}.pickle'.format(self_rf_w, self_rf_h, self_outlyr_rowcol_minh_dly, self_outlyr_rowcol_minh_G )
    connlst_pth    = cnvrt.write_flenfldr_ncrntpth(rslts_fldr, pickle_filename )
    print '#{}:: @path:: {}, \n '.format( p,  connlst_pth )
    with open( connlst_pth , 'wb') as handle:
        pickle.dump(outlyr_dsp_mext_connlst, handle, protocol=pickle.HIGHEST_PROTOCOL)
    outlyr_dsp_mext_connlst = []    
    print '#======================== {}:: done =========================\n '.format( p)       

#=================================================================================================================    
    
    
    
#                 
print '========================= generate_weights ======================'                 
klyrs =1 #number of the neighbour layer that will affected when one neuron spikes
dsp_nghbors = 3

p1= multiprocessing.Process(target=create_rf2cnet_connlst, 
                                args=('p1',self_label, self_rf_w, self_rf_h, self_rf2cnet_dly, self_rf2cnet_G,
                                      self_n_lyrs, self_n_rows, self_lyr_row_nrns, self_lyr_rf_nrns, self_lyr_col_nrns)  )  
                                
p2= multiprocessing.Process(target=create_rowcol_minh_connlst, 
                                args=( 'p2',klyrs, self_label, self_rf_w, self_rf_h, self_inlyr_rowcol_minh_dly,
                                      self_inlyr_rowcol_minh_G, self_n_cols, self_lyr_col_nrns, self_n_rows, self_lyr_row_nrns, self_n_lyrs )  )  


p3= multiprocessing.Process(target=create_dsp_mext_connlst, 
                                args=('p3',  klyrs,dsp_nghbors,  self_label,self_inlyr_dsp_mext_dly, self_inlyr_dsp_mext_G, 
                                      self_lyr_dsp_nrns, self_n_lyrs,  )  )

p1.start()
p2.start()
p3.start()

p1.join()
p2.join()
p3.join()
print '!!!!!!!!!!!!!!!!!!!!!!! done !!!!!!!!!!!!!!!!!!!!!'
    
    




