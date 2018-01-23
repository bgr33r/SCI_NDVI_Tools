# SCI_NDVI_Tools
I have uploaded a few tools for calculating NDVI at plots on Santa Cruz Island (SCI). Their purpose is to be part of a larger project where I am tracking changes in NDVI over time and space on SCI, and I wanted to create a small repository to hold copies of my scripts. 

These scripts will calculate NDVI using Landsat 8 data (NDVI_calc.py), and then find the NDVI for plots within the landsat scene (plot_intercept.py). I had hoped to include the raw scene data in this repo, but these data are far too large to store here. I have tested these data on landsat scene LC80420362017279LGN00 which you can download here: https://earthexplorer.usgs.gov/. If you have difficulties, please contact me via the commments. 

To run these scripts, you should adjust "C://path//to//folder//" to your own directory paths to point to your data. 

For more on landsat bands, see https://landsat.usgs.gov/what-are-band-designations-landsat-satellites. If you are applying this to other data sources you'll want to make sure you're pointing at the correct bands. 

Best of luck.
