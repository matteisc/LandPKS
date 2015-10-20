# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy
import shutil

from support import support_WEATHER

DISTANCE_THRESHOlD = 25

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
DLY_STORE_FOLDER = "D:/ThanhNguyen_Working/Python_APEX/2_WEATHER_PROJECT/Weather_Files/Daily_Weather_Files"




message = "Usage : python Step_1_preprocessing_WEATHER.py -x <X Coordinate _ Latitude> -y <Y Coordinate_ Longtitude> -tif <Directory to Folder contain all TIF Files> -id <Record ID"
if (len(sys.argv) < 7):
    print("Sorry, not enough arguments")
    sys.exit(message)
# Input filenames
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
#tif_slate_weather = 'test/raster.tif'
shp_slate_weather = 'SLATE_Weather/shp/cell30m_slate_v1p1_8387.shp'
X_FIELD = "X"
Y_FIELD = "Y"
VALUE_DATA = "CELL30M"
X_COOR = 0.0
Y_COOR = 0.0
ID = ""
# tif_slate_weather = 'growing_degree_days/gdd.tif'
if (sys.argv[1] == '-x'):
    if (float(sys.argv[2])):
        X_COOR = float(sys.argv[2])
    else:
        sys.exit(message)
else:
    sys.exit(message)
    
if (sys.argv[3] == '-y'):
   if (float(sys.argv[4])):
        Y_COOR = float(sys.argv[4])
   else:
        sys.exit(message)
else:
    sys.exit(message)
    
if (sys.argv[5] == '-tif'):
    if (sys.argv[6] is not None):
        src_dir = sys.argv[6]
    else:
        sys.exit(message)
else:
    sys.exit(message)

if (sys.argv[7] == '-id'):
    if (sys.argv[8] is not None):
        ID = sys.argv[8]
    else:
        sys.exit(message)
else:
    sys.exit(message)

PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE = ""

def createPrivateFolder_DAT():
   PRIVATE_FOLDER_ACCESS_DAT = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s" % (str(ID)), "DATFiles")
   if not os.path.exists(PRIVATE_FOLDER_ACCESS_DAT):
        os.makedirs(PRIVATE_FOLDER_ACCESS_DAT)
   return PRIVATE_FOLDER_ACCESS_DAT 
def createPrivateFolder_PRE_DLY_FILES():
   PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s" % (str(ID)), "Daily_Weather_Files")
   if not os.path.exists(PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE):
        os.makedirs(PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE)
   return PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE  
def createPrivateFolder_POS_DLY_FILES():
   PRIVATE_FOLDER_ACCESS_POS_DLY_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s" % (str(ID)), "POST_DLY_FILES")
   if not os.path.exists(PRIVATE_FOLDER_ACCESS_POS_DLY_FILE):
        os.makedirs(PRIVATE_FOLDER_ACCESS_POS_DLY_FILE)
   return PRIVATE_FOLDER_ACCESS_POS_DLY_FILE
def createPrivateFolder_PRE_WP1_FILES():
   PRIVATE_FOLDER_ACCESS_PRE_WP1_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s" % (str(ID)), "PRE_WP1_FILES")
   if not os.path.exists(PRIVATE_FOLDER_ACCESS_PRE_WP1_FILE):
        os.makedirs(PRIVATE_FOLDER_ACCESS_PRE_WP1_FILE)
   return PRIVATE_FOLDER_ACCESS_PRE_WP1_FILE  
def createPrivateFolder_POS_WP1_FILES():
   PRIVATE_FOLDER_ACCESS_POS_WP1_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s" % (str(ID)), "POST_DLY_FILES")
   if not os.path.exists(PRIVATE_FOLDER_ACCESS_POS_WP1_FILE):
        os.makedirs(PRIVATE_FOLDER_ACCESS_POS_WP1_FILE)
   return PRIVATE_FOLDER_ACCESS_POS_DLY_FILE
def copyFile(file_path, des):
    try:
        shutil.copy2(file_path, des)
    except Exception, err:
        print err
        pass
def main():
    
    try:
        #PRIVATE_FOLDER_ACCESS_DAT = createPrivateFolder_DAT();
        PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE = createPrivateFolder_PRE_DLY_FILES();
        #PRIVATE_FOLDER_ACCESS_POS_DLY_FILE = createPrivateFolder_POS_DLY_FILES();
        #PRIVATE_FOLDER_ACCESS_PRE_WP1_FILE = createPrivateFolder_PRE_WP1_FILES();
        #PRIVATE_FOLDER_ACCESS_POS_WP1_FILE = createPrivateFolder_POS_WP1_FILES();
        print "================================================="
        #slate_weather = getRasterValue_ThanhNguyen_SHP(src_dir + shp_slate_weather, mx, my)
        slate_weather_tif = getRasterValue_ThanhNguyen_TIF(src_dir + tif_slate_weather, X_COOR, Y_COOR);
        print "X = " + str(X_COOR)
        print "Y = " + str(Y_COOR)
        #print "Slate_Weather (SHP) = " + str(slate_weather)
        print "Slate_Weather (TIF) = " + str(slate_weather_tif)
        
        #support_WEATHER.insert_data_X_Y_dly_name(ID,Y_COOR,X_COOR,str(slate_weather_tif))
        if (not os.path.exists(os.path.join(DLY_STORE_FOLDER,"%s.DLY" %(str(slate_weather_tif))))):
            print "Not existed => Convert %s" %(str(slate_weather_tif))
            os.system("python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg D:/ThanhNguyen_Working/Python_APEX/2_WEATHER_PROJECT/wtg -Fdly %s -name %s" %(PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE,str(slate_weather_tif)))
        
        print "Start Running..."
        
        #Need to be integrated with Python CODE of NASIM to get best DLY file from Weather Station Data or From SLATE Weather ID
        print "------------------------------------------------------------------------------"
        try:   
            print ("=====ThanhNH : Creating DLY file from  Closest Weather Station")
            country_code = support_WEATHER.get_country_code_for_finding_closest_station(X_COOR,Y_COOR)
            station_data = support_WEATHER.formatClosestStationDLY(X_COOR,Y_COOR,country_code,str(slate_weather_tif))
            station_data = support_WEATHER.standard_string(station_data)
            print("====Closest weather data station is : %s" %(str(station_data)))
            array_station_data = station_data.split(' ')
            distance = array_station_data[9].strip()
            print("====Distance  : %s" %(str(distance)))
            fl_distance = float(distance)
        except Exception, err:
            print err
            fl_distance = None
            pass
            print ("=====ThanhNH : Cannot find Inventory File of this contry %s" %(country_code))
        #Check the distance threshold . Based on this value we consider one of optios to select dly Files : From Store Library or from Slate Weather Station
        if (fl_distance is not None and fl_distance <= DISTANCE_THRESHOlD):
          print("==========1====Used new DLY File from Station Weather Data====Closest Distance========")
          #dly_folder = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Station_Data\\DLY_Files\\%s.DLY" %(slate_weather_tif)   
          dly_folder = "%s\\%s.DLY" %(support_WEATHER.get_dly_folder(),slate_weather_tif) 
          copyFile(dly_folder, PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE)  
        else:
          # Copy raw DLY File to Folder Running
          print("==========2====Used  DLY File from Library====Traditional Way========")
          file_dly_path = os.path.join(DLY_STORE_FOLDER,"%s.DLY" %(str(slate_weather_tif)))
          copyFile(file_dly_path, PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE)         
        print "------------------------------------------------------------------------------"
        
        # Run model
        os.system("python Step_3_main_WEATHER_Real_Time.py -f %s -x %f -y %f -ID %s" %(PRIVATE_FOLDER_ACCESS_PRE_DLY_FILE,X_COOR,Y_COOR,ID))
    
        outfile = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/complete_map_location.csv" %(str(ID))
        csvfile = open(outfile, 'wb')
        out = UnicodeWriter(csvfile)
        out.writerow(['Name','Y', 'X','WTG File'])
        out.writerow([str(ID), str(Y_COOR),str(X_COOR),str(slate_weather_tif)])
        
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
