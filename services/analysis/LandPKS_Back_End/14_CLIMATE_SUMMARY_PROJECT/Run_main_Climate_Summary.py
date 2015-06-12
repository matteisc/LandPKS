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

from support import support_Climate_Summary
from __builtin__ import int

ID = 0
ACTION_FLAG = 1
TIF_FOLDER_COMM = ""
RECORD_NAME = ""
X_Coor = 0.0
Y_Coor = 0.0

#print len(sys.argv)

if (len(sys.argv) <> 12 and len(sys.argv) <> 2):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Run_main_AWC.py -run -x <X Coordinate> -y <Y Coordinate> -name <Record Name> -ID <Record ID> -tif <Directory to Folder contain all TIF Files>")
else:
    if (sys.argv[1] == '-run' and sys.argv[2] == '-x'):
        ACTION_FLAG = 1
        if (float(sys.argv[3])):
            X_Coor = float(sys.argv[3])
        else:
            sys.exit("====[Error] : Error in X")
        
        if (sys.argv[4] == '-y'):
            if (float(sys.argv[5])):
               Y_Coor = float(sys.argv[5])
            else:
               sys.exit("====[Error] : Error in Y")
        else:
            sys.exit("====[Error] : Error in Y")
        
        if (sys.argv[6] == '-name'):
            if (sys.argv[7] is None) :
               sys.exit(message)
            else:
               RECORD_NAME = str(sys.argv[7])
        else:
            sys.exit("====[Error] : Error in ID")
            
        if (sys.argv[8] == '-ID'):
            if (sys.argv[9] is None) :
               sys.exit(message)
            else:
               ID = str(sys.argv[9])
        else:
            sys.exit("====[Error] : Error in ID") 
            
        if (sys.argv[10] == '-tif'):
            if (sys.argv[11] is None) :
               sys.exit(message)
            else:
               TIF_FOLDER_COMM = str(sys.argv[11])
        else:
            sys.exit("====[Error] : Error in TIF")       
               
    elif (sys.argv[1] == '-rm_real_time'):
        ACTION_FLAG = 0
    elif (sys.argv[1] == '-rm_all'):
        ACTION_FLAG = 2
    else:
        sys.exit("====[Error] : Error in X")
 

def main():
    if (ACTION_FLAG == 1):
       #if (TIF_FOLDER_COMM is None):
       TIF_FOLDER_COMM = "E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"
       
       TIF_PRECIP_MON_JAN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_01_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_FEB = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_02_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_MAR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_03_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_APR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_04_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_MAY = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_05_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_JUN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_06_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_JUL = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_07_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_AUG = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_08_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_SEP = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_09_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_OCT = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_10_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_NOV = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_11_1971_2013.tif", X_Coor, Y_Coor)
       TIF_PRECIP_MON_DEC = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_12_1971_2013.tif", X_Coor, Y_Coor)
       climate_precip_data_list = [TIF_PRECIP_MON_JAN,TIF_PRECIP_MON_FEB,TIF_PRECIP_MON_MAR,TIF_PRECIP_MON_APR,TIF_PRECIP_MON_MAY,TIF_PRECIP_MON_JUN,TIF_PRECIP_MON_JUL,TIF_PRECIP_MON_AUG,TIF_PRECIP_MON_SEP,TIF_PRECIP_MON_OCT,TIF_PRECIP_MON_NOV,TIF_PRECIP_MON_DEC]
       
       
       TIF_AVG_TEMP_MON_JAN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_01_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_FEB = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_02_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_MAR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_03_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_APR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_04_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_MAY = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_05_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_JUN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_06_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_JUL = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_07_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_AUG = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_08_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_SEP = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_09_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_OCT = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_10_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_NOV = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_11_1971_2013.tif", X_Coor, Y_Coor)
       TIF_AVG_TEMP_MON_DEC = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_12_1971_2013.tif", X_Coor, Y_Coor)
       climate_avg_temp_data_list = [TIF_AVG_TEMP_MON_JAN,TIF_AVG_TEMP_MON_FEB,TIF_AVG_TEMP_MON_MAR,TIF_AVG_TEMP_MON_APR,TIF_AVG_TEMP_MON_MAY,TIF_AVG_TEMP_MON_JUN,TIF_AVG_TEMP_MON_JUL,TIF_AVG_TEMP_MON_AUG,TIF_AVG_TEMP_MON_SEP,TIF_AVG_TEMP_MON_OCT,TIF_AVG_TEMP_MON_NOV,TIF_AVG_TEMP_MON_DEC]
       
       
       TIF_MAX_TEMP_MON_JAN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_01_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_FEB = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_02_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_MAR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_03_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_APR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_04_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_MAY = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_05_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_JUN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_06_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_JUL = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_07_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_AUG = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_08_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_SEP = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_09_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_OCT = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_10_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_NOV = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_11_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MAX_TEMP_MON_DEC = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_12_1971_2013.tif", X_Coor, Y_Coor)
       climate_max_temp_data_list = [TIF_MAX_TEMP_MON_JAN,TIF_MAX_TEMP_MON_FEB,TIF_MAX_TEMP_MON_MAR,TIF_MAX_TEMP_MON_APR,TIF_MAX_TEMP_MON_MAY,TIF_MAX_TEMP_MON_JUN,TIF_MAX_TEMP_MON_JUL,TIF_MAX_TEMP_MON_AUG,TIF_MAX_TEMP_MON_SEP,TIF_MAX_TEMP_MON_OCT,TIF_MAX_TEMP_MON_NOV,TIF_MAX_TEMP_MON_DEC]
       
       
       TIF_MIN_TEMP_MON_JAN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_01_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_FEB = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_02_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_MAR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_03_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_APR = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_04_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_MAY = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_05_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_JUN = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_06_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_JUL = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_07_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_AUG = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_08_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_SEP = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_09_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_OCT = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_10_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_NOV = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_11_1971_2013.tif", X_Coor, Y_Coor)
       TIF_MIN_TEMP_MON_DEC = support_Climate_Summary.getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_12_1971_2013.tif", X_Coor, Y_Coor)
       climate_min_temp_data_list = [TIF_MIN_TEMP_MON_JAN,TIF_MIN_TEMP_MON_FEB,TIF_MIN_TEMP_MON_MAR,TIF_MIN_TEMP_MON_APR,TIF_MIN_TEMP_MON_MAY,TIF_MIN_TEMP_MON_JUN,TIF_MIN_TEMP_MON_JUL,TIF_MIN_TEMP_MON_AUG,TIF_MIN_TEMP_MON_SEP,TIF_MIN_TEMP_MON_OCT,TIF_MIN_TEMP_MON_NOV,TIF_MIN_TEMP_MON_DEC]
       
       support_Climate_Summary.insert_climate_summary_data_output(ID,RECORD_NAME,Y_Coor,X_Coor, climate_precip_data_list,climate_avg_temp_data_list,climate_max_temp_data_list,climate_min_temp_data_list)
    elif (ACTION_FLAG == 0):
       print "Thanh Nguyen"
    elif (ACTION_FLAG == 2):
       print "Thanh Nguyen" 
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
