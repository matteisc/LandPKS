# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import csv
import codecs
import struct
from support import support_SUBAREA
from osgeo import gdal, ogr
import numpy
from __builtin__ import str

TIF_FOLDER_COLLECTION = ""

mess = "Usage : python Step_1_preprocessing_SUBAREA.py -x <Longtitude X Coordinate> -y <Latitude Y coordinate> -ID <Record ID> -tif <Folder path of TIF File> -subname <Sub File name> -opsname <OPS File Name>"
if (len(sys.argv) < 10):
    print("Sorry, not enough arguments")
    sys.exit(mess)
X_COOR = 0.0
Y_COOR = 0.0
SUB_NAME_FILE = ""
OPS_NAME_FILE = ""
ID = ""
if (sys.argv[1] == '-x'):
    if (float(sys.argv[2])):
        X_COOR = float(sys.argv[2])
    else:
        sys.exit(mess)
else:
    sys.exit(mess)

if (sys.argv[3] == '-y'):
    if (float(sys.argv[4])):
        Y_COOR = float(sys.argv[4])
    else:
        sys.exit(mess)
else:
    sys.exit(mess)
    
if (sys.argv[5] == '-ID'):
    if (sys.argv[6] is not None):
        ID = sys.argv[6]
    else:
        sys.exit(mess)
else:
    sys.exit(mess)    
    
if (sys.argv[7] == '-tif'):
    if (sys.argv[8] is None):
        sys.exit(mess)
    else:
        TIF_FOLDER_COLLECTION = sys.argv[8]
else:
     sys.exit(mess)

if (sys.argv[9] == '-subname'):
    if (sys.argv[10] is not None):
        SUB_NAME_FILE = sys.argv[10]
    else:
        sys.exit(mess)
else:
    sys.exit(mess)

if (sys.argv[11] == '-opsname'):
    if (sys.argv[12] is not None):
        OPS_NAME_FILE = sys.argv[12]
    else:
        sys.exit(mess)
else:
    sys.exit(mess)
    
# define
SUB_FILE_ORIGINAL_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\7_SUBAREA_PROJECT\\Subarea_Files\\Original_Subarea_Files"
SOI_FILE_ORIGINAL_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT_REAL_TIME\\Result_HWSD\\Private\\%s\\SOL\\" %(str(ID))
DLY_FILE_ORIGINAL_PATH = "C:\\xampp\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s\\Daily_Weather_Files\\" %(str(ID))
DLY_DAT_FILE = "C:\\xampp\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Files\\Private\\%s\\DATFiles\\WDLSTCOM.DAT" %(str(ID))
PRE_SOICOM_DAT_FILE_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT_REAL_TIME\\Result_HWSD\\Private\\%s\\DAT\\" %(str(ID))
POS_SOICOM_DAT_FILE_PATH = "\\SOILCOM.DAT"
PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT_REAL_TIME\\Result_HWSD\\Private\\%s" % (str(ID)), "SIMILARITY\\%s.csv" %(str(ID)))

TIF_HWSD = 'soil_texture/HWSD_soil.tif'
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'



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
def getRasterValue_ThanhNH(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]
def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = filename
            if (file_path.endswith(".SOL")):
               file_paths.append(file_path)
    return file_paths
def main():
    try:
            sub_file_name = SUB_NAME_FILE.strip()
            full_path = os.path.join(SUB_FILE_ORIGINAL_PATH, sub_file_name)
            if (not os.path.exists(full_path)):
                sys.exit("==[Error 21] : One Sub File is Not existed" + str(full_path))
                
            #mu_global = getRasterValue(os.path.join(TIF_FOLDER_COLLECTION, TIF_HWSD), X_COOR, Y_COOR)
            soil_file_name_list = get_files_path(SOI_FILE_ORIGINAL_PATH)
            if (len(soil_file_name_list) > 1):
               surface_craking = support_SUBAREA.get_surface_craking_from_id(str(ID))
               if (surface_craking is not None and surface_craking.strip().upper() == "TRUE"):
                   count_VRe_VRd_VRk_VRy = support_SUBAREA.count_number_sol_file_in_class(soil_file_name_list)
                   if (count_VRe_VRd_VRk_VRy == 0 or count_VRe_VRd_VRk_VRy is None):
                       [soil_file_name,max_cosin] = support_SUBAREA.get_soil_file_name_closest_user_input(PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE)
                       if (max_cosin == -1 or soil_file_name is None or soil_file_name == ""):
                             soil_file_name = soil_file_name_list[0]
                       print "================================================"
                       print "===Selected SOIL FIle [1] : " + str(soil_file_name)
                       print "===Cosin [1]: " + str(max_cosin)
                       print "================================================"
                   elif (count_VRe_VRd_VRk_VRy >= 1):
                       # CAN LAM THEM CAN THAN DOAN NAY
                       soil_file_name = support_SUBAREA.get_soil_file_name_in_classes(soil_file_name_list)
                       print "================================================"
                       print "===Selected SOIL FIle  [4] : " + str(soil_file_name)
                       print "===No need cosine"
                       print "================================================"
                   else:
                       [soil_file_name,max_cosin] = support_SUBAREA.get_soil_file_name_closest_user_input(PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE)
                       if (max_cosin == -1 or soil_file_name is None or soil_file_name == ""):
                            soil_file_name = soil_file_name_list[0]
                       print "================================================"
                       print "===Selected SOIL FIle  [5] : " + str(soil_file_name)
                       print "===Cosin : [6] " + str(max_cosin)
                       print "================================================"
               else:      
                   [soil_file_name,max_cosin] = support_SUBAREA.get_soil_file_name_closest_user_input(PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE)
                   if (max_cosin == -1 or soil_file_name is None or soil_file_name == ""):
                        soil_file_name = soil_file_name_list[0]
                   print "================================================"
                   print "===Selected SOIL FIle  [2] : " + str(soil_file_name)
                   print "===Cosin : [2] " + str(max_cosin)
                   print "================================================"
            elif (len(soil_file_name_list) == 1):
                soil_file_name = soil_file_name_list[0]
                print "================================================"
                print "===Selected SOIL FIle  [3] : " + str(soil_file_name)
                print "===No need cosine"
                print "================================================"
            else:
                soil_file_name = ""
            full_path_soil = os.path.join(SOI_FILE_ORIGINAL_PATH, soil_file_name)
            if (not os.path.exists(full_path_soil)):
                sys.exit("==[Error 21] : One Selected SOIL File is Not existed " + str(full_path_soil))
                
            dly_name = getRasterValue_ThanhNH(os.path.join(TIF_FOLDER_COLLECTION, tif_slate_weather), X_COOR, Y_COOR)
            dly_name = str(dly_name) + "%s" %(".DLY")
            full_path_dly = os.path.join(DLY_FILE_ORIGINAL_PATH , dly_name)
            if (not os.path.exists(full_path_dly)):
                sys.exit("==[Error 21] : One DLY File is Not existed == " + str(full_path_dly))
            print "================================================="
            
            command = "python Step_2_main_SUBAREA_Real_Time.py -m %s -s %s %s%s -o %s -default -d %s %s -x %f -y %f -tif %s -IDapex %s" % (sub_file_name, soil_file_name, PRE_SOICOM_DAT_FILE_PATH, POS_SOICOM_DAT_FILE_PATH, OPS_NAME_FILE, dly_name, DLY_DAT_FILE,X_COOR, Y_COOR, TIF_FOLDER_COLLECTION, ID)
            print("====Command : %s" % (command))
            os.system(command)
    except Exception, err:
        print err
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
