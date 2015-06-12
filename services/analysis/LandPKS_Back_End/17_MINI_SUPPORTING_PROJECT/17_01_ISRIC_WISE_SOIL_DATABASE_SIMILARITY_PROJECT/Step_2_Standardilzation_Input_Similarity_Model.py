
__version__ = "1"

import struct, os, csv, codecs, cStringIO, sys
import numpy
from __builtin__ import str

WISE3_LANDPKS_INPUT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL.csv"
WISE3_LANDPKS_OUTPUT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL_STANDALIZATION.csv"
mess = "Usage : python Step_2_Standardilzation_Input_Similarity_Model.py -input_wise_landpks_csv <Full Path to Input> -output_wise_landpks_csv <Full Path to Output>"
if (len(sys.argv) < 2):
    print("Using default value \nWISE_LANDPKS = %s" %(WISE3_LANDPKS_OUTPUT_CSV_FILE))
else:

    if (sys.argv[1] == '-input_wise_landpks_csv'):
        if (sys.argv[2] is not None):
            WISE3_LANDPKS_INPUT_CSV_FILE = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[3] == '-output_wise_landpks_csv'):
        if (sys.argv[4] is not None):
            WISE3_LANDPKS_OUTPUT_CSV_FILE = sys.argv[4].strip()
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

def rebuildFile_Remove_All_Records_LatandLong_minus999(in_csv,out_csv):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       
       out_csvfile = open(out_csv, 'wb')
       out = UnicodeWriter(out_csvfile)
       out.writerow(['WISE3_ID','LATITUDE_DECIMAL','LONGITUDE_DECIMAL','CLIM_PRECIPITATION_DATA','CLIM_GDD','CLIM_ARIDITY_INDEX',
                     'CLIM_KOPGEIGER','CKIM_FAO_LGP','CLIM_MODIS_evapotrans','clim_precip_novdecjan','clim_precip_febmarapr',
                     'clim_precip_mayjunjul','clim_precip_augsepoct','topog_elevation','topog_geolage',
                     'topog_slope_global','topog_landform_global','topog_twi_global','topog_topi_global','topog_israd_global',
                     'landcover_modis_2012','vegind_modis_evi_m','vegind_modis_evi_sd','WISE3_FAO_74'
                     ])
       
       for row in l:
           WISE3_ID = str(row[0]).upper()
           
           latitude_decimal = str(row[9]).strip()
           longitude_decimal = str(row[10]).strip()
           clim_precipitation_date = str(row[12]).strip()
           clim_gdd =  str(row[13]).strip()
           clim_aridity_index = str(row[14]).strip()
           clim_kopgeiger = str(row[15]).strip()
           clim_fao_lgp = str(row[16]).strip()
           clim_modis_evapotrans = str(row[17]).strip()
           clim_precip_novdecjan = str(row[18]).strip()
           clim_precip_febmarapr = str(row[19]).strip()
           clim_precip_mayjunjul = str(row[20]).strip()
           clim_precip_augsepoct = str(row[21]).strip()
           topog_elevation = str(row[34]).strip()
           topog_geolage = str(row[36]).strip()
           topog_slope_global = str(row[39]).strip()
           topog_landform_global = str(row[40]).strip()
           topog_twi_global = str(row[41]).strip()
           topog_topi_global = str(row[42]).strip()
           topog_israd_global = str(row[43]).strip()
           landcover_modis_2012 = str(row[44]).strip()
           vegind_modis_evi_m = str(row[45]).strip()
           vegind_modis_evi_sd = str(row[46]).strip()
           fao_74 = str(row[47]).strip()
           if (latitude_decimal != '-999' and longitude_decimal != '-999' ):
               out.writerow([WISE3_ID,str(latitude_decimal),str(longitude_decimal),
                             str(clim_precipitation_date),str(clim_gdd),str(clim_aridity_index),str(clim_kopgeiger),str(clim_fao_lgp),str(clim_modis_evapotrans),
                             str(clim_precip_novdecjan),str(clim_precip_febmarapr),str(clim_precip_mayjunjul),str(clim_precip_augsepoct),str(topog_elevation),
                             str(topog_geolage),str(topog_slope_global),str(topog_landform_global),str(topog_twi_global),
                             str(topog_topi_global),str(topog_israd_global),str(landcover_modis_2012),str(vegind_modis_evi_m),str(vegind_modis_evi_sd),str(fao_74)
                            ])
       return 1    
    except Exception, err:
       print err
       return -1
def main():
    #Remove MIssing Value by -999 Latitude and -999 Longitude#
    if (not os.path.exists(WISE3_LANDPKS_INPUT_CSV_FILE)):
        sys.exit("===Error 405 : File is Not existed===")
        
    rebuildFile_Remove_All_Records_LatandLong_minus999(WISE3_LANDPKS_INPUT_CSV_FILE,WISE3_LANDPKS_OUTPUT_CSV_FILE)
    print "Step-2 is Sucessful"
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
