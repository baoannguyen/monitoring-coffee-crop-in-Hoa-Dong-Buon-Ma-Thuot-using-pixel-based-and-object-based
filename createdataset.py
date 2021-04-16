#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 00:12:45 2021

@author: baoannguyen
"""

from library import *

def mydataset(input_list):
    data_path = glob('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/*')
    data_path.sort()
    dates = []
    for i in data_path:
        dates.append(i[-10:]) # take only the dates'''
    row_names = dates
    column_names = ['Band 2',
                    'Band 3',
                    'Band 4',
                    'Band 8',
                    'Band 5',
                    'Band 6',
                    'Band 7',
                    'Band 11',
                    'Band 12',
                    'Band 8A']
    dataset = pd.DataFrame(data = input_list, index = row_names, columns = column_names)
    return dataset