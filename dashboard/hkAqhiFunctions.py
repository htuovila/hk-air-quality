#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:47:43 2019

@author: Heppa
"""

import math
# Function for computing the AQHI
def added_risk(beta,concentration):
    '''generic added risk function for computing the added health risk
    of a pollutant concentration'''
    ar=math.expm1(beta*float(concentration))*100.0
    return ar

def aqhi_func(conc, added_risk):
    '''each input represents the 3h moving average
    of the pollutant concentration in question'''
    #constants (regression coefficients)
    pollutants=["NO2","SO2","O3","PM10","PM25"]
    betas=[0.0004462559,0.0001393235,0.0005116328,0.0002821751,0.0002180567]
    ars=list(map(added_risk, betas, conc))
    ar_total=sum(ars[0:2])+max(ars[3:4])
    ar_total=min(10,round(ar_total,0))
    return ar_total

def aqhi_function2(added_risk):
    '''wrapper function to avoid giving added_risk every time as argument'''
    return lambda conc: aqhi_func(conc,added_risk) 
aqhi_function = aqhi_function2(added_risk)
# aqhi_function same as aqhi_func but with one argument less


if __name__=='__main__':
    conc_test=[115,15,4,65,40]
    print(aqhi_function(conc_test))