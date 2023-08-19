#!/usr/bin/env python
# coding: utf-8

# # This code is complete just add the visualization of SAR 

# ## This code deals with SAR data in chunks

# In[1]:


#pip install "dask[complete]"


# In[1]:


import rioxarray as rxr


# In[2]:


import rasterio 


# In[3]:


import matplotlib.pyplot as plt


# In[4]:


import xarray as xr 
import s3fs
import pandas as pd
import os 

import dask
from dask.distributed import Client, LocalCluster, progress


# In[5]:


env = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', 
           AWS_NO_SIGN_REQUEST='YES',
           GDAL_MAX_RAW_BLOCK_CACHE_SIZE='200000000',
           GDAL_SWATH_SIZE='200000000',
           VSI_CURL_CACHE_SIZE='200000000')
os.environ.update(env)


# In[6]:


get_ipython().run_cell_magic('time', '', "#a = input()\ns3 = s3fs.S3FileSystem(anon=True)\nobjects = s3.glob('sentinel-s1-rtc-indigo/tiles/RTC/1/IW/10/T/ET/**Gamma0_VH.tif')\n#sentinel-s1-rtc-indigo/tiles/RTC/1/IW/10/T/ET/**Gamma0_VV.tif\n#s3://earthsearch-data/sentinel-1-grd/2023/8/9/IW/S1A_IW_GRDH_1SDV_20230809T051048_20230809T051113_049794_05FCF7/S1A_IW_GRDH_1SDV_20230809T051048_20230809T051113_049794_05FCF7.json\n#s3://sentinel-s1-l1c/GRD/2023/8/9/IW/DV/S1A_IW_GRDH_1SDV_20230809T051048_20230809T051113_049794_05FCF7_47A7/measurement/iw-vh.tiff\nimages = ['s3://' + obj for obj in objects]\nprint(len(images))\nimages.sort(key=lambda x: x[-32:-24]) \nimages[:6] \n#sentinel-s1-rtc-indigo/tiles/RTC/1/IW/10/T/ET/**Gamma0_VV.tif\n")


# In[7]:


images = images[:100]
dates = [pd.to_datetime(x[-32:-24]) for x in images]


# In[8]:


cluster = LocalCluster(processes=False, local_directory='/tmp') 
client = Client(cluster) 
client


# In[9]:


@dask.delayed
def lazy_open(href):
    chunks=dict(band=1, x=2745, y=2745)
    return rxr.open_rasterio(href, chunks=chunks) 


# In[10]:


get_ipython().run_cell_magic('time', '', "dataArrays = dask.compute(*[lazy_open(href) for href in images])\nda =xr.concat(dataArrays, dim='band', join='override', combine_attrs='drop').rename(band='time')\nda['time'] = dates\nda\n")


# In[11]:


#pip install graphviz


# In[12]:


#import os
#os.environ["PATH"] += os.pathsep + 'C:\\Users\\sweta.mishra\\.conda\\pkgs\\graphviz-2.38-hfd603c8_2\\Library\\bin'


# In[11]:


da.isel(time=0).mean(dim=['x','y']).data.visualize(optimize_graph=True, rankdir='LR')


# In[14]:


#da.mean(dim=['x','y']).compute()


# In[12]:


cluster = LocalCluster(local_directory='/tmp') 
client = Client(cluster) 
client


# In[14]:


dataArrays = dask.compute(*[lazy_open(href) for href in images])
da = xr.concat(dataArrays, dim='band', join='override', combine_attrs='drop').rename(band='time')
da['time'] = dates
da


# In[15]:


import hvplot.xarray
da.hvplot.image(rasterize=True, aspect='equal', cmap='gray', clim=(0,0.4))


# In[ ]:




