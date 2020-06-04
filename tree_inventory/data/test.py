# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 02:24:17 2020

@author: abdou
"""

from bokeh.plotting import figure, show, output_notebook
from bokeh.tile_providers import get_provider, Vendors




p = figure(x_range=(-9780000, -9745000), y_range=(5130000, 5160000),
           x_axis_type="mercator", y_axis_type="mercator")
p.add_tile(get_provider(Vendors.CARTODBPOSITRON))
show(p)
