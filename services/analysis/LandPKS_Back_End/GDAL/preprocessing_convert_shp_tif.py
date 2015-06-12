from osgeo import gdal, ogr, osr

source_ds = ogr.Open("shp/cell30m_slate_v1p1_8387.shp")
source_layer = source_ds.GetLayer()

pixelWidth = pixelHeight =  0.25 # depending how fine you want your raster
x_min, x_max, y_min, y_max = source_layer.GetExtent()

cols = int((x_max - x_min) / pixelHeight)
rows = int((y_max - y_min) / pixelWidth)
target_ds = gdal.GetDriverByName('GTiff').Create('temp.tif', cols, rows, 1, gdal.GDT_Byte) 
target_ds.SetGeoTransform((x_min, pixelWidth, 0, y_max, 0, -pixelHeight))
band = target_ds.GetRasterBand(1)
NoData_value = -9999
band.SetNoDataValue(NoData_value)
band.FlushCache()

gdal.RasterizeLayer(target_ds, [1], source_layer,options = ["ATTRIBUTE=CELL30M"])  
target_dsSRS = osr.SpatialReference()
#target_dsSRS.ImportFromEPSG(4326)
target_ds.SetProjection(target_dsSRS.ExportToWkt())
gdal.Open('temp.tif').ReadAsArray()