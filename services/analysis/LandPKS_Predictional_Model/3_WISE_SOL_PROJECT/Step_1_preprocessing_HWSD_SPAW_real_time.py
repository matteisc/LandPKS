# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct,csv, os, sys

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
X_COOR = 0.0
Y_COOR = 0.0
if (len(sys.argv) < 7):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_HWSD_SPAW_real_time.py -x <X Longtitude> -y <Y Latitude> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>")
# Input filenames
tif_HWSD = 'soil_texture/HWSD_soil.tif'
if (sys.argv[1] == '-x'):
   if (float(sys.argv[2])):
       X_COOR = float(sys.argv[2])
else:
   sys.exit("Usage : python Step_1_preprocessing_HWSD_SPAW_real_time.py -x <X Longtitude> -y <Y Latitude> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>")
if (sys.argv[3] == '-y'):
     if (float(sys.argv[4])):
       Y_COOR = float(sys.argv[4])
else:
   sys.exit("Usage : python Step_1_preprocessing_HWSD_SPAW_real_time.py -x <X Longtitude> -y <Y Latitude> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>")
if (sys.argv[5]== '-tif'):
   src_dir = sys.argv[6]
else:
   sys.exit("Usage : python Step_1_preprocessing_HWSD_SPAW_real_time.py -x <X Longtitude> -y <Y Latitude> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>")
if (sys.argv[7]== '-model'):
   EXCEL_MODEL = sys.argv[8]
else:
   sys.exit("Usage : python Step_1_preprocessing_HWSD_SPAW_real_time.py -x <X Longtitude> -y <Y Latitude> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>")   
def main():
   try:
       print "================================================="
       mu_global = getRasterValue(src_dir + tif_HWSD, X_COOR, Y_COOR)
       print "X = " + str(X_COOR)
       print "Y = " + str(Y_COOR)
       print "MU_GLOBAL = " + str(mu_global)
       os.system("python main_HWSD_SPAW.py -d \Database\HWSD.mdb -m %s -model %s" %(str(mu_global),EXCEL_MODEL))
   except Exception,err:
       sys.exit(err)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
