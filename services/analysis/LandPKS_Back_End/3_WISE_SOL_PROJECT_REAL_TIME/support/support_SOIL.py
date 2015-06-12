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