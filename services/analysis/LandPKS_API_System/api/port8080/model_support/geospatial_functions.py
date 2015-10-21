'''
Created on Apr 21, 2015

@author: Thanh Nguyen Hai
'''
try:
    from osgeo import gdal, ogr
    import numpy
except Exception, err:
    print err
    sys.exit("Please install GDAL for Python")
import os
import sys
import collections

DATABASE_HOST_IP = "127.0.0.1"
DATABASE_NAME = "apex"
DATABASE_USER = "root"
DATABASE_PASS = ""

DEFINE_PRECIPITATION = "PRECIPITATION"
DEFINE_TEMPERATURE_MAX = "TMAX"
DEFINE_TEMPERATURE_MIN = "TMIN"
DEFINE_TEMPERATURE_AVG = "TAVG"

TIF_FOLDER_COMM = "D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/"

class MultipleLevelsOfDictionary(collections.OrderedDict):
    def __getitem__(self,item):
        try:
            return collections.OrderedDict.__getitem__(self,item)
        except:
            value = self[item] = type(self)()
            return value
def getRasterValue_ThanhNH(srcfile, mx, my):  
    try:  # # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception, err:
        return -1
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
        print err
        return -999
def get_value_fao_lgp_from_gdal_value_MySQL_DATABASE(gdal_gdd):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT lgp_value as label FROM landpks_gdal_fao_lgp_lookup WHERE gdal_value = %s" % (str(gdal_gdd).strip())
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None):
                return row[0]
       return None
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def get_average_value_for_period_time_AgMERRA(month, start_year, end_year, type, X_Coor, Y_Coor):
    total_value = 0.0
    for year in range(start_year, end_year + 1):
        str_year = str(year)
        if (type.strip().upper() == DEFINE_PRECIPITATION):
           TIF_FILE = TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF/AgMERRA_Prate_Monthly/%s_%s.tif" %(str(month),str(year))
        elif (type.strip().upper() == DEFINE_TEMPERATURE_AVG):
           TIF_FILE = TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF/AgMERRA_TAvg_Monthly/%s_%s.tif" %(str(month),str(year))
        elif (type.strip().upper() == DEFINE_TEMPERATURE_MAX):
           TIF_FILE = TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF/AgMERRA_TMax_Monthly/%s_%s.tif" %(str(month),str(year))
        elif (type.strip().upper() == DEFINE_TEMPERATURE_MIN):
           TIF_FILE = TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF/AgMERRA_TMin_Monthly/%s_%s.tif" %(str(month),str(year))
        else:
           TIF_FILE = TIF_FOLDER_COMM
               
        single_value = float(getRasterValue_ThanhNH_Float(TIF_FILE,X_Coor,Y_Coor))
        #print str(month) + ":" + str(year) + ":" + str(single_value) + ":" + str(type) + ":" + str(total_value)
        total_value = total_value + single_value
    return float(total_value) / (end_year - start_year + 1)
    #return total_value        
def get_climate_information_from_AgMERRA_Data(X_COOR,Y_COOR):
    d = MultipleLevelsOfDictionary()
    d['precipitation']['january'] = get_average_value_for_period_time_AgMERRA('01',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['february'] = get_average_value_for_period_time_AgMERRA('02',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['march'] = get_average_value_for_period_time_AgMERRA('03',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['april'] = get_average_value_for_period_time_AgMERRA('04',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['may'] = get_average_value_for_period_time_AgMERRA('05',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['june'] = get_average_value_for_period_time_AgMERRA('06',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['july'] = get_average_value_for_period_time_AgMERRA('07',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['august'] = get_average_value_for_period_time_AgMERRA('08',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['september'] = get_average_value_for_period_time_AgMERRA('09',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['october'] = get_average_value_for_period_time_AgMERRA('10',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['november'] = get_average_value_for_period_time_AgMERRA('11',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['december'] = get_average_value_for_period_time_AgMERRA('12',1980,2010,DEFINE_PRECIPITATION,X_COOR,Y_COOR)
    d['precipitation']['annual'] = float(d['precipitation']['january']) + float(d['precipitation']['february']) + float(d['precipitation']['march']) + float(d['precipitation']['april']) + float(d['precipitation']['may']) + float(d['precipitation']['june']) + float(d['precipitation']['july']) + float(d['precipitation']['august']) + float(d['precipitation']['september']) + float(d['precipitation']['october']) + float(d['precipitation']['november']) + float(d['precipitation']['december']) 
    
    
    d['average_temperature']['january'] = get_average_value_for_period_time_AgMERRA('01',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['february'] = get_average_value_for_period_time_AgMERRA('02',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['march'] = get_average_value_for_period_time_AgMERRA('03',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['april'] = get_average_value_for_period_time_AgMERRA('04',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['may'] = get_average_value_for_period_time_AgMERRA('05',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['june'] = get_average_value_for_period_time_AgMERRA('06',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['july'] = get_average_value_for_period_time_AgMERRA('07',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['august'] = get_average_value_for_period_time_AgMERRA('08',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['september'] = get_average_value_for_period_time_AgMERRA('09',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['october'] = get_average_value_for_period_time_AgMERRA('10',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['november'] = get_average_value_for_period_time_AgMERRA('11',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    d['average_temperature']['december'] = get_average_value_for_period_time_AgMERRA('12',1980,2010,DEFINE_TEMPERATURE_AVG,X_COOR,Y_COOR)
    
    d['max_temperature']['january'] = get_average_value_for_period_time_AgMERRA('01',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['february'] = get_average_value_for_period_time_AgMERRA('02',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['march'] = get_average_value_for_period_time_AgMERRA('03',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['april'] = get_average_value_for_period_time_AgMERRA('04',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['may'] = get_average_value_for_period_time_AgMERRA('05',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['june'] = get_average_value_for_period_time_AgMERRA('06',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['july'] = get_average_value_for_period_time_AgMERRA('07',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['august'] = get_average_value_for_period_time_AgMERRA('08',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['september'] = get_average_value_for_period_time_AgMERRA('09',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['october'] = get_average_value_for_period_time_AgMERRA('10',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['november'] = get_average_value_for_period_time_AgMERRA('11',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    d['max_temperature']['december'] = get_average_value_for_period_time_AgMERRA('12',1980,2010,DEFINE_TEMPERATURE_MAX,X_COOR,Y_COOR)
    return d
def get_climate_information_from_AgMERRA_Data_LTA(X_Coor,Y_Coor):
    d = MultipleLevelsOfDictionary()
    d['precipitation']['january'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate01_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['february'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate02_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['march'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate03_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['april'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate04_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['may'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate05_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['june'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate06_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['july'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate07_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['august'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate08_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['september'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate09_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['october'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate10_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['november'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate11_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['december'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/PRECIP_Monthly/Prate12_1980_2010.tif", X_Coor, Y_Coor)
    d['precipitation']['annual'] = float(d['precipitation']['january']) + float(d['precipitation']['february']) + float(d['precipitation']['march']) + float(d['precipitation']['april']) + float(d['precipitation']['may']) + float(d['precipitation']['june']) + float(d['precipitation']['july']) + float(d['precipitation']['august']) + float(d['precipitation']['september']) + float(d['precipitation']['october']) + float(d['precipitation']['november']) + float(d['precipitation']['december']) 
    
    
    d['average_temperature']['january'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_01_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['february'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_02_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['march'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_03_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['april'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_04_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['may'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_05_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['june'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_06_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['july'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_07_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['august'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_08_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['september'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_09_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['october'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_10_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['november'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_11_1980_2010.tif", X_Coor, Y_Coor)
    d['average_temperature']['december'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/AVG_TEMP_Monthly/tmp_12_1980_2010.tif", X_Coor, Y_Coor)
    
    d['max_temperature']['january'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_01_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['february'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_02_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['march'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_03_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['april'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_04_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['may'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_05_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['june'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_06_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['july'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_07_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['august'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_08_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['september'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_09_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['october'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_10_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['november'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_11_1980_2010.tif", X_Coor, Y_Coor)
    d['max_temperature']['december'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMAX_Monthly/tmax_12_1980_2010.tif", X_Coor, Y_Coor)
    
    d['min_temperature']['january'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_01_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['february'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_02_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['march'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_03_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['april'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_04_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['may'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_05_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['june'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_06_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['july'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_07_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['august'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_08_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['september'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_09_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['october'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_10_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['november'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_11_1980_2010.tif", X_Coor, Y_Coor)
    d['min_temperature']['december'] = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AGMERRA_TIF_LTA/TMIN_Monthly/tmin_12_1980_2010.tif", X_Coor, Y_Coor)
    return d
def get_climate_data_set(X_Coor,Y_Coor,Source):    
       data = MultipleLevelsOfDictionary()
       data['longitude'] = X_Coor
       data['latitude'] = Y_Coor
       data['data_source'] = Source
       
       d = MultipleLevelsOfDictionary()
       if (Source == "CRU"):
           TIF_PRECIP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_01_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['january'] = float(TIF_PRECIP_MON_JAN)
           TIF_PRECIP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_02_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['february'] = float(TIF_PRECIP_MON_FEB)
           TIF_PRECIP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_03_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['march'] = float(TIF_PRECIP_MON_MAR)
           TIF_PRECIP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_04_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['april'] = float(TIF_PRECIP_MON_APR)
           TIF_PRECIP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_05_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['may'] = float(TIF_PRECIP_MON_MAY)
           TIF_PRECIP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_06_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['june'] = float(TIF_PRECIP_MON_JUN)
           TIF_PRECIP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_07_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['july'] = float(TIF_PRECIP_MON_JUL)
           TIF_PRECIP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_08_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['august'] = float(TIF_PRECIP_MON_AUG)
           TIF_PRECIP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_09_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['september'] = float(TIF_PRECIP_MON_SEP)
           TIF_PRECIP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_10_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['october'] = float(TIF_PRECIP_MON_OCT)
           TIF_PRECIP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_11_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['november'] = float(TIF_PRECIP_MON_NOV)
           TIF_PRECIP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/PRECIP_Monthly/ma_prec_12_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['december'] = float(TIF_PRECIP_MON_DEC)
           d['precipitation']['annual'] = float(TIF_PRECIP_MON_JAN) + float(TIF_PRECIP_MON_FEB) + float(TIF_PRECIP_MON_MAR) + float(TIF_PRECIP_MON_APR) + float(TIF_PRECIP_MON_MAY) + float(TIF_PRECIP_MON_JUN) + float(TIF_PRECIP_MON_JUL) + float(TIF_PRECIP_MON_AUG) + float(TIF_PRECIP_MON_SEP) + float(TIF_PRECIP_MON_OCT) + float(TIF_PRECIP_MON_NOV) + float(TIF_PRECIP_MON_DEC)  
                                        
           
           
           TIF_AVG_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_01_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['january'] = float(TIF_AVG_TEMP_MON_JAN)
           TIF_AVG_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_02_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['february'] = float(TIF_AVG_TEMP_MON_FEB)
           TIF_AVG_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_03_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['march'] = float(TIF_AVG_TEMP_MON_MAR)
           TIF_AVG_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_04_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['april'] = float(TIF_AVG_TEMP_MON_APR)
           TIF_AVG_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_05_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['may'] = float(TIF_AVG_TEMP_MON_MAY)
           TIF_AVG_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_06_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['june'] = float(TIF_AVG_TEMP_MON_JUN)
           TIF_AVG_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_07_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['july'] = float(TIF_AVG_TEMP_MON_JUL)
           TIF_AVG_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_08_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['august'] = float(TIF_AVG_TEMP_MON_AUG)
           TIF_AVG_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_09_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['september'] = float(TIF_AVG_TEMP_MON_SEP)
           TIF_AVG_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_10_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['october'] = float(TIF_AVG_TEMP_MON_OCT)
           TIF_AVG_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_11_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['november'] = float(TIF_AVG_TEMP_MON_NOV)
           TIF_AVG_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/AVG_TEMP_Monthly/ma_tmp_12_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['december'] = float(TIF_AVG_TEMP_MON_DEC)
           
           
           TIF_MAX_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_01_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['january'] = float(TIF_MAX_TEMP_MON_JAN)
           TIF_MAX_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_02_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['february'] = float(TIF_MAX_TEMP_MON_FEB)
           TIF_MAX_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_03_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['march'] = float(TIF_MAX_TEMP_MON_MAR)
           TIF_MAX_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_04_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['april'] = float(TIF_MAX_TEMP_MON_APR)
           TIF_MAX_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_05_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['may'] = float(TIF_MAX_TEMP_MON_MAY)
           TIF_MAX_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_06_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['june'] = float(TIF_MAX_TEMP_MON_JUN)
           TIF_MAX_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_07_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['july'] = float(TIF_MAX_TEMP_MON_JUL)
           TIF_MAX_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_08_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['august'] = float(TIF_MAX_TEMP_MON_AUG)
           TIF_MAX_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_09_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['september'] = float(TIF_MAX_TEMP_MON_SEP)
           TIF_MAX_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_10_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['october'] = float(TIF_MAX_TEMP_MON_OCT)
           TIF_MAX_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_11_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['november'] = float(TIF_MAX_TEMP_MON_NOV)
           TIF_MAX_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMAX_Monthly/ma_tmx_12_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['december'] = float(TIF_MAX_TEMP_MON_DEC)
           
           
           TIF_MIN_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_01_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['january'] = float(TIF_MIN_TEMP_MON_JAN)
           TIF_MIN_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_02_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['february'] = float(TIF_MIN_TEMP_MON_FEB)
           TIF_MIN_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_03_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['march'] = float(TIF_MIN_TEMP_MON_MAR)
           TIF_MIN_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_04_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['april'] = float(TIF_MIN_TEMP_MON_APR)
           TIF_MIN_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_05_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['may'] = float(TIF_MIN_TEMP_MON_MAY)
           TIF_MIN_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_06_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['june'] = float(TIF_MIN_TEMP_MON_JUN)
           TIF_MIN_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_07_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['july'] = float(TIF_MIN_TEMP_MON_JUL)
           TIF_MIN_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_08_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['august'] = float(TIF_MIN_TEMP_MON_AUG)
           TIF_MIN_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_09_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['september'] = float(TIF_MIN_TEMP_MON_SEP)
           TIF_MIN_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_10_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['october'] = float(TIF_MIN_TEMP_MON_OCT)
           TIF_MIN_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_11_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['november'] = float(TIF_MIN_TEMP_MON_NOV)
           TIF_MIN_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/CRU/TMIN_Monthly/ma_tmn_12_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['december'] = float(TIF_MIN_TEMP_MON_DEC)
           
       elif (Source == "AGMERRA_TIF"):
           d = get_climate_information_from_AgMERRA_Data_LTA(X_Coor,Y_Coor)
       else:
           TIF_PRECIP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_01_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['january'] = float(TIF_PRECIP_MON_JAN)
           TIF_PRECIP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_02_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['february'] = float(TIF_PRECIP_MON_FEB)
           TIF_PRECIP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_03_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['march'] = float(TIF_PRECIP_MON_MAR)
           TIF_PRECIP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_04_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['april'] = float(TIF_PRECIP_MON_APR)
           TIF_PRECIP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_05_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['may'] = float(TIF_PRECIP_MON_MAY)
           TIF_PRECIP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_06_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['june'] = float(TIF_PRECIP_MON_JUN)
           TIF_PRECIP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_07_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['july'] = float(TIF_PRECIP_MON_JUL)
           TIF_PRECIP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_08_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['august'] = float(TIF_PRECIP_MON_AUG)
           TIF_PRECIP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_09_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['september'] = float(TIF_PRECIP_MON_SEP)
           TIF_PRECIP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_10_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['october'] = float(TIF_PRECIP_MON_OCT)
           TIF_PRECIP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_11_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['november'] = float(TIF_PRECIP_MON_NOV)
           TIF_PRECIP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/PRECIP_Monthly/ma_prec_12_1971_2013.tif", X_Coor, Y_Coor)
           d['precipitation']['december'] = float(TIF_PRECIP_MON_DEC)
           d['precipitation']['annual'] = float(TIF_PRECIP_MON_JAN) + float(TIF_PRECIP_MON_FEB) + float(TIF_PRECIP_MON_MAR) + float(TIF_PRECIP_MON_APR) + float(TIF_PRECIP_MON_MAY) + float(TIF_PRECIP_MON_JUN) + float(TIF_PRECIP_MON_JUL) + float(TIF_PRECIP_MON_AUG) + float(TIF_PRECIP_MON_SEP) + float(TIF_PRECIP_MON_OCT) + float(TIF_PRECIP_MON_NOV) + float(TIF_PRECIP_MON_DEC)
           
           
           TIF_AVG_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_01_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['january'] = float(TIF_AVG_TEMP_MON_JAN)
           TIF_AVG_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_02_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['february'] = float(TIF_AVG_TEMP_MON_FEB)
           TIF_AVG_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_03_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['march'] = float(TIF_AVG_TEMP_MON_MAR)
           TIF_AVG_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_04_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['april'] = float(TIF_AVG_TEMP_MON_APR)
           TIF_AVG_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_05_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['may'] = float(TIF_AVG_TEMP_MON_MAY)
           TIF_AVG_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_06_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['june'] = float(TIF_AVG_TEMP_MON_JUN)
           TIF_AVG_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_07_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['july'] = float(TIF_AVG_TEMP_MON_JUL)
           TIF_AVG_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_08_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['august'] = float(TIF_AVG_TEMP_MON_AUG)
           TIF_AVG_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_09_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['september'] = float(TIF_AVG_TEMP_MON_SEP)
           TIF_AVG_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_10_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['october'] = float(TIF_AVG_TEMP_MON_OCT)
           TIF_AVG_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_11_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['november'] = float(TIF_AVG_TEMP_MON_NOV)
           TIF_AVG_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/AVG_TEMP_Monthly/ma_tmp_12_1971_2013.tif", X_Coor, Y_Coor)
           d['average_temperature']['december'] = float(TIF_AVG_TEMP_MON_DEC)
           
           
           TIF_MAX_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_01_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['january'] = float(TIF_MAX_TEMP_MON_JAN)
           TIF_MAX_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_02_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['february'] = float(TIF_MAX_TEMP_MON_FEB)
           TIF_MAX_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_03_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['march'] = float(TIF_MAX_TEMP_MON_MAR)
           TIF_MAX_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_04_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['april'] = float(TIF_MAX_TEMP_MON_APR)
           TIF_MAX_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_05_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['may'] = float(TIF_MAX_TEMP_MON_MAY)
           TIF_MAX_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_06_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['june'] = float(TIF_MAX_TEMP_MON_JUN)
           TIF_MAX_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_07_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['july'] = float(TIF_MAX_TEMP_MON_JUL)
           TIF_MAX_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_08_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['august'] = float(TIF_MAX_TEMP_MON_AUG)
           TIF_MAX_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_09_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['september'] = float(TIF_MAX_TEMP_MON_SEP)
           TIF_MAX_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_10_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['october'] = float(TIF_MAX_TEMP_MON_OCT)
           TIF_MAX_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_11_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['november'] = float(TIF_MAX_TEMP_MON_NOV)
           TIF_MAX_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMAX_Monthly/ma_tmx_12_1971_2013.tif", X_Coor, Y_Coor)
           d['max_temperature']['december'] = float(TIF_MAX_TEMP_MON_DEC)
           
           
           TIF_MIN_TEMP_MON_JAN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_01_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['january'] = float(TIF_MIN_TEMP_MON_JAN)
           TIF_MIN_TEMP_MON_FEB =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_02_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['february'] = float(TIF_MIN_TEMP_MON_FEB)
           TIF_MIN_TEMP_MON_MAR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_03_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['march'] = float(TIF_MIN_TEMP_MON_MAR)
           TIF_MIN_TEMP_MON_APR =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_04_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['april'] = float(TIF_MIN_TEMP_MON_APR)
           TIF_MIN_TEMP_MON_MAY =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_05_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['may'] = float(TIF_MIN_TEMP_MON_MAY)
           TIF_MIN_TEMP_MON_JUN =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_06_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['june'] = float(TIF_MIN_TEMP_MON_JUN)
           TIF_MIN_TEMP_MON_JUL =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_07_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['july'] = float(TIF_MIN_TEMP_MON_JUL)
           TIF_MIN_TEMP_MON_AUG =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_08_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['august'] = float(TIF_MIN_TEMP_MON_AUG)
           TIF_MIN_TEMP_MON_SEP =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_09_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['september'] = float(TIF_MIN_TEMP_MON_SEP)
           TIF_MIN_TEMP_MON_OCT =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_10_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['october'] = float(TIF_MIN_TEMP_MON_OCT)
           TIF_MIN_TEMP_MON_NOV =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_11_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['november'] = float(TIF_MIN_TEMP_MON_NOV)
           TIF_MIN_TEMP_MON_DEC =  getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + "CLIMATE_SUMMARY/TMIN_Monthly/ma_tmn_12_1971_2013.tif", X_Coor, Y_Coor)
           d['min_temperature']['december'] = float(TIF_MIN_TEMP_MON_DEC)
       
       
       
       
       
       data['climate'] = d
       tif_ELEVATION = 'elevation/elevation.tif'
       elevation_data = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + tif_ELEVATION , X_Coor, Y_Coor)
       if (elevation_data == -1 or elevation_data == '-1' or elevation_data == -1.0 or elevation_data == '-1.0'):
           elevation_data = -999
       data['geospatial_data']['gdal_elevation'] = elevation_data
       
       tif_aridity_index = 'aridity/ai_yr.tif'
       aridity_index_data = getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + tif_aridity_index , X_Coor, Y_Coor)
       aridity_index_data = aridity_index_data*0.0001
       data['geospatial_data']['gdal_aridity_index'] = aridity_index_data
       
       tif_fao_lgp = 'GLOBAL_LAYER/FAO_LGP/LGP.tif'
       fao_lgp_data = int(getRasterValue_ThanhNH_Float(TIF_FOLDER_COMM + tif_fao_lgp , X_Coor, Y_Coor))
       data['geospatial_data']['gdal_fao_lgp'] =   get_value_fao_lgp_from_gdal_value_MySQL_DATABASE(fao_lgp_data)                 
                          
       return data
    
