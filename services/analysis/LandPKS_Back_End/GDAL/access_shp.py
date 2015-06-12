from osgeo import ogr, gdal
driver = ogr.GetDriverByName('ESRI Shapefile')
ds = driver.Open('shp/cell30m_slate_v1p1_8387.shp', 0)
layer = ds.GetLayer(0)
n = layer.GetFeatureCount()
print 'feature count: ' + str(n)

extent = layer.GetExtent()
print 'extent:', extent
print 'ul:', extent[0], extent[3]
print 'lr:', extent[1], extent[2]


feat = layer.GetNextFeature()

while feat:
      cell30M = feat.GetField('CELL30M')
      x = feat.GetField("X")
      y = feat.GetField("Y")
      print "X = %s | Y = %s | CELL = %s" %(str(x),str(y),str(cell30M))
      feat.Destroy()
      feat = layer.GetNextFeature() 
