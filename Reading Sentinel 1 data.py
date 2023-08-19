#!/usr/bin/env python
# coding: utf-8

# ## This notebook reads the SENTINEL 1 COG from aws s3

# This notebook deals with reading the cog file of sentinel 1 SAR data hosted on aws s3 bucket "Analysis Ready Sentinel-1 Backscatter Imagery". It reads the data in chunks, then plotting and visualizing it. For this proper libraries and their versions need to be installed. Since this notebook uses gdal, rasterio and a pythonic interface for aws s3 i.e., s3fs this takes proper system and formats to run it properly.
# Further once the data is read properly by the url, then lots of analysis and processing can be done.
# Here I have used jupyter notebook to code with python 3.11.4 . The time taken is also calculated for each action.
# 

# In[ ]:


#pip install s3fs


# In[ ]:


#pip install xarray


# In[ ]:


#pip install intake


# In[ ]:


#pip install rio-cogeo==2.0a3


# In[81]:


import dask
import s3fs
import intake
import os
import xarray 
import rasterio
import pandas as pd
import rioxarray as rxr


# ## Import gdal and set up environment

# In[2]:


from osgeo import gdal


# In[3]:


env = dict(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR', 
           AWS_NO_SIGN_REQUEST='YES',
           GDAL_MAX_RAW_BLOCK_CACHE_SIZE='200000000',
           GDAL_SWATH_SIZE='200000000',
           VSI_CURL_CACHE_SIZE='200000000')
os.environ.update(env)


# ## Fetched the data from aws s3.

# In[66]:


s3 = s3fs.S3FileSystem(anon=True)
objects = s3.ls('sentinel-s1-rtc-indigo/tiles/RTC/1/IW/14/T/PN/2020/')
#https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/13SBD/2021/S1A_20210110_13SBD_DSC/S1A_20210110_13SBD_DSC.json
images = ['s3://' + obj + '/Gamma0_VH.tif' for obj in objects]
print(len(images))
images[:11] #january 2020 scenes


# In[67]:


with open('files.txt', 'w') as f:
    lines = [x.replace('s3://', '/vsis3/') + '\n' for x in images[:6]]
    f.writelines(lines)


# In[68]:


f


# ## Builds a virtual file

# In[69]:


get_ipython().run_cell_magic('time', '', '!gdalbuildvrt stack.vrt -separate -input_file_list files.txt \n')


# In[70]:


get_ipython().run_cell_magic('time', '', "chunks= dict(band=1, x=2745, y=2745)\nda = rxr.open_rasterio('stack.vrt', chunks=chunks)  #rioxarray.open_rasterio\nda\n")


# In[71]:


da = da.rename({'band':'time'})
da['time'] = [pd.to_datetime(x[60:68]) for x in images[:6]]


# In[72]:


#pip install intake-xarray


# ## # Loading data into python objects

# In[76]:


get_ipython().run_cell_magic('time', '', "pattern = 's3://sentinel-s1-rtc-indigo/tiles/RTC/1/IW/14/T/PN/2020/{band}/Gamma0_VH.tif'\nchunks=dict(band=1, x=2745, y=2745)\nsources = intake.open_rasterio(images[:6], chunks=chunks, path_as_pattern=pattern, concat_dim='band')\nda = sources.to_dask() \nda\n")


# ## Dataclub from many COGs

# In[77]:


get_ipython().run_cell_magic('time', '', "chunks=dict(band=1, x=2745, y=2745)\ndataArrays = [rxr.open_rasterio(url, chunks=chunks) for url in images]\n\n# note use of join='override' b/c we know these COGS have the same coordinates\nda = xarray.concat(dataArrays, dim='band', join='override', combine_attrs='drop')\nda = da.rename({'band':'time'})\nda['time'] = [pd.to_datetime(x[60:68]) for x in images]\nda\n")


# ## Plotting

#  Using the bokeh library for this.

# In[78]:


import hvplot.xarray
da.hvplot.image(rasterize=True, aspect='equal', cmap='gray', clim=(0,0.4))


# In[ ]:





# In[ ]:




