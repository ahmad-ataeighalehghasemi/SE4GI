# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 17:52:08 2020

@author: abdou
"""

from raw_data import *
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
import fiona
import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx
df=gpd.GeoDataFrame(df) #creat the geodatabase
#plot of the position 
df['geometry']=None
for i in range(len(df)):
    latitude=df['3_GPS_location_taken'][i]['latitude']
    longitude=df['3_GPS_location_taken'][i]['longitude']
    if latitude or longitude !="":
        df['geometry'][i]=Point(longitude,latitude)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
df.crs = fiona.crs.from_epsg(4326) # Set the coordinate system to WGS84 using Fiona module
df.to_file(r'position.shp')
position = gpd.read_file(r'position.shp')
ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
position.plot(ax=ax, color='red')

