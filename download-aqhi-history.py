#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 15 12:33:09 2019

@author: htuovila
Purpose of this script:
    > to download Hong Kong air quality data that is available in
    monthly csv-files online
"""

# imports
import datetime
import urllib

# URLs where historical AQHI data is kept:
# "http://www.aqhi.gov.hk/epd/ddata/html/history/2016/201607_Eng.csv"

base_url="http://www.aqhi.gov.hk/epd/ddata/html/history/"
# for 2013 we have only one month data, so we start from the first full year
# of 2014
now = datetime.datetime.now()
years=list(range(2014,now.year+1))

# retrieve files until this month
months = list(range(1,13))
        
# form the urls to download from
def gen_urls(years,months):
    # initialize file_url_list to return something in an exception
    file_url_list=[]
    for y in years:
        for m in months:
            # we need to make a text-month to comply with the url
            # format with preceding zeros in one digit months
            if m<10:
                m_txt="0"+str(m)
            else:
                m_txt=str(m)
            
            file_name=str(y)+m_txt+"_Eng.csv"
            file_url=base_url+str(y)+"/"+file_name
            # add the generated file url to the list
            file_url_list.append(file_url)
            # in case we have reached current month, return the list of urls
            if y==now.year and m==now.month:
                return file_url_list
            
file_urls=gen_urls(years,months)

# check if the filenames match
# will break next month when the index changes
if now.month == 1 and now.year==2019:
    last_checked_url="http://www.aqhi.gov.hk/epd/ddata/html/history/2019/201901_Eng.csv"
    last_generated_url=file_urls[-1]
    check=last_checked_url==last_generated_url

import os
cwd = os.getcwd()
save_folder="/data-files/"
#file_name = cwd+save_folder+file_urls[-1][-14:]

# lets fetch the files in reverse order (in case our ip gets blocked)
for url in file_urls[::-1]:
    file_name = cwd+save_folder+url[-14:]
    urllib.request.urlretrieve(url, file_name)
    
# worked at least Jan 15th 2019
    