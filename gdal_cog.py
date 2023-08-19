#!/usr/bin/env python
# coding: utf-8

# ## Simple code to deal with masking of the cog

# First used gdal to build a cog nd download it into your computer memory. Then mask of this raster file is created and is savd into the ram for further processing.

# In[1]:


#pip install numpy


# In[2]:


#pip install matplotlib


# In[6]:


from osgeo import gdal


# In[9]:


import numpy


# In[11]:


import matplotlib.pyplot as plt


# In[26]:


from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt 


# In[27]:


ds = gdal.Open("merged.tif")


# In[28]:


gt = ds.GetGeoTransform()
proj = ds.GetProjection()
band = ds.GetRasterBand(1)


# In[29]:


array = band.ReadAsArray()


# In[30]:


print(type(array))


# In[31]:


plt.figure()
plt.imshow(array)


# In[32]:


binmask = np.where((array >= np.mean(array)),1,0)


# In[33]:


plt.figure()
plt.imshow(binmask)


# In[34]:


driver = gdal.GetDriverByName('GTiff')
driver.Register()
outds = driver.Create('binmask.tif', xsize = binmask.shape[1], ysize = binmask.shape[0], bands = 1, eType = gdal.GDT_Int16)


# In[35]:


outds


# In[36]:


outds.SetGeoTransform(gt)
outds.SetProjection(proj)
outband = outds.GetRasterBand(1)
outband.WriteArray(binmask)
outband.SetNoDataValue(np.nan)
outband.FlushCache()


# In[37]:


outband = None
outdds = None


# In[ ]:




