#!/usr/bin/env python
# coding: utf-8

# # Extraction of Geographic Details From Photos

# This takes in the all the images from the said file path.

# In[2]:


import os
os.chdir("C:\\Users\\Praneeth\\Desktop\\GPS\\12th May 2023")
image_list = os.listdir()
image_list = [a for a in image_list if a.startswith('IMG')]

print(image_list)


# This takes in the data and extracts the details

# In[3]:


import pandas as pd
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    """Extracts EXIF data from the image file."""
    exif_data = {}
    img = Image.open(image)
    info = img._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_data[decoded] = value
    return exif_data

def get_gps_info(exif_data):
    """Extracts GPS information from the EXIF data."""
    if 'GPSInfo' in exif_data:
        gps_info = {}
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key, key)
            gps_info[decode] = exif_data['GPSInfo'][key]

        # Converts the GPS latitude and longitude to decimal degrees
        lat = gps_info['GPSLatitude']
        lat_ref = gps_info['GPSLatitudeRef']
        lon = gps_info['GPSLongitude']
        lon_ref = gps_info['GPSLongitudeRef']

        lat_decimal = (lat[0].numerator / lat[0].denominator + 
                       lat[1].numerator / lat[1].denominator / 60 + 
                       lat[2].numerator / lat[2].denominator / 3600) * (-1 if lat_ref == 'S' else 1)
        lon_decimal = (lon[0].numerator / lon[0].denominator + 
                       lon[1].numerator / lon[1].denominator / 60 + 
                       lon[2].numerator / lon[2].denominator / 3600) * (-1 if lon_ref == 'W' else 1)

        gps_info['GPSLatitude'] = lat_decimal
        gps_info['GPSLongitude'] = lon_decimal

        return gps_info


if __name__ == '__main__':
    image_paths = image_list
    lat = []
    long = []
    img_name = []
    for image_path in image_paths:
        exif_data = get_exif_data(image_path)
        gps_info = get_gps_info(exif_data)
        a = gps_info['GPSLatitude']
        b = gps_info['GPSLongitude']
        c = image_path
        lat.append(a)
        long.append(b)
        img_name.append(c)
    data = {"Image Name" : img_name ,"Latitude" : lat, "Longitude" : long}
    df = pd.DataFrame(data)
    df


# This stores the details to a CSV file which can be further used for analysis

# In[4]:


df.to_csv("C:\\Users\\Praneeth\\Desktop\\GPS\\12th May 2023\\120523_GPSdata.csv")


# This plots all the datapoint on the map with reference to the Latitude and Longitude of the extracted data.

# In[5]:


#pip install folium

sw = (df.Latitude.max() + 3, df.Longitude.min() - 3)
ne = (df.Latitude.min() - 3, df.Longitude.max() + 3)

import folium
m = folium.Map()

for lat, lon, in zip(df.Latitude.values, df.Longitude.values,):
    folium.CircleMarker(
        [lat, lon], 
        ).add_to(m)

m.fit_bounds([sw, ne])
display(m)

