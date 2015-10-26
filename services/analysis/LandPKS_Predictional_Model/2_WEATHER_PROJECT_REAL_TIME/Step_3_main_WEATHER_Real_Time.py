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
from support import support_WEATHER

# define
# Check arguments
mess = "Usage : python Step_3_main_WEATHER.py -f <Daily Weather Files Folder Path> -x <X Coordinate> -y <Y Coordinate> -ID <Record ID>" 
if (len(sys.argv) < 7):
    print("Sorry, not enough arguments")
    sys.exit(mess)

# Input requires
full_path = os.getcwd() + "\\"
weather_files_folder = ""
# Manage arguments
if (sys.argv[1] == '-f') :
    if (sys.argv[2] is None) :
        sys.exit(mess)
    else:
        print("\n---Daily Weather Files DLY are in Folder %s" % (sys.argv[2]))
        weather_files_folder = sys.argv[2]
        weather_files_folder = weather_files_folder.replace("\\\\", "\\")
elif (sys.argv[1] == '-rm'):
    ACTION_FLAG = 0
else :
    sys.exit(mess)
    
X_COOR = 0.0
Y_COOR = 0.0

if (sys.argv[3] == '-x'):
        if (float(sys.argv[4])):
            X_COOR = float(sys.argv[4])
        else:
            sys.exit("====[Error] : Error in X")
else:
        sys.exit("====[Error] : Error in X")
    
if (sys.argv[5] == '-y'):
        if (float(sys.argv[6])):
            Y_COOR = float(sys.argv[6])
        else:
            sys.exit("====[Error] : Error in Y")
else:
        sys.exit("====[Error] : Error in Y")
        

ID = ""
if (sys.argv[7] == '-ID'):
    if (sys.argv[8] is not None):
        ID = sys.argv[8].strip()
        
    else:
        sys.exit(mess)
else:
    sys.exit(mess)
    
EXTEND_FILE_DAILY_WEATHER = ".DLY"
datDirectory = ""
tempDLYDirectory = ""
WP1_Directory = ""
WP1_FOLDER = "Weather_Files\Private\%s\WP1_Files" % (str(ID))
COMPLETE_WP1_FOLDER = "Weather_Files\Private\%s\Complete_WP1_Files" % (str(ID))
INP_OUT_Directory = ""
INP_OUT = "Weather_Files\Private\%s\INP_OUT_Files" %(str(ID))
DAT_FILE_NAME = "WXPMRUN.DAT"
WP1MO_DATA_FILE = "WPM1MO.DAT"
WDLST_DATA_FILE = "WDLSTCOM.DAT"
PRE_FOLDER_DAT_FILE = "Weather_Files/Private/%s/DATFiles" %(str(ID))
PRE_FOLDER_DAT_DILE_WINDOW = "\Weather_Files\Private\%s\DATFiles" %(str(ID))
EPIC_WEATHER_APPLICATION_FOLDER = "EPIC_Weather_Application"
EXECUTABLE_EXE_FILE_EPIC_APPLICATION = "WXPM3020.exe"
TEMP_DLY = "Weather_Files\Private\%s\Temp_DLY_Files" %(str(ID))
EXTEND_FILE_INP = ".INP"
EXTEND_FILE_OUT = ".OUT"

now = datetime.datetime.now()
CURRENT_YEAR = now.year
ACTION_FLAG = 1


#define
def checkAndCreateFolder():
    directory = full_path + "\Weather_Files\Private\%s" %(str(ID))
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\\" + "DATFiles"
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
    INP_OUT_Directory = directory + "\\" + "INP_OUT_Files"
    if not os.path.exists(INP_OUT_Directory):
        os.makedirs(INP_OUT_Directory)
    tempDLYDirectory = directory + "\\" + "Temp_DLY_Files"
    if not os.path.exists(tempDLYDirectory):
        os.makedirs(tempDLYDirectory)
    WP1_Directory = directory + "\\" + "WP1_Files"
    if not os.path.exists(WP1_Directory):
        os.makedirs(WP1_Directory)
    WP1_Directory = directory + "\\" + "Complete_WP1_Files"
    if not os.path.exists(WP1_Directory):
        os.makedirs(WP1_Directory)
def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = filename
            file_paths.append(file_path)
    return file_paths
def check_ready_epic_weather_application():
    epic_application_path = full_path + "\%s" % (EPIC_WEATHER_APPLICATION_FOLDER)
    if not os.path.exists(epic_application_path):
        sys.exit("---[Error] : Please check EPIC WEATHER APPLICATION folder and executable files are NOT located in %s" % (epic_application_path))
    file_paths = []
    check = 0
    for root, directories, files in os.walk(epic_application_path):
        for filename in files:
            file_path = filename
            if (file_path.strip() == EXECUTABLE_EXE_FILE_EPIC_APPLICATION):
                check = 1
    return check
def copyDATFile():
    originPath = full_path
    shutil.copy2(full_path + "%s\%s" % (PRE_FOLDER_DAT_DILE_WINDOW , DAT_FILE_NAME), originPath)
def get_X_longtitude(dly_file_name):
    return 0.00
def get_Y_latitude(dly_file_name):
    return 0.00
def createWDLSTCOMDatFile(weather_folder):
    if (weather_folder is None):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    if not os.path.exists(weather_folder):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    try:
        fo = open(os.path.join(PRE_FOLDER_DAT_FILE, WDLST_DATA_FILE), "wb")
        DLYFiles = get_files_path(weather_folder)
        count = 0
        for f in DLYFiles:
            check_dly_name = f[:f.index('.')]
            #coors = support_WEATHER.get_coordinate_follow_dly_file_name(check_dly_name)
            # coors = None
         
            
            str_X = "%0.2f" % (X_COOR)   
            str_Y = "%0.2f" % (Y_COOR)
                
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_DAILY_WEATHER):
                if (count == 1):
                    strContent = "    %d   %s" % (count, f)
                    # Add Y to
                    number_space = 11 - len(str_Y)
                    if (number_space > 0):
                        for i in range(0, number_space):
                           strContent = strContent + " "
                        strContent = strContent + str_Y
                    else:
                        strContent = strContent + "       0.00"
                    # Add X to
                    number_space = 11 - len(str_X)
                    if (number_space > 0):
                        for i in range(0, number_space):
                            strContent = strContent + " "
                        strContent = strContent + str_X
                    else:
                        strContent = strContent + "       0.00"
                else:
                    if (count >= 2 and count <= 9):
                       strContent = "\r\n    %d   %s" % (count, f)
                       # Add Y to
                       number_space = 11 - len(str_Y)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_Y
                       else:
                           strContent = strContent + "       0.00"
                       # Add X to
                       number_space = 11 - len(str_X)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_X
                       else:
                           strContent = strContent + "       0.00"
                    elif (count >= 10 and count <= 99):
                       strContent = "\r\n   %d   %s" % (count, f)
                       # Add Y to
                       number_space = 11 - len(str_Y)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_Y
                       else:
                           strContent = strContent + "       0.00"
                       # Add X to
                       number_space = 11 - len(str_X)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_X
                       else:
                           strContent = strContent + "       0.00"
                    elif (count >= 100 and count <= 999):
                       strContent = "\r\n  %d   %s" % (count, f)
                       # Add Y to
                       number_space = 11 - len(str_Y)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_Y
                       else:
                           strContent = strContent + "       0.00"
                       # Add X to
                       number_space = 11 - len(str_X)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_X
                       else:
                           strContent = strContent + "       0.00"
                    elif (count >= 1000 and count <= 9999):
                       strContent = "\r\n %d   %s" % (count, f)
                       # Add Y to
                       number_space = 11 - len(str_Y)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_Y
                       else:
                           strContent = strContent + "       0.00"
                       # Add X to
                       number_space = 11 - len(str_X)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_X
                       else:
                           strContent = strContent + "       0.00"
                    elif (count >= 10000 and count <= 99999):
                       strContent = "\r\n%d   %s" % (count, f)
                       # Add Y to
                       number_space = 11 - len(str_Y)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_Y
                       else:
                           strContent = strContent + "       0.00"
                       # Add X to
                       number_space = 11 - len(str_X)
                       if (number_space > 0):
                           for i in range(0, number_space):
                               strContent = strContent + " "
                           strContent = strContent + str_X
                       else:
                           strContent = strContent + "       0.00"
                fo.write(strContent)
        print("---Created %s file already---" % (WDLST_DATA_FILE))
        fo.write("\r\n")
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    finally :
        # close the cursor and connection
        fo.close()
def createDATFile(weather_folder):
    if (weather_folder is None):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    if not os.path.exists(weather_folder):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    try:
        fo = open(os.path.join(PRE_FOLDER_DAT_FILE, DAT_FILE_NAME), "wb")
        DLYFiles = get_files_path(weather_folder)
        count = 0
        for f in DLYFiles:
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_DAILY_WEATHER):
                if (count == 1):
                    strContent = f
                else:
                    strContent = "\r\n" + f
                fo.write(strContent)
        print("---Totally %d files---" % (count))
        fo.write("\r\n")
        fo.write(" \r\n")
        fo.write(" \r\n")
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    finally :
        # close the cursor and connection
        fo.close()
def process_dly_files():
    try:
        DLYFiles = get_files_path(weather_files_folder)
        count = 0
        for f in DLYFiles:
            # Read each file DLY
            fo = open(os.path.join(weather_files_folder , f), "r")
            line1 = fo.readline()
            line2 = fo.readline()
            if (line1.strip().upper() == f.strip().upper()):
                count_space = line2.strip().count(' ')
                if (count_space < 1):
                    originPath = full_path
                    copy_dly_file(os.path.join(weather_files_folder , f), originPath)
                else:
                    modify_dly_file(os.path.join(weather_files_folder , f), f)
            else:
                modify_dly_file(os.path.join(weather_files_folder , f), f)
            fo.close()
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    finally :
        # close the cursor and connection
        fo.close()
def get_second_line_content(dlyfile_path):
    try:
        fo = open(dlyfile_path, "r")
        lineList = fo.readlines()
        fo.close()

        # Process First Line => Get the beginning year
        firstLine = lineList[0]
        if firstLine is None:
            sys.exit("---[Error]: File DLY is Wrong Format in file %s" % (dlyfile_path))
        firstLine = firstLine.strip()
        firstLine = firstLine.replace("  ", " ")
        firstLine = firstLine.replace("   ", " ")
        parts = []
        parts = firstLine.split(" ")
        # Pick beginning year data
        beginningYear = parts[0].strip()


        # Process Last Line => Get the beginning year
        lastLine = lineList[-1]
        if lastLine is None:
            sys.exit("---[Error]: File DLY is Wrong Format")
        lastLine = lastLine.strip()
        lastLine = lastLine.replace("  ", " ")
        lastLine = lastLine.replace("   ", " ")
        parts = []
        parts = lastLine.split(" ")
        # Pick beginning year data
        endYear = parts[0].strip()
        delta = 0

        bYear = int(beginningYear)
        eYear = int(endYear)
        if (bYear >= 1500 and eYear >= 1500 and bYear <= CURRENT_YEAR and eYear <= CURRENT_YEAR and bYear < eYear):
            delta = eYear - bYear
        else:
            sys.exit("---[Error]: File DLY is Wrong Format in file %s" % (dlyfile_path))
        strContent = str(delta) + beginningYear
        return strContent
    except Exception, err:
        sys.stderr.write('---[Error]: Read file raised Error %s ' % (err))
    finally :
        # close the cursor and connection
        fo.close()
def modify_dly_file(dlyfile_path, file_name):
    try:
        # Copu DLY file to tempDLYDirectory
        tempDLYDirectory = full_path + "%s" % (TEMP_DLY)
        copy_dly_file(dlyfile_path, tempDLYDirectory)
        tempDLY_File = os.path.join(tempDLYDirectory, file_name)
        print(" ====Process File: %s " % (tempDLY_File))
        for linenum, line in enumerate(fileinput.FileInput(tempDLY_File, inplace=1)):
            if linenum == 0:
                print file_name
                print "  %s" % (get_second_line_content(dlyfile_path))
                print line.rstrip()
            else:
                print line.rstrip()
        originPath = full_path
        copy_dly_file(tempDLY_File, originPath)
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    # finally :
        # close the cursor and connection
        # fo.close()
def copy_dly_file(dlyfile_path, to_path):
    # print("copy to %s " %(to_path))
    shutil.copy2(dlyfile_path, to_path)
def runningModel():
    epic_application_path = full_path + "\%s" % (EPIC_WEATHER_APPLICATION_FOLDER)
    # subprocess.call(['C:\\Users\\thnguyen\\Desktop\\WISE-SOL-PROJECT\\EPIC_Weather_Application\\WXPM3020.exe'])
    os.system(epic_application_path + "\%s" % (EXECUTABLE_EXE_FILE_EPIC_APPLICATION))
def getMaxLengthOfFileName(files):
    max = 0
    for f in files:
        uF = f.upper()
        if (uF.endswith(EXTEND_FILE_INP)):
            sizeF = len(f.strip())
            if (sizeF > max):
                max = sizeF
    return max
def getLengthString(str):
    if (str is None):
        return 0
    str = str.strip()
    return len(str)
def post_processing():
    try:
        originPath = full_path
        # Copy INP and Output files to Collect Folder
        files = get_files_path(originPath)
        INP_OUT_Directory = originPath + "\%s" % (INP_OUT)
        WP1_Directory = originPath + "\%s" % (WP1_FOLDER)
        Complete_WP1_Directory = originPath + "\%s" % (COMPLETE_WP1_FOLDER)
        # os.remove(os.path.join(PRE_FOLDER_DAT_FILE,WP1MO_DATA_FILE))
        fo = open(os.path.join(PRE_FOLDER_DAT_FILE, WP1MO_DATA_FILE), "wb")
        count = 0
        maxLength = getMaxLengthOfFileName(files)
        for f in files:
            uF = f.upper()
            
            # os.remove(os.path.join(originPath,DAT_FILE_NAME))
            if (uF.endswith(EXTEND_FILE_INP)):
                check_dly_name = f[:f.index('.')]
                str_X = "%0.2f" % (X_COOR)   
                str_Y = "%0.2f" % (Y_COOR)
                
                try:
                    count = count + 1 
                    copy_dly_file(os.path.join(originPath, f), INP_OUT_Directory)
                    newName = f[:f.index('.')]
                    newName = newName + ".WP1"
                    os.rename(f, newName)
                    # print ("ThanhNH %d %d" %(maxLength, getLengthString(newName)))
                    if (maxLength == getLengthString(newName)):
                        if (count >= 1 and count <= 9):
                            # fo.write("    %d  %s     %0.2f     %0.2f    %s" % (count, newName, 0.0, 0.0, newName))
                            strContent = "    %d  %s" % (count, newName)
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                            fo.write(strContent)
                        elif (count >= 10 and count <= 99):
                            # fo.write("   %d  %s     %0.2f     %0.2f    %s" % (count, newName, 0.0, 0.0, newName))
                            strContent = "   %d  %s" % (count, newName)
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                            fo.write(strContent)
                        elif (count >= 100 and count <= 999):
                            # fo.write("  %d  %s     %0.2f     %0.2f    %s" % (count, newName, 0.0, 0.0, newName))
                            strContent = "  %d  %s" % (count, newName)
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                            fo.write(strContent)
                        elif (count >= 1000 and count <= 9999):
                            # fo.write(" %d  %s     %0.2f     %0.2f    %s" % (count, newName, 0.0, 0.0, newName))
                            strContent = " %d  %s" % (count, newName)
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                            fo.write(strContent)
                        elif (count >= 10000 and count <= 99999):
                            # fo.write("%d  %s     %0.2f     %0.2f    %s" % (count, newName, 0.0, 0.0, newName))
                            strContent = "%d  %s" % (count, newName)
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                            fo.write(strContent)
                        else:
                            sys.exit("---[ERROR] : Number and Index of File are too much. Cannot fix to format of file")
                    else:
                        numberOfSpaces = maxLength - getLengthString(newName)
                        # print("ThanhNH : %d" %(numberOfSpaces))
                        if (count >= 1 and count <= 9):
                            strContent = "    %d" % (count)
                            # Add name
                            for i in range(0, numberOfSpaces):
                                strContent = strContent + " "
                            strContent = strContent + newName
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                        elif (count >= 10 and count <= 99):
                            strContent = "   %d" % (count)
                            # Add name
                            for i in range(0, numberOfSpaces):
                                strContent = strContent + " "
                            strContent = strContent + newName
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                        elif (count >= 100 and count <= 999):
                            strContent = "  %d" % (count)
                            # Add name
                            for i in range(0, numberOfSpaces):
                                strContent = strContent + " "
                            strContent = strContent + newName
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                        elif (count >= 1000 and count <= 9999):
                            strContent = " %d" % (count)
                            # Add name
                            for i in range(0, numberOfSpaces):
                                strContent = strContent + " "
                            strContent = strContent + newName
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                        elif (count >= 10000 and count <= 99999):
                            strContent = "%d" % (count)
                            # Add name
                            for i in range(0, numberOfSpaces):
                                strContent = strContent + " "
                            strContent = strContent + newName
                            # Add Y to
                            number_space = 9 - len(str_Y)
                            if (number_space > 0):
                               for i in range(0, number_space):
                                   strContent = strContent + " "
                               strContent = strContent + str_Y
                            else:
                               strContent = strContent + "     0.00"
                            # Add X to
                            number_space = 9 - len(str_X)
                            if (number_space > 0):
                                for i in range(0, number_space):
                                   strContent = strContent + " "
                                strContent = strContent + str_X
                            else:
                                strContent = strContent + "     0.00"
                            strContent = strContent + "    %s" % (newName)
                        else:
                            sys.exit("---[ERROR] : Number and Index of File are too much. Cannot fix to format of file")
                        fo.write(strContent)
                    
                    fo.write("\r\n")
                    copy_dly_file(os.path.join(originPath, newName), WP1_Directory)
                    copy_dly_file(os.path.join(originPath, newName), Complete_WP1_Directory)
                    os.remove(os.path.join(originPath, newName))
                except OSError:
                    pass
            elif uF.endswith(EXTEND_FILE_OUT):
                try:
                   copy_dly_file(os.path.join(originPath, f), INP_OUT_Directory)
                   os.remove(os.path.join(originPath, f))
                except OSError:
                    pass
            elif uF.endswith(EXTEND_FILE_DAILY_WEATHER):
                try:
                   os.remove(os.path.join(originPath, f))
                except OSError:
                   pass
        try:
            os.remove(os.path.join(originPath, DAT_FILE_NAME))
        except OSError :
            pass
    except Exception, err:
        print('---[Waiting]: Please waiting to complete task %s' % (err))
    finally :
        fo.close()
def deleteAllFolderAndFiles():
    directory = full_path + "\Weather_Files\Private\%s" %(str(ID))
    datDirectory = directory + "\DATFiles"
    if os.path.exists(datDirectory):
        try:
            shutil.rmtree(datDirectory)
        except OSError:
            pass
    INP_OUT_Directory = directory + "\INP_OUT_Files"
    if os.path.exists(INP_OUT_Directory):
        try:
            shutil.rmtree(INP_OUT_Directory)
        except OSError:
            pass
    tempDLYDirectory = directory + "\Temp_DLY_Files"
    if  os.path.exists(tempDLYDirectory):
        try:
            shutil.rmtree(tempDLYDirectory)
        except OSError:
            pass
    WP1_Directory = directory + "\WP1_Files"
    if os.path.exists(WP1_Directory):
        try:
            shutil.rmtree(WP1_Directory)
        except OSError:
            pass
    Complete_WP1_Directory = directory + "\Complete_WP1_Files"
    if os.path.exists(Complete_WP1_Directory):
        try:
            shutil.rmtree(Complete_WP1_Directory)
        except OSError:
            pass 
def modify_WP1_Files():
    try:
        # Copu DLY file to tempDLYDirectory
        Complete_WP1_Directory = full_path + "%s" % (COMPLETE_WP1_FOLDER)
        WP1_Files = get_files_path(Complete_WP1_Directory)
        count = 0
        for f in WP1_Files:
            # Read each file WP1
            wp1_File = os.path.join(Complete_WP1_Directory, f)
            print(" ====Process File: %s " % (wp1_File))
            with open(wp1_File, 'r') as file:
                data = file.readlines()
            line_0 = data[0].strip()
            data[0] = "     %s\n" % (line_0)
            for i in range(2, len(data)):
                line = data[i]
                if (line is not None and line.strip()):
                    content_rest = line[:72]
                    data[i] = "%s\n" % (content_rest)
            with open(wp1_File, 'w') as file:
                file.writelines(data)
                file.write("\n") 
            # Standard Data : Remove Column 13; Remove Black Symbol
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
def main():
    if (ACTION_FLAG == 1):
       print("-PREPROCESSING : Create Folders--")
       checkAndCreateFolder()
       print("-START Step 1 : Check available of EPIC Weather Acpplication")
       check = check_ready_epic_weather_application()
       if (check != 1):
           sys.exit("---[Error] : Executable File WXPM3020.exe is not located in folder %s\%s" % (full_path, EPIC_WEATHER_APPLICATION_FOLDER))
       print("-FINISH : EPIC Weather Application is Ready")
       print("-START Step 2: Create WXPMRUN.DAT file-")
       createDATFile(weather_files_folder)
       createWDLSTCOMDatFile(weather_files_folder)
       print("-FINISH : WXPMRUN.DAT file is created-")
       print("-START Step 3: Copy WXPMRUN.DAT file to %s" % (full_path))
       copyDATFile()
       print("-FINISH : WXPMRUN.DAT file is COPIED-")
       print("-START Step 4: Check DLY Files to map standard format")
       print("-----If no problem, copy DLV Files to %s" % (full_path))
       print("-----If NOT, create modified DLY files with standard format and copy them to %s" % (full_path))
       process_dly_files()
       print("-FINISH : DLY Files are fixed-")
       print("=====Waiting for Preparing Model=====")
       print("-START Step 5: Runnint WXPM3020 Model")
       runningModel()
       print("-FINISH : Created Aldready INP and OUT Files in %s%s" % (full_path, INP_OUT_Directory))
       print("-START Step 6: Collect Result Files and Remove temp files")
       post_processing()
       print("-START Step 7: Modify WP1 File to map Model requires")
       modify_WP1_Files()
       print("-FINISH : Modify WPI 1 File to Map Model Requires")
       print("-DONE : -WP1MO.DAT file is in %s%s" % (full_path, PRE_FOLDER_DAT_DILE_WINDOW))
    else:
       deleteAllFolderAndFiles()
       sys.exit("===All data files and folder are removed======")
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
