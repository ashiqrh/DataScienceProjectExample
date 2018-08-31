
# coding: utf-8

# In[1]:

import pandas as pd

import fiona
import shapely
from shapely import geometry
import pyproj

import time
import datetime


# In[2]:

def find_distance(lat1, lon1, lat2, lon2):
    point1 = geometry.Point(lon1,lat1)
    point2 = geometry.Point(lon2, lat2)    
    
    geod = pyproj.Geod(ellps='WGS84')
    angle1,angle2,distance = geod.inv(point1.x, point1.y, point2.x, point2.y)
    return 0.621371*distance/1000


# In[3]:

def find_borough(polygons, lat_list, lon_list):
    
    name_list = []
    boundaries = [shapely.geometry.asShape(p['geometry'])  for p in polygons]
    boundary_names = [p['properties']['boro_name'] for p in polygons]
    points = [shapely.geometry.Point(lon, lat) for lat,lon in zip(lat_list, lon_list)]
    
    records = len(lat_list)
    batch   = 5000
    n = 0
    bn = 0
    tstart = time.time()
    tbatch = tstart
    
    for point in points:
        name = 'unknown'   
        for boundary, boundary_name  in zip(boundaries,boundary_names):    
            if boundary.contains(point):
                name = boundary_name
                break
        name_list.append(name)
        
        ### how long does it take to do the calculations
        n = n + 1
        if (n % batch) == 0:
            bn = bn + 1
            tend = time.time()
            print('*'*80)
            print('Number of records done so far', n)
            print('Time for last ', batch,' records ', str(datetime.timedelta(seconds=tend-tbatch)))
            tduration = tend - tstart
            print('Run time so far ', str(datetime.timedelta(seconds=tduration)))
            remaining_secs = float(records-n)/batch * tduration/bn
            print('Remaining time ', str(datetime.timedelta(seconds=remaining_secs)))
            tbatch = tend
        
    return name_list

