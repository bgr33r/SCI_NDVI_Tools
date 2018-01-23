###NDVI_calc.py
#By: Burke Greer
#reads in B5, B4, and QA landsat images and calculates NDVI, and produces projected geotiff

#inputs for NDVI_calc:
#sat_data_dir = the directory the landsat data is within
#NIR_name = a list that contains the b5 file or files names
#RED_name = a list that contains the b4 file or files names
#BQA_name = a list that contains the QA file or files names
#Desired_NA_Value_for_BQA = desired NA value from QA file
#new_NDVI_name = output file name (currently code is written to output GeoTIFF. Other formats possible with edits

import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt #for plotting test below

def NDVI_calc(sat_data_dir, NIR_name, RED_name, BQA_name, Desired_NA_Value_for_BQA, new_NDVI_name):
    name_list = [(x,y,z) for x in NIR_name for y in RED_name for z in BQA_name] #TODO add correct pairing check
    os.chdir(sat_data_dir) #TODO add arg for output directory, input directory
    for i in name_list:
        #open NIR, RED, QA data with GDAL, convert to NumPy array
        NIR = gdal.Open(i[0])
        NIR_array = np.array(NIR.ReadAsArray()).astype(np.float)
        RED = gdal.Open(i[1])
        RED_array = np.array(RED.ReadAsArray()).astype(np.float)
        BQA = gdal.Open(i[2])
        BQA_array = np.array(BQA.ReadAsArray()).astype(np.float)
        np.seterr(divide='ignore', invalid='ignore') #set to 'ignore' because NAs in NDVI will throw error
        #Calculate NDVI
        NDVI_out = (NIR_array - RED_array) / (NIR_array + RED_array)
        NDVI_out[BQA_array == 1] = Desired_NA_Value_for_BQA #change where BQA is 1 to desired NAN value (useful for plotting/scales/stats)
        #report names and mean for processing outputs
        print(name_list, "Mean: ", np.nanmean(NDVI_out))
        #project NumPy array in GDAL and export:
        driver = gdal.GetDriverByName('GTiff')
        new_dataset = driver.Create(new_NDVI_name,
                                    NIR.RasterXSize,  # number of columns
                                    NIR.RasterYSize,  # number of rows
                                    1,  # number of bands
                                    gdal.GDT_Float64)  # datatype of the raster
        new_dataset.SetProjection(NIR.GetProjection())
        new_dataset.SetGeoTransform(NIR.GetGeoTransform())
     
        new_band = new_dataset.GetRasterBand(1)
        new_band.SetNoDataValue(-1) # return band's nodata value to -1
        new_band.WriteArray(NDVI_out)
        return new_band
        new_dataset = None
        new_band = None

#Read in landsat files first
filesindir = os.listdir('C://path//to//folder//')
NIR_name = [s for s in filesindir if "B5" in s]  # NIR names
RED_name = [s for s in filesindir if "B4" in s]  # RED names
BQA_name = [s for s in filesindir if "BQA" in s]  #QA name

NDVI = NDVI_calc('C://path//to//folder//', NIR_name, RED_name, BQA_name, 'NAN', 'NDVI.tif') #TODO test NDVI output as list

#check output:
test = gdal.Open('NDVI.tif')
testarray = np.array(test.ReadAsArray()).astype(np.float)

plt.imshow(testarray)
plt.colorbar()
