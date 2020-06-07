# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 06:18:38 2020

@author: abdou
"""
#this function convert a longitude and latitude to x,y coordinate
import math
from ast import literal_eval
def get_coord(Coordinates):
    #Coordinates = literal_eval(Coords)
    lat = Coordinates[0]
    lon = Coordinates[1]
    
    r_major = 6378137.000
    x = r_major * math.radians(lon)
    scale = x/lon
    y = 180.0/math.pi * math.log(math.tan(math.pi/4.0 + 
        lat * (math.pi/180.0)/2.0)) * scale
    return (x, y)
