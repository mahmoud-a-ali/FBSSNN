#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 18 12:40:30 2018

@author: mali

to generate  icub in such away that wach letter with different disp
"""
import comn_conversion as cnvrt
import numpy as np
import random


# check desired requirements ==================================================
rtna_w = 64
rtna_h = 64
#line_len = 25
t_shft = .5 #msec
t_res = 0.01 #msec

i_dsp= 12
c_dsp= -8
u_dsp= -4
b_dsp= 5

n_shfts=3


ch_idx =0
t_idx = 1
pol_idx = 2
x_idx = 3
y_idx = 4

print '\n####### generateicub stimulus .... '
#-----------------------------------------------------------------------------
def Hline(xi, xf, y):
    x_=[]
    y_=[]
    for x in range(xi, xf+1 ):
        x_.append(x)        
        y_.append(y)
    return (x_, y_)
#-----------------------------------------------------------------------------
def Vline(yi, yf, x):
    x_=[]
    y_=[]
    for y in range(yi, yf+1 ):
        x_.append(x)        
        y_.append(y)
    return (x_, y_)
#-----------------------------------------------------------------------------

Xi1 ,Yi1 =Hline(10, 12, 22)
Xi2 ,Yi2 =Hline(10, 12, 38)
Xi3 ,Yi3 =Vline(22, 38, 11)
Xi= Xi1+ Xi2+ Xi3
Yi= Yi1+ Yi2+ Yi3

Xc1 ,Yc1 =Hline(19, 25, 27)
Xc2 ,Yc2 =Hline(19, 25, 38)
Xc3 ,Yc3 =Vline(27, 38, 19)
Xc= Xc1+ Xc2+ Xc3
Yc= Yc1+ Yc2+ Yc3

Xu1 ,Yu1 =Hline(32, 38, 38)
Xu2 ,Yu2 =Vline(27, 38, 32)
Xu3 ,Yu3 =Vline(27, 38, 38)
Xu= Xu1+ Xu2+ Xu3
Yu= Yu1+ Yu2+ Yu3


Xb1 ,Yb1 =Hline(43, 49, 29)
Xb2 ,Yb2 =Hline(43, 49, 38)
Xb3 ,Yb3 =Vline(22, 38, 43)
Xb4 ,Yb4 =Vline(29, 38, 49)
Xb= Xb1+ Xb2+ Xb3 + Xb4
Yb= Yb1+ Yb2+ Yb3 + Yb4

X_lft = Xi+ Xc+ Xu +Xb
Y     = Yi+ Yc+ Yu +Yb
n_evts = len( Y )
T=[0] *n_evts
T_msec = [float(t) for t in T]
POL = [0] * n_evts
CH  =  [0] * n_evts
Evts = np.transpose([CH, T_msec, POL, X_lft, Y])
Evts_arr = np.array(Evts)


Xir= [x+i_dsp for x in Xi]
Xcr= [x+c_dsp for x in Xc]
Xur= [x+u_dsp for x in Xu]
Xbr= [x+b_dsp for x in Xb]
X_rght = Xir + Xcr + Xur +Xbr
CH  =  [1] * n_evts
R_Evts = np.transpose([CH, T_msec, POL, X_rght, Y])
R_Evts_arr = np.array(R_Evts)
#print '## Xi:{}'.format(Xi)
#print '## Xir:{}'.format(Xir)
#print '## Evts_arr :\n{}'.format(Evts_arr)
#print '## R_Evts_arr :\n{}'.format(R_Evts_arr)
#print 'n_evts : {}'.format(n_evts)

Levts= np.copy(Evts_arr)
Revts= np.copy(R_Evts_arr)

L= np.copy(Evts_arr)
R= np.copy(R_Evts_arr)

for evt in range ( len(Yi) ):
    L[evt][t_idx] = L[evt][t_idx] + t_res
for evt in range ( len(Yi),  len(Yi)+len(Yc) ):
    L[evt][t_idx] = L[evt][t_idx] + 2*t_res
for evt in range ( len(Yi)+len(Yc),  len(Yi)+len(Yc)+len(Yu) ):
    L[evt][t_idx] = L[evt][t_idx] + 3*t_res
for evt in range (  len(Yi)+len(Yc)+len(Yu),   len(Yi)+len(Yc)+len(Yu)+len(Yb) ):
    L[evt][t_idx] = L[evt][t_idx] + 4*t_res

for evt in range ( len(Yi) ):
    R[evt][t_idx] = R[evt][t_idx] + t_res
for evt in range ( len(Yi),  len(Yi)+len(Yc) ):
    R[evt][t_idx] = R[evt][t_idx] + 2*t_res
for evt in range ( len(Yi)+len(Yc),  len(Yi)+len(Yc)+len(Yu) ):
    R[evt][t_idx] = R[evt][t_idx] + 3*t_res
for evt in range (  len(Yi)+len(Yc)+len(Yu),   len(Yi)+len(Yc)+len(Yu)+len(Yb) ):
    R[evt][t_idx] = R[evt][t_idx] + 4*t_res

Lcpy= np.copy(L)
Rcpy= np.copy(R)

#print '## Levts :\n{}'.format(L[:,t_idx])  
for shft in range(1, n_shfts):
    Lcpy[:,t_idx]= Lcpy[:,t_idx] + t_shft
    Rcpy[:,t_idx]= Rcpy[:,t_idx] + t_shft
    Lcpy[:,x_idx]= Lcpy[:,x_idx] + 1
    Rcpy[:,x_idx]= Rcpy[:,x_idx] + 1
    
    L= np.concatenate([L,  Lcpy])
    R= np.concatenate([R,  Rcpy])
#print '## Levts :\n{}'.format(L[:,t_idx])


print '## Levts :\n{}'.format(L)
print '## Revts :\n{}'.format(R)
print 'n_evts : {}'.format( len(L) )



##add noise beside the line
##for y in  Y:
##    if y%5==0:
##        X[y]=random.randint(0,127)
      
#for i in range(1, len(X), 5 ):
#    X[i] = random.randint(0,127)
#    Y[i]=random.randint(0,127)




import os
scrpt_name_py = os.path.basename(__file__)  # or import sys then sys.argv[0]
scrpt_name    = scrpt_name_py.split('.')[0]


fldr_name = 'txt_evts/{}/'.format(scrpt_name)
file_name = 'icub{}x{}_{}{}{}{}_lft.txt'.format( rtna_w, rtna_h, i_dsp, c_dsp, u_dsp, b_dsp)
file_path = cnvrt.write_flenfldr_ncrntpth(fldr_name, file_name)
np.savetxt(file_path , L)

R_file_name ='icub{}x{}_{}{}{}{}_rght.txt'.format( rtna_w, rtna_h, i_dsp, c_dsp, u_dsp, b_dsp)
R_file_path = cnvrt.write_flenfldr_ncrntpth(fldr_name, R_file_name)
np.savetxt(R_file_path , R)


print '\n####### data_set stored in:  {} '.format(fldr_name )
print '{} \n{}'.format(file_name, R_file_name)
print '## done !'



print '\n####### load  {} by np.loadtxt(filename to check)  '.format(file_name)
evts = np.loadtxt(file_path)
print '## n_evts : {}'.format(len(evts))
print '## start_time : {}'.format(evts[0][t_idx])
print '## first_evt : {}'.format(evts[0])
print '## last_evt : {}'.format(evts[len(evts)-1])

print '\n####### load  {} by np.loadtxt(filename to check)  '.format(R_file_name)
evts = np.loadtxt(R_file_path)
print '## n_evts : {}'.format(len(evts))
print '## start_time : {}'.format(evts[0][t_idx])
print '## first_evt : {}'.format(evts[0])
print '## last_evt : {}'.format(evts[len(evts)-1])
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        