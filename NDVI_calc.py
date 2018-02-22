'''
NDVI_calc.py
By: Burke Greer
reads in B5, B4, and QA landsat images and calculates NDVI, and produces projected geotiff

inputs for NDVI_calc:
sat_data_dir = the directory the landsat data is within
NIR_name = a list that contains the b5 file or files names
RED_name = a list that contains the b4 file or files names
BQA_name = a list that contains the QA file or files names
Desired_NA_Value_for_BQA = desired NA value from QA file
new_NDVI_name = output file name (currently code is written to output GeoTIFF. Other formats possible with edits

'''

import os
import numpy as np
from osgeo import gdal
import matplotlib.pyplot as plt  # for plotting test below


def NDVI_calc(sat_data_dir, NIR_name, RED_name, BQA_name, Desired_NA_Value_for_BQA):
    name_list = list(zip(NIR_name,RED_name,BQA_name))# TODO add correct pairing check
    os.chdir(sat_data_dir)  # TODO add arg for output directory, input directory
    for i in name_list:
        # open NIR, RED, QA data with GDAL, convert to NumPy array
        print(i[0])
        NIR = gdal.Open(i[0])
        NIR_array = np.array(NIR.ReadAsArray()).astype(np.float)
        #NIR_array[NIR_array == -9999] = 'NAN'
        print(i[1])
        RED = gdal.Open(i[1])
        RED_array = np.array(RED.ReadAsArray()).astype(np.float)
        #RED_array[RED_array == -9999] = 'NAN'
        print(i[2])
        BQA = gdal.Open(i[2])
        BQA_array = np.array(BQA.ReadAsArray()).astype(np.float)
        NDVI_outname_date = i[0][17:25] + '_NDVI.tif'
        np.seterr(divide='ignore', invalid='ignore')  # set to 'ignore' because NAs in NDVI will throw error
        # Calculate NDVI
        NDVI_out = (NIR_array - RED_array) / (NIR_array + RED_array)
        NDVI_out[BQA_array == 1] = Desired_NA_Value_for_BQA  # change where BQA is 1 to desired NAN value (useful for plotting/scales/stats)
        # report names and mean for processing outputs
        print(NDVI_outname_date, "Mean: ", np.nanmean(NDVI_out))
        # project NumPy array in GDAL and export:
        driver = gdal.GetDriverByName('GTiff')
        new_dataset = driver.Create(NDVI_outname_date,
                                    NIR.RasterXSize,  # number of columns
                                    NIR.RasterYSize,  # number of rows
                                    1,  # number of bands
                                    gdal.GDT_Float64)  # datatype of the raster
        new_dataset.SetProjection(NIR.GetProjection())
        new_dataset.SetGeoTransform(NIR.GetGeoTransform())

        new_band = new_dataset.GetRasterBand(1)
        new_band.SetNoDataValue(-1)  # return band's nodata value to -1
        new_band.WriteArray(NDVI_out)
        #return new_band
        new_dataset = None
        new_band = None

if __name__ == "__main__":

    # Read in landsat files first
    # landsat 7 bands for NDVI
#    filesindir = sorted(os.listdir('.//test_data//Landsat//Santa_Cruz_Island//LC08'),key=str)
#    NIR_name = sorted([s for s in filesindir if "band4" in s], key= lambda name: int(name[17:25]))  # NIR names
#    RED_name = sorted([s for s in filesindir if "band3" in s], key= lambda name: int(name[17:25]))  # RED names
#    BQA_name = sorted([s for s in filesindir if "pixel" in s], key= lambda name: int(name[17:25]))  # QA name

    #landsat 8 bands for NDVI
    filesindir = sorted(os.listdir('.//test_data//Landsat//Santa_Cruz_Island//LC08'), key=str)
    NIR_name = sorted([s for s in filesindir if "band5" in s], key=lambda name: int(name[17:25]))  # NIR names
    RED_name = sorted([s for s in filesindir if "band4" in s], key=lambda name: int(name[17:25]))  # RED names
    BQA_name = sorted([s for s in filesindir if "pixel" in s], key=lambda name: int(name[17:25]))  # QA name

    name_list = list(zip(NIR_name,RED_name,BQA_name))

    for i in range(0,len(name_list)):
        print(name_list[i][17:25])



    NDVI = NDVI_calc('.//test_data//Landsat//Santa_Cruz_Island//LC08', NIR_name, RED_name, BQA_name, 'NAN')

    # check output:
    #test = gdal.Open('NDVI.tif')
    #testarray = np.array(test.ReadAsArray()).astype(np.float)

    #plt.imshow(testarray)
    #plt.colorbar()
