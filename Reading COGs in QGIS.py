# Import the sat-search library in OS4Geo terminal to use the code below in QGIS python console.
from satsearch import Search

#layer = iface.activeLayer()    # Uncomment this if there's an active layer
#feature = layer.getFeatures()
#for feat in feature:
 #  extend = feat.geometry().boundingBox()
#----------------------------------------------------------------------------------------------------
extent = iface.mapCanvas().extent()                          # Use this if aoi is in pan map view .
print([extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()])
bbox =[extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]
#----------------------------------------------------------------------------------------------------
url = "https://earth-search.aws.element84.com/v0/"
scene_cloud_tolerance = 40 
date = '2022-02-12'
# Function searches for the appropriate COG
def image_search(bbox, date_range, scene_cloud_tolerance):
    """
    Using SatSearch find all Sentinel-2 images
    that meet the searching criteria
    """
    
    search = Search(
        bbox=bbox,
        datetime=date_range,
        query={
            "eo:cloud_cover": {"lt": scene_cloud_tolerance}
        },  
        collections=["sentinel-s2-l2a-cogs"],
        url=url,
    )

    return search.items()
items = image_search(bbox, date_range, scene_cloud_tolerance)
print('%s items' % len(items))                      
print(items.summary(['date', 'id', 'eo:cloud_cover'])) 
file_url = items[0].asset('green')['href']     # Item index and Asset can be changed as per requirement.
# Adds the layer directly in QGIS as COG
rlayer = iface.addRasterLayer(file_url, 'COG')