# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
import os, csv, sys
import datetime
from __builtin__ import len

now = datetime.datetime.now()

if (len(sys.argv) < 4):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
# Input filenames
WTG_FOLDER = ""
DLY_FOLDER = ""
EXTEND_WTG_FILE = ".WTG"
DLY_NAME = ""
FULL_PATH_WTG_FILE = ""
FULL_PATH_DLY_FILE = ""

if (sys.argv[1] == '-Fwtg'):
   WTG_FOLDER = sys.argv[2]
if (sys.argv[3] == '-Fdly'):
   DLY_FOLDER = sys.argv[4]
if (sys.argv[5] == '-name'):
   DLY_NAME = sys.argv[6]
   FULL_PATH_WTG_FILE = os.path.join(WTG_FOLDER,"%s%s" %(DLY_NAME,EXTEND_WTG_FILE))


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
    if (WTG_FOLDER is None or not WTG_FOLDER.strip() or WTG_FOLDER == ""):
         print("ERROR : There is NO Folder Path of Input WTG Files")
         sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
    if (DLY_FOLDER is None or not DLY_FOLDER.strip() or DLY_FOLDER == ""):    
         print("ERROR : There is NO Folder Path of Input DLY Files")
         sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
   
    if not os.path.exists(WTG_FOLDER): 
         print("ERROR : WTG FOLDER is NOT EXISTED")
         sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
    if not os.path.exists(DLY_FOLDER): 
         print("ERROR : DLY FOLDER is NOT EXISTED")
         sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
    if not os.path.exists(FULL_PATH_WTG_FILE):
         print ("WTG File is NOT Existed " + FULL_PATH_WTG_FILE)
         sys.exit("Usage : python Step_2_convert_wtg_to_dly_WEATHER_Real_Time.py -Fwtg <Folder Path contains all WTG File> -Fdly <Folder Path that you want to put result DLY Files> -name <Slate Weather ID>")
    print("--Finish Step 1 : All input data is Ready")
def get_date_string_from_date_in_wtg(original_date):
    #return "  1970   1   5"
    #Format of original date xxyyy : xx : index of year
    original_date = original_date.strip();
    if (len(original_date) <> 5):
        return "  xxxx   y   y"
    index_year = original_date[:2]
    index_day_in_year = original_date[2:]
    year = ""
    month = ""
    day = ""
    int_year = 0
    try:
        int_index_year = int(index_year)
        int_index_day_in_year = int(index_day_in_year)
        if (int_index_year < 0 or int_index_year >=100):
            return "  xxxx   y   y"
        elif (int_index_year >= 10):
            year = "19%s" %(index_year)
            int_year  = int(year)
        elif (int_index_year >= 0 and int_index_year <= 9):
            year = "20%s" %(index_year)
            int_year = int(year)
        if (int_index_day_in_year < 0 or int_index_day_in_year > 367):
            return "  xxxx   y   y" 
        else:
            consider_date = datetime.datetime(int_year, 1, 1) + datetime.timedelta(int_index_day_in_year - 1)
            month = consider_date.month
            day = consider_date.day
            str_date = "  %s" %(year)
            if (month >= 1 and month <= 9):
                str_date = str_date + "   %s" %(str(month))
            elif (month >= 10 and month <= 99):
                str_date = str_date + "  %s" %(str(month))
            else:
                 str_date = str_date + " %s" %(str(month))
        
            if (day >= 1 and day <= 9):
                str_date = str_date + "   %s" %(str(day))
            elif (day >= 10 and day <= 99):
                str_date = str_date + "  %s" %(str(day))
            else:
                 str_date = str_date + " %s" %(str(day))
            return str_date
        return "  %s   %s   %s" %(year,month,day)
    except Exception, err:
        return "  xxxx   y   y"
    
    
   
def convert_wtg_to_dly():
    try:
        if (not os.path.exists(FULL_PATH_WTG_FILE)):
             sys.exit("---ERROR : WTG File does not Existed")
        print(" ====Process File: %s " % (FULL_PATH_WTG_FILE))
        name_dly = DLY_NAME + ".DLY"
        dly_file = os.path.join(DLY_FOLDER,name_dly)
        with open(FULL_PATH_WTG_FILE,'r') as file:
                data = file.readlines()
        new_data = []
        for i in range(5,len(data)):
            line = data[i]
            original_date = line[:5]
            # Process date time
            date = get_date_string_from_date_in_wtg(original_date)
            new_line = line[5:].strip()
            new_line = date + " " + new_line
            # Process 
                    
            new_line = new_line + "  0.00  0.00 0.000\n"
            new_data.append(new_line)
        with open(dly_file,'w') as file:
            file.writelines(new_data)   
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
def main():
    # Step 1:
    checkAllInputData()
    
    # Step 2:
    convert_wtg_to_dly()
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
