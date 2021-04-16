#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 14:52:59 2021

@author: baoannguyen
"""

from glob import glob
import os

import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio
from rasterio.enums import Resampling
import geopandas as gpd
import pyproj


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from osgeo import gdal, ogr
import fiona
np.seterr(divide = 'ignore', invalid = 'ignore') #np.seterr: set how floating-points errors are handled
