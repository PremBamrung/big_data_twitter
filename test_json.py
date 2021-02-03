#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 09:32:15 2021

@author: hustachethomas
"""


import json
import numpy as np
def find_top_topics(n=3,file_name = "twitter_top_trend.json"):
    with open(file_name) as f:
        data = json.load(f)
    max_volumes = []
    for ind,value in enumerate(data[0]['trends']):
                  
        max_volumes+=[value['tweet_volume']]
    indices_sorted = np.argsort(max_volumes)
    top_hashtags=[]
    for i in indices_sorted[:n]:
        top_hashtags+=[data[0]['trends'][i]['name']]
    return top_hashtags
        
      