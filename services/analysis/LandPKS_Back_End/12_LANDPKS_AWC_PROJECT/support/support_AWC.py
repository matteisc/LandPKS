# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len

try:
    from osgeo import gdal, ogr
    import numpy
except Exception, err:
    print err
    sys.exit("Please install GDAL for Python")
    
       
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
        
        try:
            import MySQLdb
            db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
        except:
            sys.exit("Please install MySQLLib for Python or Database raised error")
            
        cur = db.cursor()
        sql = "SELECT texture_for_soil_horizon_1, texture_for_soil_horizon_2, texture_for_soil_horizon_3, texture_for_soil_horizon_4, texture_for_soil_horizon_5, texture_for_soil_horizon_6, texture_for_soil_horizon_7 FROM landpks_input_data WHERE ID = %s" %(str(ID))
        print sql
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
def insert_rosetta_value_awc_output(record_id, record_name, Y, X, FIELD_CAPACITY_LIST, WILTING_POINT_LIST, 
                                   ORIGINAL_AWC_LIST, CENTIMETER_AWC_LIST, soil_profile_awc):
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
       
       field_capacity_layer_1 = FIELD_CAPACITY_LIST[0]
       field_capacity_layer_2 = FIELD_CAPACITY_LIST[1]
       field_capacity_layer_3 = FIELD_CAPACITY_LIST[2]
       field_capacity_layer_4 = FIELD_CAPACITY_LIST[3]
       field_capacity_layer_5 = FIELD_CAPACITY_LIST[4]
       field_capacity_layer_6 = FIELD_CAPACITY_LIST[5]
       field_capacity_layer_7 = FIELD_CAPACITY_LIST[6]
       wilting_point_layer_1 = WILTING_POINT_LIST[0]
       wilting_point_layer_2 = WILTING_POINT_LIST[1]
       wilting_point_layer_3 = WILTING_POINT_LIST[2]
       wilting_point_layer_4 = WILTING_POINT_LIST[3]
       wilting_point_layer_5 = WILTING_POINT_LIST[4]
       wilting_point_layer_6 = WILTING_POINT_LIST[5]
       wilting_point_layer_7 = WILTING_POINT_LIST[6]
       original_awc_layer_1 = ORIGINAL_AWC_LIST[0]
       original_awc_layer_2 = ORIGINAL_AWC_LIST[1]
       original_awc_layer_3 = ORIGINAL_AWC_LIST[2]
       original_awc_layer_4 = ORIGINAL_AWC_LIST[3]
       original_awc_layer_5 = ORIGINAL_AWC_LIST[4]
       original_awc_layer_6 = ORIGINAL_AWC_LIST[5]
       original_awc_layer_7 = ORIGINAL_AWC_LIST[6]
       
       centimeter_awc_layer_1 = CENTIMETER_AWC_LIST[0]
       centimeter_awc_layer_2 = CENTIMETER_AWC_LIST[1]
       centimeter_awc_layer_3 = CENTIMETER_AWC_LIST[2]
       centimeter_awc_layer_4 = CENTIMETER_AWC_LIST[3]
       centimeter_awc_layer_5 = CENTIMETER_AWC_LIST[4]
       centimeter_awc_layer_6 = CENTIMETER_AWC_LIST[5]
       centimeter_awc_layer_7 = CENTIMETER_AWC_LIST[6]
       
       query = "INSERT INTO landpks_rosetta_awc_output_data (record_id,plot_id,record_name,latitude,longitude,field_capacity_layer_1,field_capacity_layer_2,field_capacity_layer_3,field_capacity_layer_4,field_capacity_layer_5,field_capacity_layer_6,field_capacity_layer_7,wilting_point_layer_1,wilting_point_layer_2,wilting_point_layer_3,wilting_point_layer_4,wilting_point_layer_5,wilting_point_layer_6,wilting_point_layer_7,original_awc_layer_1,original_awc_layer_2,original_awc_layer_3,original_awc_layer_4,original_awc_layer_5,original_awc_layer_6,original_awc_layer_7,centimeter_awc_layer_1,centimeter_awc_layer_2,centimeter_awc_layer_3,centimeter_awc_layer_4,centimeter_awc_layer_5,centimeter_awc_layer_6,centimeter_awc_layer_7,soil_profile_awc) VALUES (%s,%s,'%s',%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
               field_capacity_layer_1,field_capacity_layer_2,field_capacity_layer_3,field_capacity_layer_4,field_capacity_layer_5,
               field_capacity_layer_6,field_capacity_layer_7,wilting_point_layer_1,wilting_point_layer_2,wilting_point_layer_3,
               wilting_point_layer_4,wilting_point_layer_5,wilting_point_layer_6,wilting_point_layer_7,original_awc_layer_1,original_awc_layer_2,original_awc_layer_3,
               original_awc_layer_4,original_awc_layer_5,original_awc_layer_6,original_awc_layer_7,centimeter_awc_layer_1,
               centimeter_awc_layer_2,centimeter_awc_layer_3,centimeter_awc_layer_4,centimeter_awc_layer_5,centimeter_awc_layer_6,centimeter_awc_layer_7,soil_profile_awc)
       
       cur.execute(query)
    
       db.commit()  
     except Exception, err:
       print err
       db.rollback()
       #db.close()
     finally:
       db.close()       
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
        return -999    
# calculation_relation_analysis(1,'dwkimiti@gmail.com',1.75,3.5,1,0.5,0.75,1)
