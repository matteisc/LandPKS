# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import shutil
try:
    from osgeo import gdal, ogr
    import numpy
    import struct
    from support import support_SUBAREA
except:
    sys.exit("===[Warning] : You have to install GDAL and ORG library in your computer")

X_COOR = ""
Y_COOR = ""
FLOAT_X_COOR = 0.0
FLOAT_Y_COOR = 0.0

X_COOR_1 = 0.0
Y_COOR_1 = 0.0
ID = ""
if (len(sys.argv) < 8):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
# Input requires
full_path = os.getcwd() + "\\"
subarea_files_folder = ""
ACTION_FLAG = 1
# Manage arguments
if (sys.argv[1] == '-f') :
    ACTION_FLAG = 1
    if (sys.argv[2] is None) :
        sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
    else:
        print("\n---Subarea Files SUB are in Folder %s" % (sys.argv[2]))
        subarea_files_folder = full_path + sys.argv[2]
        subarea_files_folder = subarea_files_folder.replace("\\\\", "\\")
    
    if (sys.argv[3] == '-x'):
        if (float(sys.argv[4])):
            X_COOR_1 = float(sys.argv[4])
        else:
            sys.exit("===[Error] : Error on X")
    else:
        sys.exit("===[Error] : Error on X")
        
    if (sys.argv[5] == '-y'):
        if (float(sys.argv[6])):
            Y_COOR_1 = float(sys.argv[6])
        else:
            sys.exit("===[Error] : Error on Y")
    else:
        sys.exit("===[Error] : Error on Y")
        
    if (sys.argv[7] == '-ID'):
        if (sys.argv[8] is not None):
            ID = sys.argv[8]
        else:
            sys.exit("===[Error] : Error on Folder")
    else:
        sys.exit("===[Error] : Error on Folder")
    
elif (sys.argv[1] == '-m') :
    ACTION_FLAG = 2
    if (sys.argv[2] is None) :
        sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
    if (sys.argv[18] == '-IDapex'):
        if (sys.argv[19] is None):
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
        else:
            if (not int(sys.argv[19])):
                print("=== [ERROR] : ID Apex Record in MySQL Database need to be a Interger => Cannot find SLOPE value => Use default value 0.00")
            else:
                ID = sys.argv[19]
    else:
        sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
elif (sys.argv[1] == '-rm'):
    ACTION_FLAG = 0
else :
    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")

# define
EXTEND_FILE_SUBAREA = ".SUB"
DAT_DIRECTORY = "Subarea_Files\Private\%s\DAT_Files" % (str(ID))
ORIGINAL_SUB_FILE_DIRECTORY = "Subarea_Files\Original_Subarea_Files"
FULL_ORIGINAL_SUB_FILE_DIRECTORY = ""
MODIFIED_SUB_FILE_DIRECTORY = "Subarea_Files\Private\%s\Modified_Subarea_Files" % (str(ID))
SUBACOM_DAT_FILE_NAME = "SUBACOM.DAT"


original_subarea_file = ""
modified_subarea_file = ""
FULL_MODIFIED_SUBAREA_FILE = ""
soil_sol_file = ""
FULL_SOICCOM_DAT = ""
SOICOM_DATA_FOLDER_FILE = "3_WISE_SOL_PROJECT_REAL_TIME\Result_HWSD\Private\%s\DAT\SOILCOM.DAT" % (str(ID))
opearation_ops_file = ""
FULL_OPSCCOM_DAT = ""
OPSCCOM_DATA_FOLDER_FILE = "6_OPERATIONS_PROJECT\Operation_Files\DAT_Files\OPSCCOM.DAT"
daily_weather_dly_file = ""
FULL_WDLSTCOM_DAT = ""
DAILY_WEATHER_DATA_FOLDER_FILE = "2_WEATHER_PROJECT_REAL_TIME\Weather_Files\Private\%s\DATFiles\WDLSTCOM.DAT" % (str(ID))

FULL_SUBACOM_DAT = ""

ROOT_PATH = ""



# Function
def checkAndCreateFolder():
    directory = full_path + "\Subarea_Files\Private\%s" % (str(ID))
    if not os.path.exists(directory):
        os.makedirs(directory)
    temp = directory + "\%s" % ("DAT_Files")
    if not os.path.exists(temp):
        os.makedirs(temp)
    temp = directory + "\%s" % ("Modified_Subarea_Files")
    if not os.path.exists(temp):
        os.makedirs(temp)
def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = filename
            file_paths.append(file_path)
    return file_paths
def createDATFile(subarea_folder):
    if (subarea_folder is None):
        sys.exit("---[Error_1] : Folder that contains DLY files are NOT existed")
    if not os.path.exists(subarea_folder):
        sys.exit("---[Error_2] : Folder %s not existed" % (subarea_folder))
    try:
        fo = open(os.path.join(DAT_DIRECTORY, SUBACOM_DAT_FILE_NAME), "wb")
        OPSFiles = get_files_path(subarea_folder)
        count = 0
        for f in OPSFiles:
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_SUBAREA):
                if (count == 1):
                    strContent = "    %d %s" % (count, f)
                else:
                    if (count >= 2 and count <= 9):
                        strContent = "\r\n    %d %s" % (count, f)
                    elif (count >= 10 and count <= 99):
                        strContent = "\r\n   %d %s" % (count, f)
                    elif (count >= 100 and count <= 999):
                        strContent = "\r\n  %d %s" % (count, f)
                    elif (count >= 1000 and count <= 9999):
                        strContent = "\r\n %d %s" % (count, f)
                    elif (count >= 10000 and count <= 99999):
                        strContent = "\r\n%d %s" % (count, f)
                fo.write(strContent)
        print("---Created %s file already---" % (SUBACOM_DAT_FILE_NAME))
        fo.write("\r\n")
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    finally :
        # close the cursor and connection
        fo.close()
def deleteAllFolderAndFiles():
    if os.path.exists(DAT_DIRECTORY):
        try:
            shutil.rmtree(DAT_DIRECTORY)
        except OSError:
            pass
    if os.path.exists(MODIFIED_SUB_FILE_DIRECTORY):
        try:
            shutil.rmtree(MODIFIED_SUB_FILE_DIRECTORY)
        except OSError:
            pass
def copy_sub_file(sub_file_path, to_path):
    # print("copy to %s " %(to_path))
    shutil.copy2(sub_file_path, to_path)
def copy_all_sub_file(from_path, to_path):
    if (from_path is None):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    if not os.path.exists(from_path):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    try:
        SUBFiles = get_files_path(from_path)
        count = 0
        for f in SUBFiles:
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_SUBAREA):
                copy_sub_file(os.path.join(from_path, f), to_path)
    except Exception, err:
        sys.stderr.write('---[Error]:Copy SUB files raised Error %s ' % (err))
def check_existed_file(path):
    path = path.strip()
    if (os.path.isfile(path)):
        return True
    else:
        return False
def get_index_in_dat_file(individual_file_name, full_data_file_path):
    try:
        fo = open(full_data_file_path, "r")
        lineList = fo.readlines()
        fo.close()
        for i in range(0, len(lineList)):
            line = lineList[i]
            line = line.strip()
            line = line.replace("       ", " ")
            line = line.replace("      ", " ")
            line = line.replace("     ", " ")
            line = line.replace("    ", " ")
            line = line.replace("   ", " ")
            line = line.replace("  ", " ")
            parts = []
            parts = line.split(" ")
            if (individual_file_name.upper() == parts[1].upper()):
                return int(parts[0].strip())
        return 0
    except Exception, err:
        sys.exit("%s" % (err))
def modify_SUB_file(full_path_sub_file, subarea_number, soil_number, operation_number, dly_number, Xcoor, Ycoor, aspect_value, slope_value):
    try:
        with open(full_path_sub_file, 'r') as file:
             data = file.readlines()
        # print data
        # print "Line 1: " + data[0]
        # file.close()
         
        line_1 = data[0]
        if (line_1 is None):
           sys.exit("==[Error] : SUB File is in Wrong Format")
        else:
           content_REST = line_1[8:]
           if (subarea_number >= 0 and subarea_number <= 9):
               str_content = "       %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 10 and subarea_number <= 99):
               str_content = "      %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 100 and subarea_number <= 999):
               str_content = "     %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 1000 and subarea_number <= 9999):
               str_content = "    %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 10000 and subarea_number <= 99999):
               str_content = "   %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 100000 and subarea_number <= 999999):
               str_content = "  %d%s" % (subarea_number, content_REST)
           elif (subarea_number >= 1000000 and subarea_number <= 9999999):
               str_content = " %d%s" % (subarea_number, content_REST) 
           elif (subarea_number >= 10000000 and subarea_number <= 99999999):
               str_content = "%d%s" % (subarea_number, content_REST)
           line_1 = str_content
           data[0] = line_1
        
        line_2 = data[1]
        if (line_2 is None):
           sys.exit("==[Error] : SUB File is in Wrong Format")
        else:
           # Line 2 Field 1
           content_REST = line_2[8:]
           if (soil_number >= 0 and soil_number <= 9):
               str_content = "       %d%s" % (soil_number, content_REST)
           elif (soil_number >= 10 and soil_number <= 99):
               str_content = "      %d%s" % (soil_number, content_REST)
           elif (soil_number >= 100 and soil_number <= 999):
               str_content = "     %d%s" % (soil_number, content_REST)
           elif (soil_number >= 1000 and soil_number <= 9999):
               str_content = "    %d%s" % (soil_number, content_REST)
           elif (soil_number >= 10000 and soil_number <= 99999):
               str_content = "   %d%s" % (soil_number, content_REST)
           elif (soil_number >= 100000 and soil_number <= 999999):
               str_content = "  %d%s" % (soil_number, content_REST)
           elif (soil_number >= 1000000 and soil_number <= 9999999):
               str_content = " %d%s" % (soil_number, content_REST) 
           elif (soil_number >= 10000000 and soil_number <= 99999999):
               str_content = "%d%s" % (soil_number, content_REST)
           line_2 = str_content

           # Line 2 Field 2
           content_REST_1 = line_2[:8]
           content_REST_2 = line_2[16:]
           if (operation_number >= 0 and operation_number <= 9):
               str_content = "%s       %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 10 and operation_number <= 99):
               str_content = "%s      %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 100 and operation_number <= 999):
               str_content = "%s     %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 1000 and operation_number <= 9999):
               str_content = "%s    %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 10000 and operation_number <= 99999):
               str_content = "%s   %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 100000 and operation_number <= 999999):
               str_content = "%s  %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 1000000 and operation_number <= 9999999):
               str_content = "%s %d%s" % (content_REST_1, operation_number, content_REST_2)
           elif (operation_number >= 10000000 and operation_number <= 99999999):
               str_content = "%s%d%s" % (content_REST_1, operation_number, content_REST_2)
           line_2 = str_content

           # Line 2 Field 8
           content_REST_1 = line_2[:56]
           content_REST_2 = line_2[64:]
           if (dly_number >= 0 and dly_number <= 9):
               str_content = "%s       %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 10 and dly_number <= 99):
               str_content = "%s      %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 100 and dly_number <= 999):
               str_content = "%s     %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 1000 and dly_number <= 9999):
               str_content = "%s    %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 10000 and dly_number <= 99999):
               str_content = "%s   %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 100000 and dly_number <= 999999):
               str_content = "%s  %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 1000000 and dly_number <= 9999999):
               str_content = "%s %d%s" % (content_REST_1, dly_number, content_REST_2)
           elif (dly_number >= 10000000 and dly_number <= 99999999):
               str_content = "%s%d%s" % (content_REST_1, dly_number, content_REST_2)
           line_2 = str_content
           data[1] = line_2
        
        line_3 = data[2]
        if (float(Xcoor)):
           line_3 = data[2]
           if (line_3 is None):
               sys.exit("==[Error] : SUB File is in Wrong Format")
           else:
               # Line 3 Field 3 - X coordinate
               content_REST_1 = line_3[:24]
               content_REST_2 = line_3[32:]
               if (Xcoor >= 0 and Xcoor < 10):
                   str_content = "%s   %0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor >= 10 and Xcoor < 100):
                   str_content = "%s  %0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor >= 100 and Xcoor < 1000):
                   str_content = "%s %0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor >= 1000 and Xcoor < 10000):
                   str_content = "%s%0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor < 0 and Xcoor > -10):
                   str_content = "%s  %0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor < -9 and Xcoor > -100):
                   str_content = "%s %0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               elif (Xcoor <= -100 and Xcoor > -1000):
                   str_content = "%s%0.3f%s" % (content_REST_1, Xcoor, content_REST_2)
               line_3 = str_content
               data[2] = line_3

        if (float(Ycoor)):
           if (line_3 is None):
               sys.exit("==[Error] : SUB File is in Wrong Format")
           else:
               # Line 3 Field 3 - X coordinate
               content_REST_1 = line_3[:16]
               content_REST_2 = line_3[24:]
               if (Ycoor >= 0 and Ycoor <= 9):
                   str_content = "%s   %0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor >= 10 and Ycoor < 100):
                   str_content = "%s  %0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor >= 100 and Ycoor < 1000):
                   str_content = "%s %0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor >= 1000 and Ycoor < 10000):
                   str_content = "%s%0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor < 0 and Ycoor > -10):
                   str_content = "%s  %0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor <= -10 and Ycoor > -100):
                   str_content = "%s %0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               elif (Ycoor <= -100 and Ycoor > -1000):
                   str_content = "%s%0.3f%s" % (content_REST_1, Ycoor, content_REST_2)
               line_3 = str_content
               data[2] = line_3
               
        if (aspect_value != -1):
            if (line_3 is None):
               sys.exit("==[Error] : SUB File is in Wrong Format")
            else:
               # Line 3 Field 3 - X coordinate
               content_REST_1 = line_3[:32]
               content_REST_2 = line_3[40:]
               float_aspect_value = float(aspect_value)
               if (aspect_value >= 0 and aspect_value <= 9):
                   str_content = "%s   %0.3f%s" % (content_REST_1, float_aspect_value, content_REST_2)
               elif (aspect_value >= 10 and aspect_value <= 99):
                   str_content = "%s  %0.3f%s" % (content_REST_1, float_aspect_value, content_REST_2)
               elif (aspect_value >= 100 and aspect_value <= 999):
                   str_content = "%s %0.3f%s" % (content_REST_1, float_aspect_value, content_REST_2)
               elif (aspect_value >= 1000 and aspect_value <= 9999):
                   str_content = "%s%0.3f%s" % (content_REST_1, float_aspect_value, content_REST_2)
               line_3 = str_content
               data[2] = line_3
        
        
        line_4 = data[3]
        if (line_4 is None):
            sys.exit("==[Error] : SUB File is in Wrong Format")
        else:
            # Line 4 Field 1
            content_REST_1 = ""
            content_REST_2 = line_4[8:]
            str_content = "%s     1.0%s" % (content_REST_1, content_REST_2)
            line_4 = str_content
            # Line 4 Field 2 0.186
            content_REST_1 = line_4[:8]
            content_REST_2 = line_4[16:]
            str_content = "%s   0.186%s" % (content_REST_1, content_REST_2)
            line_4 = str_content
            # Line 4 Field 3 0.084
            content_REST_1 = line_4[:16]
            content_REST_2 = line_4[24:]
            str_content = "%s   0.084%s" % (content_REST_1, content_REST_2)
            line_4 = str_content
            
                    # Line 4 Field 4 0.003
            content_REST_1 = line_4[:24]
            content_REST_2 = line_4[32:]
            str_content = "%s   0.003%s" % (content_REST_1, content_REST_2)
            line_4 = str_content
            
            # Line 4 Field 5 0.050
            content_REST_1 = line_4[:32]
            content_REST_2 = line_4[40:]
            str_content = "%s   0.050%s" % (content_REST_1, content_REST_2)
            line_4 = str_content
            
            # Line 4 Field 6 - Slope coordinate
            content_REST_1 = line_4[:40]
            content_REST_2 = line_4[48:]
            if (slope_value >= 0 and slope_value <= 9):
                str_content = "%s   %0.3f%s" % (content_REST_1, slope_value, content_REST_2)
            elif (slope_value >= 10 and slope_value <= 99):
                str_content = "%s  %0.3f%s" % (content_REST_1, slope_value, content_REST_2)
            elif (slope_value >= 100 and slope_value <= 999):
                str_content = "%s %0.3f%s" % (content_REST_1, slope_value, content_REST_2)
            elif (slope_value >= 1000 and slope_value <= 9999):
                str_content = "%s%0.3f%s" % (content_REST_1, slope_value, content_REST_2)
            line_4 = str_content
            
            #Line 4 Field 7 - Slope AVg Upland Slope Length in meters
            content_REST_1 = line_4[:48]
            content_REST_2 = line_4[56:]
            slope_length = support_SUBAREA.get_slope_length_from_slope_range(slope_value)
            if (slope_length >= 0 and slope_length <= 9):
                str_content = "%s   %0.3f%s" % (content_REST_1, slope_length, content_REST_2)
            elif (slope_length >= 10 and slope_length <= 99):
                str_content = "%s  %0.3f%s" % (content_REST_1, slope_length, content_REST_2)
            elif (slope_length >= 100 and slope_length <= 999):
                str_content = "%s %0.3f%s" % (content_REST_1, slope_length, content_REST_2)
            elif (slope_length >= 1000 and slope_length <= 9999):
                str_content = "%s%0.3f%s" % (content_REST_1, slope_length, content_REST_2)
            line_4 = str_content
            
            data[3] = line_4

        with open(full_path_sub_file, 'w') as file:
           file.writelines(data)
    except Exception, err:
        sys.exit("==[Error] : Modify SUB File raised Error %s" % (err))
    finally:
        file.close()
def main():
    try:
        if (ACTION_FLAG == 1):
            print("-PREPROCESSING : Create Folders--")
            checkAndCreateFolder()
            print("-START Step 1 : Create %s File" % (SUBACOM_DAT_FILE_NAME))
            createDATFile(subarea_files_folder)
            print("-FINISH : %s is created and located in %s" % (SUBACOM_DAT_FILE_NAME, full_path + DAT_DIRECTORY))
            print("-START Step 2 : Copy Files in Modified Folder")
            copy_all_sub_file(ORIGINAL_SUB_FILE_DIRECTORY, MODIFIED_SUB_FILE_DIRECTORY)
            print("-FINISH : All SUB files are copied")
        elif (ACTION_FLAG == 2):
            print("-START Step 3 : Modify SUB file")
            # Modify SUB file procedure
            directory = full_path + "\Subarea_Files\Private\%s" % (str(ID))
            temp = directory + "\%s" % ("DAT_Files")
            print temp
            if not os.path.exists(temp):
                sys.exit("===Cannot run this step. Please run command 1 firstly======")
            temp = directory + "\%s" % ("Modified_Subarea_Files")
            if not os.path.exists(temp):
                sys.exit("===Cannot run this step. Please run command 1 firstly======")
            # Running
            if (sys.argv[2] is None) :
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
            else:
                modified_subarea_file = sys.argv[2]
                modified_subarea_file = modified_subarea_file.strip()
                FULL_MODIFIED_SUBAREA_FILE = os.path.join(full_path, MODIFIED_SUB_FILE_DIRECTORY + "\%s" % (modified_subarea_file))
                print("===Read File : %s" % (FULL_MODIFIED_SUBAREA_FILE))
                if (not os.path.isfile(FULL_MODIFIED_SUBAREA_FILE)):
                    sys.exit("---[Error] : File %s is NOT existed" % (modified_subarea_file))
                FULL_SUBACOM_DAT = os.path.join(full_path, DAT_DIRECTORY + "\%s" % (SUBACOM_DAT_FILE_NAME))
                if (not os.path.isfile(FULL_SUBACOM_DAT)):
                    sys.exit("===[ERROR] : File %s is NOT existed" % (FULL_SOICCOM_DAT))
                print("=======SUBACOM.DAT File : %s" % (FULL_SUBACOM_DAT))
                SUBAREA_NUMBER = get_index_in_dat_file(modified_subarea_file, FULL_SUBACOM_DAT)
                if (SUBAREA_NUMBER == 0):
                    sys.exit("===[ERROR] : File %s is NOT existed in DAT File" % (modified_subarea_file)) 
                print("=======SUBAREA INDEX : %d" % (SUBAREA_NUMBER))
            if (sys.argv[3] == "-s"):
                if (sys.argv[4] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    soil_sol_file = sys.argv[4]
                    soil_sol_file = soil_sol_file.strip()
                    ROOT_PATH = os.path.abspath(os.path.join(full_path, os.pardir))
                    if (sys.argv[5] == "-default"):
                        FULL_SOICCOM_DAT = os.path.join(ROOT_PATH, SOICOM_DATA_FOLDER_FILE)
                    else:
                        FULL_SOICCOM_DAT = os.path.join(ROOT_PATH, sys.argv[5].strip())
                    FULL_SOICOM_DATA = FULL_SOICCOM_DAT.strip()
                    if (not os.path.isfile(FULL_SOICCOM_DAT)):
                        sys.exit("===[ERROR] : File %s is NOT existed" % (FULL_SOICCOM_DAT))
                    print("=======SOILCOM.DAT File : %s" % (FULL_SOICCOM_DAT))
                    SOIL_NUMBER = get_index_in_dat_file(soil_sol_file, FULL_SOICOM_DATA)
                    if (SOIL_NUMBER == 0):
                        sys.exit("===[ERROR] : File %s is NOT existed in DAT File" % (soil_sol_file)) 
                    print("=======SOIL INDEX : %d" % (SOIL_NUMBER))
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
            if (sys.argv[6] == "-o"):
                if (sys.argv[7] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    opearation_ops_file = sys.argv[7]
                    opearation_ops_file = opearation_ops_file.strip()
                    ROOT_PATH = os.path.abspath(os.path.join(full_path, os.pardir))
                    if (sys.argv[8] == "-default"):
                        FULL_OPSCCOM_DAT = os.path.join(ROOT_PATH, OPSCCOM_DATA_FOLDER_FILE)
                    else:
                        FULL_OPSCCOM_DAT = os.path.join(ROOT_PATH, sys.argv[8].strip())
                    FULL_OPSCCOM_DAT = FULL_OPSCCOM_DAT.strip()
                    if (not os.path.isfile(FULL_OPSCCOM_DAT)):
                        sys.exit("===[ERROR] : File %s is NOT existed" % (FULL_OPSCCOM_DAT))
                    print("=======OPSCCOM.DAT File : %s" % (FULL_OPSCCOM_DAT))
                    OPERATION_NUMBER = get_index_in_dat_file(opearation_ops_file, FULL_OPSCCOM_DAT)
                    if (OPERATION_NUMBER == 0):
                        sys.exit("===[ERROR] : File %s is NOT existed in DAT File" % (opearation_ops_file)) 
                    print("=======OPERATION INDEX : %d" % (OPERATION_NUMBER))
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
            if (sys.argv[9] == "-d"):
                if (sys.argv[10] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    daily_weather_dly_file = sys.argv[10]
                    daily_weather_dly_file = daily_weather_dly_file.strip()
                    ROOT_PATH = os.path.abspath(os.path.join(full_path, os.pardir))
                    if (sys.argv[11] == "-default"):
                        FULL_WDLSTCOM_DAT = os.path.join(ROOT_PATH, DAILY_WEATHER_DATA_FOLDER_FILE)
                    else:
                        FULL_WDLSTCOM_DAT = os.path.join(ROOT_PATH, sys.argv[11].strip())
                    FULL_WDLSTCOM_DAT = FULL_WDLSTCOM_DAT.strip()
                    if (not os.path.isfile(FULL_WDLSTCOM_DAT)):
                        sys.exit("===[ERROR] : File %s is NOT existed" % (FULL_WDLSTCOM_DAT))
                    print("=======WDLSTCOM.DAT File : %s" % (FULL_WDLSTCOM_DAT))
                    DLY_NUMBER = get_index_in_dat_file(daily_weather_dly_file, FULL_WDLSTCOM_DAT)
                    if (DLY_NUMBER == 0):
                        sys.exit("===[ERROR] : File %s is NOT existed in DAT File" % (daily_weather_dly_file)) 
                    print("=======DAILY WEATHER INDEX : %d" % (DLY_NUMBER))
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
            
            if (sys.argv[12] == '-x'):
                if (sys.argv[13] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    X_COOR = sys.argv[13]
                    if (float(X_COOR)):
                        print("=====Get X = " + X_COOR)
                        FLOAT_X_COOR = float(X_COOR)
                    else:
                        sys.exit("--[ERROR] : X Coordinate is wrong format")       
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                
            if (sys.argv[14] == '-y'):
                if (sys.argv[15] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    Y_COOR = sys.argv[15]
                    if (float(Y_COOR)):
                        print("=====Get Y = " + Y_COOR)  
                        FLOAT_Y_COOR = float(Y_COOR)
                    else:
                        sys.exit("--[ERROR] : Y Coordinate is wrong format")       
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
            # Select some data from TIF File
            tif_file_aspect = '/aspect/ASPECT.tif'
            ASPECT_LAYER_VALUE = -1
            if (sys.argv[16] == '-tif'):
                if (sys.argv[17] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    full_path_aspect_tif_file = sys.argv[17] + tif_file_aspect
                    if (os.path.exists(full_path_aspect_tif_file)):
                        ASPECT_LAYER_VALUE = getRasterValue_ThanhNH(full_path_aspect_tif_file, FLOAT_X_COOR, FLOAT_Y_COOR)
                        print("=====Get ASPECT LAYER VALUE = " + str(ASPECT_LAYER_VALUE))
                    else:
                        print("===[Warning : Cannot Get Aspect Layer Value from TIF File => Use default 0.00]")
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                        
            ID_APEX = 0
            SLOPE = 0.00
            if (sys.argv[18] == '-IDapex'):
                if (sys.argv[19] is None):
                    sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                else:
                    if (not int(sys.argv[19])):
                        print("=== [ERROR] : ID Apex Record in MySQL Database need to be a Interger => Cannot find SLOPE value => Use default value 0.00")
                        SLOPE = 0.00
                    else:
                        ID_APEX = int(sys.argv[19])
                        strSlope = support_SUBAREA.get_slope_value_from_id(ID_APEX)
                        print("==Slope : %s" %(str(strSlope)))
                        SLOPE = support_SUBAREA.get_float_percentage_number_of_slope_value(strSlope)
                        print("==Lay duoc Slope la : " + str(SLOPE))
            else:
                sys.exit("Usage : python Step_2_main_SUBAREA.py -m <original SUB filename> -s <Soil SOL filename> <Path of SOILCOM.DAT file OR -default> -o <opearation OPS filename> <Path of OPSCCOM.DAT or -default>  -d <Daily weather DLY filename> <Path of WDLSTCOM.DAT or -default> -x <X coordinate> -y <Y coordinate> -IDapex <ID of entry in MySQL database - APEX>")
                
            # Write new data to file
            print("=========================================================")
            modify_SUB_file(FULL_MODIFIED_SUBAREA_FILE, SUBAREA_NUMBER, SOIL_NUMBER, OPERATION_NUMBER, DLY_NUMBER, FLOAT_X_COOR, FLOAT_Y_COOR, ASPECT_LAYER_VALUE, SLOPE)
            print("============DONE : Modified SUB File already=============")
            print("=========================================================")
        elif (ACTION_FLAG == 0):
            deleteAllFolderAndFiles()
            sys.exit("===All data files and folder are removed======")
    except Exception, err:
        sys.exit("%s" % (err))
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
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
