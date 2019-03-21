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
from datetime import datetime, timedelta

# links start with "http://www.aqhi.gov.hk/en/aqhi/"

def getAqhiData():
    
    station_name=[]
    station_link=[]
    station_aqhi_link=[]
    with open('hk_stations.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)
            station_name.append(row[0])
            station_link.append(row[1])
            station_aqhi_link.append(row[1].replace('pollutant-concentration','aqhi'))
            
    
    def getAqhiData_temp(station_aqhi_link):
        link_base="http://www.aqhi.gov.hk/en/aqhi/"
        
        response=requests.get(link_base+station_aqhi_link)
        soup=BeautifulSoup(response.content,'html.parser')
        
        # headers
        data_soup=soup.find_all('td')
        
        station_name=soup.find_all('div',id='dd_stnh24_stationName')[0].get_text()
        check=False
        data_points=[]
        for item in data_soup:
            if check:
                data_points.append(item.get_text().strip())
            if 'Time'==item.get_text():
                check=True
        
        data=np.array(data_points).reshape(round(len(data_points)/2),2)
        
        date_times=pd.to_datetime(data[:,0])
        
        data=pd.DataFrame({'Date Time': date_times,'aqhi': data[:,1], 'station':station_name})
        return data
    # test with station #2
    data=getAqhiData_temp(station_aqhi_link[2])
    
    
    for station in station_aqhi_link:
        new_data_aqhi=getAqhiData_temp(station)
        try:
            all_stations_aqhi=all_stations_aqhi.append(new_data_aqhi,ignore_index=True)
        except:
            all_stations_aqhi=new_data_aqhi
    return all_stations_aqhi

if __name__=='__main__':
    getAqhiData()