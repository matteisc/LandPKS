# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import shutil
import fileinput
import datetime
import time
import subprocess
import struct, csv, codecs, cStringIO
from osgeo import gdal, ogr
import numpy
import json

# Check arguments
message = "Usage : python Run_compute_annual_precipitation.py -x <Longitude> -y <Latitude> -year <year>"
if (len(sys.argv) < 5):
    print("ERROR_RUNNING")
    sys.exit(message)
TIF_FOLDER_FILE = "E:\\ThanhNguyen_Working\\Python_APEX\\TIF_FILE_COLLECTION\\"
tif_slate_weather = 'SLATE_Weather/tif\\SLATE_raster1.tif'
DLY_FILE_STORE = "E:\\ThanhNguyen_Working\\Python_APEX\\2_WEATHER_PROJECT\\Weather_Files\\Daily_Weather_Files_100_years"
DLY_FILE_NAME = ""
FULL_DLY_FILE_NAME = ""
X_COOR = 0
Y_COOR = 0
YEAR = 1990
# Manage arguments
in_locs = ""


if (sys.argv[1] == '-x') :
    if ((sys.argv[2] is not None) and (float(sys.argv[2]))):
         X_COOR = float(sys.argv[2])
    else :
         print("ERROR_RUNNING_1")
         sys.exit(message)
    
    if (sys.argv[3] == '-y') :
      if ((sys.argv[4] is not None) and (float(sys.argv[4]))):
            Y_COOR = float(sys.argv[4])
      else :
         print("ERROR_RUNNING_2")
         sys.exit(message)  
    else :
      print("ERROR_RUNNING_3")
      sys.exit(message)

    if (sys.argv[5] == '-year') :
      if ((sys.argv[6] is not None) and (int(sys.argv[6]))):
         YEAR = int(sys.argv[6])
      else :
         print("ERROR_RUNNING_4")
         sys.exit(message)  
    else :
      print("ERROR_RUNNING_5")
      sys.exit(message)     
elif (sys.argv[1] == '-input'):
    if ((sys.argv[2] is not None)):
         in_locs = sys.argv[2]
    else :
         print("ERROR_RUNNING_6")
         sys.exit(message)  

    if (sys.argv[3] == '-output'):
        if ((sys.argv[4] is not None)):
            outfile = sys.argv[4]
        else :
            print("ERROR_RUNNING_7")
            sys.exit(message)  
else :
    print("ERROR_RUNNING_8")
    sys.exit(message)



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

def getRasterValue_ThanhNguyen_TIF(src_file,mx,my):
    src_ds = gdal.Open(src_file) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]

def read_precipitation_data_from_file(full_DLY_file, year):
    try:
        # Read each file WP1
        count_precip = 0
        total_content_precipitation = 0.0
        #print(" ====Process File: %s " % (full_DLY_file))
        with open(full_DLY_file,'r') as file:
            data = file.readlines()
        for i in range(0,len(data)):
            line = data[i]
            if (line is not None and line.strip()):
                content_year = line[:7]
                content_year = content_year.strip()
                int_content_year = int(content_year)
                if (int_content_year == year):
                    #count_precip = count_precip + 1
                    try:
                        content_precipitation = line[33:39]
                        fl_content_prep = float(content_precipitation)
                        total_content_precipitation = total_content_precipitation + fl_content_prep
                        #print content_precipitation + " === " + str(count_precip) + " === " + str(total_content_precipitation)
                    except Exception, err:
                        pass
        return total_content_precipitation
    except Exception, err:
        #sys.exit(err)
        sys.stderr.write("ERR0R_002")
def main():
    f = open(in_locs, "rb")
    l = UnicodeReader(f)
    l.next()
    
    csvfile = open(outfile, 'wb')
    out = UnicodeWriter(csvfile)
    out.writerow(['long', 'lat', 'year', 'total_precipitation'])
    
    try:
       for row in l:
           X_COOR, Y_COOR = float(row[0]), float(row[1])
           STR_YEAR = row[2]
           print "====Process : X = %s ; Y = %s ; Year = %s" %(str(X_COOR), str(Y_COOR), str(STR_YEAR))
           if (STR_YEAR.isdigit()):
               YEAR = int(STR_YEAR)
               DLY_FILE_NAME = getRasterValue_ThanhNguyen_TIF(TIF_FOLDER_FILE + tif_slate_weather, X_COOR, Y_COOR)
               FULL_DLY_FILE_NAME = os.path.join(DLY_FILE_STORE,str(DLY_FILE_NAME) + ".DLY")
               if (os.path.exists(FULL_DLY_FILE_NAME)):         
                     total_content_precipitation = read_precipitation_data_from_file(FULL_DLY_FILE_NAME,YEAR)
               else:
                     total_content_precipitation = -999
               out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(total_content_precipitation)])
           else:
               if (STR_YEAR is not None):
                   if ("-" in STR_YEAR):
                       period_years = STR_YEAR.split("-")
                       start_year = int(period_years[0].strip())
                       end_year = int(period_years[1].strip())
                       if (end_year >= start_year):
                           try:
                               mini_total_precip = 0.0
                               total_content_precipitation_period = 0.0
                               for current_year in range(start_year, end_year + 1):          
                                   mini_total_precip = read_precipitation_data_from_file(FULL_DLY_FILE_NAME,current_year)
                                   print "============Process : %s  : => %s" %(str(current_year), str(mini_total_precip))
                                   if ((str(mini_total_precip).strip() is not None) and (mini_total_precip != -999)):
                                       total_content_precipitation_period = total_content_precipitation_period + mini_total_precip
                               total_content_precipitation_period_avg = total_content_precipitation_period / (end_year - start_year + 1)
                               out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(total_content_precipitation_period_avg)])
                           except Exception, err:
                               out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(-999)])
                       else :
                           out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(-999)])
                   else:
                       out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(-999)])
               else:    
                   out.writerow([str(X_COOR), str(Y_COOR), str(STR_YEAR), str(-999)])      
    except Exception, err:
           print err
           #print 1
        
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
