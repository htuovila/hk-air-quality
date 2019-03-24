#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 14:40:22 2019

@author: Heppa
"""

import pandas as pd
import numpy as np
# imports for air quality index functions
#import hkAqhiFunctions
#import aqi
from datetime import datetime, timedelta

import importlib
import dataQueryHkEpd
import dataQueryHkEpdAqhi

import matplotlib.pyplot as plt
import time

# possibility to reload data libraries (if they change)
if 1==0:
    importlib.reload(dataQueryHkEpd)
    importlib.reload(dataQueryHkEpdAqhi)

# if we want to make a new query to webpages
start_time=time.time()
if 1==1:
    print('html queries started')
    all_stations=dataQueryHkEpd.getPollutantData()
    all_stations_aqhi=dataQueryHkEpdAqhi.getAqhiData()
    # merge data from two sources on station name and time
    all_stations=pd.merge_asof(all_stations.sort_values('Date Time'),all_stations_aqhi.sort_values('Date Time'),on='Date Time',by='station')
    all_stations['aqhi_y']=pd.to_numeric(all_stations['aqhi_y'])
    all_stations.rename(columns={'aqhi_y':'aqhi_official'},inplace=True)
    all_stations.rename(columns={'aqhi_x':'aqhi_instant'},inplace=True)
    all_stations.to_csv('aqiDataDownload.csv',index=False)
else:
    all_stations2 = pd.read_csv('aqiDataDownload.csv') 
end_time=time.time()

difference=end_time-start_time
print('Data query took '+str(round(difference))+' seconds to complete')

# find few of the previous observations
last_observations=all_stations['Date Time']==all_stations['Date Time'].max()
earlier_observations=all_stations['Date Time']==all_stations['Date Time'].max()-timedelta(hours=3)

##################################################################
# plotting

plt.plot(all_stations['aqhi_instant'],all_stations['aqi'],'.b')
plt.plot(all_stations[last_observations]['aqhi_official'],all_stations[last_observations]['aqi'],'*r')
plt.plot(all_stations[earlier_observations]['aqhi_official'],all_stations[earlier_observations]['aqi'],'og')
plt.grid()
plt.xlim(0,10)
plt.ylim(0,300)
plt.xlabel('AQHI')
plt.ylabel('AQI US')