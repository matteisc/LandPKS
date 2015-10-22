
__version__ = "1"
from osgeo import gdal, ogr
import struct, os, csv, codecs, cStringIO, sys
import numpy
from __builtin__ import str

WISE3_SITE_INPUT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\ISRIC_WISE_DATABASE\\WISE3_SITE.csv"
WISE3_HORIZON_INPUT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\ISRIC_WISE_DATABASE\\WISE3_HORIZON.csv"
WISE3_LANDPKS_OUTPUT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL.csv"
TIF_DIR = "D:\\ThanhNguyen_Working\\Python_APEX\\TIF_FILE_COLLECTION\\"

mess = "Usage : python Step_2_Run_Stage_Similarity_Model_All_At_One_Calculation.py -ouput_wise_landpks_csv <Full Path to Output>"
if (len(sys.argv) < 6):
    print("Using default value \nWISE_SITE = %s ; \nWISE_HORIZON = %s ; \nWISE_LANDPKS = %s" %(WISE3_SITE_INPUT_CSV_FILE,WISE3_HORIZON_INPUT_CSV_FILE,WISE3_LANDPKS_OUTPUT_CSV_FILE))
else:
    if (sys.argv[1] == '-input_wise_site_csv'):
        if (sys.argv[2] is not None):
            WISE3_SITE_INPUT_CSV_FILE = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)

    if (sys.argv[3] == '-input_wise_horizon_csv'):
        if (sys.argv[4] is not None):
            WISE3_HORIZON_INPUT_CSV_FILE = sys.argv[4].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)

    if (sys.argv[5] == '-ouput_wise_landpks_csv'):
        if (sys.argv[6] is not None):
            WISE3_LANDPKS_OUTPUT_CSV_FILE = sys.argv[6].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)

class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
    
def getRasterValue(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    try:
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_UInt16)  # Assumes 16 bit int aka 'short'
        intval = struct.unpack('h' , structval)  # use the 'short' format code (2 bytes) not int (4 bytes)
        return(intval[0])
    except Exception,err:
        return -1
def getRasterValue_ThanhNH(srcfile, mx, my):  
    try:# # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception,err:
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
def readLATLONGisricToBuildLatLongLandPKS_GDAL(in_csv,out_csv):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       
       out_csvfile = open(out_csv, 'wb')
       out = UnicodeWriter(out_csvfile)
       out.writerow(['WISE3_ID', 'WISE3_LAT_I', 'WISE3_LAT_DEG', 'WISE3_LAT_MIN', 'WISE3_LAT_SEC', 'WISE3_LONG_I', 'WISE3_LONG_DEG','WISE3_LONG_MIN','WISE3_LONG_SEC','LATITUDE_DECIMAL','LONGITUDE_DECIMAL',
                     'CLIM_SLATE_WEATHER_DATA','CLIM_PRECIPITATION_DATA','CLIM_GDD','CLIM_ARIDITY_INDEX','CLIM_KOPGEIGER','CKIM_FAO_LGP','CLIM_MODIS_evapotrans','clim_precip_novdecjan','clim_precip_febmarapr',
                     'clim_precip_mayjunjul','clim_precip_augsepoct','clim_wind_data_1','clim_wind_data_2','clim_wind_data_3','clim_wind_data_4','clim_wind_data_5','clim_wind_data_6','clim_wind_data_7',
                     'clim_wind_data_8','clim_wind_data_9','clim_wind_data_10','clim_wind_data_11','clim_wind_data_12','topog_elevation','topog_aspect','topog_geolage','topog_dem_global','topog_dem_old',
                     'topog_slope_global','topog_landform_global','topog_twi_global','topog_topi_global','topog_israd_global','landcover_modis_2012','vegind_modis_evi_m','vegind_modis_evi_sd','WISE3_FAO_74'
                     ])
       
       for row in l:
           WISE3_ID = str(row[0]).upper()
           WISE3_FAO_74 = str(row[9]).strip()
           WISE3_Latit = str(row[15]).upper().strip()
           if (str(row[16]).strip() is not None and str(row[16]).strip() != ""):
               WISE3_LatDeg = float(row[16])
           else:
               WISE3_LatDeg = float(0)
           if (str(row[17]).strip() is not None and str(row[17]).strip() != ""):
               WISE3_LatMin = float(row[17])
           else:        
               WISE3_LatMin = float(0)
           if (str(row[18]).strip() is not None and str(row[18]).strip() != ""):
               WISE3_LatSec = float(row[18])
           else:
               WISE3_LatSec = float(0)
               
           WISE3_LongI = str(row[19]).upper().strip()
           
           if (str(row[20]).strip() is not None and str(row[20]).strip() != ""):
               WISE3_LongDeg = float(row[20])
           else:
               WISE3_LongDeg = float(0)
           if (str(row[21]).strip() is not None and str(row[21]).strip() != ""):     
               WISE3_LongMin = float(row[21])
           else:
               WISE3_LongMin = float(0)
           if (str(row[22]).strip() is not None and str(row[22]).strip() != ""):     
               WISE3_LongSec = float(row[22])
           else:
               WISE3_LongSec = float(0)
               
               
           if (WISE3_LatDeg == 0 and WISE3_LatMin == 0 and WISE3_LatSec == 0):
               latitude_decimal = -999
           else:    
               latitude_decimal = WISE3_LatDeg + WISE3_LatMin/60 + WISE3_LatSec/3600
               if (WISE3_Latit == "S"):
                   latitude_decimal = 0 - latitude_decimal
        
           if (WISE3_LongDeg == 0 and WISE3_LongMin == 0 and WISE3_LongSec == 0):
               longitude_decimal = -999
           else:    
               longitude_decimal = WISE3_LongDeg + WISE3_LongMin/60 + WISE3_LongSec/ 3600
               if (WISE3_LongI == "W"):
                   longitude_decimal = 0 - longitude_decimal
               
           print "================================================="
           print "ID : %s | LatI = %s | LatDeg = %s | LatMin = %s | LatSec = %s | | LongI = %s | LongDeg = %s | LongMin = %s | LongSec = %s ===> Latitude_Decimal = %s ; Longitude_Decimal = %s" % (WISE3_ID,
                WISE3_Latit,str(WISE3_LatDeg),str(WISE3_LatMin),str(WISE3_LatSec),WISE3_LongI,str(WISE3_LongDeg),str(WISE3_LongMin),str(WISE3_LongSec),str(latitude_decimal),str(longitude_decimal))
           
           #--------------------------------------------------------------------------------
           if (longitude_decimal == -999 or latitude_decimal == -999):
              slate_weather_data =-999
              anual_precipitation_data = -999
           else:
              #------------------------------------
              tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
              slate_weather_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + tif_slate_weather, longitude_decimal, latitude_decimal))
              #------------------------------------
              tif_annual_precipitation = 'annual_precipitation/annual_precip.tif'
              anual_precipitation_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_annual_precipitation , longitude_decimal, latitude_decimal)
              #------------------------------------
              tif_growing_degree_days = 'growing_degree_days/gdd.tif'
              gdd_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_growing_degree_days , longitude_decimal, latitude_decimal)
              #------------------------------------
              tif_aridity_index = 'aridity/ai_yr.tif'
              aridity_index_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_aridity_index , longitude_decimal, latitude_decimal)
              if (aridity_index_data != -999):
                  aridity_index_data = aridity_index_data*0.0001
              #------------------------------------
              tif_worldkgeiger_climate_zone = 'GLOBAL_LAYER/WorldKGeiger/WorldKGeiger.tif'
              worldkgeiger_climate_zone_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + tif_worldkgeiger_climate_zone , longitude_decimal, latitude_decimal))
              #------------------------------------
              tif_fao_lgp = 'GLOBAL_LAYER/FAO_LGP/LGP.tif'
              fao_lgp_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + tif_fao_lgp , longitude_decimal, latitude_decimal))
              #------------------------------------
              tif_MODIS_evapotrans = 'WORLD_GRID/Climate_Dataset/ETMNTS3a.tif'
              MODIS_evapotrans_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_MODIS_evapotrans , longitude_decimal, latitude_decimal)
              #------------------------------------
              tif_precip_novdecjan = 'WORLD_GRID/Climate_Dataset/PX1WCL3a.tif'
              precip_novdecjan_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_novdecjan , longitude_decimal, latitude_decimal)
              #------------------------------------
              tif_precip_febmarapr = 'WORLD_GRID/Climate_Dataset/PX2WCL3a.tif'
              precip_febmarapr_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_febmarapr , longitude_decimal, latitude_decimal)
              #------------------------------------
              tif_precip_mayjunjul = 'WORLD_GRID/Climate_Dataset/PX3WCL3a.tif'
              precip_mayjunjul_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_mayjunjul , longitude_decimal, latitude_decimal)  
              #------------------------------------
              tif_precip_augsepoct = 'WORLD_GRID/Climate_Dataset/PX4WCL3a.tif'
              precip_augsepoct_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_precip_augsepoct , longitude_decimal, latitude_decimal)
              #------------------------------------
              wind_data_1 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind12001.tif/gwind12001.tif' , longitude_decimal, latitude_decimal) 
              wind_data_2 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind22001.tif/gwind22001.tif' , longitude_decimal, latitude_decimal)
              wind_data_3 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind32001.tif/gwind32001.tif' , longitude_decimal, latitude_decimal)
              wind_data_4 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind42001.tif/gwind42001.tif' , longitude_decimal, latitude_decimal)
              wind_data_5 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind52001.tif/gwind52001.tif' , longitude_decimal, latitude_decimal)
              wind_data_6 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind62001.tif/gwind62001.tif' , longitude_decimal, latitude_decimal)
              wind_data_7 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind72001.tif/gwind72001.tif' , longitude_decimal, latitude_decimal)
              wind_data_8 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind82001.tif/gwind82001.tif' , longitude_decimal, latitude_decimal)
              wind_data_9 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind92001.tif/gwind92001.tif' , longitude_decimal, latitude_decimal)
              wind_data_10 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind102001.tif/gwind102001.tif' , longitude_decimal, latitude_decimal)
              wind_data_11 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind112001.tif/gwind112001.tif' , longitude_decimal, latitude_decimal)
              wind_data_12 = getRasterValue_ThanhNH_Float(TIF_DIR + 'global_wind_tifs/gwind122001.tif/gwind122001.tif' , longitude_decimal, latitude_decimal)
              #--------------------------------------------------------------------------------
              tif_ELEVATION = 'elevation/elevation.tif'
              elevation_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_ELEVATION , longitude_decimal, latitude_decimal)
              if (elevation_data == -999 or elevation_data == '-999' or elevation_data == -999.0 or elevation_data == '-999.0'):
                   elevation_data = -999
              #--------------------------------------------------------------------------------
              tif_file_aspect = 'aspect/ASPECT.tif'
              aspect_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_file_aspect , longitude_decimal, latitude_decimal)
              if (aspect_data == -999 or aspect_data == '-999' or aspect_data == -999.0 or aspect_data == '-999.0'):
                   aspect_data = -999
              #--------------------------------------------------------------------------------     
              topog_geolage_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/GEAISG3a.tif' , longitude_decimal, latitude_decimal))
              if (topog_geolage_data == -999 or topog_geolage_data == '-999' or topog_geolage_data == -999.0 or topog_geolage_data == '-999.0'):
                  topog_geolage_data = -999     
              #--------------------------------------------------------------------------------
              tif_DEM = 'GLOBAL_GIS_DATA/AFRICA_DEM/SRTM_MOSAIC1.tif'
              dem_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_DEM , longitude_decimal, latitude_decimal)
              #--------------------------------------------------------------------------------
              tif_DEM = 'WORLD_GRID/Topography_Dataset/DEMSRE3a/DEMSRE3a.tif'
              dem_world_grid_data = getRasterValue_ThanhNH_Float(TIF_DIR + tif_DEM , longitude_decimal, latitude_decimal)
              #--------------------------------------------------------------------------------
              topog_slope_global_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/SLPSRT3a.tif' , longitude_decimal, latitude_decimal))
              #--------------------------------------------------------------------------------
              topog_landform_global_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/L3POBI3B.tif' , longitude_decimal, latitude_decimal))
              #--------------------------------------------------------------------------------
              topog_topog_twi_global_data = getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/TWISRE3a.tif' , longitude_decimal, latitude_decimal) 
              if (topog_topog_twi_global_data != -999 and topog_topog_twi_global_data != '-999' and topog_topog_twi_global_data != -999.0 and topog_topog_twi_global_data != '-999.0'):
                 topog_topog_twi_global_data = topog_topog_twi_global_data*10 + 10
              #--------------------------------------------------------------------------------
              topog_topog_topi_global_data = getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/OPISRE3a.tif' , longitude_decimal, latitude_decimal)
              if (topog_topog_topi_global_data != -999 and topog_topog_topi_global_data != '-999' and topog_topog_topi_global_data != -999.0 and topog_topog_topi_global_data != '-999.0'):
                 topog_topog_topi_global_data = topog_topog_topi_global_data/1000    
              #--------------------------------------------------------------------------------
              topog_topog_israd_global_data = getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Topography_Dataset/INMSRE3a.tif' , longitude_decimal, latitude_decimal)
              if (topog_topog_israd_global_data != -999 and topog_topog_israd_global_data != '-999' and topog_topog_israd_global_data != -999.0 and topog_topog_israd_global_data != '-999.0'):
                   topog_topog_israd_global_data = topog_topog_israd_global_data*365/8
              #--------------------------------------------------------------------------------
              landcover_modis_2012_data = int(getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Land_Cover_Dataset/G12IGB3a.tif' , longitude_decimal, latitude_decimal))
              #--------------------------------------------------------------------------------    
              vegind_modis_evi_m_data = getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/EVMMOD3a.tif' , longitude_decimal, latitude_decimal) 
              #--------------------------------------------------------------------------------    
              vegind_modis_evi_sd_data = getRasterValue_ThanhNH_Float(TIF_DIR + 'WORLD_GRID/Vegetation_Indices/EVSMOD3a.tif' , longitude_decimal, latitude_decimal)
           #--------------------------------------------------------------------------------
           
           out.writerow([WISE3_ID, WISE3_Latit, str(WISE3_LatDeg), str(WISE3_LatMin), str(WISE3_LatSec), WISE3_LongI, str(WISE3_LongDeg),str(WISE3_LongMin),str(WISE3_LongSec),str(latitude_decimal),str(longitude_decimal),
                         str(slate_weather_data),str(anual_precipitation_data),str(gdd_data),str(aridity_index_data),str(worldkgeiger_climate_zone_data),str(fao_lgp_data),str(MODIS_evapotrans_data),
                         str(precip_novdecjan_data),str(precip_febmarapr_data),str(precip_mayjunjul_data),str(precip_augsepoct_data),str(wind_data_1),str(wind_data_2),str(wind_data_3),
                         str(wind_data_4),str(wind_data_5),str(wind_data_6),str(wind_data_7),str(wind_data_8),str(wind_data_9),str(wind_data_10),str(wind_data_11),str(wind_data_12),str(elevation_data),
                         str(aspect_data),str(topog_geolage_data),str(dem_world_grid_data),str(dem_data),str(topog_slope_global_data),str(topog_landform_global_data),str(topog_topog_twi_global_data),
                         str(topog_topog_topi_global_data),str(topog_topog_israd_global_data),str(landcover_modis_2012_data),str(vegind_modis_evi_m_data),str(vegind_modis_evi_sd_data),str(WISE3_FAO_74)
                        ])
            
       return 1    
    except Exception, err:
       print err
       return -1
def main():
    
    if (not os.path.exists(WISE3_SITE_INPUT_CSV_FILE)):
        print "==Error 405 : File WISE3_SITE.csv was not existed==="
        sys.exit()
    if (not os.path.exists(WISE3_HORIZON_INPUT_CSV_FILE)):
        print "==Error 405 : File WISE3_HORIZON.csv was not existed==="
        sys.exit()
        
    result_1 =readLATLONGisricToBuildLatLongLandPKS_GDAL(WISE3_SITE_INPUT_CSV_FILE,WISE3_LANDPKS_OUTPUT_CSV_FILE)
    if (result_1 == 1):
        print "==Step 1 : Successfully==="
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
