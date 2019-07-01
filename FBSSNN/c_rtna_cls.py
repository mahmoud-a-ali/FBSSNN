
"""
Created on Sat May 26 15:43:20 2018

@author: mali
"""


import time 
import os
import logging
import pickle
import spynnaker8 as sim 
#import pyNN.spiNNaker as sim
#import pyNN.neuron as sim 
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt
import print_chs as prnt
    
class Retina(object):
    def __init__(self, spks_pth_ ,  wdth_ , hght_, label_):
        self._wdth  = wdth_
        self._hght  = hght_
        self._label = label_
        self._pop_sz = self._wdth * self._hght
        self._spk_fle_pth = spks_pth_
        self._out_spks = None
        self._stop_tm= None
        print '## {}:: INFO w={}, h={}, sz={}'.format(self._label,  self._wdth, self._hght, self._pop_sz)
        
        
        if spks_pth_ is None:
            print '### {} :: error, no spks_ is specified ... spks_pth = {}'.format(self._label, spks_pth_)
            self._in_spks= None
            self._pop = None
        else:
            with open(spks_pth_ , 'rb') as pkl:
                self._in_spks = pickle.load(pkl)
                print '## {}:: spks_pth is loaded ! : \n {}'.format(self._label,  spks_pth_)
                print '###### length: {}'.format( len(self._in_spks) )
                print self._in_spks  
                spks=[]
                for nrn in range( len(self._in_spks) ):
                    nrn_spks =[]
                    if self._in_spks[nrn] ==[]:
                        nrn_spks.append( [] )
                    else:
                        for tm in range( len(self._in_spks[nrn]) ):
                            nrn_spks.append( float (self._in_spks[nrn][tm]))
                    spks.append( nrn_spks )     
                self._pop = sim.Population(self._pop_sz, sim.SpikeSourceArray(spike_times=spks ), label=self._label)


    # recording data-----------------------------------------------------------
    def record_data(self):
        """ called befor sim.run"""
        print '## {}:: recording data  .... '.format(self._label)
        self._pop.record(["spikes"])
    
    
    # write data to pickle file-----------------------------------------------
    def write_data(self, out_pklfle_path_ ):
        """ should be called after sim.run otherwise it will write empty file"""
#        print out_pklfle_path_
        self._pop.write_data(out_pklfle_path_)
        print '\n## {} :: data stored as : \n{}'.format(self._label, out_pklfle_path_ )


    # get recorded spks -------------------------------------------------------
    def get_spks(self):
        """  should be called bet run and end, after calling you can axis attributes:
            self._out_spks and self._stop_tm -- it mainly rturns recorded spks,"""
        print '\n### {}:: get_spks .... '.format(self._label )
        rtna_neo  =  self._pop.get_data(variables=["spikes"])  
        self._out_spks =  rtna_neo.segments[0].spiketrains 
        self._stop_tm = float( self._out_spks[0].t_stop)
        return self._out_spks


    #plt_spks after sim--------------------------------------------------------
    def plt_spks( self):
        """ plot recorded spks of rtna, should called after calling self.get_spks() methods, so 
        both self._out_spks and self._stop_tm can be accessable"""
        plot.Figure(
        plot.Panel( self._out_spks, yticks=True, xticks=True, xlim=(0, self._stop_tm) ), 
        title= self._label
        )


    # print some characteristics-----------------------------------------------
    def prnt_chs(self):
        print '\n###### general ch\'s of {}  =================================='.format(self._label)
        print 'label                 :   {}'.format(self._label)
        print 'wdth                  :   {}'.format(self._wdth)
        print 'hght                  :   {}'.format(self._hght)
        print 'size_of_pop           :   {}'.format( self._pop_sz )
        print 'input spk_fle_pth     :   {}'.format( self._spk_fle_pth )
        print 'stop_tm               :   {}'.format( self._stop_tm )
        print 'out_spks              :   {}'.format( self._out_spks)
        print '----------------------------------------------------------------'
        print '### ch\'s of {}_pop:'.format(self._label)
        print 'size                  :   {}'.format(self._pop.size)
        print 'structur              :   {}'.format(self._pop.structure)
        print 'label                 :   {}'.format(self._pop.label)
        print 'length                :   {}'.format(len(self._pop))
        print '================================================================'
        
        
#==============================================================================   
def create_rtna(spks_pth_,  wdth_ , hght_, label_):
    rtna = Retina(spks_pth_ ,  wdth_, hght_, label_)
    return rtna



























