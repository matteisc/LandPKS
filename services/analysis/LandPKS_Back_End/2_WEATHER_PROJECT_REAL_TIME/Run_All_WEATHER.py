# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
import os
import sys

if (len(sys.argv) < 6):
    os.system("python Step_1_preprocessing_WEATHER.py -in C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT/Weather_Files/map_location.csv -ou Weather_Files/complete_map_location.csv -tif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/")
    os.system("python Step_2_convert_wtg_to_dly_WEATHER.py -Fwtg D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/SLATE_Weather/wtg/ -Fdly C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT/Weather_Files/Daily_Weather_Files")
    os.system("python Step_3_main_WEATHER.py -f /Weather_Files/Daily_Weather_Files")
    os.system("python Step_4_postprocessing_WEATHER.py -Fcsv C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT/Weather_Files/complete_map_location.csv -Fwp1 C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT/Weather_Files/Complete_WP1_Files -Ftif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/global_wind_tifs/ -Wyear 2001")
else:
    X_Coor = 0.00
    Y_Coor = 0.00
    ID = ""
    if (sys.argv[1] == '-x'):
        if (float(sys.argv[2])):
            X_Coor = float(sys.argv[2])
        else:
            sys.exit("====[Error] : Error in X")
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
    
    os.system("python Step_1_preprocessing_WEATHER_Real_Time.py -x %f -y %f -tif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -id %s" %(X_Coor,Y_Coor,ID))
    
    cmd = "python Step_4_postprocessing_WEATHER_Real_Time.py -Fcsv C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/complete_map_location.csv -Fwp1 C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/Weather_Files/Private/%s/Complete_WP1_Files -Ftif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/global_wind_tifs/ -Wyear 2001" %(str(ID),str(ID))
       
    #print cmd
    os.system(cmd)
