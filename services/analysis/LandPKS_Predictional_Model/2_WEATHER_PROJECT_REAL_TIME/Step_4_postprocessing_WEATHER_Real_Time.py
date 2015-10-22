# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import datetime
import numpy

now = datetime.datetime.now()
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

# Check arguments

if (len(sys.argv) < 8):
    print("Sorry, not enough arguments == Application will read Input : File CSV contans MAP between Name of DLY or PTG File and X and Y (Result of Step 1) + Folder Contains Complete WP1 File + Folder Contains all TIF Wind Data + YEAR of Wind Data TIF File")
    sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
# Input filenames
csv_location_file = ""
wp1_folder = ""
tif_folder = ""
tif_structure = 0
pre_name_tif_file = "gwind"
post_name_tif_file = ".tif"
LINE_DECIDE = 15
wind_year = ""

if (sys.argv[1] == '-Fcsv'):
   csv_location = sys.argv[2]
if (sys.argv[3] == '-Fwp1'):
   wp1_folder = sys.argv[4]
if (sys.argv[5] == '-Ftif'):
   tif_folder = sys.argv[6]
if (sys.argv[7] == '-Wyear'):
   wind_year = sys.argv[8]

def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = filename
            file_paths.append(file_path)
    return file_paths
def get_dirs_path(directory):
    dir_paths = []
    for root, dirs, files in os.walk(directory):
         for folder in dirs:
            dir_path = folder
            dir_paths.append(dir_path)
    return dir_paths
def checkAllInputData():
    print("--Step 1 : Check available of all input data")
    if (csv_location is None or not csv_location.strip() or csv_location == ""):
         print("ERROR : There is NO CSV Location Mapping between LOCATION and NAME DLY OR PTG OR WP1 FILE")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if (wp1_folder is None or not wp1_folder.strip() or wp1_folder == ""):
         print("ERROR : There is NO Folder Path of Complete WP1 File")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if (tif_folder is None or not tif_folder.strip() or tif_folder == ""):    
         print("ERROR : There is NO Folder Path of TIFF Folder and File of Wind Data")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if (wind_year is None or not tif_folder.strip() or tif_folder == ""):    
         print("ERROR : There is NO YEAR DATA of WIND TIF FILE")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if not os.path.exists(csv_location): 
         print("ERROR : CSV Location Mapping between LOCATION and NAME DLY OR PTG OR WP1 FILE IS NOT EXISTED")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if not os.path.exists(wp1_folder): 
         print("ERROR : Complete WP1 FOLDER is NOT EXISTED")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if not os.path.exists(tif_folder): 
         print("ERROR : TIFF Files FOLDER is NOT EXISTED")
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    if (int(wind_year) < 1900 or int(wind_year) > now.year):
         print("ERROR : Year should be in range 1900 - %d" % (now.year))
         sys.exit("Usage : python Step_4_postprocessing_WEATHER.py -Fcsv <Path to CSV File - Result of Step 1> -Fwp1 <Folder contains Complete WP1 File - Result of Step 3> -Ftif <Folder Contains all TIFF File and Folder of Wind Data> -Wyear <Year of Wind Data>")
    small_tif_folders = get_dirs_path(tif_folder)
    if (len(small_tif_folders) > 0):
        tif_structure = 0
    else:
        tif_structure = 1
    if (tif_structure == 0):
         print("----Notice : TIF files as : <Main Folder>/<%s[time].tif>/%s[time].tif" % (pre_name_tif_file, pre_name_tif_file))
    else:
         print("----Notice : TIF Files as : <Main Folder>/%s[time]/tif" % (pre_name_tif_file))
    print("--Finish Step 1 : All input data is Ready")
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
def write_wind_monthly_data_to_WP1_File(full_path_wp1_file, wind_data_tif_month_1, wind_data_tif_month_2, wind_data_tif_month_3, wind_data_tif_month_4, wind_data_tif_month_5, wind_data_tif_month_6, wind_data_tif_month_7, wind_data_tif_month_8, wind_data_tif_month_9, wind_data_tif_month_10, wind_data_tif_month_11, wind_data_tif_month_12):
    try:
        if (not os.path.exists(full_path_wp1_file)):
             print("--Warning : WP1 File doest not exited")
             return -1;
        print(" ====Process WP1 File: %s " % (full_path_wp1_file))
        with open(full_path_wp1_file, 'r') as file:
            data = file.readlines()        
            # Print Jannuary
            if (wind_data_tif_month_1 >= 0 and wind_data_tif_month_1 < 10):
                content = "  %0.2f" % (wind_data_tif_month_1)
            elif (wind_data_tif_month_1 >= 10 and wind_data_tif_month_1 < 100):
                content = " %0.2f" % (wind_data_tif_month_1)
            elif (wind_data_tif_month_1 >= 100 and wind_data_tif_month_1 < 1000):
                content = "%0.2f" % (wind_data_tif_month_1)
            else:
                content = "  0.00"

             # Print February
            if (wind_data_tif_month_2 >= 0 and wind_data_tif_month_2 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_2)
            elif (wind_data_tif_month_2 >= 10 and wind_data_tif_month_2 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_2)
            elif (wind_data_tif_month_2 >= 100 and wind_data_tif_month_2 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_2)
            else:
                content = content + "  0.00"
            
            # Print March
            if (wind_data_tif_month_3 >= 0 and wind_data_tif_month_3 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_3)
            elif (wind_data_tif_month_3 >= 10 and wind_data_tif_month_3 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_3)
            elif (wind_data_tif_month_3 >= 100 and wind_data_tif_month_3 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_3)
            else:
                content = content + "  0.00"
            
            # Print April
            if (wind_data_tif_month_4 >= 0 and wind_data_tif_month_4 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_4)
            elif (wind_data_tif_month_4 >= 10 and wind_data_tif_month_4 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_4)
            elif (wind_data_tif_month_4 >= 100 and wind_data_tif_month_4 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_4)
            else:
                content = content + "  0.00"
            
            # Print May
            if (wind_data_tif_month_5 >= 0 and wind_data_tif_month_5 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_5)
            elif (wind_data_tif_month_5 >= 10 and wind_data_tif_month_5 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_5)
            elif (wind_data_tif_month_5 >= 100 and wind_data_tif_month_5 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_5)
            else:
                content = content + "  0.00"
            
            # Print June
            if (wind_data_tif_month_6 >= 0 and wind_data_tif_month_6 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_6)
            elif (wind_data_tif_month_6 >= 10 and wind_data_tif_month_6 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_6)
            elif (wind_data_tif_month_6 >= 100 and wind_data_tif_month_6 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_6)
            else:
                content = content + "  0.00"
            
            # Print July
            if (wind_data_tif_month_7 >= 0 and wind_data_tif_month_7 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_7)
            elif (wind_data_tif_month_7 >= 10 and wind_data_tif_month_7 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_7)
            elif (wind_data_tif_month_7 >= 100 and wind_data_tif_month_7 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_7)
            else:
                content = content + "  0.00"
            
            # Print August
            if (wind_data_tif_month_8 >= 0 and wind_data_tif_month_8 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_8)
            elif (wind_data_tif_month_8 >= 10 and wind_data_tif_month_8 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_8)
            elif (wind_data_tif_month_8 >= 100 and wind_data_tif_month_8 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_8)
            else:
                content = content + "  0.00"
            
            # Print September
            if (wind_data_tif_month_9 >= 0 and wind_data_tif_month_9 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_9)
            elif (wind_data_tif_month_9 >= 10 and wind_data_tif_month_9 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_9)
            elif (wind_data_tif_month_9 >= 100 and wind_data_tif_month_9 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_9)
            else:
                content = content + "  0.00"
            
            # Print October
            if (wind_data_tif_month_10 >= 0 and wind_data_tif_month_10 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_10)
            elif (wind_data_tif_month_10 >= 10 and wind_data_tif_month_10 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_10)
            elif (wind_data_tif_month_10 >= 100 and wind_data_tif_month_10 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_10)
            else:
                content = content + "  0.00"
            
             # Print November
            if (wind_data_tif_month_11 >= 0 and wind_data_tif_month_11 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_11)
            elif (wind_data_tif_month_11 >= 10 and wind_data_tif_month_11 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_11)
            elif (wind_data_tif_month_11 >= 100 and wind_data_tif_month_11 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_11)
            else:
                content = content + "  0.00"
            
             # Print December
            if (wind_data_tif_month_12 >= 0 and wind_data_tif_month_12 < 10):
                content = content + "  %0.2f" % (wind_data_tif_month_12)
            elif (wind_data_tif_month_12 >= 10 and wind_data_tif_month_12 < 100):
                content = content + " %0.2f" % (wind_data_tif_month_12)
            elif (wind_data_tif_month_12 >= 100 and wind_data_tif_month_12 < 1000):
                content = content + "%0.2f" % (wind_data_tif_month_12)
            else:
                content = content + "  0.00"
                          
            data[LINE_DECIDE] = content    
             
        with open(full_path_wp1_file, 'w') as file:
            file.writelines(data)
            file.write("\n")
        return 1; 
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
        return 0;
def main():
    checkAllInputData();
    wind_data = []
    X_Coor_List = []
    Y_Coor_List = []
    WP1_File_Name_List = []
    # Read CSV File to get X and Y and 
    try:
       f = open(csv_location, "rb")
       l = UnicodeReader(f)
       l.next()
       
       for row in l:
           mx, my = float(row[2]), float(row[1])  # coord in map units
           name = row[3]
           X_Coor_List.append(mx)
           Y_Coor_List.append(my)
           WP1_File_Name_List.append(str(name))
       
       # print X_Coor_List[0]
       number_of_records = len(WP1_File_Name_List) 
       wind_data_tif_month_1 = ""
       wind_data_tif_month_2 = ""
       wind_data_tif_month_3 = ""
       wind_data_tif_month_4 = ""
       wind_data_tif_month_5 = ""
       wind_data_tif_month_6 = ""
       wind_data_tif_month_7 = ""
       wind_data_tif_month_8 = ""
       wind_data_tif_month_9 = ""
       wind_data_tif_month_10 = ""
       wind_data_tif_month_11 = ""
       wind_data_tif_month_12 = ""
       for i in range(0, number_of_records):
           print "=============================================================================="
           if (tif_structure == 0):
               mx = X_Coor_List[i]
               my = Y_Coor_List[i]
               Full_WP1_File_Path = wp1_folder + "\%s.WP1" %(WP1_File_Name_List[i])
               if (not os.path.exists(Full_WP1_File_Path)):
                   print("--ERROR : WP1 File %s doest not exited" %(WP1_File_Name_List[i]))
                   continue
               # Jannuary 
               path = tif_folder + "%s1%s%s\%s1%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_1 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 1 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_1))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # February
               path = tif_folder + "%s2%s%s\%s2%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_2 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 2 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_2))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # March
               path = tif_folder + "%s3%s%s\%s3%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_3 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 3 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_3))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # April
               path = tif_folder + "%s4%s%s\%s4%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_4 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 4 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_4))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # May
               path = tif_folder + "%s5%s%s\%s5%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_5 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 5 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_5))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # June
               path = tif_folder + "%s6%s%s\%s6%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_6 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 6 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_6))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # July
               path = tif_folder + "%s7%s%s\%s7%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_7 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 7 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_7))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # August
               path = tif_folder + "%s8%s%s\%s8%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_8 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 8 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_8))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # September
               path = tif_folder + "%s9%s%s\%s9%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_9 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 9 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_9))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # October
               path = tif_folder + "%s10%s%s\%s10%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_10 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 10 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_10))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # November
               path = tif_folder + "%s11%s%s\%s11%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_11 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 11 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_11))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               # December 
               path = tif_folder + "%s12%s%s\%s12%s%s" % (pre_name_tif_file, wind_year, post_name_tif_file, pre_name_tif_file, wind_year, post_name_tif_file)
               if (os.path.exists(path)):
                  wind_data_tif_month_12 = getRasterValue_ThanhNH(path , mx, my)
                  print "------Get Wind Data Month 12 : From %s : X = %s ; Y = %s ; Wind Data = %s" % (str(path), str(mx), str(my), str(wind_data_tif_month_12))
               else:
                  print "------Warning : File %s does not exited" % (path)
               print "---------------------------------------------------------------"
               
               result = write_wind_monthly_data_to_WP1_File(Full_WP1_File_Path, wind_data_tif_month_1, wind_data_tif_month_2, wind_data_tif_month_3, wind_data_tif_month_4, wind_data_tif_month_5, wind_data_tif_month_6, wind_data_tif_month_7, wind_data_tif_month_8, wind_data_tif_month_9, wind_data_tif_month_10, wind_data_tif_month_11, wind_data_tif_month_12)
               if (result <> 1):
                    print "------Warning : Cannot write data to File" % (WP1_File_Name_List[i])
           else:
               sys.exit("DOES NOT SUPPPORT YET")
        # result = write_wind_monthly_data_to_WP1_File(w)
    except Exception, err:
           print err
    
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
