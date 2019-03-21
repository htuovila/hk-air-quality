#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 12:30:51 2019

@author: htuovila
"""

# Script to obtain HK environmental department air quality
# website links and to save in file

import requests
from bs4 import BeautifulSoup
import csv

response = requests.get("http://www.aqhi.gov.hk/en/aqhi/past-24-hours-pollutant-concentration9c57.html")

soup=BeautifulSoup(response.content,'html.parser')
findings=soup.find_all('a',class_='stationList_item_a')

# loop through stations and get names + links

station_identity=[]
for item in findings:
    station_identity.append([item.get_text(),item['href']])
    
with open('hk_stations.csv', 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(station_identity)
    
# links start with "http://www.aqhi.gov.hk/en/aqhi/"
# and adding the rest after the address gives the data page
    
# next: get station locations (address, or lat/lon)
# convert addresses to lat/lon readings