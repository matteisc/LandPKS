# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
from netCDF4 import Dataset
from __builtin__ import len
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy
import shutil
import datetime
# READING INPUTS
X_COOR= 0.0
Y_COOR= 0.0
START_YEAR = 1980
END_YEAR = 2010

TIF_FOLDER_COMM = "E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'

ARMERRA_SOURCE_NC4_FILES = "E:\\ThanhNguyen_Working\\Python_APEX\\NASA_WEATHERE_DATASETS_AGMIP\\AGMERRA\\"
POST_FIX_PRATE = "prate"
POST_FIX_TMAX = "tmax"
POST_FIX_TMIN = "tmin"
POST_FIX_SRAD = "srad"
POST_RELATIVE_HUMIDITY = "rhstmax"
POST_FIX_WIND = "wndspd"
PATH_DLY_FILE = "E:\\ThanhNguyen_Working\\Python_APEX\\NASA_WEATHERE_DATASETS_AGMIP\\FINAL_DLY_FILES\\"
    
if (sys.argv[1] == '-x') :
    if ((sys.argv[2] is not None) and (float(sys.argv[2]))):
         X_COOR = float(sys.argv[2])
    else :
         print("ERROR_RUNNING_1")
         sys.exit(message)
    
    if (sys.argv[3] == '-y') :
      if ((sys.argv[4] is not None) and (float(sys.argv[4]))):
            Y_COOR = float(sys.argv[4])
      else :
         print("ERROR_RUNNING_2")
         sys.exit(message)  
    else :
      print("ERROR_RUNNING_3")
      sys.exit(message)

    if (sys.argv[5] == '-start_year') :
      if ((sys.argv[6] is not None) and (int(sys.argv[6]))):
         START_YEAR = int(sys.argv[6])
      else :
         print("ERROR_RUNNING_4")
         sys.exit(message)  
    else :
      print("ERROR_RUNNING_5")
      sys.exit(message)
      
    if (sys.argv[7] == '-end_year') :
      if ((sys.argv[8] is not None) and (int(sys.argv[8]))):
         END_YEAR = int(sys.argv[8])
      else :
         print("ERROR_RUNNING_6")
         sys.exit(message)  
    else :
      print("ERROR_RUNNING_7")
      sys.exit(message)
else:
    print("ERROR_RUNNING_8")
    sys.exit(message)

#################################################
####MAIN
#################################################
def getRasterValue_ThanhNguyen_TIF(src_file,mx,my):
    try:
        src_ds = gdal.Open(src_file) 
        gt = src_ds.GetGeoTransform() 
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception, err:
        return -999
def find_index(value, array):
    size = len(array)
    index = 0
    while (index < size):
        if (float(array[index]) == float(value)):
            return index
        else :
            if (float(array[index]) < float(value) and float(array[index+1]) > float(value)):
                avg = (float(array[index]) +  float(array[index+1])) / 2
                if (float(value) > avg):
                    return (index + 1)
                else:    
                    return index
            elif (float(array[index]) > float(value) and float(array[index+1]) < float(value)):
                avg = (float(array[index]) +  float(array[index+1])) / 2
                if (float(value) > avg):
                    return index
                else:    
                    return index + 1
        index = index + 1
    return None
def check_compatible(time,lat,long):
   if (len(time) == 366 or len(time) == 365):
       if (len(long) == 1440 and len(lat) == 720):
           if (lat[0] == 89.875 and lat[719] == -89.875):
               if (long[0] == 0.125 and long[1439] == 359.875):
                   return 1
           else:
               return -1    
       else:
           return -1
   else:
       return -1
def create_DLY_Files(dly_file_name, LST_DATA_RECORD):
     try:
        print(" ====Process File: %s " % (dly_file_name))
        dly_file_name = str(dly_file_name) + ".DLY"
        dly_file = os.path.join(PATH_DLY_FILE,dly_file_name)
        new_data = []
        for record_data in LST_DATA_RECORD:
           
            year = record_data[0][0]
            month = record_data[0][1]
            day = record_data[0][2]
            srad = float(record_data[0][7])
            tmax = float(record_data[0][5])
            tmin = float(record_data[0][6])
            rainfall = float(record_data[0][4])
            relative_humidity = float(record_data[0][8])
            frag_relative_humidity = relative_humidity / 100
            wind_speed = float(record_data[0][9])
            
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
            
            str_srad = ""
            if (srad >=0) and (srad < 10):
                str_srad = "  %0.2f" %(srad)
            elif (srad >= 10) and (srad < 100):
                str_srad = " %0.2f" %(srad)
            elif (srad >= 100) and (srad < 1000):
                str_srad = "%0.2f" %(srad)
            elif (srad >= 1000) and (srad <= 9999):  
                str_srad = "%0.1f" %(srad)
           
            
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
                
            str_relative_humidity = ""
            if (frag_relative_humidity >= 0) and (frag_relative_humidity < 10):
                str_relative_humidity = "  %0.2f" %(frag_relative_humidity)
            elif (frag_relative_humidity >= 10) and (frag_relative_humidity < 100):
                str_relative_humidity = " %0.2f" %(frag_relative_humidity)
            elif (frag_relative_humidity >= 100) and (frag_relative_humidity < 1000):
                str_relative_humidity = "%0.2f" %(frag_relative_humidity)
            elif (frag_relative_humidity >= 1000) and (frag_relative_humidity <= 9999):  
                str_relative_humidity = "%0.1f" %(frag_relative_humidity)
                
            str_wind_speed = ""
            if (wind_speed >= 0) and (wind_speed < 10):
                str_wind_speed = "  %0.2f" %(wind_speed)
            elif (wind_speed >= 10) and (wind_speed < 100):
                str_wind_speed = " %0.2f" %(wind_speed)
            elif (wind_speed >= 100) and (wind_speed < 1000):
                str_wind_speed = "%0.2f" %(wind_speed)
            elif (wind_speed >= 1000) and (wind_speed <= 9999):  
                str_wind_speed = "%0.1f" %(wind_speed)               
            new_line = str(str_date_time) + str(str_srad) + str(str_tmax) + str(str_tmin) + str(str_rainfall) + str(str_relative_humidity) + str(str_wind_speed) + "\n"
            new_data.append(new_line)

        with open(dly_file,'w') as file:
            file.writelines(new_data)   
     except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
def main():
    print "Thanh Nguyen Hai"
    DLY_FILE_NAME = ""
    try:
        DLY_FILE_NAME = getRasterValue_ThanhNguyen_TIF(TIF_FOLDER_COMM + tif_slate_weather, X_COOR, Y_COOR)
        if (DLY_FILE_NAME == -999):
            sys.exit("STOP : LOCATION IS NOT SUPPORT")
    except:
        pass
    print DLY_FILE_NAME
    if (DLY_FILE_NAME == -999 or DLY_FILE_NAME == "-999" or DLY_FILE_NAME == 2147483647 or DLY_FILE_NAME == "2147483647"):
            sys.exit("STOP : LOCATION IS NOT SUPPORT")
    
    if (os.path.exists(os.path.join(PATH_DLY_FILE,str(DLY_FILE_NAME) + ".DLY" ))):
            sys.exit("STOP : FILE %s EXISTED" %(str(DLY_FILE_NAME)))
            
    DATA_RECORD = [0,0,0,0,0.0,0.0,0.0,0.0,0.0,0.0]
    LIST_DATA_RECORD = []
    #GET DATA OF RAIN FALL == PRECIPITATION = PRATE 
    year = START_YEAR
    while (year <= END_YEAR):
        print "\n Consider Year : %d" %(year) 
        ##########################################
        #########PRECIPITATION RATE###############
        ##########################################
        prate_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_FIX_PRATE)
        rootgrp_prate = Dataset(prate_nc4_file_for_this_year, 'r', format='NETCDF4')
        time = rootgrp_prate.variables['time']
        long = rootgrp_prate.variables['longitude']
        lat = rootgrp_prate.variables['latitude']
        if (check_compatible(time, lat, long) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("Prate data is not compatible")
        
        ##########################################
        #########TMAX VALUE#######################
        ##########################################
        tmax_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_FIX_TMAX)
        rootgrp_tmax = Dataset(tmax_nc4_file_for_this_year, 'r', format='NETCDF4')
        time_tmax = rootgrp_tmax.variables['time']
        long_tmax = rootgrp_tmax.variables['longitude']
        lat_tmax = rootgrp_tmax.variables['latitude']
        if (check_compatible(time_tmax, lat_tmax, long_tmax) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("Tmax data is not compatible")
            
        ##########################################
        #########TMIN VALUE#######################
        ##########################################
        tmin_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_FIX_TMIN)
        rootgrp_tmin = Dataset(tmin_nc4_file_for_this_year, 'r', format='NETCDF4')
        time_tmin = rootgrp_tmin.variables['time']
        long_tmin = rootgrp_tmin.variables['longitude']
        lat_tmin = rootgrp_tmin.variables['latitude']
        if (check_compatible(time_tmin, lat_tmin, long_tmin) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("Tmin data is not compatible")
        
        
        ##########################################
        #########SRAD VALUE#######################
        ##########################################
        srad_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_FIX_SRAD)
        rootgrp_srad = Dataset(srad_nc4_file_for_this_year, 'r', format='NETCDF4')
        time_srad = rootgrp_srad.variables['time']
        long_srad = rootgrp_srad.variables['longitude']
        lat_srad = rootgrp_srad.variables['latitude']
        if (check_compatible(time_srad, lat_srad, long_srad) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("SRAD data is not compatible")
            
        
        ##########################################
        #########RHSTMAX VALUE####################
        ##########################################
        rhstmax_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_RELATIVE_HUMIDITY)
        rootgrp_rhstmax = Dataset(rhstmax_nc4_file_for_this_year, 'r', format='NETCDF4')
        time_rhstmax = rootgrp_rhstmax.variables['time']
        long_rhstmax = rootgrp_rhstmax.variables['longitude']
        lat_rhstmax = rootgrp_rhstmax.variables['latitude']
        if (check_compatible(time_rhstmax, lat_rhstmax, long_rhstmax) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("RHSTMAX data is not compatible")
        
        ##########################################
        #########wndspd VALUE#######################
        ##########################################
        wndspd_nc4_file_for_this_year = ARMERRA_SOURCE_NC4_FILES + "AgMERRA_%s_%s.nc4" %(str(year),POST_FIX_WIND)
        rootgrp_wndspd = Dataset(wndspd_nc4_file_for_this_year, 'r', format='NETCDF4')
        time_wndspd = rootgrp_wndspd.variables['time']
        long_wndspd = rootgrp_wndspd.variables['longitude']
        lat_wndspd = rootgrp_wndspd.variables['latitude']
        if (check_compatible(time_wndspd, lat_wndspd, long_wndspd ) == -1):
            print("ERROR_RUNNING_10")
            sys.exit("RHSTMAX data is not compatible")
        
        
        #Nguy hiem khi find index X : Luu y : Neu x in [0,180] => Giu nguyen gia tri X de tim kiem
        #Neu X in [-180;0] => Thi phai quy doi ra he 0 - 360
        X_COOR_2 = X_COOR
        if (float(X_COOR) < 0.0 and float(X_COOR) >= -180.0):
            X_COOR_2 = 360 + float(X_COOR)
            
        
        index_X = find_index(X_COOR_2, long)
        if (index_X is None):
            sys.exit("X Coordinate data is not compatible")
        print "index cua x = %f la : %d " %( X_COOR_2 ,index_X)
        #print long[0]
        #print long[:]
        #print long[1439]
        index_Y = find_index(Y_COOR, lat)
        if (index_X is None):
            sys.exit("Y Coordinate data is not compatible")
        print "index cua y = %f la : %d " %( Y_COOR ,index_Y)
        #print index_Y
        #print lat[720]
        
        index_date_in_year = 0
        max_index_date_in_year = len(time)        
        print max_index_date_in_year 
        
        while (index_date_in_year < max_index_date_in_year):
            d = datetime.date(year, 1, 1) + datetime.timedelta(index_date_in_year)
            month = d.month
            date = d.day
            
            #Process for Precipitation Rate
            DATA_RECORD[0] = year
            DATA_RECORD[1] = month
            DATA_RECORD[2] = date
            DATA_RECORD[3] = index_date_in_year
            prate = rootgrp_prate.variables['prate']
            prate_value = prate[index_date_in_year,index_Y,index_X]
            if (not is_number(prate_value) or str(prate_value) == "--"):
                prate_value = 9999.0
            DATA_RECORD[4] = prate_value
            #Process for TMAX Rate
            tmax = rootgrp_tmax.variables['tmax']
            tmax_value = tmax[index_date_in_year,index_Y,index_X]
            if (tmax_value is None or str(tmax_value).strip() == "" or not is_number(tmax_value) or str(tmax_value).strip() == "--"):
                tmax_value = 9999.0
            DATA_RECORD[5] = tmax_value
            
            #Process for TMIN Rate
            tmin = rootgrp_tmin.variables['tmin']
            tmin_value = tmin[index_date_in_year,index_Y,index_X]
            if (tmin_value is None or str(tmin_value).strip() == "" or not is_number(tmin_value) or str(tmin_value).strip() == "--"):
                tmin_value = 9999.0
            DATA_RECORD[6] = tmin_value
            
            #Process for SRAD Rate
            srad = rootgrp_srad.variables['srad']
            srad_value = srad[index_date_in_year,index_Y,index_X]
            if (srad_value is None or str(srad_value).strip() == "" or not is_number(srad_value) or str(srad_value).strip() == "--"):
                srad_value = 9999.0
            DATA_RECORD[7] = srad_value
            
            #Process for HUMIDITY Rate
            rhstmax = rootgrp_rhstmax.variables['rhstmax']
            rhstmax_value = rhstmax[index_date_in_year,index_Y,index_X]
            if (rhstmax_value is None or str(rhstmax_value).strip() == "" or not is_number(rhstmax_value) or str(rhstmax_value).strip() == "--"):
                rhstmax_value = 9999.0
            DATA_RECORD[8] = rhstmax_value
            
            #Process for HUMIDITY Rate
            wndspd = rootgrp_wndspd.variables['wndspd']
            wndspd_value = wndspd[index_date_in_year,index_Y,index_X]
            if (wndspd_value is None or str(wndspd_value).strip() == "" or not is_number(wndspd_value) or str(wndspd_value).strip() == "--"):
                wndspd_value = 9999.0
            DATA_RECORD[9] = wndspd_value
            
            print "-----------------------------------------------------"
            print "%d  ;  %d  ;  %d  ;  %d  ;  X=%f  ;  Y=%f  ;  INDEX_X=%d  ;  INDEX_Y=%d  ;  PRATE = %6.2f  ;  TMAX = %6.2f  ;  TMIN = %6.2f  ;  SRAD = %6.2f  ; RELATIVE_HUMIDIDY = %6.2f   ;   WIND = %6.2f" %(year,month,date,index_date_in_year,X_COOR,Y_COOR,index_X,index_Y,prate_value,tmax_value,tmin_value,srad_value,rhstmax_value,wndspd_value)
            
            LIST_DATA_RECORD.append((list(DATA_RECORD), DATA_RECORD[0]))
            index_date_in_year = index_date_in_year + 1
        ##########################################
        year = year + 1
        
        create_DLY_Files(DLY_FILE_NAME,LIST_DATA_RECORD)
        

if __name__ == '__main__':
    main()    
