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
from bokeh.plotting import figure, show, output_file

import pandas as pd
#Importing the required packages
import geopandas as gpd
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, Select
from bokeh.plotting import figure, show, output_file
#from bokeh.tile_providers import get_provider, Vendors #bokeh version 1.1
from bokeh.tile_providers import CARTODBPOSITRON #bokeh version 1.0
from bokeh.io import curdoc
from bokeh.layouts import row

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
df.crs = fiona.crs.from_epsg(3857) # Set the coordinate system to WGS84 using Fiona module
df.to_file(r'position.shp')
position = gpd.read_file(r'position.shp')

#mapview geodateframe
ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
position.plot(ax=ax, color='red')





#creat a function for each graph


#Map_vue
##ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
##position.plot(ax=ax, color='red')
#position_df = position.drop('geometry', axis=1).copy()
#psource = ColumnDataSource(position_df)
#p1 = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000),
#           x_axis_type="mercator", y_axis_type="mercator")
#p1.add_tile(get_provider(Vendors.CARTODBPOSITRON))
#p1.circle('x', 'y', source=psource, color='red', radius=10)
#output_file("tree_map.html")
#show(p1)

#barplot of circumference
nb_tree = list(df.index)
cir=list(df['4_Circumference_of_t'])
data = ColumnDataSource({'x' : nb_tree, 'y': cir})
p2 = figure()
p2.vbar(x='x', top='y', source = data, width=0.9) 
output_file('circonf_barplot.html')
show(p2)
#Barplot of the type of trees













#histogram 













#cartogram





































 