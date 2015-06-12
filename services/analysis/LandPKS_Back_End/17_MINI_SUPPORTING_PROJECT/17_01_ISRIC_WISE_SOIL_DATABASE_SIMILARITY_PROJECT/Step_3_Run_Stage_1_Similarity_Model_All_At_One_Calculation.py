
__version__ = "1"

import struct, os, csv, codecs, cStringIO, sys
from __builtin__ import str, len
import math
from support import support_SIMILARITY

WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL_STANDALIZATION.csv"
WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL_SIMILARITY_INDEX.csv"
SIMILARITY_METHOD = "cosine_vector_space_model"
mess = "Usage : Step_3_Run_Stage_1_Similarity_Model_All_At_One_Calculation.py -input_wise_landpks_standalization_csv <Full Path to Input> -output_wise_landpks_similarity_csv <Full Path to Output> -method <cosine_vector_space_model ; > -record_id <ID>"
if (len(sys.argv) < 8):
    print("\n Using default value \nWISE_LANDPKS_STANDALIZATION = %s" %(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE))
    print("\n Using Similarity method = %s" + SIMILARITY_METHOD)
    if (sys.argv[1] == '-record_id'):
        if (sys.argv[2] is not None):
            RECORD_ID = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
    
else:

    if (sys.argv[1] == '-input_wise_landpks_standalization_csv'):
        if (sys.argv[2] is not None):
            WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[3] == '-output_wise_landpks_similarity_csv'):
        if (sys.argv[4] is not None):
            WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = sys.argv[4].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[5] == '-method'):
        if (sys.argv[6] is not None):
            SIMILARITY_METHOD = sys.argv[6].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[7] == '-record_id'):
        if (sys.argv[8] is not None):
            RECORD_ID = sys.argv[8].strip()
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
class SimilarityObject(object):
    def __init__(self, ID_1, ID_2, similarity_index):
        self.ID_1 = ID_1
        self.ID_2 = ID_2
        self.similarity_index = similarity_index
 
    def __repr__(self):
        return '{}: {} {} {}'.format(self.__class__.__name__,
                                  self.ID_1,
                                  self.ID_2,
                                  self.similarity_index)
 
    def __cmp__(self, other):
        if hasattr(other, 'similarity_index'):
            return self.similarity_index.__cmp__(other.similarity_index)
def createPrivateFolder_All_At_Once():
   PRIVATE_FOLDER_ACCESS_DAT = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\Private\\%s\\All_At_Once" % (str(RECORD_ID)))
   if (not os.path.exists(PRIVATE_FOLDER_ACCESS_DAT)):
        os.makedirs(PRIVATE_FOLDER_ACCESS_DAT)
   return PRIVATE_FOLDER_ACCESS_DAT
def createPrivateFolder_Multi_Step():
   PRIVATE_FOLDER_ACCESS_DAT = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\Private\\%s\\Multi_Step" % (str(RECORD_ID)))
   if (not os.path.exists(PRIVATE_FOLDER_ACCESS_DAT)):
        os.makedirs(PRIVATE_FOLDER_ACCESS_DAT)
   return PRIVATE_FOLDER_ACCESS_DAT
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
def length(v):
  return math.sqrt(dotproduct(v, v))
def angle(v1, v2):
  return (dotproduct(v1, v2) / (length(v1) * length(v2)))
def calculator_similarity_cosin_vector_space_model_MULTI_STEP(in_csv, out_csv,entry_plot_identify,entry_plot_data):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
      
       WISE_3_LIST = []
       
       out_csvfile = open(out_csv, 'wb')
       out = UnicodeWriter(out_csvfile)
       out.writerow(['Consider Plot'])
       out.writerow(['PLOT_ID','LATITUDE','LONGITUDE','CLIM_PRECIPITATION_DATA','CLIM_GDD','CLIM_ARIDITY_INDEX',
                     'CLIM_KOPGEIGER','CKIM_FAO_LGP','CLIM_MODIS_evapotrans','clim_precip_novdecjan','clim_precip_febmarapr',
                     'clim_precip_mayjunjul','clim_precip_augsepoct','topog_elevation','topog_geolage',
                     'topog_slope_global','topog_landform_global','topog_twi_global','topog_topi_global','topog_israd_global',
                     'landcover_modis_2012','vegind_modis_evi_m','vegind_modis_evi_sd'
                     ])
       out.writerow([str(entry_plot_identify[1]),str(entry_plot_data[0]),str(entry_plot_data[1]),str(entry_plot_data[2]),str(entry_plot_data[3]),str(entry_plot_data[4]),
                     str(entry_plot_data[5]),str(entry_plot_data[6]),str(entry_plot_data[7]),str(entry_plot_data[8]),str(entry_plot_data[9]),str(entry_plot_data[10]),str(entry_plot_data[11]),
                     str(entry_plot_data[12]),str(entry_plot_data[13]),str(entry_plot_data[14]),str(entry_plot_data[15]),str(entry_plot_data[16]),str(entry_plot_data[17]),
                     str(entry_plot_data[18]),str(entry_plot_data[19]),str(entry_plot_data[20]),str(entry_plot_data[21])])
       
       entry_plot_data_clim = [entry_plot_data[2],entry_plot_data[3],entry_plot_data[4],entry_plot_data[5],entry_plot_data[6],entry_plot_data[7],entry_plot_data[8],entry_plot_data[9],entry_plot_data[10],entry_plot_data[11]]
       entry_plot_data_togo_landcover_vegind = [entry_plot_data[12],entry_plot_data[13],entry_plot_data[14],entry_plot_data[15],entry_plot_data[16],entry_plot_data[17],entry_plot_data[18],entry_plot_data[19],entry_plot_data[20],entry_plot_data[21]]
       
       out.writerow("\n")
       out.writerow(['PLOT_ID','WISE3_ID_2','SIMILARITY_INDEX_CLIM','SIMILARITY_INDEX_TOGO_VEGIND_LANDCOVER',''])
       
       WISE_3_SIMILARITY_RESULT_CLIM_LIST = []
       WISE_3_SIMILARITY_RESULT_CLIM_LIST_SORTED = []
       

       for row in l:
           WISE_3_ID = str(row[0]).strip()
           WISE_3_CLIM_DATA = [float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12])]
           WISE_3_TOGO_LANDCOVER_VEGIND_DATA = [float(row[13]),float(row[14]),float(row[15]),float(row[16]),float(row[17]),float(row[18]),float(row[19]),float(row[20]),float(row[21]),float(row[22])]
           WISE_3_RECORD = [WISE_3_ID,WISE_3_CLIM_DATA,WISE_3_TOGO_LANDCOVER_VEGIND_DATA]
           WISE_3_LIST.append(WISE_3_RECORD)
       print "Calculating CLIM data....................."    
       for i in range(0,len(WISE_3_LIST)):
           try:
               WISE_3_ID = WISE_3_LIST[i][0]
               WISE_3_CLIM_DATA = WISE_3_LIST[i][1]
               WISE_3_TOGO_LANDCOVER_VEGIND_DATA = WISE_3_LIST[i][2]
               cosin_angle_clim_data = angle(entry_plot_data_clim, WISE_3_CLIM_DATA) 
               #out.writerow([str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle)])
               WISE_3_SIMILARITY_OBJECT = [str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle_clim_data),WISE_3_CLIM_DATA,WISE_3_TOGO_LANDCOVER_VEGIND_DATA]
               WISE_3_SIMILARITY_RESULT_CLIM_LIST.append(WISE_3_SIMILARITY_OBJECT)
           except Exception,err:
               print err
               pass
       print "Sorting CLIM DATA.............."
       WISE_3_SIMILARITY_RESULT_CLIM_LIST_SORTED = sorted(WISE_3_SIMILARITY_RESULT_CLIM_LIST, key=lambda similarity_object: similarity_object[2], reverse=True)
       WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100 = []
       print len(WISE_3_SIMILARITY_RESULT_CLIM_LIST_SORTED)
       i = 0
       for similarity_object in WISE_3_SIMILARITY_RESULT_CLIM_LIST_SORTED:
           i = i + 1
           if (i <= 100):
               WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100.append(similarity_object)
           else:
               break
           
       print "Calculating TOGOG LANDCOVER VEGIND data....................."    
       WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST = []
       WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST_SORTED = []
       for i in range(0,len(WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100)):
           try:
               IDENTIFY = WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100[i][0]
               WISE_3_ID = WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100[i][1]
               WISE_3_CLIM_DATA = WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100[i][3]
               WISE_3_TOGO_LANDCOVER_VEGIND_DATA = WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100[i][4]
               cosin_angle_clim = WISE_3_SIMILARITY_RESULT_CLIM_SORTED_100[i][2]
               cosin_angle_togo_landcover_vegind_data = angle(entry_plot_data_togo_landcover_vegind, WISE_3_TOGO_LANDCOVER_VEGIND_DATA) 
               #out.writerow([str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle)])
               WISE_3_SIMILARITY_OBJECT = [IDENTIFY,str(WISE_3_ID),str(cosin_angle_clim),str(cosin_angle_togo_landcover_vegind_data),WISE_3_CLIM_DATA,WISE_3_TOGO_LANDCOVER_VEGIND_DATA]
               WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST.append(WISE_3_SIMILARITY_OBJECT)
           except Exception,err:
               print err
               pass
       print "Sorting CLIM DATA.............."
       WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST_SORTED = sorted(WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST, key=lambda similarity_object: similarity_object[3], reverse=True)
       WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST_SORTED_50 = []
       print len(WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST_SORTED)
       i = 0
       for similarity_object in WISE_3_SIMILARITY_RESULT_CLIM_TOGO_VEGIND_LANCOVER_LIST_SORTED:
           i = i + 1
           if (i <= 50):
               out.writerow([similarity_object[0],similarity_object[1],str(similarity_object[2]),str(similarity_object[3])])
           else:
               break
               
       return 1         
    except Exception, err:
       print err
       return -1
def calculator_similarity_cosin_vector_space_model_ALL_AT_ONCE(in_csv, out_csv,entry_plot_identify,entry_plot_data):
     try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       
       WISE_3_RECORD = ['',0,0]
       WISE_3_LIST = []
       
       out_csvfile = open(out_csv, 'wb')
       out = UnicodeWriter(out_csvfile)
       out.writerow(['Consider Plot'])
       out.writerow(['PLOT_ID','LATITUDE','LONGITUDE','CLIM_PRECIPITATION_DATA','CLIM_GDD','CLIM_ARIDITY_INDEX',
                     'CLIM_KOPGEIGER','CKIM_FAO_LGP','CLIM_MODIS_evapotrans','clim_precip_novdecjan','clim_precip_febmarapr',
                     'clim_precip_mayjunjul','clim_precip_augsepoct','topog_elevation','topog_geolage',
                     'topog_slope_global','topog_landform_global','topog_twi_global','topog_topi_global','topog_israd_global',
                     'landcover_modis_2012','vegind_modis_evi_m','vegind_modis_evi_sd'
                     ])
       out.writerow([str(entry_plot_identify[1]),str(entry_plot_data[0]),str(entry_plot_data[1]),str(entry_plot_data[2]),str(entry_plot_data[3]),str(entry_plot_data[4]),
                     str(entry_plot_data[5]),str(entry_plot_data[6]),str(entry_plot_data[7]),str(entry_plot_data[8]),str(entry_plot_data[9]),str(entry_plot_data[10]),str(entry_plot_data[11]),
                     str(entry_plot_data[12]),str(entry_plot_data[13]),str(entry_plot_data[14]),str(entry_plot_data[15]),str(entry_plot_data[16]),str(entry_plot_data[17]),
                     str(entry_plot_data[18]),str(entry_plot_data[19]),str(entry_plot_data[20]),str(entry_plot_data[21])])
       out.writerow("\n")
       out.writerow(['PLOT_ID','WISE3_ID_2','SIMILARITY_INDEX','',''])
       
       
       
       WISE_3_SIMILARITY_RESULT_LIST = []
       WISE_3_SIMILARITY_RESULT_LIST_SORTED = []
       
       
       for row in l:
           WISE_3_ID = str(row[0]).strip()
           WISE_3_DATA = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),float(row[7]),float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),float(row[13]),float(row[14]),float(row[15]),float(row[16]),float(row[17]),float(row[18]),float(row[19]),float(row[20]),float(row[21]),float(row[22])]
           WISE_3_RECORD = [WISE_3_ID,WISE_3_DATA]
           WISE_3_LIST.append(WISE_3_RECORD)
       print "Calculating....................."    
       for i in range(0,len(WISE_3_LIST)):
           try:
               WISE_3_ID = WISE_3_LIST[i][0]
               WISE_3_DATA = WISE_3_LIST[i][1]
               cosin_angle = angle(entry_plot_data, WISE_3_DATA) 
               #out.writerow([str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle)])
               WISE_3_SIMILARITY_OBJECT = [str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle),
                                           WISE_3_DATA[0],WISE_3_DATA[1],WISE_3_DATA[2],WISE_3_DATA[3],WISE_3_DATA[4],WISE_3_DATA[5],WISE_3_DATA[6],
                                           WISE_3_DATA[7],WISE_3_DATA[8],WISE_3_DATA[9],WISE_3_DATA[10],WISE_3_DATA[11],WISE_3_DATA[12],WISE_3_DATA[13],
                                           WISE_3_DATA[14],WISE_3_DATA[15],WISE_3_DATA[16],WISE_3_DATA[17],WISE_3_DATA[18],WISE_3_DATA[19],WISE_3_DATA[20],
                                           WISE_3_DATA[21] 
                                          ]
               WISE_3_SIMILARITY_RESULT_LIST.append(WISE_3_SIMILARITY_OBJECT)
           except Exception,err:
               print err
               pass
       print "Sorting.............."
       
       WISE_3_SIMILARITY_RESULT_LIST_SORTED = sorted(WISE_3_SIMILARITY_RESULT_LIST, key=lambda similarity_object: similarity_object[2], reverse=True)
       print len(WISE_3_SIMILARITY_RESULT_LIST_SORTED)
       i = 0
       for similarity_object in WISE_3_SIMILARITY_RESULT_LIST_SORTED:
           i = i + 1
           if (i <= 50):
               out.writerow([similarity_object[0],similarity_object[1],str(similarity_object[2])])
           else:
               break
       return 1           
     except Exception, err:
       print err
       return -1
def main():
    # Check source data
    if (not os.path.exists(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE)):
        print "==Error 405 : File WISE3_SITE.csv was not existed==="
        sys.exit()
    
    # Create record to matching from record_id
    entry_plot_data = support_SIMILARITY.get_record_gdal_data_by_record_id(RECORD_ID)
   
    ENTRY_PLOT_IDENTIFY = [entry_plot_data[0],entry_plot_data[1]]
    ENTRY_PLOT_DATA = [float(entry_plot_data[2]),float(entry_plot_data[3]),float(entry_plot_data[4]),float(entry_plot_data[5]),float(entry_plot_data[6]),float(entry_plot_data[7]),float(entry_plot_data[8]),float(entry_plot_data[9]),
                       float(entry_plot_data[10]),float(entry_plot_data[11]),float(entry_plot_data[12]),float(entry_plot_data[13]),float(entry_plot_data[14]),float(entry_plot_data[15]),float(entry_plot_data[16]),float(entry_plot_data[17]),
                       float(entry_plot_data[18]),float(entry_plot_data[19]),float(entry_plot_data[20]),float(entry_plot_data[21]),float(entry_plot_data[22]),float(entry_plot_data[23])]
    
    print "\n Identify = "
    print ENTRY_PLOT_IDENTIFY
    print "\n Data = "
    print ENTRY_PLOT_DATA
    
    if (SIMILARITY_METHOD == 'cosine_vector_space_model'):
        print "\nStep 3 : Run Similarity based on Cosin Smilimarity for vector space models"
        print "\n===Run Similarity All At Once===="
        WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = createPrivateFolder_All_At_Once() +"\\Wise_3_LandPKS_GDAL_Highest_Similarity_Index.csv"
        result_all_at_once = calculator_similarity_cosin_vector_space_model_ALL_AT_ONCE(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE,WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE,ENTRY_PLOT_IDENTIFY,ENTRY_PLOT_DATA)
        print "\n===Run Similarity Multiple-Step=="
        WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = createPrivateFolder_Multi_Step() +"\\Wise_3_LandPKS_GDAL_Highest_Similarity_Index.csv"
        result_multiple_step = calculator_similarity_cosin_vector_space_model_MULTI_STEP(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE,WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE,ENTRY_PLOT_IDENTIFY,ENTRY_PLOT_DATA)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
