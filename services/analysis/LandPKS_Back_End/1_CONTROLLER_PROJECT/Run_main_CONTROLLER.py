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

from support import support_CONTROLLER
from __builtin__ import int

tif_countries = 'countryrastermap/Countries_Raster.tif'

AVE_ANNUAL_DATA = "AVE ANNUAL DATA"
AVE_ANNUAL_CROP_YLD_DATA = "-----AVE ANNUAL CROP YLD DATA"
# Check arguments
X_Coor = 0.00
Y_Coor = 0.00
ID = ""
RECORD_NAME = ""
ACTION_FLAG = 1


if (len(sys.argv) <> 9 and len(sys.argv) <> 2):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python main_CONTROLLER.py -x <X Coordinate> -y <Y Coordinate> -ID <Record ID>")
else:
    if (sys.argv[1] == '-x'):
        if (float(sys.argv[2])):
            X_Coor = float(sys.argv[2])
        else:
            sys.exit("====[Error] : Error in X")
        
        if (sys.argv[3] == '-y'):
            if (float(sys.argv[4])):
               Y_Coor = float(sys.argv[4])
            else:
               sys.exit("====[Error] : Error in Y")
        else:
            sys.exit("====[Error] : Error in Y")
        
        if (sys.argv[5] == '-ID'):
            if (sys.argv[6] is not None):
               ID = str(sys.argv[6])
            else:
               sys.exit("====[Error] : Error in Folder")
        else:
            sys.exit("====[Error] : Error in Folder")
            
        if (sys.argv[7] == '-name'):
            if (sys.argv[8] is not None):
               RECORD_NAME = str(sys.argv[8])
            else:
               sys.exit("====[Error] : Error in Folder")
        else:
            sys.exit("====[Error] : Error in Folder") 
    elif (sys.argv[1] == '-rm_real_time'):
        ACTION_FLAG = 0
    elif (sys.argv[1] == '-rm_all'):
        ACTION_FLAG = 2
    else:
        sys.exit("====[Error] : Error in X")
    
    
        
        
STORE_MODEL_APPLICATION_FOLDER_PATH = "C:/xampp/htdocs/APEX/Python_APEX/0_APEX_RUNTIME_MODEL/STORE_MODEL/"
APEX_MODEL_FILE_NAME = "Temple_3.exe"
APEX_MODEL_CONFIG_FILE = "schema.ini"

STORE_STATIC_INPUT_FILE_FOLDER_PATH = "C:/xampp/htdocs/APEX/Python_APEX/0_APEX_RUNTIME_MODEL/STORE_STATIC_FILES/"
NUMBER_STATIC_INPUT_FILES = 15

REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST = "C:/xampp/htdocs/APEX/Python_APEX/0_APEX_RUNTIME_MODEL/Private/%s" % (str(ID))


WEATHER_DLY_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/Daily_Weather_Files/" % (str(ID))
WEATHER_WP1_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/Complete_WP1_Files/" % (str(ID))
WEATHER_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/DATFiles/" % (str(ID))
SOL_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private/%s/DAT/" % (str(ID))
SOL_SOL_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private/%s/SOL/" % (str(ID))
SOL_DAT_FILES_FOLDER_REAL_TIME = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private/%s/DAT/" % (str(ID))
SOL_SOL_FILES_FOLDER_REAL_TIME = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private/%s/SOL/" % (str(ID))
OPS_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/6_OPERATIONS_PROJECT/Operation_Files/DAT_Files/" 
OPS_OPS_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/6_OPERATIONS_PROJECT/Operation_Files/Operation_Files/" 
SUB_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/7_SUBAREA_PROJECT_REAL_TIME/Subarea_Files/Private/%s/DAT_Files/" % (str(ID))
SUB_SUB_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/7_SUBAREA_PROJECT_REAL_TIME/Subarea_Files/Private/%s/Modified_Subarea_Files/" % (str(ID))
SITE_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/Site_Files/Private/%s/DAT" % (str(ID))
SITE_SIT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/Site_Files/Private/%s/SITE" % (str(ID))
APEX_RUN_DAT_FILES_FOLDER = "C:/xampp/htdocs/APEX/Python_APEX/9_APEX_RUN/APEX_RUN/Private/%s/DAT_Files" % (str(ID))

APEX_OUTPUT_DATA_FILE_MAIZE = REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST + "/%sM.OUT" % (str(ID))
APEX_OUTPUT_DATA_FILE_GLASS = REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST + "/%sG.OUT" % (str(ID))
# Manage arguments
# Function
def copy_dly_file(dlyfile_path, to_path):
    shutil.copy2(dlyfile_path, to_path)
def loop_and_copy(directory):  
    for root, directories, files in os.walk(directory):
        for filename in files:
            print "copy " + str(os.path.join(directory, filename)) + " to " + REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST
            copy_dly_file(os.path.join(directory, filename), REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST)
def delete_file(path):
    try:
       os.remove(path)
    except Exception , err:
       print err
       pass
def loop_and_delete(directory):  
    for root, directories, files in os.walk(directory):
        for filename in files:
            if (not filename.endswith(".OUT")):
               delete_file(os.path.join(directory, filename))
def checkFolderAndCreateEnvironment():
    if not os.path.exists(STORE_MODEL_APPLICATION_FOLDER_PATH):
        sys.exit("===[Error 1] : APEX Model Folder does not exist")     
    if not os.path.exists(os.path.join(STORE_MODEL_APPLICATION_FOLDER_PATH, APEX_MODEL_FILE_NAME)):
        sys.exit("===[Error 2] : APEX Model File does not exist")    
    if not os.path.exists(os.path.join(STORE_MODEL_APPLICATION_FOLDER_PATH, APEX_MODEL_CONFIG_FILE)):
        sys.exit("===[Error 3] : APEX Model Configure does not exist")
    if (not os.path.exists(REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST)):
        os.makedirs(REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST)
    # Copyt data
    loop_and_copy(STORE_MODEL_APPLICATION_FOLDER_PATH) 
    loop_and_copy(STORE_STATIC_INPUT_FILE_FOLDER_PATH)
def copyInputFile():
    # Copy WEATHER FILE
    if (os.path.exists(WEATHER_DLY_FILES_FOLDER)):
        loop_and_copy(WEATHER_DLY_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy WP1 File
    if (os.path.exists(WEATHER_WP1_FILES_FOLDER)):
        loop_and_copy(WEATHER_WP1_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy DAT File
    if (os.path.exists(WEATHER_DAT_FILES_FOLDER)):
        loop_and_copy(WEATHER_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy SOILCOM.DAT  
    if (os.path.exists(SOL_DAT_FILES_FOLDER)):
        loop_and_copy(SOL_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy Sol File
    if (os.path.exists(SOL_SOL_FILES_FOLDER)):
        loop_and_copy(SOL_SOL_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
        
    # Copy OPSCCOM.DAT  
    if (os.path.exists(OPS_DAT_FILES_FOLDER)):
        loop_and_copy(OPS_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy Sol File
    if (os.path.exists(OPS_OPS_FILES_FOLDER)):
        loop_and_copy(OPS_OPS_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy SUBACOM.DAT  
    if (os.path.exists(SUB_DAT_FILES_FOLDER)):
        loop_and_copy(SUB_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy SUB File
    if (os.path.exists(SUB_SUB_FILES_FOLDER)):
        loop_and_copy(SUB_SUB_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
     # Copy SITECOM.DAT  
    if (os.path.exists(SITE_DAT_FILES_FOLDER)):
        loop_and_copy(SITE_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
    # Copy SIT File
    if (os.path.exists(SITE_SIT_FILES_FOLDER)):
        loop_and_copy(SITE_SIT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
        
    if (os.path.exists(APEX_RUN_DAT_FILES_FOLDER)):
        loop_and_copy(APEX_RUN_DAT_FILES_FOLDER)
    else:
        sys.exit("===[Error 202] : System has not enough input files")
def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = filename
            file_paths.append(file_path)
    return file_paths

def runningModel():
    apex_application_path = REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST + "\%s" % (APEX_MODEL_FILE_NAME)
    # subprocess.call(['C:\\Users\\thnguyen\\Desktop\\WISE-SOL-PROJECT\\EPIC_Weather_Application\\WXPM3020.exe'])
    os.system("cd .. && cd 0_APEX_RUNTIME_MODEL && cd Private && cd %s && %s" % (str(ID), APEX_MODEL_FILE_NAME))
def deleteAllFolderAndFiles():
    loop_and_delete(REAL_FOLDER_APEX_RUNTIME_PER_EACH_REQUEST)
def clean_all_data_deeply():
    try:
       print("8--Delete All Product DAT and SOL From Project 3_WISE_SOL_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/DATFiles"
       shutil.rmtree(path)
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/SOLFiles"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:
       print("9--Delete All Input and Output From ROSETTA in Project 3_WISE_SOL_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Rosetta_Model_Application/Input"
       shutil.rmtree(path)
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Rosetta_Model_Application/Output"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
def clean_all_data_in_server():
    try:
       print("1--Delete all input files created in 2_WEATHER_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:    
       print("2--Delete all input files created in 3_WISE_SOL_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:    
       print("2--Delete all input files created in 3_WISE_SOL_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Result_HWSD/Private"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:
       print("3--Delete all input files created in 6_OPERATIONS_PROJECT")
       path = "C:/xampp/htdocs/APEX/Python_APEX/6_OPERATIONS_PROJECT/Operation_Files/DAT_Files"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:
       print("4--Delete all input files created in 7_SUBAREA_PROJECT_REAL_TIME")
       path = "C:/xampp/htdocs/APEX/Python_APEX/7_SUBAREA_PROJECT_REAL_TIME/Subarea_Files/Private/"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
    try:
       print("5--Delete all input files created in 8_SITE_PROJECT")
       path = "C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/Site_Files/Private/"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:
       print("6--Delete all input files created in 9_APEX_RUN")
       path = "C:/xampp/htdocs/APEX/Python_APEX/9_APEX_RUN/APEX_RUN/Private/"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
   
    try:   
       print("7--Delete all input files created in 0_APEX_RUNTIME_MODEL")
       path = "C:/xampp/htdocs/APEX/Python_APEX/0_APEX_RUNTIME_MODEL/Private/"
       shutil.rmtree(path)
    except Exception, err:
       print err
       pass
def checking_key(key, value):
    key = key.strip()
    key = key.upper()
    if (key == value):
        return 1
    else:
        return 0
def find_data(data, key):
    for i in range(5000, len(data) - 2):
        line = data[i]
        if (checking_key(line, key) == 1 or checking_key(line[:32], key) == 1):
            return data[i + 3]
    return None
        
def get_data_from_apex_ouput_file(APEX_OUTPUT_FILE, index_sa, index_corn, type):
    apex_output = []
    with open(APEX_OUTPUT_FILE, 'r') as file:
        data = file.readlines()
    # Get Soil Erosion
    if (index_sa > len(data)) :
        index_sa = 7000
        
    line_checking = data[index_sa - 4]
    if (checking_key(line_checking, "AVE ANNUAL DATA") == 1):
       print "===[Good] : Find line contain data Y fast => Read immediately" 
       line_7650 = data[index_sa - 1]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (index_sa)
       line_7650 = find_data(data, "AVE ANNUAL DATA")
       if (line_7650 is None):
           sys.exit("====[Error] : Output error")  
           
    line_7650 = line_7650.strip()
    line_7650 = line_7650.replace("         ", " ")
    line_7650 = line_7650.replace("        ", " ")
    line_7650 = line_7650.replace("       ", " ")
    line_7650 = line_7650.replace("      ", " ")
    line_7650 = line_7650.replace("     ", " ")
    line_7650 = line_7650.replace("    ", " ")
    line_7650 = line_7650.replace("   ", " ")
    line_7650 = line_7650.replace("  ", " ")
    
    data_line_7650 = []
    data_line_7650 = line_7650.split(" ")
    if (len(data_line_7650) == 23):
        apex_data_y = data_line_7650[10]
    else:
        print("====[WARNING] : There is problem at Line SA in Output File")
        apex_data_y = 0.0
  
    # Get Productivity
    if (index_corn > len(data)):
        index_corn = 7000
    line_checking = data[index_corn - 4]
    if (checking_key(line_checking[:32], "-----AVE ANNUAL CROP YLD DATA") == 1):
        print "===[Good] : Find line contain data YLDG BIOM fast => Read immediately" 
        line_7591 = data[index_corn - 1]
    else:
        print "===[Warning] : Line %d does not contain data => Need to loop all line" % (index_corn) 
        line_7591 = find_data(data, "-----AVE ANNUAL CROP YLD DATA")
        if (line_7591 is None):
            sys.exit("====[Error] L: Output error")  
            
            
    line_7591 = line_7591.strip()
    line_7591 = line_7591.replace("         ", " ")
    line_7591 = line_7591.replace("        ", " ")
    line_7591 = line_7591.replace("       ", " ")
    line_7591 = line_7591.replace("      ", " ")
    line_7591 = line_7591.replace("     ", " ")
    line_7591 = line_7591.replace("    ", " ")
    line_7591 = line_7591.replace("   ", " ")
    line_7591 = line_7591.replace("  ", " ")
    
    data_line_7591 = []
    data_line_7591 = line_7591.split(" ")
    
    if (len(data_line_7591) == 21):
        if (type == "MAIZE"):
            apex_data_yldg = data_line_7591[1]
            if (apex_data_yldg.endswith('/')):
                apex_data_yldg = apex_data_yldg.replace('/', '')
        elif (type == "GLASS"):
            apex_data_yldg = data_line_7591[2]
            if (apex_data_yldg.endswith('/')):
                apex_data_yldg = apex_data_yldg.replace('/', '')
        else:
            apex_data_yldg = data_line_7591[1]
            if (apex_data_yldg.endswith('/')):
                apex_data_yldg = apex_data_yldg.replace('/', '')
        
        apex_data_biom = data_line_7591[3]
        
            
    else:
        print("====[WARNING] : There is problem at Line CORN in Output File")
        apex_data_yldg = 0.0
        apex_data_biom = 0.0

    apex_output = [apex_data_y, apex_data_yldg, apex_data_biom]
    
    return apex_output
    
    
    
def save_gdal_data():
       #Insert GDAL data
       TIF_DIR = "E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"
       #--------------------------------------------------------------------------------
       tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
       slate_weather_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_slate_weather, X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------   
       country_code_data = country_identify = support_CONTROLLER.getRasterValue_ThanhNH("E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" + tif_countries, X_Coor, Y_Coor) 
       #--------------------------------------------------------------------------------
       tif_annual_precipitation = 'annual_precipitation/annual_precip.tif'
       anual_precipitation_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_annual_precipitation , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       tif_growing_degree_days = 'growing_degree_days/gdd.tif'
       gdd_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_growing_degree_days , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       tif_aridity_index = 'aridity/ai_yr.tif'
       aridity_index_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_aridity_index , X_Coor, Y_Coor)
       aridity_index_data = aridity_index_data*0.0001
       #--------------------------------------------------------------------------------
       tif_worldkgeiger_climate_zone = 'GLOBAL_LAYER/WorldKGeiger/WorldKGeiger.tif'
       worldkgeiger_climate_zone_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_worldkgeiger_climate_zone , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_fao_lgp = 'GLOBAL_LAYER/FAO_LGP/LGP.tif'
       fao_lgp_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_fao_lgp , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_MODIS_evapotrans = 'WORLD_GRID/Climate_Dataset/ETMNTS3a.tif'
       MODIS_evapotrans_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_MODIS_evapotrans , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       tif_precip_novdecjan = 'WORLD_GRID/Climate_Dataset/PX1WCL3a.tif'
       precip_novdecjan_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_novdecjan , X_Coor, Y_Coor) 
       #--------------------------------------------------------------------------------
       tif_precip_febmarapr = 'WORLD_GRID/Climate_Dataset/PX2WCL3a.tif'
       precip_febmarapr_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_febmarapr , X_Coor, Y_Coor)
       #-------------------------------------------------------------------------------- 
       tif_precip_mayjunjul = 'WORLD_GRID/Climate_Dataset/PX3WCL3a.tif'
       precip_mayjunjul_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_mayjunjul , X_Coor, Y_Coor)  
       #-------------------------------------------------------------------------------- 
       tif_precip_augsepoct = 'WORLD_GRID/Climate_Dataset/PX4WCL3a.tif'
       precip_augsepoct_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_augsepoct , X_Coor, Y_Coor) 
       #-------------------------------------------------------------------------------- 
       wind_data_1 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind12001.tif/gwind12001.tif' , X_Coor, Y_Coor) 
       wind_data_2 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind22001.tif/gwind22001.tif' , X_Coor, Y_Coor)
       wind_data_3 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind32001.tif/gwind32001.tif' , X_Coor, Y_Coor)
       wind_data_4 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind42001.tif/gwind42001.tif' , X_Coor, Y_Coor)
       wind_data_5 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind52001.tif/gwind52001.tif' , X_Coor, Y_Coor)
       wind_data_6 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind62001.tif/gwind62001.tif' , X_Coor, Y_Coor)
       wind_data_7 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind72001.tif/gwind72001.tif' , X_Coor, Y_Coor)
       wind_data_8 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind82001.tif/gwind82001.tif' , X_Coor, Y_Coor)
       wind_data_9 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind92001.tif/gwind92001.tif' , X_Coor, Y_Coor)
       wind_data_10 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind102001.tif/gwind102001.tif' , X_Coor, Y_Coor)
       wind_data_11 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind112001.tif/gwind112001.tif' , X_Coor, Y_Coor)
       wind_data_12 = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind122001.tif/gwind122001.tif' , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       tif_HWSD = 'soil_texture/HWSD_soil.tif'
       hwsd_soil_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_HWSD , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_soil_depth_gaez = 'soil_depth/depth.tif'
       soil_depth_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_soil_depth_gaez , X_Coor, Y_Coor))  #########CAI NAY LAY TAM CAI CU - CONFIRM lai voi JOSH
       #--------------------------------------------------------------------------------
       tif_soil_textclass_gaez = 'soil_texture/soil_texture.tif'
       soil_textclass_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_soil_textclass_gaez , X_Coor, Y_Coor))  #########CAI NAY LAY TAM CAI CU - CONFIRM lai voi JOSH
       #--------------------------------------------------------------------------------
       tif_soil_fert_gaez = 'GAEZ_NEW_LAYERS/GlobalSoilFertilityMap/GlobalSoilFertilityMap.tif'
       soil_fert_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_soil_fert_gaez , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_soil_workab_gaez = 'GAEZ_NEW_LAYERS/SOILWorkability/SOILWorkability.tif'
       soil_workab_gaez = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_soil_workab_gaez , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_soil_toxic_gaez = 'GAEZ_NEW_LAYERS/SoilToxicities/SoilToxicities.tif'
       soil_toxic_gaez = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_soil_toxic_gaez , X_Coor, Y_Coor))
       #--------------------------------------------------------------------------------
       tif_ELEVATION = 'elevation/elevation.tif'
       elevation_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_ELEVATION , X_Coor, Y_Coor)
       if (elevation_data == -1 or elevation_data == '-1' or elevation_data == -1.0 or elevation_data == '-1.0'):
           elevation_data = -999
       #--------------------------------------------------------------------------------
       tif_file_aspect = 'aspect/ASPECT.tif'
       aspect_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_file_aspect , X_Coor, Y_Coor)
       if (aspect_data == -1 or aspect_data == '-1' or aspect_data == -1.0 or aspect_data == '-1.0'):
           aspect_data = -999
       #--------------------------------------------------------------------------------
       topog_geolage_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/GEAISG3a.tif' , X_Coor, Y_Coor))
       if (topog_geolage_data == -1 or topog_geolage_data == '-1' or topog_geolage_data == -1.0 or topog_geolage_data == '-1.0'):
           topog_geolage_data = -999
       #--------------------------------------------------------------------------------
       topog_slope_global_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/SLPSRT3a.tif' , X_Coor, Y_Coor))
       if (topog_slope_global_data == -1 or topog_slope_global_data == '-1' or topog_slope_global_data == -1.0 or topog_slope_global_data == '-1.0'):
           topog_slope_global_data = -999
       #--------------------------------------------------------------------------------
       topog_landform_global_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/L3POBI3B.tif' , X_Coor, Y_Coor))
       if (topog_landform_global_data == -1 or topog_landform_global_data == '-1' or topog_landform_global_data == -1.0 or topog_landform_global_data == '-1.0'):
           topog_landform_global_data = -999
       #--------------------------------------------------------------------------------
       topog_topog_twi_global_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/TWISRE3a.tif' , X_Coor, Y_Coor)
       if (topog_topog_twi_global_data == -1 or topog_topog_twi_global_data == '-1' or topog_topog_twi_global_data == -1.0 or topog_topog_twi_global_data == '-1.0'):
           topog_topog_twi_global_data = -999
       topog_topog_twi_global_data = topog_topog_twi_global_data*10 + 10
       #--------------------------------------------------------------------------------
       topog_topog_topi_global_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/OPISRE3a.tif' , X_Coor, Y_Coor)
       if (topog_topog_topi_global_data == -1 or topog_topog_topi_global_data == '-1' or topog_topog_topi_global_data == -1.0 or topog_topog_topi_global_data == '-1.0'):
           topog_topog_topi_global_data = -999
       topog_topog_topi_global_data = topog_topog_topi_global_data/1000    
       #--------------------------------------------------------------------------------
       topog_topog_israd_global_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/INMSRE3a.tif' , X_Coor, Y_Coor)
       if (topog_topog_israd_global_data == -1 or topog_topog_israd_global_data == '-1' or topog_topog_israd_global_data == -1.0 or topog_topog_israd_global_data == '-1.0'):
           topog_topog_israd_global_data = -999
       topog_topog_israd_global_data = topog_topog_israd_global_data*365/8
       #--------------------------------------------------------------------------------
       tif_DEM = 'GLOBAL_GIS_DATA/AFRICA_DEM/SRTM_MOSAIC1.tif'
       dem_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_DEM , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       tif_DEM = 'WORLD_GRID/Topography_Dataset/DEMSRE3a/DEMSRE3a.tif'
       dem_world_grid_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_DEM , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       landcover_modis_2001_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G01IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2001_data == -1 or landcover_modis_2001_data == '-1' or landcover_modis_2001_data == -1.0 or landcover_modis_2001_data == '-1.0'):
           landcover_modis_2001_data = -999
       #--------------------------------------------------------------------------------
       landcover_modis_2002_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G02IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2002_data == -1 or landcover_modis_2002_data == '-1' or landcover_modis_2002_data == -1.0 or landcover_modis_2002_data == '-1.0'):
           landcover_modis_2002_data = -999
       #--------------------------------------------------------------------------------
       landcover_modis_2004_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G04IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2004_data == -1 or landcover_modis_2004_data == '-1' or landcover_modis_2004_data == -1.0 or landcover_modis_2004_data == '-1.0'):
           landcover_modis_2004_data = -999
       #--------------------------------------------------------------------------------
       landcover_modis_2010_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G10IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2010_data == -1 or landcover_modis_2010_data == '-1' or landcover_modis_2010_data == -1.0 or landcover_modis_2010_data == '-1.0'):
           landcover_modis_2010_data = -999
       #--------------------------------------------------------------------------------
       landcover_modis_2011_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G11IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2011_data == -1 or landcover_modis_2011_data == '-1' or landcover_modis_2011_data == -1.0 or landcover_modis_2011_data == '-1.0'):
           landcover_modis_2011_data = -999    
       #--------------------------------------------------------------------------------
       landcover_modis_2012_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G12IGB3a.tif' , X_Coor, Y_Coor))
       if (landcover_modis_2012_data == -1 or landcover_modis_2012_data == '-1' or landcover_modis_2012_data == -1.0 or landcover_modis_2012_data == '-1.0'):
           landcover_modis_2012_data = -999
       #--------------------------------------------------------------------------------
       landcover_cult_gaez_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GAEZ_NEW_LAYERS/Cultivated_Land/Cultivated_Land.tif' , X_Coor, Y_Coor)
       if (landcover_cult_gaez_data == -1 or landcover_cult_gaez_data == '-1' or landcover_cult_gaez_data == -1.0 or landcover_cult_gaez_data == '-1.0'):
           landcover_cult_gaez_data = -999
       #--------------------------------------------------------------------------------    
       landcover_irrcult_gaez_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GAEZ_NEW_LAYERS/irrigatedcultivatedland/irrigatedcultivatedland.tif' , X_Coor, Y_Coor)
       if (landcover_irrcult_gaez_data == -1 or landcover_irrcult_gaez_data == '-1' or landcover_irrcult_gaez_data == -1.0 or landcover_irrcult_gaez_data == '-1.0'):
           landcover_irrcult_gaez_data = -999         
       #--------------------------------------------------------------------------------    
       landcover_grass_gaez_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GAEZ_NEW_LAYERS/Grassland_woodland/Grassland_woodland.tif' , X_Coor, Y_Coor)
       if (landcover_grass_gaez_data == -1 or landcover_grass_gaez_data == '-1' or landcover_grass_gaez_data == -1.0 or landcover_grass_gaez_data == '-1.0'):
           landcover_grass_gaez_data = -999
       #--------------------------------------------------------------------------------    
       landcover_protect_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GAEZ_NEW_LAYERS/protected_area_types/protected_area_types.tif' , X_Coor, Y_Coor))
       if (landcover_protect_gaez_data == -1 or landcover_protect_gaez_data == '-1' or landcover_protect_gaez_data == -1.0 or landcover_protect_gaez_data == '-1.0'):
           landcover_protect_gaez_data = -999    
       #--------------------------------------------------------------------------------    
       landcover_agnprotect_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GAEZ_NEW_LAYERS/protectedAreasAgriculture/protectedAreasAgriculture.tif' , X_Coor, Y_Coor))
       if (landcover_agnprotect_gaez_data == -1 or landcover_agnprotect_gaez_data == '-1' or landcover_agnprotect_gaez_data == -1.0 or landcover_agnprotect_gaez_data == '-1.0'):
           landcover_agnprotect_gaez_data = -999
       #--------------------------------------------------------------------------------    
       vegind_modis_evi_m_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/EVMMOD3a.tif' , X_Coor, Y_Coor)
       if (vegind_modis_evi_m_data == -1 or vegind_modis_evi_m_data == '-1' or vegind_modis_evi_m_data == -1.0 or vegind_modis_evi_m_data == '-1.0'):
           vegind_modis_evi_m_data = -999    
       #--------------------------------------------------------------------------------    
       vegind_modis_evi_sd_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/EVSMOD3a.tif' , X_Coor, Y_Coor)
       if (vegind_modis_evi_sd_data == -1 or vegind_modis_evi_sd_data == '-1' or vegind_modis_evi_sd_data == -1.0 or vegind_modis_evi_sd_data == '-1.0'):
           vegind_modis_evi_sd_data = -999      
       #--------------------------------------------------------------------------------    
       vegind_modis_lai_m_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/LAMMOD3a.tif' , X_Coor, Y_Coor)
       if (vegind_modis_lai_m_data == -1 or vegind_modis_lai_m_data == '-1' or vegind_modis_lai_m_data == -1.0 or vegind_modis_lai_m_data == '-1.0'):
           vegind_modis_lai_m_data = -999 
       #--------------------------------------------------------------------------------    
       vegind_modis_lai_sd_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/LASMOD3a.tif' , X_Coor, Y_Coor)
       if (vegind_modis_lai_sd_data == -1 or vegind_modis_lai_sd_data == '-1' or vegind_modis_lai_sd_data == -1.0 or vegind_modis_lai_sd_data == '-1.0'):
           vegind_modis_lai_sd_data = -999    
       #--------------------------------------------------------------------------------    
       manage_cerealsuit_low_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_LAYER/CEREAL_SUITABILITY_INDEX/LOWINPUT_RC/LowInput_rainfedC.tif' , X_Coor, Y_Coor))
       if (manage_cerealsuit_low_gaez_data == -1 or manage_cerealsuit_low_gaez_data == '-1' or manage_cerealsuit_low_gaez_data == -1.0 or manage_cerealsuit_low_gaez_data == '-1.0'):
           manage_cerealsuit_low_gaez_data = -999    
       #--------------------------------------------------------------------------------    
       manage_cerealsuit_hight_gaez_data = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_LAYER/CEREAL_SUITABILITY_INDEX/HIGHINPUT_C/HighInput_cer.tif' , X_Coor, Y_Coor))
       if (manage_cerealsuit_hight_gaez_data == -1 or manage_cerealsuit_hight_gaez_data == '-1' or manage_cerealsuit_hight_gaez_data == -1.0 or manage_cerealsuit_hight_gaez_data == '-1.0'):
           manage_cerealsuit_hight_gaez_data = -999
       #--------------------------------------------------------------------------------    
       pop_density_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Population_Density/PDMGPW1a.tif' , X_Coor, Y_Coor)
       if (pop_density_data == -1 or pop_density_data == '-1' or pop_density_data == -1.0 or pop_density_data == '-1.0'):
           pop_density_data = -999
           
       #--------------------------------------------------------------------------------    
       afsis_topog_dem_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_GIS_DATA/AFRICA_DEM/SRTM_MOSAIC1.tif' , X_Coor, Y_Coor)
       if (afsis_topog_dem_data == -1 or afsis_topog_dem_data == '-1' or afsis_topog_dem_data == -1.0 or afsis_topog_dem_data == '-1.0'):
           afsis_topog_dem_data = -999
       #--------------------------------------------------------------------------------    
       afsis_topog_twi_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_GIS_DATA/AFRICA_SIS_TWI/Afsis.tif' , X_Coor, Y_Coor)
       if (afsis_topog_twi_data == -1 or afsis_topog_twi_data == '-1' or afsis_topog_twi_data == -1.0 or afsis_topog_twi_data == '-1.0'):
           afsis_topog_twi_data = -999
       #--------------------------------------------------------------------------------    
       afsis_topog_sca_data = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_GIS_DATA/AFRICA_SIS_SCA_MOSAIC/AFSIS_SCA.tif' , X_Coor, Y_Coor)
       if (afsis_topog_sca_data == -1 or afsis_topog_sca_data == '-1' or afsis_topog_sca_data == -1.0 or afsis_topog_sca_data == '-1.0'):
           afsis_topog_sca_data = -999
       #--------------------------------------------------------------------------------    
       landcover_glc30m_africa_mosaic = int(support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + 'GLOBAL_GIS_DATA/AFRICA_GLC30m_AfricaMosaic_GCS/Africa_GLC30m.tif' , X_Coor, Y_Coor))
       if (landcover_glc30m_africa_mosaic == -1 or landcover_glc30m_africa_mosaic == '-1' or landcover_glc30m_africa_mosaic == -1.0 or landcover_glc30m_africa_mosaic == '-1.0'):
           landcover_glc30m_africa_mosaic = -999
                          
       #support_CONTROLLER.insert_gdal_data_to_store( slate_weather_data, hwsd_soil_texture_data,aspect_data, dem_data, slope_data, country_code_data, elevation_data, soil_depth_data,wind_data_1, wind_data_2, wind_data_3, wind_data_4, wind_data_5, wind_data_6, wind_data_7,wind_data_8, wind_data_9, wind_data_10, wind_data_11, wind_data_12,anual_precipotation_data,worldkgeiger_climate_zone_data,fao_lgp_data,geaisga_data,slope_map_world_grid_data,physiographic_landform_units_world_grid_data,mean_potential_incoming_solar_radiation_world_grid_data,twiser3a_saga_wetness_index_world_grid_data,opisre3a_saga_openess_index_world_grid_data)
       support_CONTROLLER.insert_gdal_data_to_store(ID,RECORD_NAME, Y_Coor, X_Coor, country_code_data, slate_weather_data,anual_precipitation_data,gdd_data,aridity_index_data ,worldkgeiger_climate_zone_data,fao_lgp_data,
                                                    MODIS_evapotrans_data, precip_novdecjan_data,precip_febmarapr_data,precip_mayjunjul_data,precip_augsepoct_data,wind_data_1,wind_data_2,wind_data_3,wind_data_4,wind_data_5,wind_data_6,wind_data_7,wind_data_8,wind_data_9,
                                                    wind_data_10,wind_data_11,wind_data_12,hwsd_soil_data,soil_depth_gaez_data,soil_textclass_gaez_data,soil_fert_gaez_data,soil_workab_gaez,soil_toxic_gaez,
                                                    elevation_data,aspect_data,topog_geolage_data,dem_world_grid_data,dem_data,topog_slope_global_data,topog_landform_global_data,topog_topog_twi_global_data,topog_topog_topi_global_data,
                                                    topog_topog_israd_global_data,landcover_modis_2001_data,landcover_modis_2002_data,landcover_modis_2004_data,landcover_modis_2010_data,landcover_modis_2011_data,
                                                    landcover_modis_2012_data,landcover_cult_gaez_data,landcover_irrcult_gaez_data,landcover_grass_gaez_data,landcover_protect_gaez_data,landcover_agnprotect_gaez_data,
                                                    vegind_modis_evi_m_data,vegind_modis_evi_sd_data,vegind_modis_lai_m_data,vegind_modis_lai_sd_data,manage_cerealsuit_low_gaez_data,manage_cerealsuit_hight_gaez_data,
                                                    pop_density_data,afsis_topog_dem_data,afsis_topog_twi_data,afsis_topog_sca_data,landcover_glc30m_africa_mosaic)    
       
       
       
       #--------------------------------------------------------------------------------
       if (country_code_data == 209 or country_code_data == '209'):
          country_name= "KENYA"  
          tif_slope_percentage = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_slope/Kenya_slope.tif'
          tif_slope_reclassified = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_reclassified_slope/KenyaslopeRe.tif'
          tif_dem = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_dem/kenyademwgs1.tif'
          tif_plane_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_plancurv/kenyaplancurv.tif'
          tif_profile_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_profilecurv/kenyaprofcurv.tif'
          tif_aspect = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_aspect/kenyaAspect.tif'
          tif_curvature = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_curvature/kenyacurv.tif'  
       elif (country_code_data == 228 or str(country_code_data) == '228'): 
          country_name= "NAMIBIA" 
          tif_slope_percentage = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope/NamSlopewgs.tif'
          tif_slope_reclassified = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope_Reclassified/NamSlopeReclass.tif'
          tif_dem = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_DEM/NamDEMwgs.tif'
          tif_plane_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Plan_Curvature/NAM_curvPLANWGS.tif'
          tif_profile_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Profile_Curvature/NamProfCurvaturewgs.tif'
          tif_aspect = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_aspect/kenyaAspect.tif'
          tif_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Curvature/NAM_curvWGS.tif' 
       else:
          country_name= "UN-KNOWN" 
          tif_slope_percentage = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope/NamSlopewgs.tif'
          tif_slope_reclassified = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Slope_Reclassified/NamSlopeReclass.tif'
          tif_dem = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_DEM/NamDEMwgs.tif'
          tif_plane_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Plan_Curvature/NAM_curvPLANWGS.tif'
          tif_profile_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Profile_Curvature/NamProfCurvaturewgs.tif'
          tif_aspect = 'COUNTRY_GIS_DATA/KENYA_GIS_DATA/kenya_wgs84/kenya_aspect/kenyaAspect.tif'
          tif_curvature = 'COUNTRY_GIS_DATA/NAMIBIA_GIS_DATA/Namibia_WGS1984/Namibia_Curvature/NAM_curvWGS.tif'    
       #--------------------------------------------------------------------------------
       country_slope_percentage = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_slope_percentage , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_slope_reclassified = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_slope_reclassified , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_dem = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR + tif_dem , X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_plane_curvature = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR +  tif_plane_curvature, X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_profile_curvature = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR +  tif_profile_curvature, X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_aspect = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR +  tif_aspect, X_Coor, Y_Coor)
       #--------------------------------------------------------------------------------
       country_curvature = support_CONTROLLER.getRasterValue_ThanhNH_Float(TIF_DIR +  tif_curvature, X_Coor, Y_Coor)
       
       support_CONTROLLER.insert_gdal_data_country_level(ID,RECORD_NAME, Y_Coor, X_Coor, country_code_data,country_name,country_slope_percentage,country_slope_reclassified,country_plane_curvature,country_profile_curvature,
                                                         country_curvature,country_dem,country_aspect)
       
       
    
def main():
    if (ACTION_FLAG == 1):
       country_identify = support_CONTROLLER.getRasterValue_ThanhNH("E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" + tif_countries, X_Coor, Y_Coor)
       print "Decide contry " + str(country_identify)
       if (country_identify != 209 and country_identify != 228 and country_identify != 223 and country_identify != 205 and str(country_identify) != "209" and str(country_identify) != "228" and str(country_identify) != "223" and str(country_identify) != "205"):
             ##########INSERT GDAL DATA########################
             save_gdal_data()    
             ##################################################
             ########AWC PROJECT###############################
             model_path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Rosetta_Model_Application/Rosetta"
             os.system("cd C:/xampp/htdocs/APEX/Python_APEX/12_LANDPKS_AWC_PROJECT/ && python Run_main_AWC.py -run -x %f -y %f -model C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/Rosetta_Model_Application/Rosetta -ID %s" % (X_Coor, Y_Coor, ID))
             ##################################################
             ########CLIMATE PROJECT###############################
             os.system("cd C:/xampp/htdocs/APEX/Python_APEX/14_CLIMATE_SUMMARY_PROJECT/ && python Run_main_Climate_Summary.py -run -x %f -y %f -name %s -ID %s -tif %s" % (X_Coor, Y_Coor, RECORD_NAME ,ID, "E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"))
             #######ISRIC SIMILARITY PROJECT##################
             print "ERROR[100]:LOCATION_IS_NOT_SUPPORTED"
             sys.exit() 
       
       ##########INSERT GDAL DATA########################
       save_gdal_data()    
       ##################################################
       ########AWC PROJECT###############################
       model_path = "C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT/Rosetta_Model_Application/Rosetta"
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/12_LANDPKS_AWC_PROJECT/ && python Run_main_AWC.py -run -x %f -y %f -model C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT/Rosetta_Model_Application/Rosetta -ID %s" % (X_Coor, Y_Coor, ID))
       ##################################################
       ########CLIMATE PROJECT##########################
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/14_CLIMATE_SUMMARY_PROJECT/ && python Run_main_Climate_Summary.py -run -x %f -y %f -name %s -ID %s -tif %s" % (X_Coor, Y_Coor, RECORD_NAME ,ID, "E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"))
       ########ISRIC SIMILARITY PROJECT#################
       
       
       print("-PREPROCESSING 1: Create Folders Copy All Static Files to Runtime Folder--")
       checkFolderAndCreateEnvironment()
       print("-PRERPOCESSING 2: Run Script Python")
       if (not os.path.exists(os.path.join(OPS_DAT_FILES_FOLDER, "OPSCCOM.DAT"))):
          os.system("cd C:/xampp/htdocs/APEX/Python_APEX/6_OPERATIONS_PROJECT/ && python main_OPERATION.py -f \Operation_Files\Operation_Files")
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/ && python Run_All_WEATHER.py -x %f -y %f -ID %s" % (X_Coor, Y_Coor, ID))
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/3_WISE_SOL_PROJECT_REAL_TIME/ && python Run_All_HWSD.py -x %f -y %f -ID %s" % (X_Coor, Y_Coor, ID))
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/ && python Run_All_SITE.py -x %f -y %f -ID %s" % (X_Coor, Y_Coor, ID))
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/7_SUBAREA_PROJECT_REAL_TIME/ && python Run_All_SUBAREA.py -x %f -y %f -ID %s" % (X_Coor, Y_Coor, ID))
       os.system("cd C:/xampp/htdocs/APEX/Python_APEX/9_APEX_RUN/ && python Run_All_APEX_RUN.py -x %f -y %f -ID %s" % (X_Coor, Y_Coor, ID))
       print("PREPROCESSING 3: Copy input files to APEX RUNTIME")
       copyInputFile()
       print("PROCESSING : RUN APEX MODEL")
       runningModel()
       print("POST-PROCESSING 1 : Delete not neccessary files")
       deleteAllFolderAndFiles()
       print("POST-PROCESSING 2 : Read APEX")
       output_apex_data = []
       apex_outout_maize = [0.0, 0.0, 0.0]
       apex_outout_glass = [0.0, 0.0, 0.0]
       if (country_identify == 209 or country_identify == "209"):  # Kenya
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_MAIZE)):
              apex_outout_maize = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_MAIZE, 7650, 7591, "MAIZE")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_MAIZE))
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_GLASS)):
              apex_outout_glass = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_GLASS, 7225, 7166, "GLASS")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_GLASS)) 
       elif (country_identify == 228 or str(country_identify) == '228'):  # Namibia
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_MAIZE)):
              apex_outout_maize = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_MAIZE, 7707, 7648, "MAIZE")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_MAIZE))
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_GLASS)):
              apex_outout_glass = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_GLASS, 7223, 7164, "GLASS")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_GLASS))
       elif (country_identify == 223 or str(country_identify) == '223'):  # Angola
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_MAIZE)):
              apex_outout_maize = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_MAIZE, 7707, 7648, "MAIZE")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_MAIZE))
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_GLASS)):
              apex_outout_glass = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_GLASS, 7223, 7164, "GLASS")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_GLASS))
       elif (country_identify == 205 or str(country_identify) == '205'):  # Boswana
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_MAIZE)):
              apex_outout_maize = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_MAIZE, 7707, 7648, "MAIZE")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_MAIZE))
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_GLASS)):
              apex_outout_glass = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_GLASS, 7223, 7164, "GLASS")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_GLASS))
       else:
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_MAIZE)):
              apex_outout_maize = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_MAIZE, 7707, 7648, "MAIZE")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_MAIZE))
           if (os.path.exists(APEX_OUTPUT_DATA_FILE_GLASS)):
              apex_outout_glass = get_data_from_apex_ouput_file(APEX_OUTPUT_DATA_FILE_GLASS, 7223, 7164, "GLASS")
           else:
               sys.exit("===[Error] : File %s does not exited" % (APEX_OUTPUT_DATA_FILE_GLASS))              
       # print apex_outout_maize
       
       print("==================[RELATIVE CALCULATION]===============================")
       print("====New Record data MAIZE: Y = " + str(apex_outout_maize[0]) + " ; YLDG = " + str(apex_outout_maize[1]) + " ; BIOM = " + str(apex_outout_maize[2]))
       print("====New Record data GLASS: Y = " + str(apex_outout_glass[0]) + " ; YLDG = " + str(apex_outout_glass[1]) + " ; BIOM = " + str(apex_outout_glass[2]))
       print("=======================================================================")
       
       # Insert and Update Data
       result = support_CONTROLLER.calculation_relation_analysis(ID, RECORD_NAME, str(apex_outout_maize[0]), str(apex_outout_maize[1]), str(apex_outout_maize[2]), str(apex_outout_glass[0]), str(apex_outout_glass[1]), str(apex_outout_glass[2]))
       
       if (result == 1):
           print ("====Congratulation : DONE APEX MODEL RUNNING=================")
       else:
           print ("===[Error] : Error, please recheck")
           
              
    elif (ACTION_FLAG == 0):
       clean_all_data_in_server()
       sys.exit("===All data files and folder are removed======")
    elif (ACTION_FLAG == 2):
       clean_all_data_in_server() 
       clean_all_data_deeply()
       sys.exit("===All data files and folder are removed======") 
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
