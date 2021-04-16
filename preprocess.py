#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 01:52:01 2021

@author: baoannguyen
"""
import os
os.chdir('/home/baoannguyen/Desktop/Thesis/coffee/Code/project')
from library import *

#
class PreProcessing():
    def __init__(self, list_path):
        self.path = list_path
    def resampling(self, scale, index):
        for date in range(0,len(self.path)):
            for ind in index:
                with rio.open(self.path[date][ind], 'r') as f:
                    data = f.read(
                        1, # 1 means get only 1 band from raster in order to obtain the output's shape of (height,width) in stead of (band, height, width)
                        out_shape = (
                            f.count,
                            int(f.height*scale),
                            int(f.width*scale)),
                        resampling = Resampling.bilinear)
                    transform = f.transform*f.transform.scale(
                        (f.height/data.shape[-1]),
                        (f.width/data.shape[-2]))
                self.path[date][ind] = data
        return self.path
    def array2raster(self, index, geotransform, projection, output_path):
        bands_name = ['B02','B03','B04','B05','B06','B07','B08','B11','B12','B8A']
        for date in range(0,len(self.path)):
            for ind in index:
                f = self.path[date][ind]
                pixels_x = f.shape[1] # columns
                pixels_y = f.shape[0] # rows
                driver = gdal.GetDriverByName('GTiff')
                data = driver.Create(
                        output_path[date]+bands_name[ind],
                        pixels_x,
                        pixels_y,
                        1,
                        gdal.GDT_Float64)
                data.SetGeoTransform(geotransform)
                data.SetProjection(projection)
                data.GetRasterBand(1).WriteArray(f)
                data.FlushCache() # write to disk
                self.path[date][ind] = output_path[date]+bands_name[ind] # assign path[date][ind] the destination path
        return self.path
    def crop(self, shapefile):
        for date in range(0,len(self.path)):
            for bands in range(0,len(self.path[date])):
                b = self.path[date][bands]
                with rio.open(b,'r') as f:
                    out_image, out_transform = rio.mask.mask(f, shapefile, crop = True, all_touched = True)
                    out_meta = f.meta
                    out_meta.update({'driver': 'GTiff', 'height': out_image.shape[1], 'width': out_image.shape[2],'transform': out_transform})
                    out_image = out_image.squeeze()
                self.path[date][bands] = out_image
            #self.path[date] = np.stack(self.path[date])
        return self.path