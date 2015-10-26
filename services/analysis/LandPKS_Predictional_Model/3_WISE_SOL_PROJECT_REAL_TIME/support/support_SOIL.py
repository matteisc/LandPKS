# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len

MAXIMUM_NUMBER_LAYERS = 7

try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
       

def select_isric_soilgrids_soil_modified_data(record_id):
    try:    
       try:
          import MySQLdb
          db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
          
       cur = db.cursor()
       sql = "SELECT sd1_soil_soilgrids_orcdrc,sd2_soil_soilgrids_orcdrc,sd3_soil_soilgrids_orcdrc,sd4_soil_soilgrids_orcdrc,sd5_soil_soilgrids_orcdrc,sd6_soil_soilgrids_orcdrc,sd1_soil_soilgrids_phihox,sd2_soil_soilgrids_phihox,sd3_soil_soilgrids_phihox,sd4_soil_soilgrids_phihox,sd5_soil_soilgrids_phihox,sd6_soil_soilgrids_phihox,sd1_soil_soilgrids_bld,sd2_soil_soilgrids_bld,sd3_soil_soilgrids_bld,sd4_soil_soilgrids_bld,sd5_soil_soilgrids_bld,sd6_soil_soilgrids_bld,sd1_soil_soilgrids_cec,sd2_soil_soilgrids_cec,sd3_soil_soilgrids_cec,sd4_soil_soilgrids_cec,sd5_soil_soilgrids_cec,sd6_soil_soilgrids_cec FROM landpks_isric_soilgrids_soil_original_data WHERE record_id = %s" %(str(record_id))
        
       cur.execute(sql)
       results = cur.fetchall()
       
       i = 0
       
       for row in results :
            i = 1
            #ORCDRC
            if (row[0] is not None):
                sd1_orcdrc  = row[0]
            else:
                sd1_orcdrc = 0
            
            if (row[1] is not None):
                sd2_orcdrc  = row[1]
            else:
                sd2_orcdrc = 0
            
            if (row[2] is not None):
                sd3_orcdrc  = row[2]
            else:
                sd3_orcdrc = 0
            
            if (row[3] is not None):
                sd4_orcdrc  = row[3]
            else:
                sd4_orcdrc = 0
            
            if (row[4] is not None):
                sd5_orcdrc  = row[4]
            else:
                sd5_orcdrc = 0
            
            if (row[5] is not None):
                sd6_orcdrc  = row[5]
            else:
                sd6_orcdrc = 0
            
          
            #PHIHOX
            if (row[6] is not None):
                sd1_phihox  = row[6]
            else:
                sd1_phihox = 0
            
            if (row[7] is not None):
                sd2_phihox  = row[7]
            else:
                sd2_phihox = 0
            
            if (row[8] is not None):
                sd3_phihox  = row[8]
            else:
                sd3_phihox = 0
            
            if (row[9] is not None):
                sd4_phihox  = row[9]
            else:
                sd4_phihox = 0
            
            if (row[10] is not None):
                sd5_phihox  = row[10]
            else:
                sd5_phihox = 0
            
            if (row[11] is not None):
                sd6_phihox  = row[11]
            else:
                sd6_phihox = 0  
            
            #BLD
            if (row[12] is not None):
                sd1_bld  = row[12]
            else:
                sd1_bld = 0
            
            if (row[13] is not None):
                sd2_bld  = row[13]
            else:
                sd2_bld = 0
            
            if (row[14] is not None):
                sd3_bld  = row[14]
            else:
                sd3_bld = 0
            
            if (row[15] is not None):
                sd4_bld  = row[15]
            else:
                sd4_bld = 0
            
            if (row[16] is not None):
                sd5_bld  = row[16]
            else:
                sd5_bld = 0
            
            if (row[17] is not None):
                sd6_bld  = row[17]
            else:
                sd6_bld = 0
                                    
             
             
            #CEC
            if (row[18] is not None):
                sd1_cec  = row[18]
            else:
                sd1_cec = 0
            
            if (row[19] is not None):
                sd2_cec  = row[19]
            else:
                sd2_cec = 0
            
            if (row[20] is not None):
                sd3_cec  = row[20]
            else:
                sd3_cec = 0
            
            if (row[21] is not None):
                sd4_cec  = row[21]
            else:
                sd4_cec = 0
            
            if (row[22] is not None):
                sd5_cec  = row[22]
            else:
                sd5_cec = 0
            
            if (row[23] is not None):
                sd6_cec  = row[23]
            else:
                sd6_cec = 0       
       
       if (i == 0):
           return None
       else:
           ORCDRC_MAPPING_LIST = [0,0,0,0,0,0,0]
           layer_1_orcdrc = float(sd1_orcdrc)
           layer_2_orcdrc = (float(sd1_orcdrc) + float(sd2_orcdrc)) / 2
           layer_3_orcdrc = (float(sd2_orcdrc) + float(sd3_orcdrc)) / 2
           layer_4_orcdrc = float(sd3_orcdrc)*0.33 + float(sd4_orcdrc)*0.67
           layer_5_orcdrc = (float(sd4_orcdrc) + float(sd5_orcdrc)) / 2
           layer_6_orcdrc = float(sd5_orcdrc)
           layer_7_orcdrc = float(sd6_orcdrc)
           ORCDRC_MAPPING_LIST = [layer_1_orcdrc,layer_2_orcdrc,layer_3_orcdrc,layer_4_orcdrc,layer_5_orcdrc,layer_6_orcdrc,layer_7_orcdrc]
           
           PHIHOX_MAPPING_LIST = [0,0,0,0,0,0,0]
           layer_1_phihox = float(sd1_phihox)
           layer_2_phihox = (float(sd1_phihox) + float(sd2_phihox)) / 2
           layer_3_phihox = (float(sd2_phihox) + float(sd3_phihox)) / 2
           layer_4_phihox = float(sd3_phihox)*0.33 + float(sd4_phihox)*0.67
           layer_5_phihox = (float(sd4_phihox) + float(sd5_phihox)) / 2
           layer_6_phihox = float(sd5_phihox)
           layer_7_phihox = float(sd6_phihox)
           PHIHOX_MAPPING_LIST = [layer_1_phihox,layer_2_phihox,layer_3_phihox,layer_4_phihox,layer_5_phihox,layer_6_phihox,layer_7_phihox]
           
           
           BLD_MAPPING_LIST = [0,0,0,0,0,0,0]
           layer_1_bld = float(sd1_bld)
           layer_2_bld = (float(sd1_bld) + float(sd2_bld)) / 2
           layer_3_bld = (float(sd2_bld) + float(sd3_bld)) / 2
           layer_4_bld = float(sd3_bld)*0.33 + float(sd4_bld)*0.67
           layer_5_bld = (float(sd4_bld) + float(sd5_bld)) / 2
           layer_6_bld = float(sd5_bld)
           layer_7_bld = float(sd6_bld)
           BLD_MAPPING_LIST = [layer_1_bld,layer_2_bld,layer_3_bld,layer_4_bld,layer_5_bld,layer_6_bld,layer_7_bld]
           
           CEC_MAPPING_LIST = [0,0,0,0,0,0,0]
           layer_1_cec = float(sd1_cec)
           layer_2_cec = (float(sd1_cec) + float(sd2_cec)) / 2
           layer_3_cec = (float(sd2_cec) + float(sd3_cec)) / 2
           layer_4_cec = float(sd3_cec)*0.33 + float(sd4_cec)*0.67
           layer_5_cec = (float(sd4_cec) + float(sd5_cec)) / 2
           layer_6_cec = float(sd5_cec)
           layer_7_cec = float(sd6_cec)
           CEC_MAPPING_LIST = [layer_1_cec,layer_2_cec,layer_3_cec,layer_4_cec,layer_5_cec,layer_6_cec,layer_7_cec]
           
           SOIL_GRIDS_VALUE_LIST = [ORCDRC_MAPPING_LIST,PHIHOX_MAPPING_LIST,BLD_MAPPING_LIST,CEC_MAPPING_LIST]
       
           return SOIL_GRIDS_VALUE_LIST
    except Exception, err:
       print err
       db.rollback()
       return None
       #db.close()
    finally:
       db.close()      

def insert_isric_soilgrids_soil_original_data(record_id, record_name, Y, X, ORCDRC_LIST, PHIHOX_LIST, 
                                   BLD_LIST, CEC_LIST, DBR_VALUE, TAXWRB_VALUE, TAXGOUUSDA_VALUE):
     try:    
       try:
          import MySQLdb
          db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
       except:
          sys.exit("Please install MySQLLib for Python or Database raised error")
        
       cur = db.cursor()
     
       str_record_id = str(record_id)
       str_record_name = str(record_name)
       str_X = str(X)
       str_Y = str(Y)
       
       sd1_orcdrc = ORCDRC_LIST[0]
       sd2_orcdrc = ORCDRC_LIST[1]
       sd3_orcdrc = ORCDRC_LIST[2]
       sd4_orcdrc = ORCDRC_LIST[3]
       sd5_orcdrc = ORCDRC_LIST[4]
       sd6_orcdrc = ORCDRC_LIST[5]
       
       sd1_phihox = PHIHOX_LIST[0]
       sd2_phihox = PHIHOX_LIST[1]
       sd3_phihox = PHIHOX_LIST[2]
       sd4_phihox = PHIHOX_LIST[3]
       sd5_phihox = PHIHOX_LIST[4]
       sd6_phihox = PHIHOX_LIST[5]
       
       sd1_bld = BLD_LIST[0]
       sd2_bld = BLD_LIST[1]
       sd3_bld = BLD_LIST[2]
       sd4_bld = BLD_LIST[3]
       sd5_bld = BLD_LIST[4]
       sd6_bld = BLD_LIST[5]
       
       sd1_cec = CEC_LIST[0]
       sd2_cec = CEC_LIST[1]
       sd3_cec = CEC_LIST[2]
       sd4_cec = CEC_LIST[3]
       sd5_cec = CEC_LIST[4]
       sd6_cec = CEC_LIST[5]
       
       query = "INSERT INTO landpks_isric_soilgrids_soil_original_data (record_id,plot_id,latitude,longitude,sd1_soil_soilgrids_orcdrc,sd2_soil_soilgrids_orcdrc,sd3_soil_soilgrids_orcdrc,sd4_soil_soilgrids_orcdrc,sd5_soil_soilgrids_orcdrc,sd6_soil_soilgrids_orcdrc,sd1_soil_soilgrids_phihox,sd2_soil_soilgrids_phihox,sd3_soil_soilgrids_phihox,sd4_soil_soilgrids_phihox,sd5_soil_soilgrids_phihox,sd6_soil_soilgrids_phihox,sd1_soil_soilgrids_bld,sd2_soil_soilgrids_bld,sd3_soil_soilgrids_bld,sd4_soil_soilgrids_bld,sd5_soil_soilgrids_bld,sd6_soil_soilgrids_bld,sd1_soil_soilgrids_cec,sd2_soil_soilgrids_cec,sd3_soil_soilgrids_cec,sd4_soil_soilgrids_cec,sd5_soil_soilgrids_cec,sd6_soil_soilgrids_cec,soil_soilgrids_dbr,soil_soilgrids_taxgwrb_major,soil_soilgrids_taxgousda_major) VALUES (%s,%s,%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,'%s','%s','%s')" %(str_record_id, str_record_id, str_Y, str_X,
               sd1_orcdrc,sd2_orcdrc,sd3_orcdrc,sd4_orcdrc,sd5_orcdrc,
               sd6_orcdrc,sd1_phihox,sd2_phihox,sd3_phihox,sd4_phihox,
               sd5_phihox,sd6_phihox,sd1_bld,sd2_bld,sd3_bld,sd4_bld,sd5_bld,
               sd6_bld,sd1_cec,sd2_cec,sd3_cec,sd4_cec,
               sd5_cec,sd6_cec,DBR_VALUE,TAXWRB_VALUE,TAXGOUUSDA_VALUE)
       
       cur.execute(query)
    
       db.commit()  
     except Exception, err:
       print err
       db.rollback()
       #db.close()
     finally:
       db.close()       
       
       
def get_rock_value_to_consider_number_layer(text_rock_value):
    if (text_rock_value is None or text_rock_value == ""):
        return 0
    if (text_rock_value.strip() == "0-15%"):
        return 1
    elif (text_rock_value.strip() == "15-35%"):
        return 1
    elif (text_rock_value.strip() == "35-60%"):
        return 1
    elif (text_rock_value.strip() == ">60%"):
        return 1
    else:
        return 0
def get_rock_value(text_rock_value):
    if (text_rock_value is None or text_rock_value == ""):
        return 0
    if (text_rock_value.strip() == "0-15%"):
        return 0
    elif (text_rock_value.strip() == "15-35%"):
        return 25
    elif (text_rock_value.strip() == "35-60%"):
        return 47.5
    elif (text_rock_value.strip() == ">60%"):
        return 70
    else:
        return 0
def get_list_value_of_rock_fragment(ID):
     try: 
        cur = db.cursor()
        sql = "SELECT rock_fragment_for_soil_horizon_1,rock_fragment_for_soil_horizon_2,rock_fragment_for_soil_horizon_3,rock_fragment_for_soil_horizon_4,rock_fragment_for_soil_horizon_5,rock_fragment_for_soil_horizon_6,rock_fragment_for_soil_horizon_7 FROM landpks_input_data WHERE ID = %s" %(str(ID))
        
        cur.execute(sql)
        results = cur.fetchall()
        list_records = []
        rock_fragment_for_soil_horizon_0 = ""
        rock_fragment_for_soil_horizon_1 = ""
        rock_fragment_for_soil_horizon_2 = ""
        rock_fragment_for_soil_horizon_3 = ""
        rock_fragment_for_soil_horizon_4 = ""
        rock_fragment_for_soil_horizon_5 = ""
        rock_fragment_for_soil_horizon_6 = ""
        
        for row in results :
            if (row[0] is not None):
                rock_fragment_for_soil_horizon_0 = row[0]
            else:
                rock_fragment_for_soil_horizon_0 = None
                
            if (row[1] is not None):
                rock_fragment_for_soil_horizon_1 = row[1]
            else:
                rock_fragment_for_soil_horizon_1 = None
            
            if (row[2] is not None):
                rock_fragment_for_soil_horizon_2 = row[2]
            else:
                rock_fragment_for_soil_horizon_2 = None
            
            if (row[3] is not None):
                rock_fragment_for_soil_horizon_3 = row[3]
            else:
                rock_fragment_for_soil_horizon_3 = None
            
            if (row[4] is not None):
                rock_fragment_for_soil_horizon_4 = row[4]
            else:
                rock_fragment_for_soil_horizon_4 = None
            
            if (row[5] is not None):
                rock_fragment_for_soil_horizon_5 = row[5]
            else:
                rock_fragment_for_soil_horizon_5 = None  
                
            if (row[6] is not None):
                rock_fragment_for_soil_horizon_6 = row[6]
            else:
                rock_fragment_for_soil_horizon_6 = None
                       
            break
         
        rock_0 = get_rock_value(rock_fragment_for_soil_horizon_0)
        rock_1 = get_rock_value(rock_fragment_for_soil_horizon_1)
        rock_2 = get_rock_value(rock_fragment_for_soil_horizon_2)
        rock_3 = get_rock_value(rock_fragment_for_soil_horizon_3)
        rock_4 = get_rock_value(rock_fragment_for_soil_horizon_4)
        rock_5 = get_rock_value(rock_fragment_for_soil_horizon_5)
        rock_6 = get_rock_value(rock_fragment_for_soil_horizon_6)
        entry_records = [rock_0,rock_1,rock_2,rock_3,rock_4,rock_5,rock_6]
        
        return entry_records
     except Exception,err:
        print err
        return None
def get_list_value_of_rock_fragment_to_consider_number_layer(ID):
     try: 
        cur = db.cursor()
        sql = "SELECT rock_fragment_for_soil_horizon_1,rock_fragment_for_soil_horizon_2,rock_fragment_for_soil_horizon_3,rock_fragment_for_soil_horizon_4,rock_fragment_for_soil_horizon_5,rock_fragment_for_soil_horizon_6,rock_fragment_for_soil_horizon_7 FROM landpks_input_data WHERE ID = %s" %(str(ID))
        
        cur.execute(sql)
        results = cur.fetchall()
        list_records = []
        rock_fragment_for_soil_horizon_0 = ""
        rock_fragment_for_soil_horizon_1 = ""
        rock_fragment_for_soil_horizon_2 = ""
        rock_fragment_for_soil_horizon_3 = ""
        rock_fragment_for_soil_horizon_4 = ""
        rock_fragment_for_soil_horizon_5 = ""
        rock_fragment_for_soil_horizon_6 = ""
        
        for row in results :
            if (row[0] is not None):
                rock_fragment_for_soil_horizon_0 = row[0]
            else:
                rock_fragment_for_soil_horizon_0 = None
                
            if (row[1] is not None):
                rock_fragment_for_soil_horizon_1 = row[1]
            else:
                rock_fragment_for_soil_horizon_1 = None
            
            if (row[2] is not None):
                rock_fragment_for_soil_horizon_2 = row[2]
            else:
                rock_fragment_for_soil_horizon_2 = None
            
            if (row[3] is not None):
                rock_fragment_for_soil_horizon_3 = row[3]
            else:
                rock_fragment_for_soil_horizon_3 = None
            
            if (row[4] is not None):
                rock_fragment_for_soil_horizon_4 = row[4]
            else:
                rock_fragment_for_soil_horizon_4 = None
            
            if (row[5] is not None):
                rock_fragment_for_soil_horizon_5 = row[5]
            else:
                rock_fragment_for_soil_horizon_5 = None  
                
            if (row[6] is not None):
                rock_fragment_for_soil_horizon_6 = row[6]
            else:
                rock_fragment_for_soil_horizon_6 = None
                       
            break
         
        rock_0 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_0)
        rock_1 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_1)
        rock_2 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_2)
        rock_3 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_3)
        rock_4 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_4)
        rock_5 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_5)
        rock_6 = get_rock_value_to_consider_number_layer(rock_fragment_for_soil_horizon_6)
        entry_records = [rock_0,rock_1,rock_2,rock_3,rock_4,rock_5,rock_6]
        return entry_records
     except Exception,err:
        print err
        return None    
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
            return entry_record    
     except Exception,err:
        print err
        return None
def get_values_texture_for_soil_horizon(ID):
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
            return entry_records
    except Exception,err:
        print err
        return None
def get_texture_value_to_consider_number_layer(text_rock_value):
    list_template_texture = ['SAND','LOAMY SAND','SANDY LOAM','LOAM','SILT LOAM','SILT','SANDY CLAY LOAM','CLAY LOAM','SILTY CLAY LOAM','SILTY CLAY','SANDY CLAY','CLAY']
    text_rock_value = text_rock_value.strip().upper()
    if (text_rock_value in list_template_texture):
        return 1
    else:
        return 0
def get_values_texture_for_soil_horizon_to_consider_number_layers(ID):
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
            v_0 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_0)
            v_1 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_1)
            v_2 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_2)
            v_3 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_3)
            v_4 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_4)
            v_5 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_5)
            v_6 = get_texture_value_to_consider_number_layer(texture_for_soil_horizon_6)
            entry_records = [v_0,v_1,v_2,v_3,v_4,v_5,v_6]
            return entry_records
    except Exception,err:
        print err
        return None
def get_number_layers(ID):
    lst_rock_values = get_list_value_of_rock_fragment_to_consider_number_layer(ID)
    length_lst_rock_values = len(lst_rock_values)
    lst_texture_values = get_values_texture_for_soil_horizon_to_consider_number_layers(ID)
    length_lst_texture_values = len(lst_texture_values)
    
    if (( not int("0") in lst_rock_values) or (not int("0") in lst_texture_values)):
        return MAXIMUM_NUMBER_LAYERS
    elif ((lst_rock_values[length_lst_rock_values-1] == 1) or (lst_texture_values[length_lst_texture_values-1] == 1)):
        return MAXIMUM_NUMBER_LAYERS
    else:
        for i in reversed(range(0,MAXIMUM_NUMBER_LAYERS)):
            if ((lst_rock_values[i] == 1) and (lst_rock_values[i+1] == 0)):
                return (i+1)
    return MAXIMUM_NUMBER_LAYERS
