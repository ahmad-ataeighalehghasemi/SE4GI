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
from numpy import *

import pandas as pd
#Importing the required packages
import geopandas as gpd
import pandas as pd
from bokeh.models import ColumnDataSource, LabelSet, Select
from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors #bokeh version 1.1
from bokeh.tile_providers import CARTODBPOSITRON #bokeh version 1.0
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import Title
from get_coord import *


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
#ax = world[world.continent == 'North America'].plot(color='white', edgecolor='black')
#position.plot(ax=ax, color='red')
#position_df = position.drop('geometry', axis=1).copy()
#psource = ColumnDataSource(position_df)
#p1 = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000),
#           x_axis_type="mercator", y_axis_type="mercator")
#p1.add_tile(get_provider(Vendors.CARTODBPOSITRON))
#p1.circle('x', 'y', source=psource, color='red', radius=10)
#output_file("tree_map.html")
#show(p1)

df['location']=None
for i in range(len(df)):
    latitude=df['3_GPS_location_taken'][i]['latitude']
    longitude=df['3_GPS_location_taken'][i]['longitude']
    if latitude or longitude !="":
        df['location'][i]=(longitude,latitude)
df['x_coord']=None
df['y_coord']=None
for i in range(len(df)):
    if df['location'][i]!=None:
        coord=get_coord(df['location'][i])
        df['x_coord'][i]=coord[0]
        df['y_coord'][i]=coord[1]
#p1 = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000),x_axis_type="mercator", y_axis_type="mercator")
#p1.add_tile(CARTODBPOSITRON)
#p = figure(x_axis_type="mercator", y_axis_type="mercator")
#p.add_tile(CARTODBPOSITRON)
p1=figure()
p1.circle(x = df['x_coord'],y = df['y_coord'],   #ploting of the trees
         line_color="#FF0000", 
         fill_color="#FF0000",
         fill_alpha=0.05)
p1.add_layout(Title(text="Cartography of the trees", align="center"), "above")
p1.xaxis[0].axis_label = 'X'
p1.yaxis[0].axis_label = 'Y'
output_file('carto.html')  #out_put the html figure
#show(p1)



#barplot of circumference
nb_tree = list(df.index)
cir=list(df['4_Circumference_of_t'])
data = ColumnDataSource({'x' : nb_tree, 'y': cir})
p2 = figure()
p2.vbar(x='x', top='y', source = data, width=0.9) 
p2.add_layout(Title(text="Circumference barplot", align="center"), "above")
p2.xaxis[0].axis_label = 'Number of tree'
p2.yaxis[0].axis_label = 'Circomference'
output_file('circonf_barplot.html')
#show(p2)
#type                #exploting the type of the trees
type_tree=list(df['13_Type_of_tree__com']) 
d_tree={} #initialisation of the dict
for ntree in type_tree:
    if ntree is not None:
        d_tree[ntree]=type_tree.count(ntree)
tree_numb=[]
type_tree=[]
for (k, val) in d_tree.items():
    tree_numb.append(val)
    type_tree.append(k)
    
#ploting 
p3 = figure(x_range=type_tree, plot_height=500, title="Tree Type",
           toolbar_location=None, tools="")

p3.vbar(x=type_tree, top=tree_numb, width=0.9)
p3.xgrid.grid_line_color = None
p3.y_range.start = 0
p3.xaxis[0].axis_label = 'Type of tree'
p3.yaxis[0].axis_label = 'Number'
output_file('Number_tree.html')
#show(p3)
#condition
condition=df['14_Condition']
cond=[]
for c in condition:
    if c=='Excellent':
        cond.append(3)    #3 for Excellent
    elif c=='Good':
        cond.append(2)    #2 for Good
    else:
        cond.append(1)    #1 for fair

p4 = figure(x_range=type_tree, plot_height=500, title="Condition of trees",
           toolbar_location=None, tools="")

p4.vbar(x=type_tree, top=cond, width=0.9)
p4.xgrid.grid_line_color = None
p4.y_range.start = 0
p4.xaxis[0].axis_label = 'Type of tree'
p4.yaxis[0].axis_label = 'Condition 3 (excellent) 2 (good) 1 (fair)'
output_file('Condition_tree.html')
#show(p4)
#histogram 






#cartogram





































 