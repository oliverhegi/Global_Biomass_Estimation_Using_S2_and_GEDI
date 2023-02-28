# Creating Global Coverage for Biomass Estimation using Sentinel 2 Imagery and GEDI LIDAR Biomass Observations

This project was created as a final project for the course EAEEE4000 Machine Learning for Environmental Engineering and Science.

This repository consists of two components:
   1. The main folder ('Global_Biomass_Estimation_Using_S2_and_GEDI') contains all the models used for this project.
   2. The folder 'DATA/Dataset Generation' contains the code which was used to generate the training and testing data. 

'DATA/' includes all data except for Sentinel-2 data which can be pulled from the Sentinel Hub API with the Dataset_Generation_SentinelHub_GEDI.py file. 

Data generation:
The target data is fully contained in a GeoTiff file (GEDI04_B_MW019MW138_02_002_05_R01000M_MU.tif which can be downloaded from https://daac.ornl.gov/GEDI/guides/GEDI_L4B_Gridded_Biomass.html). The predictors are a set of images pulled from the SentinelHub API. The document 'Dataset_Generation_SentinelHub_GEDI.py' (DATA/Dataset Generation/Dataset_Generation_SentinelHub_GEDI.py) can be used to pull images and combine them with corresponding datapoints from the GeoTiff. This will require a functioning user id and key for the SentinelHub API. The id and key can be entered into 'Config.py' to initiate. 
