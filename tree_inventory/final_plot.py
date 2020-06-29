# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 11:50:33 2020

@author: abdou
"""

from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import get_provider, Vendors
from data_construction import *
from bokeh.models import ColumnDataSource, LabelSet, Select, Title
from bokeh.plotting import figure, show, output_file
from psycopg2 import (
        connect
        )
import pandas as pd
from bokeh.layouts import row
from bokeh.io import curdoc
def getPointCoords(rows, geom, coord_type):
   """Calculates coordinates ('x' or 'y') of a Point geometry"""
   if coord_type == 'x':
        return rows[geom].x
   elif coord_type == 'y':
        return rows[geom].y
    
Data['x'] = Data.apply(getPointCoords, geom='geometry', coord_type='x', axis=1)
Data['y'] = Data.apply(getPointCoords, geom='geometry', coord_type='y', axis=1)
Data = Data.drop('geometry', axis=1).copy()
psource = ColumnDataSource(Data)
TOOLTIPS = [
        ("circom", "@circom"),
        ("type", "@type"),
        ("condition","@condition"),
        ("title","@title")]
p1 = figure(x_range=(-9730000, -9758100), y_range=(5140000, 5180000),
           x_axis_type="mercator", y_axis_type="mercator", tooltips=TOOLTIPS)

tile_provider = get_provider(Vendors.CARTODBPOSITRON)
p1.add_tile(tile_provider)

#Add Glyphs
p1.circle('x', 'y', source=psource, color='red', radius=30)

#Add Labels and add to the plot layout
labels = LabelSet(x='x', y='y', text='index',
              x_offset=500, y_offset=500, source=psource, render_mode='css')
p1.add_layout(labels)

#Bar Plot
conn = connect("dbname=postgres user=postgres password=Kassim123*")
cur = conn.cursor()
cur.execute("SELECT circomference, type, condition FROM tress")
data = cur.fetchall()
tree = pd.DataFrame(data,columns=['circom','type','condition'])
tree['circom'] = pd.to_numeric(data_df['circom'])
widget_opt = list(tree) 
del widget_opt[1]
tree_grouped = tree.groupby('type', axis=0).median()

options=[] #Empty List -> quello che voglio far vedere nel mio select widget

for i in widget_opt:
    string = '%s' %i
    options.append(string) 
typ = list(tree_grouped.index) 
x = typ
data = ColumnDataSource({'x' : x, 'y': list(tree_grouped['circom'])})
p2 = figure(x_range = x, y_range = (0,400))
p2.vbar(x='x', top='y', source = data, width=0.9)  
p2.legend.orientation = "vertical"
p2.legend.location = "top_left"
p2.xaxis.major_label_orientation = 1.2

select_widget = Select(options = options, value = widget_opt[0], title = 'Select a Variable')
def callback(attr, old, new):
    column2plot = select_widget.value
    data.data = {'x' : x, 'y': list(tree_grouped[column2plot])}
    p2.vbar(x='x', top='y' , source = data, color = 'color' , width=0.9, legend_field ="x")
    p2.legend.orientation = "vertical"
    p2.legend.location = "top_left"
    p2.xaxis.major_label_orientation = 1.2
select_widget.on_change('value', callback)
'''OUTPUT MULTI PLOT'''
#Create the plot layout
layout = row(select_widget, p1, p2)
#Output the plot
#output_file("interactive_map.html")
#show(layout)
curdoc().add_root(layout)



type                #exploting the type of the trees
type_tree=list(tree['type']) 
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
p3.legend.orientation = "vertical"
p3.legend.location = "top_left"
p3.xaxis.major_label_orientation = 1.2
#output_file('tree_numb.html')
#show(p3)
#condition
condition=tree['condition']
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
p4.legend.orientation = "vertical"
p4.legend.location = "top_left"
p4.xaxis.major_label_orientation = 1.2
#output_file('Condition.html')
#show(p4)