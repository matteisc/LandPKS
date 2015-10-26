# Date: 12/01/03
# Import system modules
import sys, string, os, win32com.client

# Create the Geoprocessor object

gp = win32com.client.Dispatch("esriGeoprocessing.GpDispatch.1")
#gp = win32com.client.Dispatch("what")
print 'win32com work'

try:
# Set local variables
    #InFeatures = "C:/data/global.mdb/fd_inpoint/inpoint_point"
    InFeatures = "shp/cell30m_slate_v1p1_8387.shp"
    InField = "CELL30M"
    OutRaster = "shp/raster.tif"
    InCellSize = "30"

# Process: FeatureToRaster_conversion
    gp.FeatureToRaster_conversion(InFeatures, InField, OutRaster, InCellSize)
    print ' featuretoraster work '

except:
# Print error message if an error occurs
    print gp.GetMessages()
    print ' featuretoraster dont work '