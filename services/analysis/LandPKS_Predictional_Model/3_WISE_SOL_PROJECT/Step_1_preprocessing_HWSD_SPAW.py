# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys

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
message = "Usage : python Step_1_preprocessing_HWSD_SPAW.py -in <Input CSV File contains X and Y> -ou <Output CSV File contains X,Y,DLY File and WTG File> -tif <Directory to Folder contain all TIF Files> -model <Excel Model File>"
if (len(sys.argv) < 7):
    print("Sorry, not enough arguments")
    sys.exit(message)
# Input filenames
tif_HWSD = 'soil_texture/HWSD_soil.tif'
if (sys.argv[1] == '-in'):
   in_locs = sys.argv[2]
else:
   sys.exit(message)
if (sys.argv[3] == '-ou'):
   outfile = sys.argv[4]
else:
   sys.exit(message)
if (sys.argv[5]== '-tif'):
   src_dir = sys.argv[6]
else:
   sys.exit(message)
if (sys.argv[7]== '-model'):
   EXCEL_MODEL = sys.argv[8]
else:
   sys.exit(message)   
def main():
    f = open(in_locs, "rb")
    l = UnicodeReader(f)
    l.next()
    
    csvfile = open(outfile, 'wb')
    out = UnicodeWriter(csvfile)
    out.writerow(['Name', 'Y', 'X', 'MU_GLOBAL'])
    try:
       for row in l:
           name = row[0]
           mx, my = float(row[2]), float(row[1])  # coord in map units
           print "================================================="
           mu_global = getRasterValue(src_dir + tif_HWSD, mx, my)
           print "X = " + str(mx)
           print "Y = " + str(my)
           print "MU_GLOBAL = " + str(mu_global)
           out.writerow([name,str(my), str(mx),str(mu_global)])
           # Run Script create soil file
           os.system("python main_HWSD_SPAW.py -d \Database\HWSD.mdb -m %s -model %s" %(str(mu_global),EXCEL_MODEL))
       f.close()
    except Exception, err:
           print err
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
