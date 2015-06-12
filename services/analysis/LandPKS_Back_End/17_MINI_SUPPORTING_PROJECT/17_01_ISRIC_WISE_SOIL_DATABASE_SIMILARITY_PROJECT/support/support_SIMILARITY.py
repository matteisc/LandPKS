# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import sys
def get_collection_value_from_all_layer_texture(LIST_TEXTURE):
    try:
        SAND_LIST = [0,0,0,0,0,0,0]
        SILT_LIST = [0,0,0,0,0,0,0]
        CLAY_LIST = [0,0,0,0,0,0,0]
        BULK_DENSITY_LIST = [0,0,0,0,0,0,0]
        for i in range(0,len(LIST_TEXTURE)):
            #print "%d = %s " %(i,LIST_TEXTURE[i])
            if (LIST_TEXTURE[i] is None or LIST_TEXTURE[i] == ""):
                SAND_LIST[i] = 0
                SILT_LIST[i] = 0
                CLAY_LIST[i] = 0
                BULK_DENSITY_LIST[i] = 0
            else:
                record = get_collection_value_from_texture(LIST_TEXTURE[i])
                SAND_LIST[i] = float(record[0])
                SILT_LIST[i] = float(record[1])
                CLAY_LIST[i] = float(record[2]) 
                BULK_DENSITY_LIST[i] = float(record[3])
               
        BIG_LIST = [SAND_LIST,SILT_LIST,CLAY_LIST,BULK_DENSITY_LIST]
        return BIG_LIST
    except Exception,err:
        print err
        return None
def get_collection_value_from_texture(TEXTURE):
     
     try: 
        try:
            import MySQLdb
            db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
        except:
            sys.exit("Please install MySQLLib for Python or Database raised error")       
        if (TEXTURE is None or TEXTURE == ""):
            return None
        TEXTURE = TEXTURE.strip()
        TEXTURE = TEXTURE.upper()
        
        cur = db.cursor()
        sql = "SELECT sand, silt, clay, bulk_density FROM landpks_soil_texture_lookup WHERE UCASE(texture) = '%s'" %(str(TEXTURE))
        cur.execute(sql)
        results = cur.fetchall()
        sand = 0
        silt = 0
        clay = 0
        bulk_density = 0
        for row in results :
            if (row[0] is not None and float(row[0])):
                sand = float(row[0])
            else:
                sand = 0
            
            if (row[1] is not None and float(row[1])):
                silt = float(row[1])
            else:
                silt = 0
                
            if (row[2] is not None and float(row[2])):
                clay = float(row[2])
            else:
                clay = 0
                
            if (row[3] is not None and float(row[3])):
                bulk_density = float(row[3])
            else:
                bulk_density = 0
             
            entry_record = [sand,silt,clay,bulk_density]
            db.close()
            return entry_record    
     except Exception, err:
       db.rollback()
       db.close()
       return None
def get_values_texture_for_soil_horizon(ID):
    try:
        import MySQLdb
        db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except Exception, err:
        print err
        sys.exit("Please install MySQLLib for Python or Database raised error")
    try: 
        cur = db.cursor()
        sql = "SELECT texture_for_soil_horizon_1, texture_for_soil_horizon_2, texture_for_soil_horizon_3, texture_for_soil_horizon_4, texture_for_soil_horizon_5, texture_for_soil_horizon_6, texture_for_soil_horizon_7 FROM landpks_input_data WHERE ID = %s" %(str(ID))
        cur.execute(sql)
        results = cur.fetchall()
        list_records = []
        texture_for_soil_horizon_0 = ""
        texture_for_soil_horizon_1 = ""
        texture_for_soil_horizon_2 = ""
        texture_for_soil_horizon_3 = ""
        texture_for_soil_horizon_4 = ""
        texture_for_soil_horizon_5 = ""
        texture_for_soil_horizon_6 = ""
        
        for row in results :
            if (row[0] is not None):
                texture_for_soil_horizon_0 = row[0]
            else:
                texture_for_soil_horizon_0 = None
                
            if (row[1] is not None):
                texture_for_soil_horizon_1 = row[1]
            else:
                texture_for_soil_horizon_1 = None
            
            if (row[2] is not None):
                texture_for_soil_horizon_2 = row[2]
            else:
                texture_for_soil_horizon_2 = None
            
            if (row[3] is not None):
                texture_for_soil_horizon_3 = row[3]
            else:
                 texture_for_soil_horizon_3 = None
            
            if (row[4] is not None):
                texture_for_soil_horizon_4 = row[4]
            else:
                texture_for_soil_horizon_4 = None
            
            if (row[5] is not None):
                texture_for_soil_horizon_5 = row[5]
            else:
                texture_for_soil_horizon_5 = None
            
            if (row[6] is not None):
                texture_for_soil_horizon_6 = row[6]
            else:
                texture_for_soil_horizon_6 = None         
            
            entry_records = [texture_for_soil_horizon_0,texture_for_soil_horizon_1,texture_for_soil_horizon_2,texture_for_soil_horizon_3,texture_for_soil_horizon_4,texture_for_soil_horizon_5,texture_for_soil_horizon_6]
            db.close()
            return entry_records
        
    except Exception,err:
        print err
        db.close()
        return None
def get_soil_profile_awc_by_record_id(record_id):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
    
    try: 
        cur = db.cursor()
        sql = "SELECT soil_profile_awc FROM landpks_rosetta_awc_output_data WHERE record_id = %s" %(str(record_id))
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            if (row[0] is not None):
                awc = float(row[0])
            else:
                awc = 0
            break
        db.close()
        return awc
    except Exception, err:
        print err
        db.close()
        return None
def get_surface_craking_from_record_id(record_id):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
    try: 
        cur = db.cursor()
        sql = "SELECT surface_cracking FROM landpks_input_data WHERE ID = %s" %(str(record_id))
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            if (row[0] is not None): 
                db.close()#ID
                return row[0]
            else:
                db.close()
                return None
        
    except Exception, err:
        print err
        db.close()
        return None
def get_record_user_data_by_record_id(record_id):
    
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
    
    try: 
        cur = db.cursor()
        sql = "SELECT ID, name, latitude, longitude, slope, slope_shape, texture_for_soil_horizon_1, texture_for_soil_horizon_2, texture_for_soil_horizon_3, texture_for_soil_horizon_4, texture_for_soil_horizon_5, texture_for_soil_horizon_6, texture_for_soil_horizon_7 FROM landpks_input_data WHERE ID = %s" %(str(record_id))
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            if (row[0] is not None): #ID
                ID = row[0]
            else:
                ID = ""
            if (row[1] is not None): #ID
                name = row[1]
            else:
                name = ""
            if (row[2] is not None): #ID
                latitude = row[2]
            else:
                latitude = ""
            if (row[3] is not None): #ID
                longitude = row[3]
            else:
                longitude = ""
            if (row[4] is not None): #ID
                slope = row[4]
            else:
                slope = ""
            if (row[5] is not None): #ID
                slope_shape = row[5]
            else:
                slope_shape = ""
            if (row[6] is not None): #ID
                texture_for_soil_horizon_1 = row[6]
            else:
                texture_for_soil_horizon_1 = ""
            if (row[7] is not None): #ID
                texture_for_soil_horizon_2 = row[7]
            else:
                texture_for_soil_horizon_2 = ""
            if (row[8] is not None): #ID
                texture_for_soil_horizon_3 = row[8]
            else:
                texture_for_soil_horizon_3 = ""
            if (row[9] is not None): #ID
                texture_for_soil_horizon_4 = row[9]
            else:
                texture_for_soil_horizon_4 = ""
            if (row[10] is not None): #ID
                texture_for_soil_horizon_5 = row[10]
            else:
                texture_for_soil_horizon_5 = ""
            if (row[11] is not None): #ID
                texture_for_soil_horizon_6 = row[11]
            else:
                texture_for_soil_horizon_6 = ""
            if (row[12] is not None): #ID
                texture_for_soil_horizon_7 = row[12]
            else:
                texture_for_soil_horizon_7 = ""
                
        sand_silt_clay_values = get_collection_value_from_texture(texture_for_soil_horizon_1.strip().upper())
        soil_profile_awc = get_soil_profile_awc_by_record_id(record_id)
        entry_records = [ID, name, latitude, longitude, slope, slope_shape, texture_for_soil_horizon_1, 
                             texture_for_soil_horizon_2, texture_for_soil_horizon_3, texture_for_soil_horizon_4, texture_for_soil_horizon_5, texture_for_soil_horizon_6, 
                             texture_for_soil_horizon_7,sand_silt_clay_values,soil_profile_awc]
        db.close()
        return entry_records
    except Exception, err:
        print err
        db.close()
        return None
def get_record_gdal_data_by_record_id(record_id):
    
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
    
    try: 
        cur = db.cursor()
        sql = "SELECT ID, record_id, latitude, longitude, clim_precipitation_data, clim_gdd, clim_aridity_index, clim_kopgeiger, clim_fao_lgp, clim_modis_evapotrans, clim_precip_novdecjan, clim_precip_febmarapr, clim_precip_mayjunjul, clim_precip_augsepoct, topog_elevation, topog_geolage, topog_slope_global, topog_landform_global, topog_twi_global, topog_topi_global, topog_israd_global, landcover_modis_2012, vegind_modis_evi_m, vegind_modis_evi_sd FROM landpks_gdal_data_global_level WHERE record_id = %s" %(str(record_id))
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
            if (row[0] is not None): #ID
                ID = row[0]
            else:
                ID = ""
                
            if (row[1] is not None): #Record_ID
                record_id = row[1]
            else:
                record_id = ""
            
            if (row[2] is not None and float(row[2])): #Latitude
                latitude = row[2]
            else:
                latitude = 0.0
            
            if (row[3] is not None and float(row[3])):
                longitude = row[3]
            else:
                longitude = 0.0  
            
            if (row[4] is not None and float(row[4])):
                clim_precipitation_data = row[4]
            else:
                clim_precipitation_data = 0.0
            
            if (row[5] is not None and float(row[5])):
                clim_gdd = row[5]
            else:
                clim_gdd = 0.0      
            
            if (row[6] is not None and float(row[6])):
                clim_aridity_index = row[6]
            else:
                clim_aridity_index = 0.0
            
            if (row[7] is not None and float(row[7])):
                clim_kopgeiger = row[7]
            else:
                clim_kopgeiger = 0.0
                
            if (row[8] is not None and float(row[8])):
                clim_fao_lgp = row[8]
            else:
                clim_fao_lgp = 0.0
                
            if (row[9] is not None and float(row[9])):
                clim_modis_evapotrans = row[9]
            else:
                clim_modis_evapotrans = 0.0
                
            if (row[10] is not None and float(row[10])):
                clim_precip_novdecjan = row[10]
            else:
                clim_precip_novdecjan = 0.0
                
            if (row[11] is not None and float(row[11])):
                clim_precip_febmarapr = row[11]
            else:
                clim_precip_febmarapr = 0.0
            
            if (row[12] is not None and float(row[12])):
                clim_precip_mayjunjul = row[12]
            else:
                clim_precip_mayjunjul = 0.0
            
            if (row[13] is not None and float(row[13])):
                clim_precip_augsepoct = row[13]
            else:
                clim_precip_augsepoct = 0.0
                
            if (row[14] is not None and float(row[14])):
                topog_elevation = row[14]
            else:
                topog_elevation = 0.0
                
            if (row[15] is not None and float(row[15])):
                topog_geolage = row[15]
            else:
                topog_geolage = 0.0
                
            if (row[16] is not None and float(row[16])):
                topog_slope_global = row[16]
            else:
                topog_slope_global = 0.0
                
            if (row[17] is not None and float(row[17])):
                topog_landform_global = row[17]
            else:
                topog_landform_global = 0.0
                
            if (row[18] is not None and float(row[18])):
                topog_twi_global = row[18]
            else:
                topog_twi_global = 0.0
                
            if (row[19] is not None and float(row[19])):
                topog_topi_global = row[19]
            else:
                topog_topi_global = 0.0
            
            if (row[20] is not None and float(row[20])):
                topog_israd_global = row[20]
            else:
                topog_israd_global = 0.0
                
            if (row[21] is not None and float(row[21])):
                landcover_modis_2012 = row[21]
            else:
                landcover_modis_2012 = 0.0
                
            if (row[22] is not None and float(row[22])):
                vegind_modis_evi_m = row[22]
            else:
                vegind_modis_evi_m = 0.0
                
            if (row[23] is not None and float(row[23])):
                vegind_modis_evi_sd = row[23]
            else:
                vegind_modis_evi_sd = 0.0
            
            entry_records = [ID, record_id, latitude, longitude, clim_precipitation_data, clim_gdd, clim_aridity_index, 
                             clim_kopgeiger, clim_fao_lgp, clim_modis_evapotrans, clim_precip_novdecjan, clim_precip_febmarapr, 
                             clim_precip_mayjunjul, clim_precip_augsepoct, topog_elevation, topog_geolage, topog_slope_global, 
                             topog_landform_global, topog_twi_global, topog_topi_global, topog_israd_global, landcover_modis_2012, vegind_modis_evi_m, vegind_modis_evi_sd]
            db.close()
            return entry_records
    except Exception, err:
        print err
        db.close()
        return None

