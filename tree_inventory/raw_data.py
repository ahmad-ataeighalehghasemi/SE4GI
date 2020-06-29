# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 18:14:08 2020

@author: abdou
"""

#this script collect de data from epicollect and initialize the datframe
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt 
import contextily as ctx
import fiona
from shapely.geometry import Point, LineString, Polygon


response=requests.get('https://five.epicollect.net/api/export/entries/asm-su19-trees/')
engine = create_engine('postgresql://postgres:Kassim123*@localhost:5432/postgres')
raw_data = response.text
data = json.loads(raw_data)
data=data['data']['entries']
q=data[0]
colum_name=[]
for col_name in q.keys():
    colum_name.append(col_name)
ind=list(range(len(data)))
df=pd.DataFrame(data, index=ind, columns=colum_name) #DataFrame
#creating the database
df['latitude']=None
df['longitude']=None
for i in range(len(df)):
    latitude=df['3_GPS_location_taken'][i]['latitude']
    longitude=df['3_GPS_location_taken'][i]['longitude']
    df['latitude'][i]=latitude
    df['longitude'][i]=longitude
#    if latitude or longitude !="":
#        df['geometry'][i]=Point(longitude,latitude)
del df['3_GPS_location_taken']
df['circomference']=df['4_Circumference_of_t']
df['type']=df['13_Type_of_tree__com']
df['condition']=df['14_Condition']
df.to_sql('tress', engine, if_exists = 'replace', index=False) 

#df['geometry']=None

#gdf=gpd.GeoDataFrame(df)
#gdf = gdf.dropna()
#gdf.crs = fiona.crs.from_epsg(3857)
#gdf.to_file(r'shape.shp')
#tree = gpd.read_file(r'shape.shp').to_crs(epsg=3857)
#def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
#  xmin, xmax, ymin, ymax = ax.axis()
#  basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url) 
#  ax.imshow(basemap, extent=extent, interpolation='bilinear')
## restore original x/y limits
#  ax.axis((xmin, xmax, ymin, ymax))
#ax = gdf.plot(figsize=(5,5), alpha=0.5, marker='x', color='red', edgecolor='k')
#add_basemap(ax, zoom = 13)






