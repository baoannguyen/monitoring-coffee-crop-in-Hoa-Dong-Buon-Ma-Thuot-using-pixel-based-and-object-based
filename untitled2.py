#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 01:48:17 2021

@author: baoannguyen
"""

#%% test
from library import *
from createdataset import *
from preprocess import *

#%% prepare path
path = '/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/'
input_path = glob(path + '*')
input_path.sort()
input_bands = []
print('Studying dates: {}'.format([i[-10:] for i in input_path]))
for date in input_path:
    bands = glob(date + '/*_*_B0[2-4,8]*') + glob(date + '/*_*_B0[5-7]*') + glob(date + '/*_*_B[11,12,8A]*')
    bands.sort()
    input_bands.append(bands) 
input_bands # 2,3,4,5,6,7,8,11,12,8A
input_bands[0][3]
len(input_bands)
'''for i in range(0, len(input_bands)):
    for j in ind_20m:
        print(input_bands[i][j])'''

#%% resampling 20m to 10m
ind_20m = [3,4,5,7,8,9]
upscaling = 2
preprocess = PreProcessing(input_bands)
list_resampled = preprocess.resampling(scale = upscaling, index = ind_20m)
list_resampled[7]
'''def resample(raster, scale = 2):
    with rio.open(raster, 'r') as f:
        data = f.read(
            1,
            out_shape = (
                f.count,
                int(f.height*scale),
                int(f.width*scale)),
            resampling = Resampling.bilinear)
    return data
test_1 = resample('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/L2A_T48PZV_A025383_20200502T031146_2020-05-02/T48PZV_A025383_20200502T031146_B07.jp2', scale = 2)'''
#%%
# take reference
file = gdal.Open('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/L2A_T48PZV_A018805_20190128T031602_2019-01-28/T48PZV_A018805_20190128T031602_B02.jp2')
geotransform = file.GetGeoTransform()
projection = file.GetProjection()

output_path = glob('/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/*/resample/')
output_path.sort()

a2r = PreProcessing(list_resampled)
list_path = preprocess.array2raster(ind_20m, geotransform, projection, output_path)

list_path[5]
'''def array2raster(data, geotransform, projection, index, dest_path):
         bands_name = ['B2','B3','B4','B5','B6','B7','B8','B11','B12','B8A']
         for date in range(0,len(data)):
            for ind in index:
                    pixels_x = data[date][ind].shape[1] # columns
                    pixels_y = data[date][ind].shape[0] # rows
                    driver = gdal.GetDriverByName('GTiff')
                    dataset = driver.Create(
                        dest_path[date]+bands_name[ind],
                        pixels_x,
                        pixels_y,
                        1,
                        gdal.GDT_Float64)
                    dataset.SetGeoTransform(geotransform)
                    dataset.SetProjection(projection)
                    dataset.GetRasterBand(1).WriteArray(data[date][ind])
                    dataset.FlushCache() # write to disk
                    data[date][ind] = dest_path[date]+bands_name[ind]
         return data
test = rio.open(list_path[4][3], 'r')
test_array = test.read(1)
test_array
test_1
a = test_array - test_1
a.any()'''

#%%
with fiona.open('/home/baoannguyen/Desktop/Thesis/coffee/Hoa_Dong/Hoa_Dong.shp') as shapefile:
    shape = [feature['geometry'] for feature in shapefile]
path = '/home/baoannguyen/Desktop/Thesis/coffee/sentinel2/'
input_path = glob(path + '*')
input_path.sort()
input_bands = []
for date in input_path:
    bands = glob(date + '/*_*_B0[2-4,8]*') + glob(date + '/resample/B*')
    bands.sort()
    input_bands.append(bands) 
input_bands[2]

'''def cropraster(input_list, shapefile):
    for date in range(0,len(input_list)):
        for bands in range(0,len(input_list[date])):
            b = input_list[date][bands]
            with rio.open(b,'r') as f:
                out_image, out_transform = rio.mask.mask(f, shape, crop = True)
                out_meta = f.meta
                out_meta.update({'driver': 'GTiff', 'height': out_image.shape[1], 'width': out_image.shape[2], 'transform': out_transform})
                out_image = out_image.squeeze()
            input_list[date][bands] = out_image
        #input_list[date] = np.stack(input_list[date])
    return input_list
test_crop = cropraster(test_input_bands, shape)
d20190128 = test_crop[0]
d20190128.shape
ep.plot_rgb(d20190128_array, rgb = (2,1,0), figsize = (12,12), stretch = True, str_clip = 0.2)     '''

#%% 
cropping = PreProcessing(input_bands)
list_cropped = cropping.crop(shapefile = shape)
list_cropped[0]
len(list_cropped)
dataset = mydataset(list_cropped)
dataset['Band 2']

