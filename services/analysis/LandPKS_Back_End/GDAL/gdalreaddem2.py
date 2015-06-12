#Python Version 2.6.5 GDAL version 1.11.0 older version uses osgeo to load gdal libraries
#edit the directory(os.chdir) and set the filename(gdal.open) then run
import os, sys, arcpy, glob
from osgeo import gdal, gdalconst, osr
from osgeo.gdal import *
from osgeo.gdalconst import *
import struct
import numpy

arcpy.env.overwriteOutput= "true"
def pt2fmt(pt):
	fmttypes = {
		GDT_Byte: 'B',
		GDT_Int16: 'h',
		GDT_UInt16: 'H',
		GDT_Int32: 'i',
		GDT_UInt32: 'I',
		GDT_Float32: 'f',
		GDT_Float64: 'f'
		}
	return fmttypes.get(pt, 'x')
    
xValues =[36.25,36.75,37.25,37.75,38.25,36.25,36.75,37.25,37.75,38.25,36.25,36.75,37.25,37.75,38.25,36.25,36.75,37.25,37.75,38.25,36.25,36.75,37.25,37.75,36.88]
yValues =[2.25,2.25,2.25,2.25,2.25,1.75,1.75,1.75,1.75,1.75,1.25,1.25,1.25,1.25,1.25,0.75,0.75,0.75,0.75,0.75,0.25,0.25,0.25,0.25,0.338]
#xynames =[126432,126433,126434,126435,126436,127152,127153,127154,127155,127156,127872,127873,127874,127875,127876,128592,128593,128594,128595,128596,129312,129313,129314,129315,129316]

def scanfolder():
    os.chdir('D:/PRODUCTS/21august/reproj/kenya wgs84/')
    for file in glob.glob('*/*.tif'):
   
        ds = gdal.Open(file, GA_ReadOnly)
        rb=ds.GetRasterBand(1)
        if ds is None:
            print 'Could not open image'
            sys.exit(1)
        # get image size
        rows = ds.RasterYSize
        cols = ds.RasterXSize
        bands = ds.RasterCount
        band = ds.GetRasterBand(1)
        bandtype = gdal.GetDataTypeName(band.DataType) #Int16
        # get georeference info
        transform = ds.GetGeoTransform()
        xOrigin = transform[0] 
        yOrigin = transform[3]
        pixelWidth = transform[1]
        pixelHeight = transform[5]
        success, transfInv = gdal.InvGeoTransform(transform)
        if not success:
            print "Failed InvGeoTransform()"
            sys.exit(1)
        # loop through the coordinates
        for i in range(25):
                # get x,y
            x = xValues[i]
            y = yValues[i]
            
            xsize = band.XSize
            ysize = band.YSize
            #print xsize, ysize
            # compute pixel offset
            px, py = gdal.ApplyGeoTransform(transfInv, x, y)
            # create a string to print out 
            structval=ds.ReadRaster(int(px),int(py),1,1,buf_type=gdal.GDT_Float32)
            intval = struct.unpack('f',structval)
            s =str(x) + ' ' + str(y) + ': ' + str(round(intval[0],6))
            print str(file)+'' + s
            #print structval[0][0] #intval is a tuple, length=1 as we only asked for 1 pixel value
            
                 
        
scanfolder()





