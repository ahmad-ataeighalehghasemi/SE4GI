# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:14:08 2020

@author: abdou
"""

import requests
import json
import pandas as pd
import geopandas as gpd
response=requests.get('https://five.epicollect.net/api/export/entries/asm-su19-trees/')
raw_data = response.text
data = json.loads(raw_data)
data=data['data']['entries']
q=data[0]
colum_name=[]
for col_name in q.keys():
    colum_name.append(col_name)
ind=list(range(len(data)))
df=pd.DataFrame(data, index=ind, columns=colum_name)
