# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy

from support import support_WEATHER

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row) 
def getRasterValue(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_UInt16)  # Assumes 16 bit int aka 'short'
    intval = struct.unpack('h' , structval)  # use the 'short' format code (2 bytes) not int (4 bytes)
    return(intval[0])

# Check arguments

if (len(sys.argv) < 7):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_WEATHER.py -in <Input CSV File contains X and Y> -ou <Output CSV File contains X,Y,DLY File and WTG File> -tif <Directory to Folder contain all TIF Files>")
# Input filenames
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
#tif_slate_weather = 'test/raster.tif'
shp_slate_weather = 'SLATE_Weather/shp/cell30m_slate_v1p1_8387.shp'
X_FIELD = "X"
Y_FIELD = "Y"
VALUE_DATA = "CELL30M"
# tif_slate_weather = 'growing_degree_days/gdd.tif'
if (sys.argv[1] == '-in'):
   in_locs = sys.argv[2]
if (sys.argv[3] == '-ou'):
   outfile = sys.argv[4]
if (sys.argv[5] == '-tif'):
   src_dir = sys.argv[6]

def main():
    f = open(in_locs, "rb")
    l = UnicodeReader(f)
    l.next()
    
    csvfile = open(outfile, 'wb')
    out = UnicodeWriter(csvfile)
    out.writerow(['Name','Y', 'X','WTG File'])
    try:
       for row in l:
           dly_file = row[0]
           mx, my = float(row[2]), float(row[1])  # coord in map units
           print "================================================="
           #slate_weather = getRasterValue_ThanhNguyen_SHP(src_dir + shp_slate_weather, mx, my)
           slate_weather_tif = getRasterValue_ThanhNguyen_TIF(src_dir + tif_slate_weather, mx, my);
           print "X = " + str(mx)
           print "Y = " + str(my)
           #print "Slate_Weather (SHP) = " + str(slate_weather)
           print "Slate_Weather (TIF) = " + str(slate_weather_tif)
           out.writerow([str(dly_file), str(my),str(mx),str(slate_weather_tif)])
           support_WEATHER.insert_data_X_Y_dly_name(dly_file,my,mx,str(slate_weather_tif))
    except Exception, err:
           print err
def getRasterValue_ThanhNguyen_TIF(src_file,mx,my):
    src_ds = gdal.Open(src_file) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]          
def getRasterValue_ThanhNguyen_SHP(src_file, mx, my):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.Open(src_file, 0)
    layer = ds.GetLayer(0)
    n = layer.GetFeatureCount()
    extent = layer.GetExtent()
    feat = layer.GetNextFeature()
    while feat:
        cell30M = int(feat.GetField(VALUE_DATA))
        x = feat.GetField(X_FIELD)
        y = feat.GetField(Y_FIELD)
        if (x == mx and y == my):
            print "X = %s | Y = %s | CELL = %s" % (str(x), str(y), str(cell30M)) 
            feat.Destroy()
            return cell30M  
        feat.Destroy()
        feat = layer.GetNextFeature() 
    return -1
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
