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

def insert_climate_summary_data_output(record_id, record_name, Y, X, climate_precip_list,climate_average_temp_list,climate_max_temp_list,climate_min_temp_list):
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
       
       climate_precip_jan = climate_precip_list[0] 
       climate_precip_feb = climate_precip_list[1]
       climate_precip_mar = climate_precip_list[2]
       climate_precip_apr = climate_precip_list[3]
       climate_precip_may = climate_precip_list[4]
       climate_precip_jun = climate_precip_list[5]
       climate_precip_jul = climate_precip_list[6]
       climate_precip_aug = climate_precip_list[7]
       climate_precip_sep = climate_precip_list[8]
       climate_precip_oct = climate_precip_list[9]
       climate_precip_nov = climate_precip_list[10]
       climate_precip_dec = climate_precip_list[11]
       
       query = "INSERT INTO landpks_climate_precip_summary (record_id,plot_id,record_name,latitude,longitude,climate_precip_jan,climate_precip_feb,climate_precip_mar,climate_precip_apr,climate_precip_may,climate_precip_jun,climate_precip_jul,climate_precip_aug,climate_precip_sep,climate_precip_oct,climate_precip_nov,climate_precip_dec) VALUES (%s,%s,'%s',%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
                climate_precip_jan,climate_precip_feb,climate_precip_mar,climate_precip_apr,climate_precip_may,climate_precip_jun,climate_precip_jul,climate_precip_aug,climate_precip_sep,climate_precip_oct,
                climate_precip_nov,climate_precip_dec)
       cur.execute(query)
       db.commit()
       
       
       climate_average_temp_jan = climate_average_temp_list[0] 
       climate_average_temp_feb = climate_average_temp_list[1]
       climate_average_temp_mar = climate_average_temp_list[2]
       climate_average_temp_apr = climate_average_temp_list[3]
       climate_average_temp_may = climate_average_temp_list[4]
       climate_average_temp_jun = climate_average_temp_list[5]
       climate_average_temp_jul = climate_average_temp_list[6]
       climate_average_temp_aug = climate_average_temp_list[7]
       climate_average_temp_sep = climate_average_temp_list[8]
       climate_average_temp_oct = climate_average_temp_list[9]
       climate_average_temp_nov = climate_average_temp_list[10]
       climate_average_temp_dec = climate_average_temp_list[11]
       query = "INSERT INTO landpks_climate_average_temp_summary (record_id,plot_id,record_name,latitude,longitude,climate_avg_temp_jan,climate_avg_temp_feb,climate_avg_temp_mar,climate_avg_temp_apr,climate_avg_temp_may,climate_avg_temp_jun,climate_avg_temp_jul,climate_avg_temp_aug,climate_avg_temp_sep,climate_avg_temp_oct,climate_avg_temp_nov,climate_avg_temp_dec) VALUES (%s,%s,'%s',%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
                climate_average_temp_jan,climate_average_temp_feb,climate_average_temp_mar,climate_average_temp_apr,climate_average_temp_may,
                climate_average_temp_jun,climate_average_temp_jul,climate_average_temp_aug,climate_average_temp_sep,climate_average_temp_oct,climate_average_temp_nov,
                climate_average_temp_dec)
       cur.execute(query)
       db.commit()
       
       
       climate_max_temp_jan = climate_max_temp_list[0] 
       climate_max_temp_feb = climate_max_temp_list[1]
       climate_max_temp_mar = climate_max_temp_list[2]
       climate_max_temp_apr = climate_max_temp_list[3]
       climate_max_temp_may = climate_max_temp_list[4]
       climate_max_temp_jun = climate_max_temp_list[5]
       climate_max_temp_jul = climate_max_temp_list[6]
       climate_max_temp_aug = climate_max_temp_list[7]
       climate_max_temp_sep = climate_max_temp_list[8]
       climate_max_temp_oct = climate_max_temp_list[9]
       climate_max_temp_nov = climate_max_temp_list[10]
       climate_max_temp_dec = climate_max_temp_list[11]
       query = "INSERT INTO landpks_climate_max_temp_summary (record_id,plot_id,record_name,latitude,longitude,climate_max_temp_jan,climate_max_temp_feb,climate_max_temp_mar,climate_max_temp_apr,climate_max_temp_may,climate_max_temp_jun,climate_max_temp_jul,climate_max_temp_aug,climate_max_temp_sep,climate_max_temp_oct,climate_max_temp_nov,climate_max_temp_dec) VALUES (%s,%s,'%s',%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
                climate_max_temp_jan,climate_max_temp_feb,climate_max_temp_mar,climate_max_temp_apr,climate_max_temp_may,
                climate_max_temp_jun,climate_max_temp_jul,climate_max_temp_aug,climate_max_temp_sep,climate_max_temp_oct,climate_max_temp_nov,
                climate_max_temp_dec)
       cur.execute(query)
       db.commit()
       
       climate_min_temp_jan = climate_min_temp_list[0]
       climate_min_temp_feb = climate_min_temp_list[1]
       climate_min_temp_mar = climate_min_temp_list[2]
       climate_min_temp_apr = climate_min_temp_list[3]
       climate_min_temp_may = climate_min_temp_list[4]
       climate_min_temp_jun = climate_min_temp_list[5]
       climate_min_temp_jul = climate_min_temp_list[6]
       climate_min_temp_aug = climate_min_temp_list[7]
       climate_min_temp_sep = climate_min_temp_list[8]
       climate_min_temp_oct = climate_min_temp_list[9]
       climate_min_temp_nov = climate_min_temp_list[10]
       climate_min_temp_dec = climate_min_temp_list[11]
       query = "INSERT INTO landpks_climate_min_temp_summary (record_id,plot_id,record_name,latitude,longitude,climate_min_temp_jan,climate_min_temp_feb,climate_min_temp_mar,climate_min_temp_apr,climate_min_temp_may,climate_min_temp_jun,climate_min_temp_jul,climate_min_temp_aug,climate_min_temp_sep,climate_min_temp_oct,climate_min_temp_nov,climate_min_temp_dec) VALUES (%s,%s,'%s',%s,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(str_record_id, str_record_id, str_record_name, str_Y, str_X,
                climate_min_temp_jan,climate_min_temp_feb,climate_min_temp_mar,climate_min_temp_apr,climate_min_temp_may,
                climate_min_temp_jun,climate_min_temp_jul,climate_min_temp_aug,climate_min_temp_sep,climate_min_temp_oct,climate_min_temp_nov,
                climate_min_temp_dec)
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
