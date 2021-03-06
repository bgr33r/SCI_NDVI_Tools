#plot_intercept.py
#By: Burke Greer
#Below code intersects site data with NDVI data

#inputs for reprojSites:
#file_name = is the file name of an excel file containin plot IDs and lat and long (in degrees)
#sheetname = is the name of the sheet with the data
#keyname = primary key of the data (plot #)
#sitecrs = is the crs of the plot data (currently st to WGS84)
#NDVIcrs = is the crs of hte projected data (area of interest is UTM11)

#inputs for get_value_at_ndvi:
#ndvi_raster = raster file in same projection as point file (previous step reprojected so they match)
#pos = is the point file which is the site data
#!!! not written for batch processing yet

import pandas as pd
import os
from shapely.geometry import Point
import geopandas as gpd
from osgeo import gdal
import numpy as np

def reprojSites(file_name, sheetname, keyname, sitecrs, NDVIcrs):
    #read in plot,lat,long data
    df = pd.DataFrame(pd.read_excel(file_name, sheetname = sheetname))
    #set primary key
    df.set_index(keys=keyname)
    #calculate geometry from lat long
    geometry = [Point(xy) for xy in zip(df.long, df.lat)]
    #Create geopandas dataframe and fill with plot data
    sites = gpd.GeoDataFrame(df, crs=sitecrs, geometry=geometry)
    #reproject if needed
    sitesreproj = sites.to_crs(crs=NDVIcrs)
    return sitesreproj

def get_value_at_ndvi(ndvi_raster, pos):
    #get geotransform from input raster(s) for extraction below
    gt = ndvi_raster.GetGeoTransform() 
    data = np.array(ndvi_raster.ReadAsArray()).astype(np.float) #convert to numpy array #TODO write for loop or list comprehension to set output from list of rasters
    x,y = list(map(int, (pos.geometry.x - gt[0])/gt[1])),list(map(int, (pos.geometry.y - gt[3])/gt[5])) #extract xy list of features in pos
    out = data[y,x] #create output - note that x and y are reversed
    #print(out)
    return(out)

data_dir = os.path.expanduser('C://path//to//folder//')
os.chdir(data_dir)

plots = reprojSites('SCI.xlsx', 'site', 'plot', {'init': 'epsg:4326'}, {'init': 'epsg:26911'})

#load in NDVI.tif
NDVI = gdal.Open('C://path//to//folder//NDVI.tif')
#extract NDVI for each point in raster:
plots['NDVI'] = get_value_at_ndvi(NDVI,plots)
#save to .shp
#write pandas geodataframe to shapefile
plots[['plot','geometry','NDVI']].to_file('siteswNDVI.shp', driver='ESRI Shapefile')
