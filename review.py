# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 12:30:51 2019

@author: 26059
"""
from collections import defaultdict

price_dict = defaultdict(int)

price_dict['音响'] = 3000
price_dict['笔记本电脑'] = 2000
price_dict['吉他'] = 1500
price_dict['手机'] = 2000

size_dict = defaultdict(int)

size_dict['音响'] = 4
size_dict['笔记本电脑'] = 3
size_dict['吉他'] = 1
size_dict['手机'] = 1

price_of_iron = [1,2,4,6,7,8,9,11,13,15,17]
price_of_iron_dict = defaultdict(int)
for i in range(len(price_of_iron)):
    price_of_iron_dict[i+1] = price_of_iron[i]

def get_price(n):
    return max([price_of_iron_dict[n]]+[get_price(n-i)+get_price(i) for i in range(1,n)])

get_price(15)

def get_times():
    
