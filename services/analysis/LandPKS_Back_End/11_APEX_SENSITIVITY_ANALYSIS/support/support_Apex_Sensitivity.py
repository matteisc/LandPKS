# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len

try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
       from osgeo import gdal, ogr
       import struct
       import numpy
except:
       sys.exit("Please install MySQLLib for Python or Database raised error")
def getRasterValue(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_UInt16)  # Assumes 16 bit int aka 'short'
    intval = struct.unpack('h' , structval)  # use the 'short' format code (2 bytes) not int (4 bytes)
    return(intval[0])
def getRasterValue_ThanhNguyen_TIF(src_file,mx,my):
    src_ds = gdal.Open(src_file) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]
def standard_string(line_7650):
    line_7650 = line_7650.strip()
    line_7650 = line_7650.replace("         ", " ")
    line_7650 = line_7650.replace("        ", " ")
    line_7650 = line_7650.replace("       ", " ")
    line_7650 = line_7650.replace("      ", " ")
    line_7650 = line_7650.replace("     ", " ")
    line_7650 = line_7650.replace("    ", " ")
    line_7650 = line_7650.replace("   ", " ")
    line_7650 = line_7650.replace("  ", " ")
    return line_7650
def get_collection_data_from_record_name(record_name):
    try: 
        cur = db.cursor()
        sql = "SELECT ID, name, recorder_name, latitude, longitude, insert_normal_time, organization  FROM landpks_input_data WHERE UCASE(recorder_name) = '%s' ORDER BY ID" % (record_name.strip().upper())
        
        cur.execute(sql)
        results = cur.fetchall()
        list_records = []
        for row in results :
            if (row[0] is not None):
                ID = row[0]
            else:
                ID = ""
                
            if (row[1] is not None):
                name = str(row[1])
            else:
                name = ""
            
            if (row[2] is not None):
                recorder_name = str(row[2])
            else:
                recorder_name = ""
            
            if (row[3] is not None and float(row[3])):
                latitude = row[3]
            else:
                latitude = 0.0  
            
            if (row[4] is not None and float(row[4])):
                longitude = row[4]
            else:
                longitude = 0.0
                
            if (row[5] is not None):
                time = row[5]
            else:
                time = ""
            if (row[6] is not None):
                org = row[6]
            else:
                org = ""    
            entry_records = [ID,name,recorder_name,latitude,longitude,time,org]
            list_records.append(entry_records)
        return list_records
    except Exception,err:
        print err
        return None