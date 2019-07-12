# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 08:55:27 2019

@author: ric
"""
coordination_source = """
{name:'兰州', geoCoord:[103.73, 36.03]},
{name:'嘉峪关', geoCoord:[98.17, 39.47]},
{name:'西宁', geoCoord:[101.74, 36.56]},
{name:'成都', geoCoord:[104.06, 30.67]},
{name:'石家庄', geoCoord:[114.48, 38.03]},
{name:'拉萨', geoCoord:[102.73, 25.04]},
{name:'贵阳', geoCoord:[106.71, 26.57]},
{name:'武汉', geoCoord:[114.31, 30.52]},
{name:'郑州', geoCoord:[113.65, 34.76]},
{name:'济南', geoCoord:[117, 36.65]},
{name:'南京', geoCoord:[118.78, 32.04]},
{name:'合肥', geoCoord:[117.27, 31.86]},
{name:'杭州', geoCoord:[120.19, 30.26]},
{name:'南昌', geoCoord:[115.89, 28.68]},
{name:'福州', geoCoord:[119.3, 26.08]},
{name:'广州', geoCoord:[113.23, 23.16]},
{name:'长沙', geoCoord:[113, 28.21]},
//{name:'海口', geoCoord:[110.35, 20.02]},
{name:'沈阳', geoCoord:[123.38, 41.8]},
{name:'长春', geoCoord:[125.35, 43.88]},
{name:'哈尔滨', geoCoord:[126.63, 45.75]},
{name:'太原', geoCoord:[112.53, 37.87]},
{name:'西安', geoCoord:[108.95, 34.27]},
//{name:'台湾', geoCoord:[121.30, 25.03]},
{name:'北京', geoCoord:[116.46, 39.92]},
{name:'上海', geoCoord:[121.48, 31.22]},
{name:'重庆', geoCoord:[106.54, 29.59]},
{name:'天津', geoCoord:[117.2, 39.13]},
{name:'呼和浩特', geoCoord:[111.65, 40.82]},
{name:'南宁', geoCoord:[108.33, 22.84]},
//{name:'西藏', geoCoord:[91.11, 29.97]},
{name:'银川', geoCoord:[106.27, 38.47]},
{name:'乌鲁木齐', geoCoord:[87.68, 43.77]},
{name:'香港', geoCoord:[114.17, 22.28]},
{name:'澳门', geoCoord:[113.54, 22.19]}
"""

city_location = {
        '香港':(114.17, 22.28)
        }

import re

test_string = "{name:'澳门', geoCoord:[113.54, 22.19]}"

pattern = r"name:'(\w+)'" #不加括号显示name：澳门
re.findall(pattern,test_string)

pattern = r"name:'(\w+)',\s+geoCoord:\[(\d+.?\d+),\s(\d+.?\d+)\]"
re.findall(pattern,test_string)

pattern = re.compile(r"name:'(\w+)',\s+geoCoord:\[(\d+.?\d+),\s(\d+.?\d+)\]")
for line in coordination_source.split('\n'):
    city_info = pattern.findall(line)
    if not city_info:
        continue
    city,long,lat = city_info[0]
    city_location[city] = (float(long),float(lat))
city_location

import math

def geo_distance(origin, destination):
    """
    Calculate the Haversine distance.

    Parameters
    ----------
    origin : tuple of float
        (lat, long)
    destination : tuple of float
        (lat, long)

    Returns
    -------
    distance_in_km : float

    Examples
    --------
    >>> origin = (48.1372, 11.5756)  # Munich
    >>> destination = (52.5186, 13.4083)  # Berlin
    >>> round(distance(origin, destination), 1)
    504.2
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def get_geo_distance(city_1,city_2):
    return geo_distance(city_location[city_1],city_location[city_2])

get_geo_distance('北京','杭州')

import networkx as nx #用于画图的包
city_graph = nx.Graph()
city_graph.add_nodes_from(city_location.keys())
nx.draw(city_graph,city_location,with_labels=True,node_size=10)
#city_graph.nodes
import matplotlib
print(matplotlib.__path__)
#from matplotlib.font_manager import FontProperties
#font_song = FontProperties(fname=r"C:\Users\ric\AppData\Local\Continuum\anaconda3\Lib\site-packages\matplotlib\mpl-data\fonts\ttf\DejaVuSans.ttf", size=15)
simple_connection_info = {
        '北京':['太原'],
        '太原':['北京','西安','郑州'],
        '兰州':['西安'],
        '西安':['兰州','长沙'],
        '长沙':['福州','南宁']
        }
nx.draw(nx.Graph(simple_connection_info),city_location,with_labels=True,node_size = 10)

class search:
    def __init__(self,city1,city2):
        self.path = ['北京']
        self.arrive = ['北京']
    def get_route(self,city1,city2):
        for i in simple_connection_info[city1]:
            if i == city2:
                self.path.append(i)
                return self.path
            elif i not in simple_connection_info.keys():
                self.arrive.append(i)
#                print(i)
                continue
            if i not in self.arrive:
#                print(i)
                self.arrive.append(i)
                self.path.append(i)
                self.get_route(i,city2)
        return self.path

p = search('北京','福州') #要先调用类，相当于初始化
print(p.get_route('北京','福州'))
