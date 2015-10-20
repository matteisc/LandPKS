# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import time
import datetime
import sys
import os
import collections
import hashlib
import re
from drupalpassword import DrupalHash

from object import LandPKS_LandInfo
from utility import LandPKS_Ultility

try:
       import MySQLdb
       conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
except:
       sys.exit("Please install MySQLLib for Python or Database raised error")

DATABASE_HOST_IP = "127.0.0.1"
DATABASE_NAME = "apex"
DATABASE_USER = "root"
DATABASE_PASS = ""

class MultipleLevelsOfDictionary(collections.OrderedDict):
    def __getitem__(self,item):
        try:
            return collections.OrderedDict.__getitem__(self,item)
        except:
            value = self[item] = type(self)()
            return value
def check_auth_api_account(username,password):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = conn.cursor()
       sql = "SELECT pass FROM users WHERE UCASE(name) = '%s' AND status = 1" % (str(username).strip().upper())
       cur.execute(sql)
       results = cur.fetchall()
       stored_password = ""
       for row in results :
            stored_password = str(row[0]).strip()
       if (stored_password is None or stored_password == ""):
           return 0
       drupalhash = DrupalHash()
       check = drupalhash.user_check_password(password,stored_password)
       if (check):
           return 1
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
            return 1
    return 0
def get_username_from_input(input_string):
    if (validateEmail(input_string) == 0):
        return input_string
    else:
        try:
            try:
              import MySQLdb
              conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
            except:
              sys.exit("Please install MySQLLib for Python or Database raised error")
            cur = conn.cursor()
            sql = "SELECT name FROM users WHERE UCASE(mail) = '%s'" % (str(input_string).strip().upper())
            cur.execute(sql)
            results = cur.fetchall()
            for row in results:
                if (row[0] <> "" or row[0] is not None):
                    return str(row[0])
        except Exception,err:
            print err
            return None
        finally:
            conn.close()
def get_key_pair_landcover_MySQL_Database(recorder_name,after_date,before_date):
    try:
       land_cover_list = []
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       type = 0 
       cur = conn.cursor()
       cur_apex = conn.cursor()
       if ((recorder_name == "" or recorder_name is None) and (before_date == "" or before_date is None)):
          sql = "SELECT DISTINCT name,recorder_name FROM rhm_input_data WHERE DATE(rhm_input_data.insert_normal_time) >= '%s' ORDER BY ID DESC" % (str(after_date).strip().upper())
       elif ((recorder_name == "" or recorder_name is None) and (after_date == "" or after_date is None)):
          sql = "SELECT DISTINCT name,recorder_name FROM rhm_input_data WHERE DATE(rhm_input_data.insert_normal_time) <= '%s' ORDER BY ID DESC" % (str(before_date).strip().upper())
       elif ((recorder_name == "" or recorder_name is None) and (after_date <> "" and after_date is not None) and (before_date <> "" or before_date is not None)):
          sql = "SELECT DISTINCT name,recorder_name FROM rhm_input_data WHERE DATE(rhm_input_data.insert_normal_time) <= '%s' AND DATE(rhm_input_data.insert_normal_time) >= '%s' ORDER BY ID DESC" % (str(before_date).strip().upper(),str(after_date).strip().upper()) 
       else:
          return -1     
       cur.execute(sql)
       results = cur.fetchall()
       list_key = []
       for row in results:
           if (row[0] <> "" or row[0] is not None):
             list_key.append([row[0],row[1]])
       return list_key
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def get_land_info_IDs_by_After_Before_Date_MySQL_Database(recorder_name,before_date,after_date):
    try:
       list_id = [] 
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       if ((recorder_name == "" or recorder_name is None) and (before_date == "" or before_date is None)):
           sql = "SELECT ID FROM landpks_input_data WHERE insert_normal_time >= '%s' AND landpks_input_data.deleted <> 1" % (str(after_date).strip())
       elif ((recorder_name == "" or recorder_name is None) and (after_date == "" or after_date is None)):
           sql = "SELECT ID FROM landpks_input_data WHERE insert_normal_time <= '%s' AND landpks_input_data.deleted <> 1" % (str(before_date).strip())
       elif ((recorder_name == "" or recorder_name is None) and (after_date <> "" and after_date is not None) and (before_date <> "" and before_date is not None)):
           sql = "SELECT ID FROM landpks_input_data WHERE insert_normal_time <= '%s' AND insert_normal_time >= '%s' AND landpks_input_data.deleted <> 1" % (str(before_date).strip(),str(after_date).strip())
       else: 
          '''  
          #sql = "SELECT ID FROM landpks_input_data WHERE UCASE(recorder_name) = '%s' AND latitude <= %s AND latitude >= %s AND longitude <= %s AND longitude >= %s AND landpks_input_data.deleted <> 1" % (str(recorder_name).strip().upper(),str(maxlat).strip(),str(minlat).strip(),str(maxlong).strip(),str(minlong).strip())
          ''' 
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None):
                list_id.append(int(row[0]))
       return list_id
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def get_land_info_IDs_by_Polygon_MySQL_Database(recorder_name,minlat,minlong,maxlat,maxlong):
    try:
       list_id = [] 
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       if (recorder_name == "" or recorder_name is None):
          sql = "SELECT ID FROM landpks_input_data WHERE latitude <= %s AND latitude >= %s AND longitude <= %s AND longitude >= %s AND landpks_input_data.deleted <> 1" % (str(maxlat).strip(),str(minlat).strip(),str(maxlong).strip(),str(minlong).strip())
       else:   
          sql = "SELECT ID FROM landpks_input_data WHERE UCASE(recorder_name) = '%s' AND latitude <= %s AND latitude >= %s AND longitude <= %s AND longitude >= %s AND landpks_input_data.deleted <> 1" % (str(recorder_name).strip().upper(),str(maxlat).strip(),str(minlat).strip(),str(maxlong).strip(),str(minlong).strip()) 
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None):
                list_id.append(int(row[0]))
       return list_id
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def get_land_info_IDs_by_Recorder_Name_MySQL_Database(recorder_name):
    try:
       list_id = [] 
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT ID FROM landpks_input_data WHERE UCASE(recorder_name) = '%s' AND landpks_input_data.deleted <> 1" % (str(recorder_name).strip().upper())
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None):
                list_id.append(int(row[0]))
       return list_id
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def get_list_name_landcover_by_recorder_name_MySQL_Database(recorder_name):
    try:
       land_cover_list = []
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       type = 0 
       cur = conn.cursor()
       cur_apex = conn.cursor()
      
       sql = "SELECT DISTINCT name FROM rhm_input_data WHERE UCASE(rhm_input_data.recorder_name) = '%s' ORDER BY ID DESC" % (str(recorder_name).strip().upper())

       cur.execute(sql)
       results = cur.fetchall()
       list_name = []
       for row in results:
           if (row[0] <> "" or row[0] is not None):
             list_name.append(row[0])
       return list_name
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()                                                        
def get_list_landcover_data_by_IDs_MySQL_Database(name,recorder_name):
    try:
       land_cover_list = []
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       type = 0 
       cur = conn.cursor()
       cur_apex = conn.cursor()
       if (name is not None and recorder_name is not None):
           sql = "SELECT * FROM rhm_input_data WHERE UCASE(rhm_input_data.name) = '%s' AND UCASE(rhm_input_data.recorder_name) = '%s' ORDER BY ID DESC" % (str(name).strip().upper(),str(recorder_name).strip().upper())
           type = 1
       elif (name is None and recorder_name is not None):
           sql = "SELECT * FROM rhm_input_data WHERE UCASE(rhm_input_data.recorder_name) = '%s' ORDER BY ID DESC" % (str(recorder_name).strip().upper())
           type = 2
       elif (name is not None and recorder_name is None):
           return -1
       
       cur.execute(sql)
       results = cur.fetchall()
       if (type == 1):
           data = MultipleLevelsOfDictionary()
           data['name'] = name
           data['recorder_name'] = recorder_name
           date = '0'
           for row in results :
                if (date == '0'):
                    date = row[28]
                d = MultipleLevelsOfDictionary()
                d['direction'] = row[4]
                d['segment']['range'] = row[5]
                d['segment']['time'] = row[28]
                d['segment']['canopy_height'] = row[7]
                d['segment']['canopy_gap'] = row[8]
                d['segment']['basal_gap'] = row[9]
                d['segment']['species_1_density'] = row[10]
                d['segment']['species_2_density'] = row[11]
                d['segment']['species_list'] = row[12]
                d['segment']['stick_segment']['0']['index'] = 0
                d['segment']['stick_segment']['0']['cover'] = row[13]
                d['segment']['stick_segment']['1']['index'] = 1
                d['segment']['stick_segment']['1']['cover'] = row[14]
                d['segment']['stick_segment']['2']['index'] = 2
                d['segment']['stick_segment']['2']['cover'] = row[15]
                d['segment']['stick_segment']['3']['index'] = 3
                d['segment']['stick_segment']['3']['cover'] = row[16]
                d['segment']['stick_segment']['4']['index'] = 4
                d['segment']['stick_segment']['4']['cover'] = row[17]
                d['segment']['summary']['bare_total'] = row[18]
                d['segment']['summary']['trees_total'] = row[19]
                d['segment']['summary']['shrubs_total'] = row[20]
                d['segment']['summary']['sub_shrubs_total'] = row[21]
                d['segment']['summary']['perennial_grasses_total'] = row[23]
                d['segment']['summary']['annuals_total'] = row[24]
                d['segment']['summary']['herb_litter_total'] = row[25]
                d['segment']['summary']['wood_litter_total'] = row[26]
                d['segment']['summary']['rock_total'] = row[26]
                land_cover_list.append(d)
           data['date'] = date
           data['transect'] = land_cover_list
           return data
       else:
            return -1
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()         
def get_list_landinfo_predicted_data_by_IDs_MySQL_Database(list_id,display_set):
    try:
       land_info_list = []
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       cur_apex = conn.cursor()
       sql = "SELECT * FROM landpks_input_data WHERE landpks_input_data.ID in (%s) AND landpks_input_data.deleted <> 1 ORDER BY ID DESC" % (str(list_id).strip())
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            d = MultipleLevelsOfDictionary()
            ID = row[0]
            d['id'] = row[0]
            d['name'] = row[1]
            d['recorder_name'] = row[2]
            d['test_plot'] = row[3]
            d['organization'] = row[5]
            d['latitude'] = row[6]
            d['longitude'] = row[7]
            d['city'] = row[8]
            d['notes'] = row[9]
            d['land_cover'] = row[11]
            d['grazed'] = row[12]
            d['grazing'] = row[14]
            d['flooding'] = row[15]
            d['slope'] = row[17]
            d['slope_shape'] = row[18]
            if (LandPKS_Ultility.is_Float(str(row[19]))):
               d['bedrock_depth'] = float(str(row[19]))
            else:
               d['bedrock_depth'] = ""
            
            if (LandPKS_Ultility.is_Float(str(row[20]))):
               d['stopped_digging_depth'] = float(str(row[20]))
            else:
               d['stopped_digging_depth'] = ""
                   
            d['rock_fragment']['soil_horizon_1'] = row[21]
            d['rock_fragment']['soil_horizon_2'] = row[22]
            d['rock_fragment']['soil_horizon_3'] = row[23]
            d['rock_fragment']['soil_horizon_4'] = row[24]
            d['rock_fragment']['soil_horizon_5'] = row[25]
            d['rock_fragment']['soil_horizon_6'] = row[26]
            d['rock_fragment']['soil_horizon_7'] = row[27]
            d['color']['soil_horizon_1'] = row[28]
            d['color']['soil_horizon_2'] = row[29]
            d['color']['soil_horizon_3'] = row[30]
            d['color']['soil_horizon_4'] = row[31]
            d['color']['soil_horizon_5'] = row[32]
            d['color']['soil_horizon_6'] = row[33]
            d['color']['soil_horizon_7'] = row[34]
           
            d['texture']['soil_horizon_1'] = row[35]
            d['texture']['soil_horizon_2'] = row[36]
            d['texture']['soil_horizon_3'] = row[37]
            d['texture']['soil_horizon_4'] = row[38]
            d['texture']['soil_horizon_5'] = row[39]
            d['texture']['soil_horizon_6'] = row[40]
            d['texture']['soil_horizon_7'] = row[41]
            
            d['surface_cracking'] = row[42]
            d['surface_salt'] = row[44]
            d['soil_pit_photo_url'] = row[46]
            d['soil_samples_photo_url'] = row[47]
            d['landscape_north_photo_url'] = row[48]
            d['landscape_east_photo_url'] = row[49]
            d['landscape_south_photo_url'] = row[50]
            d['landscape_west_photo_url'] = row[51]
            d['insert_normal_time'] = str(row[53])
            d['ip_address'] = row[54]
            
            
            if ('PREDICTION' in display_set):
                sql = "SELECT apex_output_y_maize,apex_output_yldg_maize,apex_output_biom_meize,apex_output_y_glass,apex_output_yldg_glass,apex_output_biom_glass,maize_productivity,maize_erosion,glass_productivity,glass_erosion FROM lanpks_apex_output_data WHERE lanpks_apex_output_data.record_id = %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['prediction']['apex_output_y_crop'] = row_apex[0]
                    d['prediction']['apex_output_yldg_crop'] = row_apex[1]
                    d['prediction']['apex_output_biom_crop'] = row_apex[2]
                    d['prediction']['apex_output_y_grass'] = row_apex[3]
                    d['prediction']['apex_output_yldg_grass'] = row_apex[4]
                    d['prediction']['apex_output_biom_grass'] = row_apex[5]
                    d['prediction']['crop_productivity'] = row_apex[6]
                    d['prediction']['crop_erosion'] = row_apex[7]
                    d['prediction']['grass_productivity'] = row_apex[8]
                    d['prediction']['glass_erosion'] = row_apex[9]
           
            if ('GEOSPATIAL_DATA' in display_set):
                sql = "SELECT gdal.topog_elevation as old_elevation, gdal.clim_gdd as gdd, gdal.clim_aridity_index as aridity, gdal.clim_fao_lgp as fao_lgp FROM landpks_gdal_data_global_level gdal WHERE gdal.record_id = %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['geospatial_data']['gdal_elevation'] = float(row_apex[0])
                    d['geospatial_data']['gdal_gdd'] = float(row_apex[1])
                    d['geospatial_data']['gdal_aridity_index'] = float(row_apex[2])
                    d['geospatial_data']['gdal_fao_lgp'] = get_value_fao_lgp_from_gdal_value_MySQL_DATABASE(int(row_apex[3]))
           
            if ('ANALYTIC_DATA_SOIL' in display_set):    
                sql = "SELECT awc.soil_profile_awc as soil_profile_awc FROM  landpks_rosetta_awc_output_data awc WHERE  awc.record_id = %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['analytic_data_soil']['awc_soil_profile_awc'] = float(row_apex[0])
            
            if ('CLIMATE' in display_set):
                sql = "SELECT climate_precip_jan,climate_precip_feb,climate_precip_mar,climate_precip_apr,climate_precip_may,climate_precip_jun,climate_precip_jul,climate_precip_aug,climate_precip_sep,climate_precip_oct,climate_precip_nov,climate_precip_dec  FROM  landpks_climate_precip_summary WHERE record_id =  %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['climate']['precipitation']['january'] = float(row_apex[0])
                    d['climate']['precipitation']['february'] = float(row_apex[1])
                    d['climate']['precipitation']['march'] = float(row_apex[2])
                    d['climate']['precipitation']['april'] = float(row_apex[3])
                    d['climate']['precipitation']['may'] = float(row_apex[4])
                    d['climate']['precipitation']['june'] = float(row_apex[5])
                    d['climate']['precipitation']['july'] = float(row_apex[6])
                    d['climate']['precipitation']['august'] = float(row_apex[7])
                    d['climate']['precipitation']['september'] = float(row_apex[8])
                    d['climate']['precipitation']['october'] = float(row_apex[9])
                    d['climate']['precipitation']['november'] = float(row_apex[10])
                    d['climate']['precipitation']['december'] = float(row_apex[11])
                    
                sql = "SELECT climate_avg_temp_jan,climate_avg_temp_feb,climate_avg_temp_mar,climate_avg_temp_apr,climate_avg_temp_may,climate_avg_temp_jun,climate_avg_temp_jul,climate_avg_temp_aug,climate_avg_temp_sep,climate_avg_temp_oct,climate_avg_temp_nov,climate_avg_temp_dec  FROM  landpks_climate_average_temp_summary  WHERE record_id =  %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['climate']['average_temperature']['january'] = float(row_apex[0])
                    d['climate']['average_temperature']['february'] = float(row_apex[1])
                    d['climate']['average_temperature']['march'] = float(row_apex[2])
                    d['climate']['average_temperature']['april'] = float(row_apex[3])
                    d['climate']['average_temperature']['may'] = float(row_apex[4])
                    d['climate']['average_temperature']['june'] = float(row_apex[5])
                    d['climate']['average_temperature']['july'] = float(row_apex[6])
                    d['climate']['average_temperature']['august'] = float(row_apex[7])
                    d['climate']['average_temperature']['september'] = float(row_apex[8])
                    d['climate']['average_temperature']['october'] = float(row_apex[9])
                    d['climate']['average_temperature']['november'] = float(row_apex[10])
                    d['climate']['average_temperature']['december'] = float(row_apex[11])
                
                sql = "SELECT climate_max_temp_jan,climate_max_temp_feb,climate_max_temp_mar,climate_max_temp_apr,climate_max_temp_may,climate_max_temp_jun,climate_max_temp_jul,climate_max_temp_aug,climate_max_temp_sep,climate_max_temp_oct,climate_max_temp_nov,climate_max_temp_dec  FROM  landpks_climate_max_temp_summary  WHERE record_id =  %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['climate']['max_temperature']['january'] = float(row_apex[0])
                    d['climate']['max_temperature']['february'] = float(row_apex[1])
                    d['climate']['max_temperature']['march'] = float(row_apex[2])
                    d['climate']['max_temperature']['april'] = float(row_apex[3])
                    d['climate']['max_temperature']['may'] = float(row_apex[4])
                    d['climate']['max_temperature']['june'] = float(row_apex[5])
                    d['climate']['max_temperature']['july'] = float(row_apex[6])
                    d['climate']['max_temperature']['august'] = float(row_apex[7])
                    d['climate']['max_temperature']['september'] = float(row_apex[8])
                    d['climate']['max_temperature']['october'] = float(row_apex[9])
                    d['climate']['max_temperature']['november'] = float(row_apex[10])
                    d['climate']['max_temperature']['december'] = float(row_apex[11])
                    
                sql = "SELECT climate_min_temp_jan,climate_min_temp_feb,climate_min_temp_mar,climate_min_temp_apr,climate_min_temp_may,climate_min_temp_jun,climate_min_temp_jul,climate_min_temp_aug,climate_min_temp_sep,climate_min_temp_oct,climate_min_temp_nov,climate_min_temp_dec FROM  landpks_climate_min_temp_summary WHERE record_id =  %s" % (str(ID).strip())
                cur_apex.execute(sql)
                results_apex = cur_apex.fetchall()
                for row_apex in results_apex :
                    d['climate']['min_temperature']['january'] = float(row_apex[0])
                    d['climate']['min_temperature']['february'] = float(row_apex[1])
                    d['climate']['min_temperature']['march'] = float(row_apex[2])
                    d['climate']['min_temperature']['april'] = float(row_apex[3])
                    d['climate']['min_temperature']['may'] = float(row_apex[4])
                    d['climate']['min_temperature']['june'] = float(row_apex[5])
                    d['climate']['min_temperature']['july'] = float(row_apex[6])
                    d['climate']['min_temperature']['august'] = float(row_apex[7])
                    d['climate']['min_temperature']['september'] = float(row_apex[8])
                    d['climate']['min_temperature']['october'] = float(row_apex[9])
                    d['climate']['min_temperature']['november'] = float(row_apex[10])
                    d['climate']['min_temperature']['december'] = float(row_apex[11])
                    
            land_info_list.append(d)
       return land_info_list
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
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
def get_land_cover_id_from_key_pair_MySQL_Database(name, recorder_name):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = conn.cursor()
       sql = "SELECT 1 FROM rhm_input_data WHERE UCASE(name) = '%s' and UCASE(recorder_name) = '%s'" % (str(name).strip().upper(),str(recorder_name).strip().upper())
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None and (row[0] == 1 or row[0] == "1")):
                return 1
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def delete_land_cover_record_name_recorder_name_MySQL_Database(name, recorder_name):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = conn.cursor()
       sql = "DELETE FROM rhm_input_data WHERE UCASE(name) = '%s' and UCASE(recorder_name) = '%s'" % (str(name).strip().upper(),str(recorder_name).strip().upper())
       cur.execute(sql)
       conn.commit()
       return 1
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def delete_land_cover_record_MySQL_Database(landcover_id):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = conn.cursor()
       sql = "DELETE FROM rhm_input_data WHERE ID = %s" % (str(landcover_id))
       cur.execute(sql)
       conn.commit()
       return 1
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def check_be_able_deleted_LANDCOVER_before_delete_MySQL_Database(landcover_id):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT 1 FROM rhm_input_data WHERE ID = %s" % (str(landcover_id))
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None and (row[0] == 1 or row[0] == "1")):
                return 1
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def check_be_able_deleted_before_delete_MySQL_Database(plot_id):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT 1 FROM landpks_input_data WHERE ID = %s and (deleted = 0 or deleted IS NULL)" % (str(plot_id))
       cur.execute(sql)
       print sql
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None and (row[0] == 1 or row[0] == "1")):
                return 1
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def delete_land_info_plot_MySQL_Database(plot_id):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = conn.cursor()
       sql = "UPDATE landpks_input_data SET deleted=1 WHERE ID = %s" % (str(plot_id))
       
       cur.execute(sql)
       conn.commit()
       return 1
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()     
def check_exist_predicted_data_MySQL_Database(plot_id):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT 1 FROM lanpks_apex_output_data WHERE record_id = %s" % (str(plot_id))
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None and (row[0] == 1 or row[0] == "1")):
                return 1
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def insert_new_plot_LandInfo_MySQL_Database(plot_data):
     try:
        
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
     
       name = str(plot_data['name']).strip()
       recorder_name = str(plot_data['recorder_name']).strip()
       test_plot = str(plot_data['test_plot']).strip()
       boolean_test_plot = str(plot_data['boolean_test_plot'])
       organization = str(plot_data['organization'])
       latitude = str(plot_data['latitude'])
       longitude = str(plot_data['longitude'])
       city = str(plot_data['city'])
       notes = str(plot_data['notes'])
       modified_date = str(plot_data['modified_date'])
       land_cover = str(plot_data['land_cover'])
       grazed = str(plot_data['grazed'])
       boolean_grazed = str(plot_data['boolean_grazed'])
       grazing = str(plot_data['grazing'])
       flooding = str(plot_data['flooding'])
       boolean_flooding = str(plot_data['boolean_flooding'])
       slope = str(plot_data['slope'])
       slope_shape = str(plot_data['slope_shape'])
       bedrock_depth = str(plot_data['bedrock_depth'])
       stopped_digging_depth = str(plot_data['stopped_digging_depth'])
       rock_fragment_for_soil_horizon_1 = str(plot_data['rock_fragment_for_soil_horizon_1'])
       rock_fragment_for_soil_horizon_2 = str(plot_data['rock_fragment_for_soil_horizon_2'])
       rock_fragment_for_soil_horizon_3 = str(plot_data['rock_fragment_for_soil_horizon_3'])
       rock_fragment_for_soil_horizon_4 = str(plot_data['rock_fragment_for_soil_horizon_4'])
       rock_fragment_for_soil_horizon_5 = str(plot_data['rock_fragment_for_soil_horizon_5'])
       rock_fragment_for_soil_horizon_6 = str(plot_data['rock_fragment_for_soil_horizon_6'])
       rock_fragment_for_soil_horizon_7 = str(plot_data['rock_fragment_for_soil_horizon_7'])
       color_for_soil_horizon_1 = str(plot_data['color_for_soil_horizon_1'])
       color_for_soil_horizon_2 = str(plot_data['color_for_soil_horizon_2'])
       color_for_soil_horizon_3 = str(plot_data['color_for_soil_horizon_3'])
       color_for_soil_horizon_4 = str(plot_data['color_for_soil_horizon_4'])
       color_for_soil_horizon_5 = str(plot_data['color_for_soil_horizon_5'])
       color_for_soil_horizon_6 = str(plot_data['color_for_soil_horizon_6'])
       color_for_soil_horizon_7 = str(plot_data['color_for_soil_horizon_7'])
       texture_for_soil_horizon_1 = str(plot_data['texture_for_soil_horizon_1'])
       texture_for_soil_horizon_2 = str(plot_data['texture_for_soil_horizon_2'])
       texture_for_soil_horizon_3 = str(plot_data['texture_for_soil_horizon_3'])
       texture_for_soil_horizon_4 = str(plot_data['texture_for_soil_horizon_4'])
       texture_for_soil_horizon_5 = str(plot_data['texture_for_soil_horizon_5'])
       texture_for_soil_horizon_6 = str(plot_data['texture_for_soil_horizon_6'])
       texture_for_soil_horizon_7 = str(plot_data['texture_for_soil_horizon_7'])
       surface_cracking = plot_data['surface_cracking']
       b_surface_cracking= plot_data['boolean_surface_cracking']  
       surface_salt=  plot_data['surface_salt'] 
       b_surface_salt = plot_data['boolean_surface_salt']  
       soil_pit_photo_url= plot_data['soil_pit_photo_url']
       soil_samples_photo_url= plot_data['soil_samples_photo_url']
       landscape_north_photo_url = plot_data['landscape_north_photo_url']
       landscape_east_photo_url = plot_data['landscape_east_photo_url']
       landscape_south_photo_url= plot_data['landscape_south_photo_url']
       landscape_west_photo_url=plot_data['landscape_west_photo_url']
       
       ts = time.time()
       insert_unix_time = ts
       insert_unix_time = str(insert_unix_time)
       insert_normal_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
       ip_address = plot_data['client_ip']
       print insert_unix_time
       
       query = "INSERT INTO landpks_input_data (name,recorder_name,test_plot,boolean_test_plot,organization,latitude,longitude,city,notes,modified_date,land_cover,grazed,boolean_grazed,grazing,flooding,boolean_flooding,slope,slope_shape,bedrock_depth,stopped_digging_depth,rock_fragment_for_soil_horizon_1,rock_fragment_for_soil_horizon_2,rock_fragment_for_soil_horizon_3,rock_fragment_for_soil_horizon_4,rock_fragment_for_soil_horizon_5,rock_fragment_for_soil_horizon_6,rock_fragment_for_soil_horizon_7, \
                color_for_soil_horizon_1,color_for_soil_horizon_2,color_for_soil_horizon_3,color_for_soil_horizon_4,color_for_soil_horizon_5,color_for_soil_horizon_6,color_for_soil_horizon_7, \
                texture_for_soil_horizon_1,texture_for_soil_horizon_2,texture_for_soil_horizon_3,texture_for_soil_horizon_4,texture_for_soil_horizon_5,texture_for_soil_horizon_6,texture_for_soil_horizon_7,surface_cracking, \
                boolean_surface_cracking,surface_salt,boolean_surface_salt,soil_pit_photo_url,soil_samples_photo_url,landscape_north_photo_url,landscape_east_photo_url,landscape_south_photo_url, \
                landscape_west_photo_url,insert_unix_time,insert_normal_time,ip_address,deleted) \
                VALUES ('%s','%s','%s',%s,'%s',%s,%s,'%s','%s','%s','%s','%s',%s,'%s','%s',%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s,'%s',%s,'%s','%s','%s','%s','%s','%s',%s,'%s','%s',%s)"  \
               %(name, recorder_name, test_plot, boolean_test_plot, organization,latitude,longitude,city,notes,modified_date,land_cover,grazed,boolean_grazed,grazing,flooding,boolean_flooding,
                 slope,slope_shape,bedrock_depth,stopped_digging_depth,rock_fragment_for_soil_horizon_1,rock_fragment_for_soil_horizon_2,rock_fragment_for_soil_horizon_3,rock_fragment_for_soil_horizon_4,rock_fragment_for_soil_horizon_5,
                 rock_fragment_for_soil_horizon_6,rock_fragment_for_soil_horizon_7,color_for_soil_horizon_1,color_for_soil_horizon_2,color_for_soil_horizon_3,color_for_soil_horizon_4,color_for_soil_horizon_5,
                 color_for_soil_horizon_6, color_for_soil_horizon_7,texture_for_soil_horizon_1,texture_for_soil_horizon_2,texture_for_soil_horizon_3,texture_for_soil_horizon_4,texture_for_soil_horizon_5,texture_for_soil_horizon_6,
                 texture_for_soil_horizon_7,surface_cracking,b_surface_cracking,surface_salt,b_surface_salt,soil_pit_photo_url,soil_samples_photo_url,landscape_north_photo_url,landscape_east_photo_url,landscape_south_photo_url,
                 landscape_west_photo_url,insert_unix_time,insert_normal_time,ip_address,0)
       
       cur.execute(query)
       inser_id = conn.insert_id()
       conn.commit()  
       return inser_id
   
     except Exception, err:
       print err
       conn.rollback()
       return -1
     finally:
       conn.close()
def get_plot_id_land_info(name,recorder_name):
    try:
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       sql = "SELECT ID FROM landpks_input_data WHERE UCASE(name) = '%s' AND UCASE(recorder_name) = '%s' AND deleted <> 1" % (str(name).strip().upper(),str(recorder_name).strip().upper())
       cur.execute(sql)
       results = cur.fetchall()
       for row in results :
            if (row[0] is not None):
                return row[0]
       return 0
    except Exception,err:
       print err
       return -1
    finally:
       conn.close()
def insert_LandCover_Object_MySQL_Database(landcover_data):
    try:    
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = conn.cursor()
       
       str_record_name = landcover_data['recorder_name']
       str_name = landcover_data['name']
       str_transect = landcover_data['transect']
       str_segment = landcover_data['segment']
       str_date = ""
       land_info_id = int(landcover_data['landinfor_id'])
       str_canopy_height = landcover_data['canopy_height']
       str_canopy_gap = landcover_data['canopy_gap']
       str_basal_gap = landcover_data['basal_gap']
       int_species_1_density = int(landcover_data['species_1_density'])
       int_species_2_density = int(landcover_data['species_2_density'])
       str_species_list = landcover_data['species_list']
       str_stick_segment_0 = landcover_data['stick_segment_0']
       str_stick_segment_1 = landcover_data['stick_segment_1']
       str_stick_segment_2 = landcover_data['stick_segment_2']
       str_stick_segment_3 = landcover_data['stick_segment_3']
       str_stick_segment_4 = landcover_data['stick_segment_4']
       int_bare_total = int(landcover_data['int_bare_total'])
       int_trees_total = int(landcover_data['int_trees_total'])
       int_shrubs_total = int(landcover_data['int_shrubs_total'])
       int_sub_shrubs_total = int(landcover_data['int_sub_shrubs_total'])
       int_perennial_grasses_total = int(landcover_data['int_perennial_grasses_total'])
       int_annuals_total = int(landcover_data['int_annuals_total'])
       int_herb_litter_total = int(landcover_data['int_herb_litter_total'])
       int_wood_litter_total = int(landcover_data['int_wood_litter_total'])
       int_rock_total = int(landcover_data['int_rock_total'])
       current = time.time()
       fl_insert_unix_time = float(current)
       str_insert_normal_time = str(datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S'))
       str_ip_address = landcover_data['client_ip']
       
       query = "INSERT INTO rhm_input_data (record_id,name,recorder_name,transect,segment,date,canopy_height,canopy_gap,basal_gap,species_1_density,species_2_density,species_list,stick_segment_0,stick_segment_1,stick_segment_2,stick_segment_3,stick_segment_4,bare_total,trees_total,shrubs_total,sub_shrubs_total,perennial_grasses_total,annuals_total,herb_litter_total,wood_litter_total,rock_total,insert_unix_time,insert_normal_time,ip_address) VALUES (%d,'%s','%s','%s','%s','%s','%s','%s','%s',%d, %d, '%s','%s','%s','%s','%s','%s', %d,%d,%d,%d,%d,%d,%d,%d,%d, %f,'%s','%s')" %(land_info_id,str_name,
               str_record_name, str_transect, str_segment, str_date, str_canopy_height, str_canopy_gap, str_basal_gap, int_species_1_density, int_species_2_density,
               str_species_list, str_stick_segment_0, str_stick_segment_1, str_stick_segment_2, str_stick_segment_3, str_stick_segment_4,int_bare_total,int_trees_total, int_shrubs_total,
               int_sub_shrubs_total, int_perennial_grasses_total, int_annuals_total, int_herb_litter_total, int_wood_litter_total, int_rock_total, fl_insert_unix_time, str_insert_normal_time,str_ip_address)
       
       cur.execute(query)
       insert_id = conn.insert_id() 
       conn.commit()
       return insert_id 
    except Exception, err:
       print err
       conn.rollback()
       return -1
    finally:
       conn.close()
def check_exit_landcover_record_MySQL_Database(name,recorder_name,transect,segment):
    try:    
       try:
          import MySQLdb
          conn = MySQLdb.connect(host=DATABASE_HOST_IP, user=DATABASE_USER, passwd=DATABASE_PASS, db=DATABASE_NAME)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       name = name.strip().upper()
       recorder_name = recorder_name.strip().upper()
       transect = transect.strip().upper()
       segment = segment.strip().upper()
       
       cur = conn.cursor()
       sql = "SELECT COUNT(ID) FROM rhm_input_data WHERE UCASE(name) = '%s' AND UCASE(recorder_name) = '%s' AND UCASE(transect) = '%s' AND UCASE(segment) = '%s'" %(name,recorder_name,transect,segment)
       cur.execute(sql)
       results = cur.fetchone()[0]
       if (results == 0):
           return False
       else:
           return True
       
    except Exception, err:
       print err
       return False
    finally:
       conn.close()
