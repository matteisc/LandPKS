# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, sys
import numpy
import time

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

# Check arguments
X_COOR = 0.0
Y_COOR = 0.0
site_file_name = ""
ID = ""
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
if (len(sys.argv) < 9):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_APEX_RUN_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")
# Input filenames
if (sys.argv[1] == '-x'):
   if (float(sys.argv[2])):
       X_COOR = float(sys.argv[2])
else:
   sys.exit("Usage : python Step_1_preprocessing_APEX_RUN_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")
if (sys.argv[3] == '-y'):
     if (float(sys.argv[4])):
       Y_COOR = float(sys.argv[4])
else:
   sys.exit("Usage : python Step_1_preprocessing_APEX_RUN_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")

if (sys.argv[5] == '-id'):
   ID = sys.argv[6]
else:
   sys.exit("Usage : python Step_1_preprocessing_APEX_RUN_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")

if (sys.argv[7] == '-tif'):
   src_dir = sys.argv[8]
else:
   sys.exit("Usage : python Step_1_preprocessing_APEX_RUN_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")

#Define   
APEX_RUN_DAT_FILE_NAME = "APEXRUN.DAT"
full_path = os.getcwd() + "\\"
FULL_PATH_DAT_FILE_WPM1MO = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/DATFiles/WPM1MO.DAT" %(str(ID))

def checkAndCreateFolder():
    directory = full_path + "\APEX_RUN\Private\%s" %(str(ID))
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\%s" % ("DAT_Files")
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
def create_APEX_Run_File_Only_One_Row(ID, site_index, wp1_index, wind_index, subarea_index):
    try:
        fo = open(os.path.join("APEX_RUN/Private/%s/DAT_Files/%s" % (str(ID),APEX_RUN_DAT_FILE_NAME)), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write DATA to File %s" % (str(APEX_RUN_DAT_FILE_NAME)))
        print range(0,len(subarea_index))
        for j in range(0,len(subarea_index)):
            # Line 1
            ####Field ID
            if (len(ID) > 16):
                ID = ID[:16]
            space_number = 16 - len(ID)
            if (j==0):
              content = ID + "M"
            elif (j==1):
              content = ID + "G"
            for i in range(1, space_number):
                content = content + " "
            ####Field Site File Index 
            if (len(str(site_index)) > 7):
                sys.exit("===[Error] : Data is Wrong")
            space_number = 7 - len(str(site_index))
            content = content + str(site_index)
            for i in range(0, space_number):
                content = content + " "
            ####Field WP1 Index 
            if (len(str(wp1_index)) > 7):
                sys.exit("===[Error] : Data is Wrong")
            space_number = 7 - len(str(wp1_index))
            content = content + str(wp1_index)
            for i in range(0, space_number):
                content = content + " "
             ####Field Wind Index 
            if (len(str(wind_index)) > 7):
                sys.exit("===[Error] : Data is Wrong")
            space_number = 7 - len(str(wind_index))
            content = content + str(wind_index)
            for i in range(0, space_number):
                content = content + " "
            
            ####Field Subarea Index 
           
            if (len(str(subarea_index[j])) > 7):
                sys.exit("===[Error] : Data is Wrong")
            space_number = 7 - len(str(subarea_index[j]))
            content = content + str(subarea_index[j])
            for i in range(0, space_number):
                content = content + " "
                
            ####Field 6
            content = content + "0      " 
            ####Field 7
            content = content + "0\n"
            fo.write(content)
        content = "XXXXXXXXXX      0      0      0      0      0      0"
        fo.write(content)
        fo.write("\n")
        fo.close()
    except Exception, err:
        fo.close()
        sys.exit("Error : %s" % (err))
    finally:
        print("Done")
        fo.close()
def getRasterValue_ThanhNguyen_TIF(src_file, mx, my):
    src_ds = gdal.Open(src_file) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]
def get_wp1_index(wp1_name, dat_file_path):
    dat_file_path = os.path.join(dat_file_path)
    if (not os.path.exists(dat_file_path)):
        return 0
    with open(dat_file_path, 'r') as file:
        data = file.readlines()
    for i in range(0, len(data)):
        line = data[i]
        str_index_wp1 = line[:5]
        str_name_wp1 = line[5:17]
        #print ("%s    %s" % (str_index_wp1, str_name_wp1))
        if (str_name_wp1.strip() == wp1_name.strip()):
            int_wp1_index = int(str_index_wp1)
            return int_wp1_index
    return 0   
def main():
   try:
       print "================================================="
       wp1_name = getRasterValue_ThanhNguyen_TIF(src_dir + tif_slate_weather, X_COOR, Y_COOR)
       print "X = " + str(X_COOR)
       print "Y = " + str(Y_COOR)
       print "WP1 File name = " + str(wp1_name)
       wp1_index = get_wp1_index(str(wp1_name) + ".WP1", FULL_PATH_DAT_FILE_WPM1MO)
       if (wp1_index == 0):
           sys.exit("===[Error] : Cannot find WP1 file nam in WPM1MO.DAT File")
       print("-PREPROCESSING : Create Folders--")
       checkAndCreateFolder()
       print("-Create File and Folder already")
       print("-Create APEXRUN.DAT File")
       subarea_indexes = [1,2]
       create_APEX_Run_File_Only_One_Row(ID, 1, wp1_index, 1, subarea_indexes)
       print("-APEX RUN File is created already")
   except Exception, err:
       sys.exit(err)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
