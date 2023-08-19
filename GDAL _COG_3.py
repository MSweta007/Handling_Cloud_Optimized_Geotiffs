#!/usr/bin/env python
# coding: utf-8

# In[74]:


#pip install xarray


# In[75]:


#pip install rasterio


# In[76]:


#SSpip install rioxarray


# In[ ]:


#pip install hvplot


# In[ ]:


pip install rio-cogeo==2.0a3


# In[1]:


from osgeo import gdal


# In[2]:


import os
import numpy as np
import pandas as pd
import xarray as xr
import rasterio
import rioxarray
import hvplot.xarray
import requests


# In[3]:


print(xr.__version__)
print(rasterio.__version__)
print(gdal.VersionInfo())


# In[4]:


#The http url link to the COG 
url = 'https://maxar-opendata.s3.us-west-2.amazonaws.com/events/Emilia-Romagna-Italy-flooding-may23/ard/33/031111212320/2015-05-28/1050410012C31100-visual.tif'


# In[ ]:





# In[ ]:





# In[5]:


print(url)


# In[6]:


get_ipython().run_cell_magic('time', '', '!curl -O {url}\nlocalFile = os.path.basename(url)\n#da = xr.open_rasterio(localFile)\nda = rioxarray.open_rasterio(localFile)\n')


# In[11]:


print(len(localFile))
print(type(localFile))


# In[12]:


print(f'Uncompressed size: {da.nbytes/1e6} MB')
da


# In[13]:


get_ipython().run_cell_magic('time', '', "da.mean(dim=['x','y'])\n")


# In[14]:


da.hvplot.image(cmap='kbc_r', clabel='T [C]')


# In[15]:


#Done for reading the file using the url in gdal
del da


# In[16]:


os.environ['GDAL_DISABLE_READDIR_ON_OPEN']='EMPTY_DIR' 
os.environ['AWS_NO_SIGN_REQUEST']='YES'
os.environ['GDAL_MAX_RAW_BLOCK_CACHE_SIZE']='200000000'  
os.environ['GDAL_SWATH_SIZE']='200000000'  
os.environ['VSI_CURL_CACHE_SIZE']='200000000' 


# In[17]:


get_ipython().run_cell_magic('time', '', 'da = rioxarray.open_rasterio(url)\n')


# In[18]:


get_ipython().run_cell_magic('time', '', "da.mean(dim=['x','y'])\n")


# In[ ]:


da.hvplot.image(cmap='kbc_r', clabel='T [C]')


# In[19]:


del da


# In[30]:


#pip install "dask[distributed]"


# In[58]:


from dask.distributed import Client, LocalCluster
cluster = LocalCluster(processes=False, local_directory='/tmp') # specify dask worker directory to avoid /home NFS mount
client = Client() 
client #this will give you a url such as /user/scottyhq/proxy/8787/status that goes into the labextension dashboard


# In[59]:


get_ipython().run_cell_magic('time', '', 'chunks=dict(band=1, x=2745, y=2745) \nda = rioxarray.open_rasterio(url, chunks==chunks)\n')


# In[60]:


get_ipython().run_cell_magic('time', '', "ave = da.mean(dim=['x','y'])\nave\n")


# In[68]:


da.mean(dim=['x','y']).plot()


# In[69]:


get_ipython().run_cell_magic('time', '', 'ave.compute()\n')


# In[16]:


get_ipython().run_cell_magic('time', '', "da = rioxarray.open_rasterio(url, masked=True, overview_level=1)\nda.hvplot.image(cmap='gray', aspect='equal', clim=(0,0.4), title=url[64:])\n#.squeeze('band')\n")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




