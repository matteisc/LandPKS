# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import sys
import os
import subprocess
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy
import shutil
import time
import datetime
from datetime import date, timedelta as td



DEF_PERL_SCRIPT_FOLDER = 'D:/ThanhNguyen_Working/Python_APEX/Perl_Africa_Weather/'
DEF_PERL_SCRIPT_RAINFALL_DRIVER = "africa_rainfall.pl"
DEF_PERL_SCRIPT_TMAX_DRIVER = "africa_tmax.pl"
DEF_PERL_SCRIPT_TMIN_DRIVER = "africa_tmin.pl"
DEF_START_DATE = "2001-02-13"
DEF_END_DATE = "2014-12-31"
DEF_DLY_FILES_WEATHER_SATELLINE_DATA_AFTER_CONVERT = "D:\\ThanhNguyen_Working\\Python_APEX\\SATELLINE_WEATHER_DATA\\WEATHER_DLY_FILES"
DEF_DLY_FILES_WEATHER_SATELLINE_DATA_MAP_SLATE_WEATHER = "D:\\ThanhNguyen_Working\\Python_APEX\\SATELLINE_WEATHER_DATA\\WEATHER_DLY_FILES_SLATE"

X_MAX = 14.063139287754893
X_MIN = 14.063139287754893
Y_MAX = -19.15491965599358
Y_MIN = -19.15491965599358
DATA_SOURCE = ""
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
src_dir = "D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"

TIF_FILE_WEATHER_SATELLINE_PRECIPITATION_FOLDER = "D:\\ThanhNguyen_Working\\Python_APEX\\Perl_Africa_Weather\\data\\weather_tif_files\\precipitation\\extract\\"
TIF_FILE_WEATHER_SATELLINE_TMAX_FOLDER = "D:\\ThanhNguyen_Working\\Python_APEX\\Perl_Africa_Weather\\data\\weather_tif_files\\tmax\\extract\\"
TIF_FILE_WEATHER_SATELLINE_TMAX_FOLDER = "D:\\ThanhNguyen_Working\\Python_APEX\\Perl_Africa_Weather\\data\\weather_tif_files\\tmin\\extract\\"

message ="Usage : python Weather_Setelline_Data_Project.py -data_source <TIF or BIN> -x_max <X Max> -x_min <X Min> -y_max <Y Max> -y_min <Y Min> -start_data <Start date yyyy-mm-dd> -end_date <End date yyyy-mm-dd>"

if (sys.argv[1] == '-data_source') :
    if (sys.argv[2] is not None):
         DATA_SOURCE = str(sys.argv[2])
    else :
         print("ERROR_RUNNING_1")
         sys.exit(message)
elif (sys.argv[1] == '-help'):  
    sys.exit(message)       
else:
    print("ERROR_RUNNING_0")
    sys.exit(message)
    
def getRasterValue_ThanhNH_Float(srcfile, mx, my):
    try:  # # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
        return structval[0][0]
    except Exception,err:
        return -1
def getRasterValue_ThanhNguyen_TIF(src_file,mx,my):
    src_ds = gdal.Open(src_file) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]
def get_dly_folder_satelline_data():
    return DEF_DLY_FILES_WEATHER_SATELLINE_DATA_AFTER_CONVERT

def standard_string(line):
    line = line.strip()
    line = line.replace("         ", " ")
    line = line.replace("        ", " ")
    line = line.replace("       ", " ")
    line = line.replace("      ", " ")
    line = line.replace("     ", " ")
    line = line.replace("    ", " ")
    line = line.replace("   ", " ")
    line = line.replace("  ", " ")
    line = line.replace("\t"," ")
    return line
def requestAccessTIFFile_docToFile(PATH_DLY_FILE, X_COOR, Y_COOR, DLY_FILE_NAME):
    array_line_rainfall = []
    record_raingfall = [0,0,0,0.0]
    start_year = int(DEF_START_DATE[0:4])
    end_year = int(DEF_END_DATE[0:4])
    
    
    d1 = date(start_year, 01, 01)
    d2 = date(end_year, 12, 31)
    delta = d2 - d1
    for i in range(delta.days + 1):
        str_current_date = str(d1 + td(days=i))
        str_consider_date = str_current_date.replace("-", "")
        year = int(str_consider_date[0:4])
        month = int(str_consider_date[4:6])
        day = int(str_consider_date[6:])
        full_tif_file_name_rainfall = os.path.join(TIF_FILE_WEATHER_SATELLINE_PRECIPITATION_FOLDER,"africa_rfe.%s.tif" %(str_consider_date))
        if (not os.path.exists(full_tif_file_name_rainfall)):
            rain_fall_value_datetime = 9999.0
        else:    
            rain_fall_value_datetime = getRasterValue_ThanhNH_Float(full_tif_file_name_rainfall,X_COOR, Y_COOR)
            if (rain_fall_value_datetime == -1):
                 rain_fall_value_datetime = 9999.0
        
        tmax_value_datetime = 9999.0
        tmin_value_datetime = 9999.0
        record_raingfall = [year,month,day,rain_fall_value_datetime,tmax_value_datetime,tmin_value_datetime]
        print record_raingfall
        array_line_rainfall.append(record_raingfall)
    
    try:
       
        print(" ====Process File: %s " % (DLY_FILE_NAME))
        DLY_FILE_NAME = str(DLY_FILE_NAME) + ".DLY"
        dly_file = os.path.join(PATH_DLY_FILE,DLY_FILE_NAME)
        new_data = []
        for record_data in array_line_rainfall:
            year = record_data[0]
            month = record_data[1]
            day = record_data[2]
            tmax = float(record_data[4])
            tmin = float(record_data[5])
            rainfall = float(record_data[3])
    
            str_year = "  %s" %(str(year))
            str_month = ""
            if (int(month) >= 1 and int(month) <= 9):
                str_month = "   %s" % (str(int(month)))
            else:
                str_month = "  %s" % (str(int(month)))
            
            
            if (int(day) >= 1 and int(day) <= 9):
                str_day = "   %s" % (str(int(day)))
            else :
                str_day = "  %s" % (str(int(day)))
            
            str_date_time = str_year + str_month + str_day
            srad = " 000.0"
            
            str_tmax = ""
            if (tmax >=0) and (tmax < 10):
                str_tmax = "  %0.2f" %(tmax)
            elif (tmax >= 10) and (tmax < 100):
                str_tmax = " %0.2f" %(tmax)
            elif (tmax >= 100) and (tmax < 1000):
                str_tmax = "%0.2f" %(tmax)
            elif (tmax >= 1000) and (tmax <= 9999):  
                str_tmax = "%0.1f" %(tmax)
            elif (tmax < 0) and (tmax > -10):
                str_tmax = " %0.2f" %(tmax)
            elif (tmax <= -10) and (tmax > -100):
                str_tmax = "%0.2f" %(tmax)
            elif (tmax <= -100) and (tmax > -1000):
                str_tmax = "%0.1f" %(tmax)
                
            str_tmin = ""
            if (tmin >=0) and (tmin < 10):
                str_tmin = "  %0.2f" %(tmin)
            elif (tmin >= 10) and (tmin < 100):
                str_tmin = " %0.2f" %(tmin)
            elif (tmin >= 100) and (tmin < 1000):
                str_tmin = "%0.2f" %(tmin)
            elif (tmin >= 1000) and (tmin <= 9999):  
                str_tmin = "%0.1f" %(tmin)
            elif (tmin < 0) and (tmin > -10):
                str_tmin = " %0.2f" %(tmin)
            elif (tmin <= -10) and (tmin > -100):
                str_tmin = "%0.2f" %(tmin)
            elif (tmin <= -100) and (tmin > -1000):
                str_tmin = "%0.2f" %(tmin) 
                
            str_rainfall = ""
            if (rainfall >=0) and (rainfall < 10):
                str_rainfall = "  %0.2f" %(rainfall)
            elif (rainfall >= 10) and (rainfall < 100):
                str_rainfall = " %0.2f" %(rainfall)
            elif (rainfall >= 100) and (rainfall < 1000):
                str_rainfall = "%0.2f" %(rainfall)
            elif (rainfall >= 1000) and (rainfall <= 9999):  
                str_rainfall = "%0.1f" %(rainfall)
               
            new_line = str(str_date_time) + str(srad) + str(str_tmax) + str(str_tmin) + str(str_rainfall) + "  0.00  0.00\n"
            new_data.append(new_line)
        with open(dly_file,'w') as file:
            file.writelines(new_data)   
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
    
def requestPerlScipt_docToFile(PATH_DLY_FILE, X_COOR, Y_COOR, DLY_FILE_NAME):
    os.chdir(DEF_PERL_SCRIPT_FOLDER)
    os.system("set TZ=PST8PDT")
    #pipe = subprocess.Popen(["perl", "%s%s" %(DEF_PERL_SCRIPT_FOLDER,DEF_PERL_SCRIPT_RAINFALL_DRIVER)], stdout=subprocess.PIPE)
    params = "%s %s %s %s" %(str(X_COOR),str(Y_COOR),DEF_START_DATE,DEF_END_DATE)
    
    # Get data RainFall
    pipe = subprocess.Popen(["perl", "%s%s" %(DEF_PERL_SCRIPT_FOLDER,DEF_PERL_SCRIPT_RAINFALL_DRIVER),str(X_COOR), str(Y_COOR), DEF_START_DATE, DEF_END_DATE], stdout=subprocess.PIPE)
    first_line = pipe.stdout.readline()
    grid_infor = pipe.stdout.readline()
    array_line_rainfall = []
    line = standard_string(pipe.stdout.readline())
    while (line is not None) and (line <> ""):
        data_line = line.split(",")
        array_line_rainfall.append(data_line)
        line = standard_string(pipe.stdout.readline())
    #print array_line_rainfall
    number_rainfall_records = len(array_line_rainfall)
    print "===Number of RainFall Records : %s " % (str(number_rainfall_records))
    # Get data Tmax
    pipe = subprocess.Popen(["perl", "%s%s" %(DEF_PERL_SCRIPT_FOLDER,DEF_PERL_SCRIPT_TMAX_DRIVER),str(X_COOR), str(Y_COOR), DEF_START_DATE, DEF_END_DATE], stdout=subprocess.PIPE)
    first_line = pipe.stdout.readline()
    grid_infor = pipe.stdout.readline()
    array_line_tmax = []
    line = standard_string(pipe.stdout.readline())
    while (line is not None) and (line <> ""):
        #print line
        data_line = line.split(",")
        array_line_tmax.append(data_line)
        line = standard_string(pipe.stdout.readline())
    #print grid_infor
    number_tmax_records = len(array_line_tmax)
    #print array_line_tmax
    print "===Number of TMAX Records : %s " % (str(number_tmax_records))
    # Get data Tmax
    pipe = subprocess.Popen(["perl", "%s%s" %(DEF_PERL_SCRIPT_FOLDER,DEF_PERL_SCRIPT_TMIN_DRIVER),str(X_COOR), str(Y_COOR), DEF_START_DATE, DEF_END_DATE], stdout=subprocess.PIPE)
    first_line = pipe.stdout.readline()
    grid_infor = pipe.stdout.readline()
    array_line_tmin = []
    line = standard_string(pipe.stdout.readline())
    while (line is not None) and (line <> ""):
        #print line
        data_line = line.split(",")
        array_line_tmin.append(data_line)
        line = standard_string(pipe.stdout.readline())
    #print array_line_tmin
    number_tmin_records = len(array_line_tmin)
    
    print "===Number of TMIN Records : %s " % (str(number_tmin_records))
    
    if (number_rainfall_records >= number_tmax_records) and (number_rainfall_records >= number_tmin_records):
         for i in range(0, number_rainfall_records):
             data_rain_fall = array_line_rainfall[i]
             data_rain_fall[0] = data_rain_fall[0].strip()
             data_rain_fall[1] = data_rain_fall[1].strip()
             data_rain_fall[2] = data_rain_fall[2].strip()
            
             date_time_data_rain_fall = data_rain_fall[1].strip()
             array_line_rainfall[i] = data_rain_fall
             
             isFounded = 0
             for data_tmax in array_line_tmax:
                    date_time_data_tmax = data_tmax[1].strip()
                    if (date_time_data_rain_fall == date_time_data_tmax):
                        array_line_rainfall[i].append(data_tmax[2].strip())
                        isFounded = 1
             if (isFounded == 0):
                  array_line_rainfall[i].append(9999)
           
             isFounded = 0
             for data_tmin in array_line_tmin:
                    date_time_data_tmin = data_tmin[1].strip()
                    if (date_time_data_rain_fall == date_time_data_tmin):
                        array_line_rainfall[i].append(data_tmin[2].strip())
                        isFounded = 1
             if (isFounded == 0):
                  array_line_rainfall[i].append(9999)
        
    try:
       
        print(" ====Process File: %s " % (DLY_FILE_NAME))
        DLY_FILE_NAME = str(DLY_FILE_NAME) + ".DLY"
        dly_file = os.path.join(PATH_DLY_FILE,DLY_FILE_NAME)
        new_data = []
        for record_data in array_line_rainfall:
            date_time = record_data[1].strip().split("-")
            year = date_time[0]
            month = date_time[1]
            day = date_time[2]
            tmax = float(record_data[3])
            tmin = float(record_data[4])
            rainfall = float(record_data[2])
    
            str_year = "  %s" %(str(year))
            str_month = ""
            if (int(month) >= 1 and int(month) <= 9):
                str_month = "   %s" % (str(int(month)))
            else:
                str_month = "  %s" % (str(int(month)))
            
            
            if (int(day) >= 1 and int(day) <= 9):
                str_day = "   %s" % (str(int(day)))
            else :
                str_day = "  %s" % (str(int(day)))
            
            str_date_time = str_year + str_month + str_day
            srad = " 000.0"
            
            str_tmax = ""
            if (tmax >=0) and (tmax < 10):
                str_tmax = "  %0.2f" %(tmax)
            elif (tmax >= 10) and (tmax < 100):
                str_tmax = " %0.2f" %(tmax)
            elif (tmax >= 100) and (tmax < 1000):
                str_tmax = "%0.2f" %(tmax)
            elif (tmax >= 1000) and (tmax <= 9999):  
                str_tmax = "%0.1f" %(tmax)
            elif (tmax < 0) and (tmax > -10):
                str_tmax = " %0.2f" %(tmax)
            elif (tmax <= -10) and (tmax > -100):
                str_tmax = "%0.2f" %(tmax)
            elif (tmax <= -100) and (tmax > -1000):
                str_tmax = "%0.1f" %(tmax)
                
            str_tmin = ""
            if (tmin >=0) and (tmin < 10):
                str_tmin = "  %0.2f" %(tmin)
            elif (tmin >= 10) and (tmin < 100):
                str_tmin = " %0.2f" %(tmin)
            elif (tmin >= 100) and (tmin < 1000):
                str_tmin = "%0.2f" %(tmin)
            elif (tmin >= 1000) and (tmin <= 9999):  
                str_tmin = "%0.1f" %(tmin)
            elif (tmin < 0) and (tmin > -10):
                str_tmin = " %0.2f" %(tmin)
            elif (tmin <= -10) and (tmin > -100):
                str_tmin = "%0.2f" %(tmin)
            elif (tmin <= -100) and (tmin > -1000):
                str_tmin = "%0.2f" %(tmin) 
                
            str_rainfall = ""
            if (rainfall >=0) and (rainfall < 10):
                str_rainfall = "  %0.2f" %(rainfall)
            elif (rainfall >= 10) and (rainfall < 100):
                str_rainfall = " %0.2f" %(rainfall)
            elif (rainfall >= 100) and (rainfall < 1000):
                str_rainfall = "%0.2f" %(rainfall)
            elif (rainfall >= 1000) and (rainfall <= 9999):  
                str_rainfall = "%0.1f" %(rainfall)
               
            new_line = str(str_date_time) + str(srad) + str(str_tmax) + str(str_tmin) + str(str_rainfall) + "  0.00  0.00\n"
            new_data.append(new_line)
        with open(dly_file,'w') as file:
            file.writelines(new_data)   
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))    
def copyFile(file_path, des):
    try:
        shutil.copy(file_path, des)
    except Exception, err:
        print err
        pass    
def Build_Africa_DLY_Library():
    x = X_MIN
    while (x <= X_MAX):
        y = Y_MIN
        while (y <= Y_MAX):
             print "X = %s ; Y = %s" %(str(x), str(y))
             try:
                  slate_weather_tif = getRasterValue_ThanhNguyen_TIF(src_dir + tif_slate_weather, x, y);
                  if (slate_weather_tif == 2147483647) or (str(slate_weather_tif) == "2147483647"):
                        print "Location is not mapped : " + str(slate_weather_tif)
                  else :
                        if (DATA_SOURCE.upper().strip() == "BIN"):
                            requestPerlScipt_docToFile(DEF_DLY_FILES_WEATHER_SATELLINE_DATA_AFTER_CONVERT, x, y, "RFE_" + str(x) + "_" + str(y) + "_" + str(slate_weather_tif))
                        elif (DATA_SOURCE.upper().strip() == "TIF"):
                            requestAccessTIFFile_docToFile(DEF_DLY_FILES_WEATHER_SATELLINE_DATA_AFTER_CONVERT, x, y, "RFE_" + str(x) + "_" + str(y) + "_" + str(slate_weather_tif))
                        else:    
                            print "ERROR_PRINTING_10"
                            sys.exit(message)
                        SOURCE = os.path.join(DEF_DLY_FILES_WEATHER_SATELLINE_DATA_AFTER_CONVERT, "RFE_" + str(x) + "_" + str(y) + "_" + str(slate_weather_tif) + ".DLY")
                        DES = os.path.join("D:\\ThanhNguyen_Working\\Python_APEX\\SATELLINE_WEATHER_DATA","WEATHER_DLY_FILES _SLATE")
                        copyFile(SOURCE, DES)
                        OLD_FILE = os.path.join(DES,"RFE_" + str(x) + "_" + str(y) + "_" + str(slate_weather_tif) + ".DLY")
                        NEW_FILE = os.path.join(DES,str(slate_weather_tif) + ".DLY")
                        os.rename(OLD_FILE, NEW_FILE)
             except Exception, err:
                  pass 
             y = y + 0.25
        x = x + 0.25
Build_Africa_DLY_Library()
