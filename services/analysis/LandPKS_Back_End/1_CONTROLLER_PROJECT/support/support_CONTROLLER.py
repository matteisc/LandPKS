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

try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
       
       
def insert_gdal_data_country_level(record_id, record_name, Y, X, country_code_data,country_name,country_slope_percentage,country_slope_reclassified,country_plane_curvature,
                                   country_profile_curvature,country_curvature,country_dem,country_aspect):
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
       str_country_code_data = (str(country_code_data)).strip()
       str_country_name = (str(country_name)).strip()
       str_country_slope_percentage = (str(country_slope_percentage)).strip()
       str_country_slope_reclassified = (str(country_slope_reclassified)).strip()
       str_country_plane_curvature = (str(country_plane_curvature)).strip()
       str_country_profile_curvature = (str(country_profile_curvature)).strip()
       str_country_curvature = (str(country_curvature)).strip()
       str_dem = (str(country_dem)).strip()
       str_aspect = (str(country_aspect)).strip()
       
       query = "INSERT INTO landpks_gdal_data_country_level (record_id,plot_id,record_name,latitude,longitude,country_code_data,country_name,slope_percentage,slope_reclassified,plane_curvature,profile_curvature,curvature,dem,aspect) VALUES (%s,%s,'%s',%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
               str_country_code_data,str_country_name,str_country_slope_percentage,str_country_slope_reclassified,str_country_plane_curvature,str_country_profile_curvature,str_country_curvature,
               str_dem,str_aspect)
       
       cur.execute(query)
    
       db.commit()  
     except Exception, err:
       print err
       db.rollback()
       db.close()
     finally:
       db.close()
       
       
def insert_gdal_data_to_store(record_id, record_name, Y, X, country_code_data, clim_slate_weather_data, clim_precipitation_data, clim_gdd, clim_aridity_index, clim_kopgeiger, clim_fao_lgp, 
                              MODIS_evapotrans_data,precip_novdecjan_data ,precip_febmarapr_data,precip_mayjunjul_data,precip_augsepoct_data,wind_data_1, wind_data_2, wind_data_3, wind_data_4, wind_data_5, wind_data_6, wind_data_7, 
                              wind_data_8, wind_data_9, wind_data_10, wind_data_11, wind_data_12,hwsd_soil_data,soil_depth_gaez_data,soil_textclass_gaez_data,soil_fert_gaez_data,soil_workab_gaez,soil_toxic_gaez,
                              topog_elevation,topog_aspect,topog_geolage_data,dem_world_grid_data,dem_data,topog_slope_global_data,topog_landform_global_data,topog_twi_global_data,topog_topi_global_data,topog_israd_global_data,
                              landcover_modis_2001_data,landcover_modis_2002_data,landcover_modis_2004_data,landcover_modis_2010_data,landcover_modis_2011_data,landcover_modis_2012_data,
                              landcover_cult_gaez_data,landcover_irrcult_gaez_data,landcover_grass_gaez_data,landcover_protect_gaez_data,landcover_agnprotect_gaez_data,
                              vegind_modis_evi_m_data,vegind_modis_evi_sd_data,vegind_modis_lai_m_data,vegind_modis_lai_sd_data,manage_cerealsuit_low_gaez_data,manage_cerealsuit_hight_gaez_data,
                              pop_density_data,afsis_topog_dem_data,afsis_topog_twi_data,afsis_topog_sca_data):
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
       str_slate_weather_data = (str(clim_slate_weather_data)).strip()
       str_country_code_data = (str(country_code_data)).strip()
       str_wind_data_1 = (str(wind_data_1)).strip()
       str_wind_data_2 = (str(wind_data_2)).strip()
       str_wind_data_3 = (str(wind_data_3)).strip()
       str_wind_data_4 = (str(wind_data_4)).strip()
       str_wind_data_5 = (str(wind_data_5)).strip()
       str_wind_data_6 = (str(wind_data_6)).strip()
       str_wind_data_7 = (str(wind_data_7)).strip()
       str_wind_data_8 = (str(wind_data_8)).strip()
       str_wind_data_9 = (str(wind_data_9)).strip()
       str_wind_data_10 = (str(wind_data_10)).strip()
       str_wind_data_11 = (str(wind_data_11)).strip()
       str_wind_data_12 = (str(wind_data_12)).strip()
       str_clim_precipitation_data = (str(clim_precipitation_data)).strip()
       str_clim_gdd = (str(clim_gdd)).strip()
       str_clim_aridity_index = (str(clim_aridity_index)).strip()
       str_clim_kopgeiger = (str(clim_kopgeiger)).strip()
       str_clim_fao_lgp = (str(clim_fao_lgp)).strip()
       str_clim_MODIS_evapotrans_data = (str(MODIS_evapotrans_data)).strip()
       str_clim_precip_novdecjan_data = (str(precip_novdecjan_data)).strip()
       str_clim_precip_febmarapr_data = (str(precip_febmarapr_data)).strip()
       str_clim_precip_mayjunjul_data = (str(precip_mayjunjul_data)).strip()
       str_clim_precip_augsepoct_data = (str(precip_augsepoct_data)).strip()
       
       str_hwsd_soil_data = (str(hwsd_soil_data)).strip()
       str_soil_depth_gaez_data = (str(soil_depth_gaez_data)).strip()
       str_soil_textclass_gaez_data = (str(soil_textclass_gaez_data)).strip()
       str_soil_fert_gaez_data = (str(soil_fert_gaez_data)).strip()
       str_soil_workab_gaez_data = (str(soil_workab_gaez)).strip()
       str_soil_toxic_gaez_data = (str(soil_toxic_gaez)).strip()
       
       str_topog_elevation_data = (str(topog_elevation)).strip()
       str_topog_aspect_data = (str(topog_aspect)).strip()
       str_topog_geolage_data = (str(topog_geolage_data)).strip()
       str_topog_slope_global_data = (str(topog_slope_global_data)).strip()
       str_topog_landform_global_data = (str(topog_landform_global_data)).strip()
       
       str_topog_twi_global_data = (str(topog_twi_global_data)).strip()
       str_topog_topi_global_data = (str(topog_topi_global_data)).strip()
       str_topog_israd_global_data = (str(topog_israd_global_data)).strip()
       
       str_dem = (str(dem_data)).strip()
       str_dem_world_grid = (str(dem_world_grid_data)).strip()
       
       str_landcover_modis_2001_data = (str(landcover_modis_2001_data)).strip()
       str_landcover_modis_2002_data = (str(landcover_modis_2002_data)).strip()
       str_landcover_modis_2004_data = (str(landcover_modis_2004_data)).strip()
       str_landcover_modis_2010_data = (str(landcover_modis_2010_data)).strip()
       str_landcover_modis_2011_data = (str(landcover_modis_2011_data)).strip()
       str_landcover_modis_2012_data = (str(landcover_modis_2012_data)).strip()
       str_landcover_cult_gaez_data = (str(landcover_cult_gaez_data)).strip()
       str_landcover_irrcult_gaez_data = (str(landcover_irrcult_gaez_data)).strip()
       str_landcover_grass_gaez_data = (str(landcover_grass_gaez_data)).strip()
       str_landcover_protect_gaez_data = (str(landcover_protect_gaez_data)).strip()
       str_landcover_agnprotect_gaez_data = (str(landcover_agnprotect_gaez_data)).strip()
       
       
       str_vegind_modis_evi_m_data = (str(vegind_modis_evi_m_data)).strip()
       str_vegind_modis_evi_sd_data = (str(vegind_modis_evi_sd_data)).strip()
       str_vegind_modis_lai_m_data = (str(vegind_modis_lai_m_data)).strip()
       str_vegind_modis_lai_sd_data = (str(vegind_modis_lai_sd_data)).strip()
       
       
       str_manage_cerealsuit_low_gaez_data = (str(manage_cerealsuit_low_gaez_data)).strip()
       str_manage_cerealsuit_hight_gaez_data = (str(manage_cerealsuit_hight_gaez_data)).strip()
       
       str_pop_density_data = (str(pop_density_data)).strip()
       
       str_afsis_topog_dem_data = (str(afsis_topog_dem_data)).strip()
       str_afsis_topog_twi_data = (str(afsis_topog_twi_data)).strip()
       str_afsis_topog_sca_data = (str(afsis_topog_sca_data)).strip()
       
       query = "INSERT INTO landpks_gdal_data_global_level (record_id,plot_id,record_name,latitude,longitude,country_code_data,clim_slate_weather_data,clim_precipitation_data,clim_gdd,clim_aridity_index,clim_kopgeiger,clim_fao_lgp,clim_modis_evapotrans,clim_precip_novdecjan,clim_precip_febmarapr,clim_precip_mayjunjul,clim_precip_augsepoct,clim_wind_data_1,clim_wind_data_2,clim_wind_data_3,clim_wind_data_4,clim_wind_data_5,clim_wind_data_6,clim_wind_data_7,clim_wind_data_8,clim_wind_data_9,clim_wind_data_10,clim_wind_data_11,clim_wind_data_12,soil_hwsd_data,soil_depth_gaez,soil_textclass_gaez,soil_fert_gaez,soil_workab_gaez,soil_toxic_gaez,topog_elevation,topog_aspect,topog_geolage,topog_dem_global,topog_dem_old,topog_slope_global,topog_landform_global,topog_twi_global,topog_topi_global,topog_israd_global,landcover_modis_2001,landcover_modis_2002,landcover_modis_2004,landcover_modis_2010,landcover_modis_2011,landcover_modis_2012,landcover_cult_gaez,landcover_irrcult_gaez,landcover_grass_gaez,landcover_protect_gaez,landcover_agnprotect_gaez,vegind_modis_evi_m,vegind_modis_evi_sd,vegind_modis_lai_m,vegind_modis_lai_sd,manage_cerealsuit_low_gaez,manage_cerealsuit_hight_gaez,pop_density,afsis_topog_dem,afsis_topog_twi,afsis_topog_sca) VALUES (%s,%s,'%s',%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
               str_country_code_data,str_slate_weather_data, str_clim_precipitation_data, str_clim_gdd, 
               str_clim_aridity_index, str_clim_kopgeiger, str_clim_fao_lgp, str_clim_MODIS_evapotrans_data,str_clim_precip_novdecjan_data,str_clim_precip_febmarapr_data,str_clim_precip_mayjunjul_data,str_clim_precip_augsepoct_data,str_wind_data_1,
               str_wind_data_2,str_wind_data_3,str_wind_data_4,str_wind_data_5,
               str_wind_data_6,str_wind_data_7,str_wind_data_8,str_wind_data_9,str_wind_data_10,str_wind_data_11,str_wind_data_12,str_hwsd_soil_data,str_soil_depth_gaez_data,str_soil_textclass_gaez_data,
               str_soil_fert_gaez_data,str_soil_workab_gaez_data,str_soil_toxic_gaez_data,str_topog_elevation_data,str_topog_aspect_data,
               str_topog_geolage_data,str_dem_world_grid,str_dem,str_topog_slope_global_data,str_topog_landform_global_data,str_topog_twi_global_data,str_topog_topi_global_data,str_topog_israd_global_data,
               str_landcover_modis_2001_data,str_landcover_modis_2002_data,str_landcover_modis_2004_data,str_landcover_modis_2010_data,str_landcover_modis_2011_data,str_landcover_modis_2012_data,
               str_landcover_cult_gaez_data,str_landcover_irrcult_gaez_data,str_landcover_grass_gaez_data,str_landcover_protect_gaez_data,str_landcover_agnprotect_gaez_data,
               str_vegind_modis_evi_m_data,str_vegind_modis_evi_sd_data,str_vegind_modis_lai_m_data,str_vegind_modis_lai_sd_data,str_manage_cerealsuit_low_gaez_data,str_manage_cerealsuit_hight_gaez_data,
               str_pop_density_data,str_afsis_topog_dem_data,str_afsis_topog_twi_data,str_afsis_topog_sca_data)
       
       
       #query = "INSERT INTO landpks_map_input_files (name,latitude,longitude,dly_file_name) VALUES ('%s',%s,%s,'%s')" %("FUCK",12.12,13.13,"FUCKKING")
       
       #query = "INSERT INTO landpks_map_input_files (name,latitude,longitude,dly_file_name) VALUES ('FUCK',12.12,13.13,'FUCKING')"
       
       cur.execute(query)
    
       db.commit()  
    except Exception, err:
       print err
       db.rollback()
       db.close()
    finally:
       db.close() 

def perform_update(ID, maize_erosion, maize_productivity, glass_erosion, glass_productivity):
    try:
       cur = db.cursor()
       sql = "UPDATE lanpks_apex_output_data SET maize_productivity = %s, maize_erosion = %s, glass_productivity = %s, glass_erosion = %s WHERE ID = %s" % (str(maize_productivity), str(maize_erosion), str(glass_productivity), str(glass_erosion), str(ID))
       cur.execute(sql)
       db.commit()
       return 1
    except:
       db.rollback()
       return 0
def update_new_erosion_group_by_record_name(record_name, max_apex_output_y_maize, max_apex_output_yldg_maize, max_apex_output_y_glass, max_apex_output_yldg_glass):
    try:
        cur = db.cursor()
        sql = "SELECT ID, apex_output_y_maize, apex_output_yldg_maize, apex_output_y_glass, apex_output_yldg_glass FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
        cur.execute(sql)
        results = cur.fetchall()
        for row in results :
           ID = row[0]
           if (max_apex_output_y_maize <> 0):
               maize_erosion = float(row[1]) / float(max_apex_output_y_maize)
           else:
               maize_erosion = 0.0
           if (max_apex_output_yldg_maize <> 0):
               maize_productivity = float(row[2]) / float(max_apex_output_yldg_maize)
           else:
               maize_productivity = 0.0
               
           if (max_apex_output_y_glass <> 0):    
               glass_erosion = float(row[3]) / float(max_apex_output_y_glass)
           else:
               glass_erosion = 0.0
               
           if (max_apex_output_yldg_glass <> 0):
               glass_productivity = float(row[4]) / float(max_apex_output_yldg_glass)
           else:
               glass_productivity = 0.0
               
           result = perform_update(ID, maize_erosion, maize_productivity, glass_erosion, glass_productivity)
           
           if (result == 1):
               print ("Update Done %s " % (str(ID)))
           else:
               print ("Update not DONE %s " % (str(ID)))
    except:
        db.rollback()

def get_list_analytics_data_from_apex_output_and_relative_calculation_model(record_name, number_of_record):
    try: 
        cur = db.cursor()
        sql = "SELECT ID, record_id, maize_productivity, maize_erosion, glass_productivity, glass_erosion FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s' ORDER BY ID DESC LIMIT 0, %s" % (record_name.strip().upper(), number_of_record)
        
        cur.execute(sql)
        results = cur.fetchall()
        list_records = []
        for row in results :
            if (row[0] is not None):
                ID = row[0]
            else:
                ID = ""
                
            if (row[1] is not None):
                record_id = row[1]
            else:
                record_id = ""
            
            if (row[2] is not None and float(row[2])):
                maize_productivity = row[2]
            else:
                maize_productivity = 0.0
            
            if (row[3] is not None and float(row[3])):
                maize_erosion = row[3]
            else:
                maize_erosion = 0.0  
            
            if (row[4] is not None and float(row[4])):
                glass_productivity = row[4]
            else:
                glass_productivity = 0.0
            
            if (row[5] is not None and float(row[5])):
                glass_erosion = row[5]
            else:
                glass_erosion = 0.0      
            
            entry_records = [ID, record_id, maize_productivity, maize_erosion, glass_productivity, glass_erosion]
            list_records.append(entry_records)
        return list_records
    except Exception, err:
        print err
        return None
def calculation_relation_analysis_2_only_insert_donot_calculate(record_id, record_name, maize_y, maize_yldg, maize_biom, glass_y, glass_yldg, glass_biom):
    try: 
       sql = "INSERT INTO lanpks_apex_output_data (record_id, record_name, apex_output_y_maize, apex_output_yldg_maize, apex_output_biom_meize, apex_output_y_glass, apex_output_yldg_glass, apex_output_biom_glass, maize_productivity, maize_erosion, glass_productivity, glass_erosion) VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (str(record_id), str(record_name), str(maize_y), str(maize_yldg), str(maize_biom), str(glass_y), str(glass_yldg), str(glass_biom), "0.0" , "0.0", "0.0", "0.0")
       cur = db.cursor()
          
       cur.execute(sql)
       db.commit()
       return 1
    except Exception, err:
       print err
       db.rollback()
       db.close()
       return 0
    finally:
       db.close()    
def calculation_relation_analysis(record_id, record_name, maize_y, maize_yldg, maize_biom, glass_y, glass_yldg, glass_biom):
    # Get Current max from Y data
    try: 
       cur = db.cursor()
       sql = "SELECT COUNT(1) FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
       cur.execute(sql)
       results = cur.fetchone()[0]
      
       if (results == 0):  # It means that this Record is the first time calling of this Record Name
           # Insert data to database only set up maize erosion, maize productivity and glass erosion and glass productivity is 0
           sql = "INSERT INTO lanpks_apex_output_data (record_id, record_name, apex_output_y_maize, apex_output_yldg_maize, apex_output_biom_meize, apex_output_y_glass, apex_output_yldg_glass, apex_output_biom_glass, maize_productivity, maize_erosion, glass_productivity, glass_erosion) VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (str(record_id), str(record_name), str(maize_y), str(maize_yldg), str(maize_biom), str(glass_y), str(glass_yldg), str(glass_biom), "0.0" , "0.0", "0.0", "0.0")
           cur = db.cursor()
          
           cur.execute(sql)
           db.commit()
           return 1
       else:    
            
            
           sql = "INSERT INTO lanpks_apex_output_data (record_id, record_name, apex_output_y_maize, apex_output_yldg_maize, apex_output_biom_meize, apex_output_y_glass, apex_output_yldg_glass, apex_output_biom_glass, maize_productivity, maize_erosion, glass_productivity, glass_erosion) VALUES (%s,'%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (str(record_id), str(record_name), str(maize_y), str(maize_yldg), str(maize_biom), str(glass_y), str(glass_yldg), str(glass_biom), "0.0" , "0.0", "0.0", "0.0")
           cur = db.cursor()
          
           cur.execute(sql)
           db.commit()
            
           # Get max Y Maize
           sql = "SELECT MAX(apex_output_y_maize) FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
           cur.execute(sql)
           results = cur.fetchone()[0]
           max_apex_output_y_maize = results
           
           
           # Get max YLDG Maize
           sql = "SELECT MAX(apex_output_yldg_maize) FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
           cur.execute(sql)
           results = cur.fetchone()[0]
           max_apex_output_yldg_maize = results
           
           
           # Get max Y Glass
           sql = "SELECT MAX(apex_output_y_glass) FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
           cur.execute(sql)
           results = cur.fetchone()[0]
           max_apex_output_y_glass = results
           
           
           # Get max YLDG Glass
           sql = "SELECT MAX(apex_output_yldg_glass) FROM lanpks_apex_output_data WHERE UCASE(record_name) = '%s'" % (record_name.strip().upper())
           cur.execute(sql)
           results = cur.fetchone()[0]
           max_apex_output_yldg_glass = results
           
           # Update for all Record
           update_new_erosion_group_by_record_name(record_name, max_apex_output_y_maize, max_apex_output_yldg_maize, max_apex_output_y_glass, max_apex_output_yldg_glass)
           # return get_list_analytics_data_from_apex_output_and_relative_calculation_model(record_name, 8)
           return 1
    except Exception, err:
       print err
       db.rollback()
       db.close()
       return 0
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
