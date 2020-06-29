# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 12:12:55 2020

@author: abdou
"""
from psycopg2 import (
        connect
        )
import pandas as pd
from shapely.geometry import Point, LineString, Polygon
import geopandas as gpd
import contextily as ctx

conn = connect("dbname=postgres user=postgres password=Kassim123*")
cur = conn.cursor()
cur.execute("SELECT latitude,longitude, circomference, type, condition, title FROM tress")
data = cur.fetchall()
data_df = pd.DataFrame(data,columns=['latitude', 'longitude','circom','type','condition','title'])
data_df['latitude'] = pd.to_numeric(data_df['latitude'])
data_df['longitude'] = pd.to_numeric(data_df['longitude'])
data_df['circom'] = pd.to_numeric(data_df['circom'])



gdf=gpd.GeoDataFrame(data_df)
gdf = gdf.dropna()
Data= gpd.GeoDataFrame(data_df, geometry=gpd.points_from_xy(data_df['longitude'], data_df['latitude']))
Data.crs= '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
Data.to_file(r'shape.shp')
Data = gpd.read_file(r"shape.shp").to_crs(epsg=3857)
#gdf.crs = fiona.crs.from_epsg(3857)
def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
  xmin, xmax, ymin, ymax = ax.axis()
  basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url) 
  ax.imshow(basemap, extent=extent, interpolation='bilinear')
# restore original x/y limits
  ax.axis((xmin, xmax, ymin, ymax))
ax = Data.plot(figsize=(5,5), alpha=0.5, marker='o', color='red', edgecolor='k')
add_basemap(ax, zoom = 17)
