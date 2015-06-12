# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import numpy
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
full_path = os.getcwd() + "\\"
def getRasterValue_ThanhNH(srcfile, mx, my):
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 
    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel
    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
    return structval[0][0]           
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
if (len(sys.argv) < 5):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -in <Input CSV File contain ID X Y of location to get Site File> -tif <Directory to Folder contain all TIF Files>")
# Input filenames
tif_ELEVATION = 'elevation/elevation.tif'
INPUT_CSV_LOCATION = ""
src_dir = ""
if (sys.argv[1] == '-in'):
   if (sys.argv[2] is None or sys.argv[2] == ''):
       sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -in <Input CSV File contain ID X Y of location to get Site File> -tif <Directory to Folder contain all TIF Files>")
   else:
       INPUT_CSV_LOCATION = sys.argv[2]
       if (not os.path.exists(INPUT_CSV_LOCATION)):
           sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -in <Input CSV File contain ID X Y of location to get Site File> -tif <Directory to Folder contain all TIF Files>")
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -in <Input CSV File contain ID X Y of location to get Site File> -tif <Directory to Folder contain all TIF Files>")

if (sys.argv[3]== '-tif'):
   src_dir = sys.argv[4]
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -in <Input CSV File contain ID X Y of location to get Site File> -tif <Directory to Folder contain all TIF Files>")
def checkAndCreateFolder():
    directory = full_path + "\Site_Files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\%s" % ("DAT_Files")
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
    siteDirectory = directory + "\%s" % ("Site_Files")
    if not os.path.exists(siteDirectory):
        os.makedirs(siteDirectory)    
def createSOILFile(site_file_name,elevation,X,Y):
    try:
        fo = open(os.path.join("Site_Files/Site_Files/%s.SIT" %(site_file_name)), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SIT property to File %s.SIT" % (str(site_file_name)))
        # Line 1
        length = len(site_file_name)
        space_number = 81 - length
        strContent = ""
        for i in range(1, space_number):
            strContent = strContent + " "
        strContent = strContent + site_file_name
        fo.write(strContent)
        # Line 2
        full_site_file_name = site_file_name + ".SIT"
        length = len(full_site_file_name)
        space_number = 81 - length
        strContent = ""
        for i in range(1, space_number):
            strContent = strContent + " "
        strContent = strContent + full_site_file_name
        fo.write("\n" + strContent)
        # Line 3
        fo.write("\n                                                                        %s" % ("OUTLET 1"))
        # Line 4 
        fo.write("\n")
          #Field 1  Y Coor
        if (Y >= 0 and Y < 10):
            strContent = "    %0.2f" % (Y)
        elif (Y >= 10 and Y < 100):
            strContent = "   %0.2f" % (Y)
        elif (Y >= 100 and Y < 1000):
            strContent = "  %0.2f" % (Y)
        elif (Y >= 1000 and Y < 10000):
            strContent = " %0.2f" % (Y)
        elif (Y >= 10000 and Y < 100000):
            strContent = "%0.2f" % (Y)
        elif (Y < 0 and Y > -10):
            strContent = "   %0.2f" % (Y)
        elif (Y <= -10 and Y > -100):
            strContent = "  %0.2f" % (Y)
        elif (Y <= -100 and Y > -1000):
            strContent = " %0.2f" % (Y)
        elif (Y <= -1000 and Y > -10000):
            strContent = "0.2f" % (Y)
        fo.write(strContent)
           #Field 2  X Coor
        if (X >= 0 and X < 10):
            strContent = "    %0.2f" % (X)
        elif (X >= 10 and X < 100):
            strContent = "   %0.2f" % (X)
        elif (X >= 100 and X < 1000):
            strContent = "  %0.2f" % (X)
        elif (X >= 1000 and X < 10000):
            strContent = " %0.2f" % (X)
        elif (X >= 10000 and X < 100000):
            strContent = "%0.2f" % (X)
        elif (X < 0 and X > -10):
            strContent = "   %0.2f" % (X)
        elif (X <= -10 and X > -100):
            strContent = "  %0.2f" % (X)
        elif (X <= -100 and X > -1000):
            strContent = " %0.2f" % (X)
        elif (X <= -1000 and X > -10000):
            strContent = "0.2f" % (X)
        fo.write(strContent)
        
          #Field 3  Elevation
        if (elevation >= 0 and elevation < 10):
            strContent = "    %0.2f" % (elevation)
        elif (elevation >= 10 and elevation < 100):
            strContent = "   %0.2f" % (elevation)
        elif (elevation >= 100 and elevation < 1000):
            strContent = "  %0.2f" % (elevation)
        elif (elevation >= 1000 and elevation < 10000):
            strContent = " %0.2f" % (elevation)
        elif (elevation >= 10000 and elevation < 100000):
            strContent = "%0.2f" % (elevation)
        elif (elevation < 0 and elevation > -10):
            strContent = "   %0.2f" % (elevation)
        elif (elevation <= -10 and elevation > -100):
            strContent = "  %0.2f" % (elevation)
        elif (elevation <= -100 and elevation > -1000):
            strContent = " %0.2f" % (elevation)
        elif (elevation <= -1000 and elevation > -10000):
            strContent = "0.2f" % (elevation)
        fo.write(strContent)
        
          #Field 4  
        fo.write("    %0.2f" % (1))
          #Field 5  n
        fo.write("    %0.2f" % (0))
          #Field 6  n
        fo.write("    %0.2f" % (0))
          #Field 7  n
        fo.write("    %0.2f" % (0.8))
          #Field 8  n
        fo.write("    %0.2f" % (0))
          #Field 9  n
        fo.write("    %0.2f" % (0))
        
        #Line 5
        fo.write("\n                                                                                ")
        #Line 6
        fo.write("\n                                                                                ")
        #Line 7
        fo.write("\n       %d       %d       %d       %d       %d       %d       %d       %d       %d       %d" %(0,0,0,0,0,0,0,0,0,0))
        #Line 8
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" %(0,0,0,0,0,0,0,0,0,0))
        #Line 9
        fo.write("\n\n");
        #Line 10
        fo.write("                                                                                \n")
        fo.close()
    except Exception, err:
        fo.close()
        sys.exit("Error : %s" % (err))
    finally:
        print("Done")
        fo.close()
           
def main():
   f = open(INPUT_CSV_LOCATION, "rb")
   l = UnicodeReader(f)
   l.next()
   try:
       print("-PREPROCESSING : Create Folders--")
       checkAndCreateFolder()
       print("-Create File and Folder already")
       for row in l:
           name = row[0]
           mx, my = float(row[2]), float(row[1])  # coord in map units
           site_file_name = row[3]
           print "================================================="
           elevation = getRasterValue_ThanhNH(src_dir + tif_ELEVATION, mx, my)
           print "X = " + str(mx)
           print "Y = " + str(my)
           print "Elevation = " + str(elevation)
           print("-Create SITE Files")
           createSOILFile(site_file_name,elevation,mx,my)
           print("-Site File is created already")
       os.system("python Step_2_main_SITE.py -fsite C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/Site_Files/Site_Files -fdat C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/Site_Files/DAT_Files")
       f.close()
   except Exception,err:
       sys.exit(err)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
