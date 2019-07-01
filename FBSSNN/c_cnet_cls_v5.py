#!/usr/bin/env python2
# -*- coding: utf-8 -*-
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

#logger = logging.getLogger(__file__)
        
class C_NET(object):
    def __init__(self, Lrf_, Rrf_, lif_param_,  label_, dly_, G_, max_dsp_, min_dsp_ ) :
        if Lrf_._wdth != Rrf_._wdth or Lrf_._hght != Rrf_._hght:
            print '## ERROR:  Lrf_._wdth != Rrf_._wdth or Lrf_._hght != Rrf_._hght'
            return False
        self._Lrf = Lrf_
        self._Rrf = Rrf_
                
        self._min_dsp = min_dsp_   # -( self._Lrf._wdth - 1 )      # min_dsp_
        self._max_dsp = max_dsp_  # ( self._Lrf._wdth - 1 )       # max_dsp_
        self._min_x = 0
        self._max_x = 2*( self._Lrf._wdth -1 )
        
        self._n_lyrs  = self._Lrf._hght
        self._n_rows  = self._Lrf._wdth 
        self._n_cols  = self._Lrf._wdth  
        self._n_dsps  = self._max_dsp - self._min_dsp
        self._n_xs     = self._max_x - self._min_x 
        
        self._n_nrns_lyr = self._n_rows * self._n_cols
        self._n_nrns_row = self._n_cols 
        self._n_nrns_col = self._n_rows 
        
        self._n_inlyr_rowcol_minh_conn = None
        self._n_inlyr_dsp_mext_conn = None
        self._n_inlyr_xminh_conn = None
        
        
        self._label = label_
        self._pop_sz = self._n_rows * self._n_cols * self._n_lyrs 
        self._pop = None
        self._lif_param= lif_param_
        self._out_spks = None
        self._out_v    = None
        self._stop_tm= None
        
        
        self._rf2cnet_dly      = None
        self._rf2cnet_G        = None
        self._Lrf2cnet_connlst = None
        self._Rrf2cnet_connlst = None
        self._Lrf2cnet_proj  = None
        self._Rrf2cnet_proj  = None

        
        self._lyr_nrns = []
        self._lyr_Lrf_nrns = []
        self._lyr_Rrf_nrns = []
        self._lyr_col_nrns = []
        self._lyr_row_nrns = [] 
        self._lyr_x_nrns = []
        self._lyr_dsp_nrns = []
        
        self._lyr_inlyr_rowcol_minh_connlst = None
        self._lyr_outlyr_rowcol_minh_connlst = None
        self._lyr_inlyr_xminh_connlst = None
        self._lyr_outlyr_xminh_connlst = None
        self._lyr_inlyr_dsp_mext_connlst = None
        self._lyr_outlyr_dsp_mext_connlst = None
        
        
        self._inlyr_rowcol_minh_dly = None
        self._inlyr_rowcol_minh_G = None  
        self._outlyr_rowcol_minh_dly = None
        self._outlyr_rowcol_minh_G = None  
        
        self._inlyr_xminh_dly = None 
        self._inlyr_xminh_G= None    
        self._outlyr_xminh_dly = None 
        self._outlyr_xminh_G= None  

        self._inlyr_dsp_mext_dly = None
        self._inlyr_dsp_mext_G= None
        self._outlyr_dsp_mext_dly = None 
        self._outlyr_dsp_mext_G= None       
        
        
        self._minh_connlst = None
        self._minh_proj = None
        self._mext_connlst = None
        self._mext_proj = None
        
        rf2cnet_dly = 0
        selfcnet_dly = 0
        rf2cnet_w = 3
        cnet_inh_w= -50
        cnet_ext_w= 1.5
        print "\n### {} :: Creating pop .... ".format ( self._label)
        self._pop=  sim.Population(self._pop_sz,  sim.IF_curr_exp(**self._lif_param),                
                                   label=self._label  )    


        rslts_fldr = 'connlsts/' #rslts_fldr = 'rslts/{}/{}'.format( spks_fldr, scrpt_nm.split('.')[0]  )
            
        fle1 = 'Lrf2cnet_connlsts_31x31_1w20.pickle'
#        fle1 = 'Lrf2cnet_connlsts_109x109_1_2.pickle'
        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle1)
        print 'pth1 : {}'.format(pth)
        with open(pth , 'rb') as pkl:
            connlst = pickle.load(pkl)
            print '## len:  {}'.format( len( connlst ) )
        self._Lrf2cnet_proj =   sim.Projection(  self._Lrf._pop, self._pop,
                                      sim.FromListConnector(connlst),
                                      synapse_type=sim.StaticSynapse(weight= rf2cnet_w, delay= rf2cnet_dly),
                                      receptor_type='excitatory', space=None, source=None,
                                      label='{} --> {}'.format( self._Lrf._label, self._label)    )
        connlst=[]    
#        self._Rrf2cnet_proj = self._Lrf2cnet_proj    
#            
        fle2 = 'Rrf2cnet_connlsts_31x31_1w20.pickle'
#        fle2 = 'Rrf2cnet_connlsts_109x109_1_2.pickle'
        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle2)
        print 'pth2 : {}'.format(pth)
        with open(pth , 'rb') as pkl:
            connlst = pickle.load(pkl)
            print '## len:  {}'.format( len( connlst ) )            
        self._Rrf2cnet_proj =   sim.Projection( self._Rrf._pop,  self._pop, 
                                      sim.FromListConnector(connlst),
                                      synapse_type=sim.StaticSynapse(weight= rf2cnet_w, delay= rf2cnet_dly),
                                      receptor_type='excitatory', #space=None, source=None,
                                      label='{} --> {}'.format( self._Rrf._label, self._label )  )    
        connlst=[]    
        self._Lrf2cnet_proj = self._Rrf2cnet_proj    
        fle5 = 'inlyr_dsp_mext_connlst_31x31_0w2.0.pickle'
        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle5)
        print 'pth5 : {}'.format(pth)
        with open(pth , 'rb') as pkl:
            connlst = pickle.load(pkl)
            print '## len:  {}'.format( len( connlst ) )
        self._mext_proj =   sim.Projection( self._pop,  self._pop, 
                                      sim.FromListConnector(connlst),
                                      synapse_type=sim.StaticSynapse(weight= cnet_ext_w, delay= selfcnet_dly),
                                      receptor_type='excitatory', #space=None, source=None,
                                      label='mutual_mext_proj_{}'.format( self._label )  )            
#            
#            
            
        fle6 = 'outlyr_dsp_mext_connlst_31x31_0w20.pickle'
        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle6)
        print 'pth : {}'.format(pth)
        with open(pth , 'rb') as pkl:
            connlst = pickle.load(pkl)
            print '## len:  {}'.format( len( connlst ) )
        self._mext_proj =   sim.Projection( self._pop,  self._pop, 
                                      sim.FromListConnector( connlst ),
                                      synapse_type=sim.StaticSynapse(weight= cnet_ext_w, delay= selfcnet_dly),
                                      receptor_type='excitatory', #space=None, source=None,
                                      label='mutual_mext_proj_{}'.format( self._label )  )        
#
        fle3 = 'inlyr_rwcl_minh_connlsts_31x31_0w20.pickle'        
        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle3)
        print 'pth3 : {}'.format(pth)
        with open(pth , 'rb') as pkl:
            connlst0 = pickle.load(pkl)
        print '## len0:  {}'.format( len( connlst0 ) )
        print '## connlst0[0:10]:  {}'.format(  connlst0[0:30] )
        
#        for conn in range ():
#        connlst = connlst0[0:150000]
#        print '## len_cut:  {}'.format( len( connlst ) )
#        self._minh_proj1 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= selfcnet_dly),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj1_{}'.format( self._label )  )
#        connlst = connlst0[150001:300000]
#        print '## len_cut:  {}'.format( len( connlst ) )
#        self._minh_proj2 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= selfcnet_dly),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj2_{}'.format( self._label )  )
#        connlst = connlst0[300001:450000]
#        print '## len_cut:  {}'.format( len( connlst ) )
#        self._minh_proj3 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= selfcnet_dly),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj3_{}'.format( self._label )  )
#
#        connlst = connlst0[450001:len(connlst0)]
#        print '## len_cut:  {}'.format( len( connlst ) )
#        self._minh_proj4 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= 0.5),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj3_{}'.format( self._label )  )
        self._minh_project =[]
        for i in range (  (len(connlst0)/180000)+1):
            j= i*180000
            k= j + 180000 
            if k< len(connlst0):
                print i, j, k
                connlst = connlst0[j:k]
                print '\n## len_cut:  {}'.format( len( connlst ) )
                self._minh_project.append(  sim.Projection( self._pop,  self._pop, 
                                              sim.FromListConnector(connlst),
                                              synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= 0.5),
                                              receptor_type='inhibitory', #space=None, source=None,
                                              label='mutual_minh_proj{}_{}'.format( i, self._label )  )   )
            
            if k>= len(connlst0):
                k =len(connlst0)-1
                print i, j, k
                connlst = connlst0[j:k]
                print'k>len'                
                print '\n## len_cut:  {}'.format( len( connlst ) )
                self._minh_project.append(  sim.Projection( self._pop,  self._pop, 
                                              sim.FromListConnector(connlst),
                                              synapse_type=sim.StaticSynapse(weight= cnet_inh_w, delay= 0.5),
                                              receptor_type='inhibitory', #space=None, source=None,
                                              label='mutual_minh_proj{}_{}'.format(i,  self._label )  )  )
                break
#        connlst = connlst0[ len(connlst0)-2: len(connlst0)-1]
#        print '## len_cut:  {}'.format( connlst )
#        self._minh_proj0 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= -3, delay= 0.5),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj0_{}'.format( self._label )  )
#                                      
#        self._minh_proj00 =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      synapse_type=sim.StaticSynapse(weight= 3, delay= 0.5),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj0_{}'.format( self._label )  )

###
#
#        fle4 = 'outlyr_rwcl_minh_connlsts_41x41_0_2.pickle'
#        pth = cnvrt.read_flenfldr_ncrntpth(rslts_fldr, fle4)
#        print 'pth4 : {}'.format(pth)
#        with open(pth , 'rb') as pkl:
#            connlst = pickle.load(pkl)
#            print '## len:  {}'.format( len( connlst ) )
#        self._minh_proj =   sim.Projection( self._pop,  self._pop, 
#                                      sim.FromListConnector(connlst),
#                                      #synapse_type=sim.StaticSynapse(weight= W_rtna2rf, delay= dly_rtna_rf),
#                                      receptor_type='inhibitory', #space=None, source=None,
#                                      label='mutual_minh_proj_{}'.format( self._label )  )  
##            
        print '=============== projection done !!! ======================'
        

#============================================================================================================
#====================================== population operations ===============================================
#============================================================================================================
        
    # write data to pickle file-----------------------------------------------
    def write_data(self, rslts_fldr_ ):
       """ should be called after sim.run otherwise it will write empty file"""
       rslt_fle =  cnvrt.write_flenfldr_ncrntpth(  rslts_fldr_, '{}.pickle'.format(self._label) ) 
       self._pop.write_data( rslt_fle  )
       print '\n### {}:: data stored in file : \n{}'.format(self._pop.label, rslt_fle )


    # set lif_param for a pop -------------------------------------------------
    def set_lif_param_of_pop(self, lif_param_):
        print '### {} :: set_lif_param_of_pop .... '.format(self._label)
        self._pop.set(         cm = lif_param_['cm']          )
        self._pop.set(      tau_m = lif_param_['tau_m']       )
        self._pop.set( tau_refrac = lif_param_['tau_refrac']  )
        self._pop.set(  tau_syn_E = lif_param_['tau_syn_E']   )
        self._pop.set(  tau_syn_I = lif_param_['tau_syn_I']   )
        self._pop.set(     v_rest = lif_param_['v_rest']      )
        self._pop.set(    v_reset = lif_param_['v_reset']     )
        self._pop.set(   v_thresh = lif_param_['v_thresh']    )
        self._pop.set(   i_offset = lif_param_['i_offset']    )
        self._lif_param = self.get_crnt_lif_param() # or lif_param_ to update it
        
    
    
    # get current values  of lif_para------------------------------------------
    def get_crnt_lif_param(self):
        print '### {} :: get_crnt_lif_param .... '.format(self._label)
        param ={}
        for key in self._lif_param:
            param[key]= self._pop.get(key)#[0]
        self._lif_param = param
        return self._lif_param
         
    
    # print current values  of lif_para----------------------------------------
    def prnt_crnt_lif_param(self):
            self.get_crnt_lif_param()
            print '### {}._lif_param : \n{}'.format( self._pop.label, self._lif_param  )
  

    # get recorded spks -------------------------------------------------------
    def get_spks(self):
        """  should be called bet run and end, after calling you can axis attributes:
            self._out_spks and self._stop_tm -- it mainly rturns recorded spks,"""
        """  should be called bet run and end, after calling you can axis attributes:
            self._out_spks,  self._out_v,  and self._stop_tm -- it does not return,
            its called by other methods get_spks and get_v"""
        print '\n### {}:: get_spks for all pop,  now (_out_spks, _stop_tm) have values '.format(self._label )
        rf_neo  =  self._pop.get_data(variables=["spikes"])  
        self._out_spks=  rf_neo.segments[0].spiketrains 
        self._stop_tm = float( self._out_spks[0].t_stop)
        return self._out_spks

    # get recorded voltage-----------------------------------------------------
    def get_v(self):
        """  should be called bet run and end, after calling you can axis attributes:
            self._out_spks and self._stop_tm -- it mainly rturns recorded spks,"""
        """  should be called bet run and end, after calling you can axis attributes:
            self._out_spks,  self._out_v,  and self._stop_tm -- it does not return,
            its called by other methods get_spks and get_v"""
        print '\n### {}:: get_v for all pop,  now (_out_v, _stop_tm) have values '.format(self._label )
        rf_neo  =  self._pop.get_data(variables=["v"])  
        self._out_v= rf_neo.segments[0].filter(name="v")[0]   # simulation [:] otherwise[0]
        self._stop_tm = float( self._out_spks[0].t_stop)
        return self._out_v

  
    def plt_spks( self, lrf, Rrf, v=1, wth_param=1):
        """ plot recorded spks of rtna, should called after calling self.get_data() methods, so 
           self._out_spks, self._out_spks, and self._stop_tm can be accessable"""
        if wth_param ==1:
            param =self.get_crnt_lif_param() 
            ttle= "{}, \n {}".format(self._label, param)
        else:
            ttle= "{}".format(self._label)
        if v==1:
            print '\n### {}:: plot in_rtna_out_spks, rf_pop_v, and rf_pop_spks .... '.format(self._pop.label )
            plot.Figure(
            plot.Panel(lrf._out_spks, yticks=True, xlim=(0, self._stop_tm)), 
            plot.Panel(Rrf._out_spks, yticks=True, xlim=(0, self._stop_tm)), 
            plot.Panel( self._out_v, yticks=True, xticks=True, xlim=(0, self._stop_tm) ), 
            plot.Panel(self._out_spks,     yticks=True, xticks=True, markersize=5, xlim=(0, self._stop_tm)),
            title= ttle
            )
        else:
            print '\n### {}:: plot in_rtna_out_spks, and rf_pop_spks .... '.format(self._pop.label )
            plot.Figure(
            plot.Panel(lrf._out_spks, yticks=True, xlim=(0, self._stop_tm)), 
            plot.Panel(Rrf._out_spks, yticks=True, xlim=(0, self._stop_tm)), 
#            plot.Panel( self._out_v, yticks=True, xticks=True, xlim=(0, self._stop_tm) ), 
            plot.Panel(self._out_spks,     yticks=True, xticks=True, markersize=5, xlim=(0, self._stop_tm)),
            title= ttle
            )
    

#============================================================================================================
#================================== population network characteristic =======================================
#============================================================================================================
 
    # print some characteristics-----------------------------------------------
    def prnt_chs(self):
        print '\n###### general ch\'s of {}  =================================='.format(self._label)
        print '# label                 :   {}'.format(self._label)
        print '# wdth                  :   {}'.format(self._n_cols)
        print '# hght                  :   {}'.format(self._n_rows)
        print '# n_of_pop              :   {}'.format( len(self._pop) )
        print '# min_dsp               :   {}'.format( self._min_dsp )
        print '# max_dsp               :   {}'.format( self._max_dsp )
        print '# min_x                 :   {}'.format( self._min_x  ) 
        print '# max_x                 :   {}'.format( self._max_x   ) 
        
        print '# lif_param             :   {}'.format(self._lif_param)
        print '# stop_tm               :   {}'.format( self._stop_tm )
        print '# out_spks              :   {}'.format( self._out_spks)
        print '# related L-nrns        :   {}'.format( self._lyr_Lrf_nrns )
        print '# related R-nrns        :   {}'.format( self._lyr_Rrf_nrns )
        print '# self._row_nrns        :   {}'.format( self._row_nrns )
        print '# self._col_nrns        :   {}'.format( self._col_nrns )
        print '# self._dsp_nrns        :   {}'.format( self._dsp_nrns )
        print '# self._x_nrns          :   {}'.format( self._x_nrns )
        print '# self._2Lrf_proj       :   {}'.format( self._2Lrf_proj )
        print '# self._2Rrf_proj       :   {}'.format( self._2Rrf_proj )
        print '# self._minh_proj       :   {}'.format( self._minh_proj )        
        
        print '# self._2Lrf_connlst    :   {}'.format( self._2Lrf_connlst )
        print '# self._2Rrf_connlst    :   {}'.format( self._2Rrf_connlst )
        print '# self._minh_connlst    :   {}'.format( self._minh_connlst )
        print '# self._xminh_connlst    :   {}'.format( self._xminh_connlst )
        print '# self._dspmext_connlst    :   {}'.format( self._dspmext_connlst )
        
        print '----------------------------------------------------------------'
        print '#### ch\' of {}       :'.format(self._label)
        #print 'positions            :   {}'.format(L_rtna._positions)
        print 'label                 :   {}'.format(self._pop.label)
        print 'size = n_nrns         :   {}'.format(self._pop.size)
#        print 'local_size           :   {}'.format(self._pop.local_size)
        print 'structure             :   {}'.format(self._pop.structure)
#        print 'length               :   {}'.format(len(self._pop))
#        print 'length__             :   {}'.format(self._pop.__len__())
        print 'first_id              :   {}'.format(self._pop.first_id) 
        print 'last_id               :   {}'.format(self._pop.last_id)
        print 'index of first id     :   {}'.format(self._pop.id_to_index(self._pop.first_id))
#        print 'all_ids              :  {} '.format(self._pop._all_ids)
        print '================================================================'




    # print all conn lst  ------------------------------------
    def prnt_conn_lsts(self, lyr):
        print '\n=============================== {}_lyr[{}] :: prnt_conn_lsts ======================================='.format(self._label, lyr)
        print '## self._n_inlyr_rowcol_minh_conn               :   {}'.format( self._n_inlyr_rowcol_minh_conn )
        print '## self._n_inlyr_xminh_conn                     :   {}'.format( self._n_inlyr_xminh_conn )
        print '## self._n_inlyr_dsp_mext_conn                  :   {}'.format( self._n_inlyr_dsp_mext_conn )
        
        print '\n## self._Lrf2cnet_connlst [{}]                :   \n{}'.format( lyr,  self._Lrf2cnet_connlst[ lyr*self._n_nrns_lyr : (lyr+1)*self._n_nrns_lyr ] )
        print '\n## self._Rrf2cnet_connlst [{}]                :   \n{}'.format( lyr,  self._Rrf2cnet_connlst[ lyr*self._n_nrns_lyr : (lyr+1)*self._n_nrns_lyr ] )
        print '\n## self._lyr_inlyr_rowcol_minh_connlst [{}]   :  {}\n{}'.format( lyr,  len(self._lyr_inlyr_rowcol_minh_connlst[lyr]),   self._lyr_inlyr_rowcol_minh_connlst[lyr] )
        print '\n## self._lyr_inlyr_xminh_connlst [{}]         :  {} \n{}'.format( lyr,  len(self._lyr_inlyr_xminh_connlst[lyr]),         self._lyr_inlyr_xminh_connlst[lyr] )
        print '\n## self._lyr_inlyr_dsp_mext_connlst [{}]      :  {} \n{}'.format( lyr,   len(self._lyr_inlyr_dsp_mext_connlst[lyr]),      self._lyr_inlyr_dsp_mext_connlst[lyr] )
        print '\n## self._lyr_outlyr_rowcol_minh_connlst [{}]  :  {} \n{}'.format( lyr, len(self._lyr_outlyr_rowcol_minh_connlst[lyr]),  self._lyr_outlyr_rowcol_minh_connlst[lyr] )
        print '\n## self._lyr_outlyr_xminh_connlst [{}]        :  {} \n{}'.format( lyr,  len(self._lyr_outlyr_xminh_connlst[lyr]),       self._lyr_outlyr_xminh_connlst[lyr] )
        print '\n## self._lyr_outlyr_dsp_mext_connlst [{}]     :  {} \n{}'.format( lyr,  len(self._lyr_outlyr_dsp_mext_connlst[lyr]),    self._lyr_outlyr_dsp_mext_connlst[lyr] )
        
        
        
    # print proj chs of each pop of the rf ------------------------------------
    def prnt_proj_chs(self):
        """   should call after  after sim.run like all commands has xxx.get() """
#        print inhb_proj[0].receptor_type
        print '\n====================================== cnet_lyr : {} ============================================='.format(self._label)
        print'--------------------------- {} ---------------------------'.format(self._Lrf2cnet_proj)  
        print '#### _2Lrf_proj                :{}'.format(self._Lrf2cnet_proj)  
        print '\n#### _2Lrf_proj_delay_array          :\n{}'.format(self._Lrf2cnet_proj.get('delay', format='array')  )
        print '\n##### _2Lrf_proj_weights_array        :\n{}'.format(self._Lrf2cnet_proj.get('weight', format='array') )
        
        
        print'\n--------------------------- {} ----------------------------'.format(self._2Rrf_proj) 
        print '#### _2Rrf_proj                :\n{}'.format(self._Rrf2cnet_proj)  
        print '\n#### _2Lrf_proj_delay_array          :\n{}'.format(self._Rrf2cnet_proj.get('delay', format='array')  )
        print '\n##### _2Lrf_proj_weights_array        :\n{}'.format(self._Rrf2cnet_proj.get('weight', format='array') )
        
        
        print '====================================================================================='    
           

        
        
# wrapper to create cnet ========================================================
def create_cnet_lyr(Lrf_, Rrf_, lif_param_, dly2rf, G2rf, max_dsp_, min_dsp_, label_='cnet'):

    cnet = C_NET( Lrf_, Rrf_, lif_param_,  label_, dly2rf, G2rf, max_dsp_, min_dsp_ )
    print '## self._n_lyrs:  {}'.format(  cnet._n_lyrs )
    print '## self._n_rows:  {}'.format(  cnet._n_rows )
    print '## self._n_cols:  {}'.format(  cnet._n_cols )                                
    return cnet
#==============================================================================











