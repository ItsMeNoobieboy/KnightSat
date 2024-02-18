# edited from https://nasa-gibs.github.io/gibs-api-docs/python-usage/#basic-wms-connection

import os
from io import BytesIO
from skimage import io
import requests
import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import urllib.request
import urllib.parse
import mapbox_vector_tile
import xml.etree.ElementTree as xmlet
import lxml.etree as xmltree
from PIL import Image as plimg
import numpy as np
from owslib.wms import WebMapService
from IPython.display import Image, display

def download_image(longitude, latitude, output_name):
    # Connect to GIBS WMS Service
    wms = WebMapService('https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?', version='1.1.1')

    pixles = 1024
    distance = 1

    layer = "VIIRS_CityLights_2012"

    # Configure request for MODIS_Terra_CorrectedReflectance_TrueColor
    img = wms.getmap(layers=[layer],  # Layers VIIRS_Night_Lights, VIIRS_CityLights_2012
                    srs='epsg:4326',  # Map projection
                    bbox=(longitude-distance,latitude-distance,longitude+distance,latitude+distance),  # Bounds (-180,-90,180,90)
                    size=(pixles, pixles),  # Image size
                    #time='2021-09-21',  # Time of data
                    format='image/png',  # Image format
                    transparent=True)  # Nodata transparency

    # Save output PNG to a file

    out = open(f'satelite_images/{layer}-{output_name}.png', 'wb')
    out.write(img.read())
    out.close()

download_image(-71.060909, 42.358386, "boston")