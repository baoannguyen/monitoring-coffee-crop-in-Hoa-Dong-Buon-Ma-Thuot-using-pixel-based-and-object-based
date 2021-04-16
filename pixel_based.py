#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:45:06 2021

@author: baoannguyen
"""

#%% change file's direction
import os
os.chdir('/home/baoannguyen/Desktop/Thesis/coffee/Code/project')

#%% import modules
from library import *
from preprocess import *
from createdataset import *


#%% Preprocess the data (only run this step when creating resampled images; after that, comment it)
'''## prepare the data path
path = '/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/'
dates = glob(path + '*')
dates.sort()
input_bands = []
print('Studying dates: {}'.format([i[-10:] for i in dates]))
for date in dates:
    bands = glob(date + '/*_*_B0[2-4,8]*') + glob(date + '/*_*_B0[5-7]*') + glob(date + '/*_*_B[11,12,8A]*')
    bands.sort()
    input_bands.append(bands) 
input_bands # 2,3,4,5,6,7,8,11,12,8A
len(input_bands)

## resample 20m to 10m (5,6,7,8A,11,12)
ind_20m = [3,4,5,7,8,9]
upscaling = 2
resampling = PreProcessing(input_bands)
resampled_list = resampling.resampling(scale = upscaling, index = ind_20m)
#resampled_list[3][5] # check
#resampled_list[4][7].shape # check

## change arrays to rasters
# take geotransformation and projectin reference
ref = gdal.Open('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/L2A_T48PZV_A018805_20190128T031602_2019-01-28/T48PZV_A018805_20190128T031602_B02.jp2')
geotransform = ref.GetGeoTransform()
projection = ref.GetProjection()
# prepare output
output_path = glob('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/*/resample/')
output_path.sort()

ar2ras = PreProcessing(resampled_list)
list_dates = ar2ras.array2raster(ind_20m, geotransform, projection, output_path)
#list_dates[5] # check'''

## crop bands
# import shapefile
with fiona.open('/home/baoannguyen/Desktop/Thesis/coffee/Hoa_Dong/Hoa_Dong.shp') as shapefile:
    shape = [feature['geometry'] for feature in shapefile]
# run these lines below if you've already had the resampled raster; else, comment them and uncomment above lines for the processing flow running
path = '/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/'
dates = glob(path + '*')
dates.sort()
input_bands = []
for date in dates:
    bands = glob(date + '/*_*_B0[2-4,8]*') + glob(date + '/resample/B*')
    bands.sort()
    input_bands.append(bands) 
input_bands[2] # 2,3,4,8,5,6,7,11,12,8A

# crop
cropping = PreProcessing(input_bands)
cropped_list = cropping.crop(shapefile = shape)
cropped_list[0][7].max()
cropped_list[0]
# change from DN to reflectance: DN = 10000*reflectance
for i in cropped_list:
    for j in range(0,len(i)):
        a = i[j]
        i[j] = a/10000
cropped_list[0][7].max()

#%% create the dataset
dataset = mydataset(cropped_list)
len(dataset)
#%% Plot RGB
date = dataset.index.tolist()
for i in range(0,len(dataset)):
    d = dataset.iloc[i]
    stacking = np.stack(d)
    ep.plot_rgb(stacking, rgb = (2,1,0), figsize = (12,12), stretch = True, str_clip = 0.2, title = 'RGB {}'.format(date[i]))

#%% Plot ndvi
for i in range(0,len(dataset)):
    stacking = np.stack(d)
    ndvi = es.normalized_diff(stacking[3],stacking[2])
    ep.plot_bands(ndvi, cmap = 'RdYlGn', cols = 1, vmin = -1, vmax = 1, title = 'NDVI {}'.format(date[i]), figsize = (12,12))
