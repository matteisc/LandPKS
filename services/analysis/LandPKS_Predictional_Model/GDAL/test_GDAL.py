from osgeo import gdal
import numpy as np

    # Read the input raster into a Numpy array
infile = "D:\ThanhNguyen_Working\Python_APEX\GDAL\soil_texture\soil_texture.tif"
data   = gdal.Open(infile)
arr    = data.ReadAsArray()

    # Do some processing....

    # Save out to a GeoTiff

    # First of all, gather some information from the original file
[cols,rows] = arr.shape
trans       = data.GetGeoTransform()
proj        = data.GetProjection()
nodatav     = data.GetNoDataValue()
outfile     = "outputfile.tif"

    # Create the file, using the information from the original file
outdriver = gdal.GetDriverByName("GTiff")
outdata   = outdriver.Create(str(outfile), rows, cols, 1, gdal.GDT_Float32)

    # Write the array to the file, which is the original array in this example
outdata.GetRasterBand(1).WriteArray(arr)

    # Set a no data value if required
outdata.GetRasterBand(1).SetNoDataValue(nodatav)

    # Georeference the image
outdata.SetGeoTransform(trans)

    # Write projection information
outdata.SetProjection(proj)