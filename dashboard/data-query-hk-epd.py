#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:30:51 2019

@author: Heppa
"""


import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
# imports for air quality index functions
import hkAqhiFunctions
import aqi
from datetime import datetime, timedelta

# links start with "http://www.aqhi.gov.hk/en/aqhi/"

station_name=[]
station_link=[]
with open('hk_stations.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        station_name.append(row[0])
        station_link.append(row[1])
        

def getAqiData(station_link):
    link_base="http://www.aqhi.gov.hk/en/aqhi/"
    
    response=requests.get(link_base+station_link)
    soup=BeautifulSoup(response.content,'html.parser')
    
    # headers
    soup.find_all('th', class_='H24C_ColDateTime')
    
    header_items=soup.find_all('th', class_='H24C_ColItem')
    
    header=[]
    header.append(soup.find_all('th', class_='H24C_ColDateTime')[0].get_text())
    for item in header_items:
        header.append(item.get_text())
        
    aqi_data=pd.DataFrame(columns=header)
    
    #datafields
    
    time_stamps=[]
    for ts in soup.find_all('td', class_='H24C_ColDateTime'):
        time_stamps.append(ts.get_text())
    
    data_points=[]
    for data_point in soup.find_all('td', class_='H24C_ColItem'):
        data_points.append(data_point.get_text())
    data_array=np.reshape(data_points,(24,6))
    
    # input data to the dataframe
    aqi_data['Date Time']=time_stamps
    aqi_data[aqi_data.keys()[1:]]=data_array
    
    station_name=soup.find_all('div',id='dd_stnh24_stationName')[0].get_text()
    print(station_name)
    # add station name
    aqi_data['station']=station_name
    return aqi_data

# test with station #2
getAqiData(station_link[2])


for station in station_link:
    new_data=getAqiData(station)
    try:
        all_stations=all_stations.append(new_data,ignore_index=True)
    except:
        all_stations=new_data

###############################################################      
# Convert pollutant concentrations to air quality indices

# Convert to numeric values
for column_name in all_stations.keys()[1:-1]:
    all_stations[column_name]=pd.to_numeric(all_stations[column_name],errors='coerce')
    
# Convert date strings to datetime
all_stations[all_stations.keys()[0]]=pd.to_datetime(all_stations[all_stations.keys()[0]])

# Finally calculate aqhi and aqi based on the values

pollutants=["NO2","SO2","O3","PM10","PM2.5"]
all_stations['aqhi']=all_stations[pollutants].apply(hkAqhiFunctions.aqhi_function, axis=1)


aqi.to_aqi([(pollutant, conc)])

def pollutant_to_aqi(pollutant):
    return lambda conc: float(aqi.to_aqi([(pollutant, conc)]))
aqi_pm25=pollutant_to_aqi(aqi.POLLUTANT_PM25)
aqi_pm10=pollutant_to_aqi(aqi.POLLUTANT_PM10)

aqi_pm25(Decimal(100))
aqi_pm10(100)

for concentration in all_stations['PM2.5']:
    aqi_value=aqi_pm25(concentration)

indices_to_ignore=(np.isnan(all_stations['PM2.5']))
indices_to_use=~indices_to_ignore

all_stations['aqi']=np.nan


all_stations.loc[indices_to_use,'aqi']=all_stations.loc[indices_to_use,'PM2.5'].apply(aqi_pm25)
import matplotlib.pyplot as plt


try:
    del indices_to_drop
except:
    pass
for key in pollutants:
    try:
        indices_to_drop=indices_to_drop | np.isnan(all_stations[key])
    except:
        indices_to_drop=np.isnan(all_stations[key])


plt.plot(all_stations[~indices_to_drop]['aqhi'],all_stations[~indices_to_drop]['aqi'],'o')
plt.grid()

# mark invalid values with np.nan
all_stations.loc[indices_to_drop,'aqhi']=np.nan

# pick latest observations and observation couple hours ago



#################################################################
# Ways to estimate pm2.5 based on pm10 - so little impact
# so ignored at this stage
#################################################################
# way to estimate pm25 concentration when only pm10 is available
# https://aqicn.org/experiments/south-korea-pm25-air-quality/

if 1==0:
    def pm10_to_pm25(masspm10):
        masspm25 = 1094.4 + 0.437 * masspm10
        return masspm25
    
    all_stations['PM25_replacement']=all_stations['PM10'].apply(pm10_to_pm25)
    
    
    
    plt.plot(all_stations['PM25_replacement'],all_stations['PM2.5'],'.')
    
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    
    def fit_linear_model(all_stations):
        '''Function to return linear model object to fit missing values'''
        non_na_indices=~(np.isnan(all_stations['PM10']) | np.isnan(all_stations['PM2.5']))
        X=all_stations[non_na_indices]['PM10']
        y=all_stations[non_na_indices]['PM2.5']
        X=np.array(X)
        y=np.array(y)
        y = y[:, np.newaxis]
        X = X[:, np.newaxis]
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)
        
        # model to estimate pm2.5 based on pm10 when pm2.5 is unavailable
        
        lm = LinearRegression()
        lm.fit(X_train,y_train)
        predictions = lm.predict(X_test)
        return lm
    
    lm=fit_linear_model(all_stations)
    
    indices_to_estimate=(np.isnan(all_stations['PM2.5']) & ~np.isnan(all_stations['PM10']))
    
    X_to_predict=np.array(all_stations[indices_to_estimate]['PM10'])
    X_to_predict=X_to_predict[:,np.newaxis]
    y_to_predict=predictions = lm.predict(X_to_predict)
    
    
    
    
    
    # List of pollutant symbols from aqi library
    # "POLLUTANT_PM25, POLLUTANT_PM10,
    #                          POLLUTANT_O3_8H, POLLUTANT_O3_1H,
    #                          POLLUTANT_CO_8H, POLLUTANT_SO2_1H,
    #                          POLLUTANT_NO2_1H"