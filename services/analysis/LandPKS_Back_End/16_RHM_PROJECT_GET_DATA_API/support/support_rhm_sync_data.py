# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import datetime
import time

HOST = "127.0.0.1"
USER = "root"
PASSWORD= ""
DATABASE = "apex"

BARE = "Bare"
TREES = "Trees"
SHRUBS = "Shrubs"
SUB_SHRUBS = "Sub-shrubs"
PER_GRASS = "Perennial grasses"
ANNUAL = "Annuals"
HERB_LITTER = "Herb litter"
WOOD_LITTER = "Wood litter"
ROCK = "Rock"

def get_list_recorder_name_from_landpks():
     try: 
       try:
          import MySQLdb
          db = MySQLdb.connect(host= HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
    
       cur = db.cursor()
       sql = "SELECT DISTINCT recorder_name FROM landpks_input_data"
       cur.execute(sql)
       results = cur.fetchall()
       
       recorder_name_lists = []
       for row in results :
           if (row[0] is not None):
             recorder_name_lists.append(str(row[0]))
    
       return recorder_name_lists
     except Exception, err:
       print err
       db.close()
       return None
     finally:
       db.close()
def get_last_update_date_follow_recorder_name(recorder_name):
     try: 
       try:
          import MySQLdb
          db = MySQLdb.connect(host= HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
    
       cur = db.cursor()
       sql = "SELECT MAX(insert_unix_time) FROM rhm_input_data WHERE recorder_name = '%s'" %(str(recorder_name).strip())
       cur.execute(sql)
       results = cur.fetchall()
       
       recorder_name_lists = []
       for row in results :
           if (row[0] is not None):
             return datetime.datetime.fromtimestamp(row[0]).strftime('%Y%m%d')
       return None
     except Exception, err:
       print err
       db.close()
       return None
     finally:
       db.close()
def get_last_update_date():
     try: 
       try:
          import MySQLdb
          db = MySQLdb.connect(host= HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
    
       cur = db.cursor()
       sql = "SELECT MAX(insert_unix_time) FROM rhm_input_data"
       cur.execute(sql)
       results = cur.fetchall()
       
       recorder_name_lists = []
       for row in results :
           if (row[0] is not None):
             return datetime.datetime.fromtimestamp(row[0]).strftime('%Y%m%d')
       return None
     except Exception, err:
       print err
       db.close()
       return None
     finally:
       db.close()
def occurrences(string, sub):
    try:
        count = start = 0
        while True:
            start = string.find(sub, start) + 1
            if start > 0:
                count+=1
            else:
                return count
    except:
        return 0
def count_value_in_string(value, string):
    return occurrences(string, value)
def insert_rhm_data_to_rhm_store(name, recorder_name, transect, dominant_woody_species,dominant_nonwoody_species, species_of_interest_1, species_of_interest_2, segment, date, canopy_height, canopy_gap, basal_gap, species_1_density, species_2_density, species_of_interest_1_count,species_of_interest_2_count, species_list, 
                                 stick_segment_0, stick_segment_1, stick_segment_2, stick_segment_3, stick_segment_4):
    try:    
       try:
          import MySQLdb
          db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = db.cursor()
       str_record_name = str(recorder_name).strip()
       str_name = str(name).strip()
       str_transect = str(transect).strip()
       str_dominant_woody_species = str(dominant_woody_species).strip()
       str_dominant_nonwoody_species = str(dominant_nonwoody_species).strip()
       str_species_of_interest_1 = str(species_of_interest_1).strip()
       str_species_of_interest_2 = str(species_of_interest_2).strip()
       str_segment = str(segment).strip()
       str_date = str(date).strip()
       str_canopy_height = str(canopy_height).strip()
       str_canopy_gap = str(canopy_gap).strip()
       str_basal_gap = str(basal_gap).strip()
       int_species_1_density = int(species_1_density)
       int_species_2_density = int(species_2_density)
       int_species_of_interest_1_count = int(species_of_interest_1_count)
       int_species_of_interest_2_count = int(species_of_interest_2_count)
       str_species_list = str(species_list)
       str_stick_segment_0 = str(stick_segment_0).strip()
       str_stick_segment_1 = str(stick_segment_1).strip()
       str_stick_segment_2 = str(stick_segment_2).strip()
       str_stick_segment_3 = str(stick_segment_3).strip()
       str_stick_segment_4 = str(stick_segment_4).strip()
       stick_segment_string = str_stick_segment_0 + " | " + str_stick_segment_1 + " | " + str_stick_segment_2 + " | " + str_stick_segment_3 + " | " + str_stick_segment_4
       stick_segment_string = stick_segment_string.upper().strip()
       int_bare_total = count_value_in_string(BARE.upper(), stick_segment_string)
       int_trees_total = count_value_in_string(TREES.upper(), stick_segment_string)
       int_shrubs_total = count_value_in_string(SHRUBS.upper(), stick_segment_string)
       int_sub_shrubs_total = count_value_in_string(SUB_SHRUBS.upper(), stick_segment_string)
       int_perennial_grasses_total = count_value_in_string(PER_GRASS.upper(), stick_segment_string)
       int_annuals_total = count_value_in_string(ANNUAL.upper(), stick_segment_string)
       int_herb_litter_total = count_value_in_string(HERB_LITTER.upper(), stick_segment_string)
       int_wood_litter_total = count_value_in_string(WOOD_LITTER.upper(), stick_segment_string)
       int_rock_total = count_value_in_string(ROCK.upper(), stick_segment_string)
       current = time.time()
       fl_insert_unix_time = float(current)
       str_insert_normal_time = str(datetime.datetime.fromtimestamp(current).strftime('%Y-%m-%d %H:%M:%S'))
       str_ip_address = ""
       
       query = "INSERT INTO rhm_input_data (name,recorder_name,transect,dominant_woody_species,dominant_nonwoody_species,species_of_interest_1,species_of_interest_2,segment,date,canopy_height,canopy_gap,basal_gap,species_1_density,species_2_density,species_of_interest_1_count,species_of_interest_2_count,species_list,stick_segment_0,stick_segment_1,stick_segment_2,stick_segment_3,stick_segment_4,bare_total,trees_total,shrubs_total,sub_shrubs_total,perennial_grasses_total,annuals_total,herb_litter_total,wood_litter_total,rock_total,insert_unix_time,insert_normal_time,ip_address) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%d, %d, %d, %d, '%s','%s','%s','%s','%s','%s', %d,%d,%d,%d,%d,%d,%d,%d,%d, %f,'%s','%s')" %(str_name,
               str_record_name, str_transect,str_dominant_woody_species,str_dominant_nonwoody_species,str_species_of_interest_1,str_species_of_interest_2, str_segment, str_date, str_canopy_height, str_canopy_gap, str_basal_gap, int_species_1_density, int_species_2_density,int_species_of_interest_1_count,int_species_of_interest_2_count,
               str_species_list, str_stick_segment_0, str_stick_segment_1, str_stick_segment_2, str_stick_segment_3, str_stick_segment_4,int_bare_total,int_trees_total, int_shrubs_total,
               int_sub_shrubs_total, int_perennial_grasses_total, int_annuals_total, int_herb_litter_total, int_wood_litter_total, int_rock_total, fl_insert_unix_time, str_insert_normal_time,str_ip_address)
       
       cur.execute(query)
       db.commit()
       return 1  
    except Exception, err:
       print err
       db.rollback()
       db.close()
       return 0
    finally:
       db.close() 
def update_photos_landinfo(landinfor_name,landinfor_recorder_name, landinfor_landscapeNorthPhotoURL, landinfor_landscapeEastPhotoURL, landinfor_landscapeSouthPhotoURL, landinfor_landscapeWestPhotoURL, landinfor_soilPitPhotoURL, landinfor_soilSamplesPhotoURL):
     try:    
       try:
          import MySQLdb
          db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       cur = db.cursor()
       key = landinfor_recorder_name +"-" + landinfor_name
       query = "UPDATE landpks_input_data SET soil_pit_photo_url = '%s', soil_samples_photo_url = '%s', landscape_north_photo_url = '%s', landscape_east_photo_url = '%s', landscape_south_photo_url = '%s', landscape_west_photo_url = '%s' WHERE name = '%s'"  %(str(landinfor_soilPitPhotoURL),str(landinfor_soilSamplesPhotoURL),str(landinfor_landscapeNorthPhotoURL),str(landinfor_landscapeEastPhotoURL),str(landinfor_landscapeSouthPhotoURL),str(landinfor_landscapeWestPhotoURL),str(key))
       cur.execute(query)
       db.commit()
       return 1   
     except Exception, err:
       print err
       db.rollback()
       db.close()
       return 0
     finally:
       db.close()     
def check_exit_rhm_record(name,recorder_name,transect,segment):
    try:    
       try:
          import MySQLdb
          db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWORD, db=DATABASE)
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
       name = name.strip().upper()
       recorder_name = recorder_name.strip().upper()
       transect = transect.strip().upper()
       segment = segment.strip().upper()
       
       cur = db.cursor()
       sql = "SELECT COUNT(ID) FROM rhm_input_data WHERE UCASE(name) = '%s' AND UCASE(recorder_name) = '%s' AND UCASE(transect) = '%s' AND UCASE(segment) = '%s'" %(name,recorder_name,transect,segment)
       cur.execute(sql)
       results = cur.fetchone()[0]
       if (results == 0):
           return False
       else:
           return True
       
    except Exception, err:
       print err
       db.rollback()
       db.close()
       return False
    finally:
       db.close()
