# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 10:09:57 2019

@author: ric
"""
import re
import requests
from bs4 import BeautifulSoup
url = 'https://zh.wikipedia.org/wiki/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
#print(soup.prettify)
tb = soup.find('table',class_='wikitable')

tb = str(tb)

pattern = re.compile(r'<a href="(/wiki/.+)" title="\w+线">(\w+线)</a>')
route_url = pattern.findall(tb)

url_dict = {}
for url,route_number in route_url:
    url_dict[route_number] = 'https://zh.wikipedia.org/' + url

def get_station_list(url):
    station_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text,'html.parser')
    tb = soup.find('table',class_='wikitable')
    available = 0    
    for tr in tb.find_all('tr'):
        tr = str(tr)
        not_connect = re.compile(r'各自独立运营')
        station_list += not_connect.findall(tr)
        start_time = re.compile(r'[0-9]*年[0-9]*月[0-9]*日')
        if start_time.findall(tr) != []:
            longth_w = re.compile(r'<td rowspan="(\d*)">[0-9]*年[0-9]*月[0-9]*日')
            longth = longth_w.findall(tr)
            if longth == []:
                longth.append('1')
            available = int(longth[0])
        if available != 0:
            pattern = re.compile(r'<a *.* *href=".+" title="(\w+)站 *.*"><?b?>?\w+站<?/?b?>?</a>')
            station_list += pattern.findall(tr)
            available -= 1
                
    tb = str(tb)
    circle = re.compile(r"成环运行")
    if circle.findall(tb) !=[]:
        station_list.append('环线')
    else:
        station_list.append('非环线')

    return station_list

get_station_dict = {}
for route_number in url_dict:
    get_station_dict[route_number] = get_station_list(url_dict[route_number])

def station_dict2station_list(station_dict):
    station_list = []
    for route in station_dict:
        station_list += station_dict[route]
    station_list = set(station_list)-set(['各自独立运营','环线','非环线'])
    station_list = list(station_list)
    return station_list

station_list = station_dict2station_list(get_station_dict)

import googlemaps

def get_station_location(station_list):
    station_location = {}
    key = 'AIzaSyBjvoVlXrAbeb7nTR1Ejh8tH7IdtnTuoU0'
    gmaps = googlemaps.Client(key=key)
    for station in station_list:
        result = gmaps.geocode('北京' + station + '站')
        try:
            station_location[station] = (float('%.6f' % result[0]['geometry']['location']['lng']),
                            float('%.6f' % result[0]['geometry']['location']['lat']))
        except:
#            result = gmaps.geocode('北京' + station+'站')
#            try:
#                station_location[station] = (str(result[0]['geometry']['location']['lat']),
#                            str(result[0]['geometry']['location']['lng']))            
#            except:
            station_location[station] = list([])
            
        print(station,station_location[station])
    return station_location

station_location = get_station_location(station_list)

#manual = {'天桥':(39.8820887,116.3986683),
#          '关庄':(40.00113,116.4242126)
##        '北京南站':(39.8651096,116.3789463),
##          '瀛海站':(39.7613096,116.4492894),
##          '泥洼站':(39.8585918,116.3042086),
##          '':()
#        }

#def get_unlocation_station(station_location):
#    unlocation_station = []
#    for station in station_location:
#        if station_location[station] == []:
#            unlocation_station.append(station)
#    return unlocation_station
#unlocation_station = get_unlocation_station(station_location)

manual = {'百子湾':('39.8931331','116.4987503'),
          '丰台':('39.8477','116.3035131'),
          '平西府':('40.0906191','116.3483983'),
          '南锣鼓巷':('39.9336901','116.4018183'),
        '天桥':('39.8820887','116.3986683'),
          '北京南':('39.8651311','116.3767333'),
          '关庄':('40.00113','116.4242126'),
          '房山城关':('39.7065859','115.9890513'),
          '泥洼':('39.8585565','116.3041782'),
        '大红门南':('39.8364378','116.4009991'),
        '和义':('39.8141619','116.4020978'),
        '西黄村':('39.9337301','116.2067523'),
        '万安':('39.9837376','116.2318392'),
        '景泰':('39.8651886','116.4103889'),
        '瀛海':('39.7613096','116.4492894'),
        '北工大西门':('39.8743367','116.4773286'),
        '星城':('39.7134098','116.060666'),
        '马各庄':('39.7052246','116.0167246'),
        '小园':('39.8904402','116.115525'),
        '屯佃':('40.0682772','116.215485'),
        '大石河东':('39.7092826','116.0367371'),
        '石厂':('39.8892415','116.1016521'),
        '东高地':('39.8052289','116.4092997'),
        '孙河':('40.0451681','116.5324573'),
        '阎村':('39.7170079','116.0799132'),
        '四道桥':('39.9161176','116.1336201'),
        '田村':('39.9295131','116.2528935'),
        '上岸':('39.9063416','116.1171084'),
        '桥户营':('39.9124869','116.1259126'),
        '杨庄':('39.9279639','116.1871259'),
        '火箭万源':('39.7991134','116.418546'),
        '茶棚':('39.9820854','116.247742'),
        '亦庄火车':('39.8132191','116.6002863'),
        '阎村东':('39.7290021','116.1013608'),
        #-----------------------------
        '香山':('39.9942379','116.2048295'),
        '德茂':('39.7730668','116.4412372'),
        '国贸':('39.9091266','116.4617271'),
        '动物园':('39.9382736','116.3389298'),
        '石门':('40.1298735','116.641205'),
        '新街口':('39.9406042','116.3675413'),
        '植物园':('39.9936094','116.2155736'),
        '和平门':('39.9000941','116.3819433'),
        '小红门':('39.8280451','116.4570063'),
        '桥湾':('39.8926505','116.4058665'),
        '高碑店':('39.9094826','116.5317188'),
}

for station in manual:
    station_location[station] = [float(manual[station][1]),float(manual[station][0])]

#for station in station_location:
#    station_location[station] = [float(station_location[station][1]),
#                    float(station_location[station][0])]
    
import networkx as nx #用于画图的包
import matplotlib.pyplot as plt
city_graph = nx.Graph()
city_graph.add_nodes_from(station_location.keys())
plt.figure(figsize=(40,40))
nx.draw(city_graph,station_location,with_labels=True,font_size=12,node_size=1)

station_connect = {}
for station in station_list:
    station_connect[station] = []

for route in get_station_dict:
    for i,station in enumerate(get_station_dict[route][:-2]):
#        print(i,station)
        if station !='各自独立运营' and get_station_dict[route][i+1] !='各自独立运营':
            station_connect[station] += [get_station_dict[route][i+1]]
    get_station_dict[route].reverse()
    for i,station in enumerate(get_station_dict[route][1:-1]):
#        print(station,get_station_dict[route][i+2])
        if station !='各自独立运营' and get_station_dict[route][i+2] !='各自独立运营':
            station_connect[station] += [get_station_dict[route][i+2]]
    get_station_dict[route].reverse()
    if get_station_dict[route][-1] == '环线':
        station_connect[get_station_dict[route][-2]] += [get_station_dict[route][0]]
        station_connect[get_station_dict[route][0]] += [get_station_dict[route][-2]]

plt.figure(figsize=(40,40))
nx.draw(nx.Graph(station_connect),station_location,with_labels=True,font_size=12,node_size = 1)

def search(start,desitination,connection_graph,sort_candidate):#广度优先
    pathes = [[start]]
    visitied = set()
    while pathes:
        path = pathes.pop(0)
        froninter = path[-1]
        if froninter in visitied: continue
        successors = connection_graph[froninter]
        
        for city in successors:
            new_path = path + [city]
            pathes.append(new_path)
            if city == desitination:return new_path
        
        visitied.add(froninter)
#        print(pathes)
        pathes = sort_candidate(pathes)
def pretty_print(cities):
    print('🚗→'.join(cities))

def transfer_stations_first(pathes):
    return sorted(pathes,key=len)

station_route_dict = {}
for station in station_list:
    station_route_dict[station] = []
    for route,stations in get_station_dict.items():
        if station in stations:
            station_route_dict[station].append(route)

def change_times(path):
    station_route_list = [station_route_dict[station] for station in path]
    change_time = 0
    for i,route in enumerate(station_route_list[:-1]):
        use_route = list(set(route).intersection(set(station_route_list[i+1])))
        if i==0: used = use_route
        if use_route != used:
            change_time += 1
            used = use_route
    return change_time
    
def least_change(pathes):
    return sorted(pathes,key=change_times)

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
    lat1, lon1 = station_location[origin]
    lat2, lon2 = station_location[destination]
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def distance(pathes):
    distance = 0
    for i in range(len(pathes[:-1])):
        distance += geo_distance(pathes[i],pathes[i+1])
    return distance

def shortest_distance(pathes):
    return sorted(pathes,key=distance)

pretty_print(search('魏公村','北工大西门',station_connect,sort_candidate=shortest_distance))

import itertools

#start,desitination,by_way,connection_graph,sort_candidate = '魏公村','北工大西门',['人民大学','金台夕照'],station_connect,shortest_distance
def search_byway(start,desitination,by_way,connection_graph,sort_candidate):#广度优先
    route_list = []
    for i in itertools.permutations(by_way,len(by_way)):
        route_byway = [start]
        for station in i:
            route_byway.append(station)
        route_byway.append(desitination)
#        print(route_byway)
        route = []
        for j,station in enumerate(route_byway[:-1]):
            route += search(route_byway[j],route_byway[j+1],station_connect,sort_candidate=shortest_distance)[:-1]
        route.append(desitination)
        route_list.append(route)
    route_list = sort_candidate(route_list)
    return route_list[0]
        
pretty_print(search_byway('西直门','建国门',['北安河','俸伯','燕山','亦庄火车'],station_connect,sort_candidate=shortest_distance))
