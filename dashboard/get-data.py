#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:48:21 2019

@author: Heppa
"""
import requests


# test request from aqi.cn API
response = requests.get("https://api.waqi.info/feed/shanghai/?token=demo")
response.json()