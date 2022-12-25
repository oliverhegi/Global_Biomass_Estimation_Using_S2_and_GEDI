#_____PART 1_____
#__STEP 1 – Load packages
import pandas as pd
import numpy as np
from osgeo import gdal
import rasterio as rio
import datetime
import os
import random
from rasterio import windows
from rasterio.windows import bounds, from_bounds
#from rasterio.enums import Resampling
import matplotlib.pyplot as plt
from rasterio.plot import show, adjust_band
from tqdm import trange, tqdm

#__STEP 2 – Configure API access for SentinelHub
# Configuration for the SentinelHub API can by set up with config.py
# This requires a SentinelHub user accound for an id and secret code
from sentinelhub import SHConfig
config = SHConfig() 

if not config.sh_client_id or not config.sh_client_secret:
    print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")    

%reload_ext autoreload
%autoreload 2
%matplotlib inline

from sentinelhub import get_area_info
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

from utils import plot_image #Not a package file "utils.py" must be in local directory

#__STEP 3 – Define evalscript
evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""


#_____PART 2_____
#__STEP 4 – Load source data for GEDI
GEDI_img = 'GEDI_L4B_Gridded_Biomass/data/GEDI04_B_MW019MW138_02_002_05_R01000M_MU.tif'
full = rio.open(GEDI_img)

#__STEP 5 – Get geographic bounds of the GEDI coverage
F_West, F_South, F_East, F_North  = [C/100000 for C in full.bounds]
F_South, F_North = -52, 52 # Tiff contains a bound of empty pixels at the top and bottom of the image the notes show that the data ends at -52, 52

#__STEP 6 – Define static parameters for sentinel hub
time_interval = ["2019-04-18", "2021-08-04"]
resolution = 10
size = 111,111

#__STEP 7 – Genderate random coordinates
l_cords = []
l_GEDI = []
l_S2 = []
n = 0
tot = 10000 #How many samples you want to generate – 10,000 will have a very long runtime

pbar = tqdm(desc='while loop', total = tot) #Use tqdm to track the time taken for each itteration
while n < tot:
    West = random.sample(range(int(F_West),int(F_East)),1)[0]
    East = West+0.01 # for East not > F_East, else pass
    South = random.sample(range(int(F_South),int(F_North)), 1)[0]
    North = South+0.01
    # Check if nan
    dst = full.read(1, window = from_bounds(West, South, East, North, rio.Affine(*[C/100000 for C in full.transform][:6])))
    if dst[0][0] != -9999:
        # Set params for sentinel
        coords = West, South, East, North
        bbox = BBox(bbox=coords, crs=CRS.WGS84)
        # Pull image
        request_download = SentinelHubRequest(
        evalscript=evalscript_true_color,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L2A,
                time_interval=time_interval,
                mosaicking_order=MosaickingOrder.LEAST_CC,)],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=bbox,
            size=size,
            config=config,)
        # Check if S2 data exists
        if request_download.get_data()[0].sum() != 0:
            # Save all
            n = n+1
            l_cords.append(coords)
            l_GEDI.append(dst[0][0])
            l_S2.append(request_download.get_data()[0])   
            pbar.update(1) #Time
##
#pbar.close()               
                
#__STEP 8 – Save
df_cords = pd.DataFrame(l_cords, columns=('West', 'South', 'East', 'North'))        
df_GEDI = pd.DataFrame(l_GEDI)  

directory = 'DATA/'

df_cords.to_csv(f'{directory}l_cords.csv')
df_GEDI.to_csv(f'{directory}l_GEDI.csv')
np.save(f'{directory}l_S2.npy', l_S2, allow_pickle=True)