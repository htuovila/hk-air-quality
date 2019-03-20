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
        

# next: run this function to all stations