__version__ = "1"

import struct, os, csv, codecs, cStringIO, sys
from __builtin__ import str, len
import math
from support import support_SIMILARITY

WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL_STANDALIZATION.csv"
WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_GDAL_SIMILARITY_INDEX.csv"
SIMILARITY_METHOD = "cosine_vector_space_model"
DATA_TYPE = "1"
mess = "Usage : Step_3_Run_Stage_1_Similarity_Model_All_At_One_Calculation.py -input_wise_landpks_standalization_csv <Full Path to Input> -output_wise_landpks_similarity_csv <Full Path to Output> -method <cosine_vector_space_model ; > -record_id <ID>"
if (len(sys.argv) < 8):
    print("\n Using default value \nWISE_LANDPKS_STANDALIZATION = %s" %(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE))
    print("\n Using Similarity method = " + SIMILARITY_METHOD)
    if (sys.argv[1] == '-record_id'):
        if (sys.argv[2] is not None):
            RECORD_ID = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[3] == '-method'):
        if (sys.argv[4] is not None):
            SIMILARITY_METHOD = sys.argv[4].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
    
    if (sys.argv[5] == '-data_type'):
        if (sys.argv[6] is not None):
            DATA_TYPE = sys.argv[6].strip()
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
        
    if (sys.argv[9] == '-data_type'):
        if (sys.argv[10] is not None):
            DATA_TYPE = sys.argv[6].strip()
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
def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
def length(v):
  return math.sqrt(dotproduct(v, v))
def angle(v1, v2):
  return (dotproduct(v1, v2) / (length(v1) * length(v2)))
def calculate_Normalization(BIG_LIST,entry_plot_data_numberous):
    print "=== Normalization Calculation====="
    datasets = []
    for i in range(0,len(BIG_LIST)):
        datasets.append(BIG_LIST[i][3])
    #print "Before : "
    #print datasets[0]
    max_list_value = []
    min_list_value = []
    for i in range(0,len(datasets[0])):
         max_list_value.append(-9999999999999999999999999999)
         min_list_value.append(9999999999999999999999999999)
    for record in datasets:
        for i in range(0,len(record)): 
            if (float(record[i]) > max_list_value[i]):
                max_list_value[i] = float(record[i])
            if (float(record[i]) < min_list_value[i]):
                min_list_value[i] = float(record[i])
    
    for i in range(0,len(entry_plot_data_numberous)):
        if (float(entry_plot_data_numberous[i]) > max_list_value[i]):
                max_list_value[i] = float(entry_plot_data_numberous[i])
        if (float(entry_plot_data_numberous[i]) < min_list_value[i]):
                min_list_value[i] = float(entry_plot_data_numberous[i])
        entry_plot_data_numberous[i] = (float(entry_plot_data_numberous[i]) - float(min_list_value[i])) / (float(max_list_value[i]) - float(min_list_value[i]))
                
    print "Max List : " 
    print max_list_value
    print "Min List : " 
    print min_list_value
    for record in datasets:
        for i in range(0,len(record)):
            new_record_value = (float(record[i]) - float(min_list_value[i])) / (float(max_list_value[i]) - float(min_list_value[i]))
            record[i] = new_record_value

def calculator_similarity_cosin_vector_space_model_ALL_AT_ONCE(in_csv, out_csv,entry_plot_identify,entry_plot_data,data_type):
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
                     'CLIM_KOPGEIGER','CKIM_FAO_LGP',
                     #'CLIM_MODIS_evapotrans',
                     #'clim_precip_novdecjan',
                     #'clim_precip_febmarapr',
                     #'clim_precip_mayjunjul',
                     #'clim_precip_augsepoct',
                     'topog_elevation','topog_geolage',
                     'topog_slope_global','topog_landform_global','topog_twi_global','topog_topi_global','topog_israd_global'
                     #'landcover_modis_2012','vegind_modis_evi_m','vegind_modis_evi_sd'
                     ])
       out.writerow([str(entry_plot_identify[1]),str(entry_plot_data[0]),str(entry_plot_data[1]),str(entry_plot_data[2]),str(entry_plot_data[3]),str(entry_plot_data[4]),
                     str(entry_plot_data[5]),str(entry_plot_data[6]),
                     #str(entry_plot_data[7]),
                     #str(entry_plot_data[8]),
                     #str(entry_plot_data[9]),
                     #str(entry_plot_data[10]),
                     #str(entry_plot_data[11]),
                     str(entry_plot_data[12]),str(entry_plot_data[13]),str(entry_plot_data[14]),str(entry_plot_data[15]),str(entry_plot_data[16]),str(entry_plot_data[17]),
                     str(entry_plot_data[18])
                     #str(entry_plot_data[19]),str(entry_plot_data[20]),str(entry_plot_data[21])
                     ])
       out.writerow("\n")
       out.writerow(['PLOT_ID','WISE3_ID_2','SIMILARITY_INDEX','',''])
       
       
       
       WISE_3_SIMILARITY_RESULT_LIST = []
       WISE_3_SIMILARITY_RESULT_LIST_SORTED = []
       
       # Separate Category data out of Numberous data 
       entry_plot_data_numberous = [entry_plot_data[0],entry_plot_data[1],entry_plot_data[2],entry_plot_data[3],entry_plot_data[4],
                                    #entry_plot_data[7],
                                    #entry_plot_data[8],
                                    #entry_plot_data[9],
                                    #entry_plot_data[10],
                                    #entry_plot_data[11],
                                    entry_plot_data[12],entry_plot_data[14],entry_plot_data[16],entry_plot_data[17],
                                    entry_plot_data[18]]
       
       
       # User Category data out 
       entry_plot_kop_geiger_value = entry_plot_data[5]
       entry_plot_fao_lgp_value = entry_plot_data[6]
       entry_plot_geolage_value = entry_plot_data[13]
       entry_plot_landform_value = entry_plot_data[15]
       
       #Filtering by SURFACE CRACKING field
       SURFACE_CRAKING = support_SIMILARITY.get_surface_craking_from_record_id(entry_plot_identify[1])
       bSurface_craking = 0
       if (SURFACE_CRAKING is None):
           bSurface_craking = 0
       elif (str(SURFACE_CRAKING).strip().upper() == 'TRUE'):
           bSurface_craking = 1
       else:
           bSurface_craking = 0
           
           
       if (data_type == "1" or data_type == 1):
           print "\n====Run Calculation based on only NUMEROUS Data Fields ============="
           for row in l:
               WISE_3_ID = str(row[0]).strip()
               WISE_3_DATA = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),
                          float(row[7]),
                          float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),float(row[13]),
                          float(row[14]),
                          float(row[15]),
                          float(row[16]),
                          float(row[17]),float(row[18]),float(row[19]),row[23]
                          #float(row[20]),float(row[21]),float(row[22])
                          ]
               WISE_3_DATA_NUMBEROUS = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                          #float(row[6]), ==> Bo Kopgeiger
                          #float(row[7]), ==> Bo FAO_LGP
                          #float(row[8]), ==> Bo MODIS Evapotrans
                          #float(row[9]), ==> Bo precip novdecjan
                          #float(row[10]),==> BO precip febmarap
                          #float(row[11]), ==> BO mayjunjul
                          #float(row[12]), ==> Bo Augsepoct
                          float(row[13]),
                          #float(row[14]), ==> Bo GEOLAGE
                          float(row[15]),
                          #float(row[16]), ==>Bo LandForm_Global
                          float(row[17]),float(row[18]),float(row[19])
                          #float(row[20]),float(row[21]),float(row[22])
                          ]
               WISE_3_DATA_NUMBEROUS_NEW = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                          #float(row[6]), ==> Bo Kopgeiger
                          #float(row[7]), ==> Bo FAO_LGP
                          #float(row[8]), ==> Bo MODIS Evapotrans
                          #float(row[9]), ==> Bo precip novdecjan
                          #float(row[10]), ==> BO precip febmarapr
                          #float(row[11]), ==> BO mayjunjul
                          #float(row[12]), ==> Bo Augsepoct
                          float(row[13]),
                          #float(row[14]), ==> Bo GEOLAGE
                          float(row[15]),
                          #float(row[16]), ==>Bo LandForm_Global
                          float(row[17]),float(row[18]),float(row[19])
                          #float(row[20]),float(row[21]),float(row[22])
                          ]
               WISE_3_RECORD = [WISE_3_ID,WISE_3_DATA,WISE_3_DATA_NUMBEROUS,WISE_3_DATA_NUMBEROUS_NEW]
               WISE_3_LIST.append(WISE_3_RECORD)
       elif(data_type == "2" or data_type == 2):
           print "\n====Run Calculation based on NUMEROUS + CATEGORICAL Data Fields ============="
           print "\n====DECISION TREE Filtering : 1) Selected Tranning Set RECOREDS same KOP-GEIGER Category with User Input==========="
           if (bSurface_craking == 1):
               print "\n                              2.1) IFFFF SURFACE_CRAKING in User Input === TRUE ==> Selected Tranning Set RECOREDS FAO_74 is Vc or Vp  ==========="
               print "\n                              2.2) IFFFF SURFACE_CRAKING in User Input === FALSE ==> Do not do anything  ==========="
               for row in l:
                   fl_kop_geiger_value = float(row[6])
                   str_fao_74 = str(row[23]).strip()
                   if (fl_kop_geiger_value == entry_plot_kop_geiger_value and (str_fao_74 == 'Vc' or str_fao_74 == 'Vp')):
                       WISE_3_ID = str(row[0]).strip()
                       WISE_3_DATA = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),
                                  float(row[7]),
                                  float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),
                                  float(row[13]),
                                  float(row[14]),
                                  float(row[15]),
                                  float(row[16]),
                                  float(row[17]),float(row[18]),float(row[19]),row[23]
                                  #float(row[20]),float(row[21]),float(row[22])
                                  ]
                       WISE_3_DATA_NUMBEROUS = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                             #float(row[6]), ==> Bo Kopgeiger
                             #float(row[7]), ==> Bo FAO_LGP
                             #float(row[8]), ==> Bo MODIS Evapotrans
                             #float(row[9]), ==> Bo precip novdecjan
                             #float(row[10]),==> BO precip febmarap
                             #float(row[11]), ==> BO mayjunjul
                             #float(row[12]), ==> Bo Augsepoct
                             float(row[13]),
                             #float(row[14]), ==> Bo GEOLAGE
                             float(row[15]),
                             #float(row[16]), ==>Bo LandForm_Global
                             float(row[17]),float(row[18]),float(row[19])
                             #float(row[20]),float(row[21]),float(row[22])
                             ]
                       WISE_3_DATA_NUMBEROUS_NEW = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                              #float(row[6]), ==> Bo Kopgeiger
                              #float(row[7]), ==> Bo FAO_LGP
                              #float(row[8]), ==> Bo MODIS Evapotrans
                              #float(row[9]), ==> Bo precip novdecjan
                              #float(row[10]), ==> BO precip febmarap
                              #float(row[11]), ==> BO mayjunjul
                              #float(row[12]), ==> Bo Augsepoct
                              float(row[13]),
                              #float(row[14]), ==> Bo GEOLAGE
                              float(row[15]),
                              #float(row[16]), ==>Bo LandForm_Global
                              float(row[17]),float(row[18]),float(row[19])
                              #float(row[20]),float(row[21]),float(row[22])
                              ]
                       WISE_3_RECORD = [WISE_3_ID,WISE_3_DATA,WISE_3_DATA_NUMBEROUS,WISE_3_DATA_NUMBEROUS_NEW]
                       WISE_3_LIST.append(WISE_3_RECORD)
           else:
               for row in l:
                   fl_kop_geiger_value = float(row[6])
                   if (fl_kop_geiger_value == entry_plot_kop_geiger_value):
                       WISE_3_ID = str(row[0]).strip()
                       WISE_3_DATA = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),
                                  float(row[7]),
                                  float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),
                                  float(row[13]),
                                  float(row[14]),
                                  float(row[15]),
                                  float(row[16]),
                                  float(row[17]),float(row[18]),float(row[19]),row[23]
                                  #float(row[20]),float(row[21]),float(row[22])
                                  ]
                       WISE_3_DATA_NUMBEROUS = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                             #float(row[6]), ==> Bo Kopgeiger
                             #float(row[7]), ==> Bo FAO_LGP
                             #float(row[8]), ==> Bo MODIS Evapotrans
                             #float(row[9]), ==> Bo precip novdecjan
                             #float(row[10]),==> BO precip febmarap
                             #float(row[11]), ==> BO mayjunjul
                             #float(row[12]), ==> Bo Augsepoct
                             float(row[13]),
                             #float(row[14]), ==> Bo GEOLAGE
                             float(row[15]),
                             #float(row[16]), ==>Bo LandForm_Global
                             float(row[17]),float(row[18]),float(row[19])
                             #float(row[20]),float(row[21]),float(row[22])
                             ]
                       WISE_3_DATA_NUMBEROUS_NEW = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                              #float(row[6]), ==> Bo Kopgeiger
                              #float(row[7]), ==> Bo FAO_LGP
                              #float(row[8]), ==> Bo MODIS Evapotrans
                              #float(row[9]), ==> Bo precip novdecjan
                              #float(row[10]), ==> BO precip febmarap
                              #float(row[11]), ==> BO mayjunjul
                              #float(row[12]), ==> Bo Augsepoct
                              float(row[13]),
                              #float(row[14]), ==> Bo GEOLAGE
                              float(row[15]),
                              #float(row[16]), ==>Bo LandForm_Global
                              float(row[17]),float(row[18]),float(row[19])
                              #float(row[20]),float(row[21]),float(row[22])
                              ]
                       WISE_3_RECORD = [WISE_3_ID,WISE_3_DATA,WISE_3_DATA_NUMBEROUS,WISE_3_DATA_NUMBEROUS_NEW]
                       WISE_3_LIST.append(WISE_3_RECORD)
       else:
           print "\n====Run Calculation based on only NUMEROUS Data Fields ============="
           for row in l:
              WISE_3_ID = str(row[0]).strip()
              WISE_3_DATA = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),float(row[6]),
                          float(row[7]),
                          float(row[8]),float(row[9]),float(row[10]),float(row[11]),float(row[12]),
                          float(row[13]),
                          float(row[14]),
                          float(row[15]),
                          float(row[16]),
                          float(row[17]),float(row[18]),float(row[19]),row[23]
                          #float(row[20]),float(row[21]),float(row[22])
                          ]
              WISE_3_DATA_NUMBEROUS = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                             #float(row[6]), ==> Bo Kopgeiger
                             #float(row[7]), ==> Bo FAO_LGP
                             #float(row[8]), ==> Bo MODIS Evapotrans
                             #float(row[9]), ==> Bo precip novdecjan
                             #float(row[10]),==> BO precip febmarap
                             #float(row[11]), ==> BO mayjunjul
                             #float(row[12]), ==> Bo Augsepoct
                             float(row[13]),
                             #float(row[14]), ==> Bo GEOLAGE
                             float(row[15]),
                             #float(row[16]), ==>Bo LandForm_Global
                             float(row[17]),float(row[18]),float(row[19])
                             #float(row[20]),float(row[21]),float(row[22])
                             ]
              WISE_3_DATA_NUMBEROUS_NEW = [float(row[1]),float(row[2]),float(row[3]),float(row[4]),float(row[5]),
                              #float(row[6]), ==> Bo Kopgeiger
                              #float(row[7]), ==> Bo FAO_LGP
                              #float(row[8]), ==> Bo MODIS Evapotrans
                              #float(row[9]), ==> Bo precip novdecjan
                              #float(row[10]), ==> BO precip febmarap
                              #float(row[11]), ==> BO mayjunjul
                              #float(row[12]), ==> Bo Augsepoct
                              float(row[13]),
                              #float(row[14]), ==> Bo GEOLAGE
                              float(row[15]),
                              #float(row[16]), ==>Bo LandForm_Global
                              float(row[17]),float(row[18]),float(row[19])
                              #float(row[20]),float(row[21]),float(row[22])
                              ]
              WISE_3_RECORD = [WISE_3_ID,WISE_3_DATA,WISE_3_DATA_NUMBEROUS,WISE_3_DATA_NUMBEROUS_NEW]
              WISE_3_LIST.append(WISE_3_RECORD)    
           
       print "Calculating....................."    
       # Tinh toan Normalization first #
       calculate_Normalization(WISE_3_LIST,entry_plot_data_numberous)
       print "Normalization USer input : "
       print entry_plot_data_numberous
       # End Normalization #
       print WISE_3_LIST[0]
       for i in range(0,len(WISE_3_LIST)):
           try:
               WISE_3_ID = WISE_3_LIST[i][0]
               WISE_3_DATA = WISE_3_LIST[i][1]
               WISE_3_DATA_NUMBEROUS = WISE_3_LIST[i][2]
               WISE_3_DATA_NUMBEROUS_NORMALIZATION = WISE_3_LIST[i][3]
               
               cosin_angle = angle(entry_plot_data_numberous, WISE_3_DATA_NUMBEROUS_NORMALIZATION) 
               #out.writerow([str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle)])
               WISE_3_SIMILARITY_OBJECT = [str(entry_plot_identify[0])+"-"+ str(entry_plot_identify[1]),str(WISE_3_ID),str(cosin_angle),
                                           WISE_3_DATA[0],WISE_3_DATA[1],WISE_3_DATA[2],WISE_3_DATA[3],WISE_3_DATA[4],WISE_3_DATA[5],WISE_3_DATA[6],
                                           WISE_3_DATA[7],
                                           WISE_3_DATA[8],
                                           WISE_3_DATA[9],
                                           WISE_3_DATA[10],
                                           WISE_3_DATA[11],
                                           WISE_3_DATA[12],WISE_3_DATA[13],
                                           WISE_3_DATA[14],WISE_3_DATA[15],WISE_3_DATA[16],WISE_3_DATA[17],WISE_3_DATA[18],WISE_3_DATA[19]
                                           #WISE_3_DATA[19],WISE_3_DATA[20],WISE_3_DATA[21] 
                                          ]
               WISE_3_SIMILARITY_RESULT_LIST.append(WISE_3_SIMILARITY_OBJECT)
           except Exception,err:
               print err
               pass
       print "Sorting.............."
       
       WISE_3_SIMILARITY_RESULT_LIST_SORTED = sorted(WISE_3_SIMILARITY_RESULT_LIST, key=lambda similarity_object: similarity_object[2], reverse=True)
       print "==+++++++ : Number Records Computing : " + str(len(WISE_3_SIMILARITY_RESULT_LIST_SORTED))
       i = 0
       for similarity_object in WISE_3_SIMILARITY_RESULT_LIST_SORTED:
           i = i + 1
           if (i <= 50):
               out.writerow([similarity_object[0],similarity_object[1],str(similarity_object[2]),str(similarity_object[3]),str(similarity_object[4]),str(similarity_object[5]),
                             str(similarity_object[6]),str(similarity_object[7]),str(similarity_object[8]),str(similarity_object[9]),
                             #str(similarity_object[10]),
                             #str(similarity_object[11]),
                             #str(similarity_object[12]),
                             #str(similarity_object[13]),
                             #str(similarity_object[14]),
                             str(similarity_object[15]),str(similarity_object[16]),str(similarity_object[17]),
                             str(similarity_object[18]),str(similarity_object[19]),str(similarity_object[20]),
                             str(similarity_object[21]),str(similarity_object[22])])
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
                       float(entry_plot_data[10]),float(entry_plot_data[11]),float(entry_plot_data[12]),
                       float(entry_plot_data[13]),float(entry_plot_data[14]),float(entry_plot_data[15]),float(entry_plot_data[16]),float(entry_plot_data[17]),
                       float(entry_plot_data[18]),float(entry_plot_data[19]),float(entry_plot_data[20])
                       #float(entry_plot_data[21]),float(entry_plot_data[22]),float(entry_plot_data[23])
                       ]
    
    print "\n Identify = "
    print ENTRY_PLOT_IDENTIFY
    print "\n Data = "
    print ENTRY_PLOT_DATA
    if (SIMILARITY_METHOD == 'cosine_vector_space_model'):
        print "\nStep 3 : Run Similarity based on Cosin Smilimarity for vector space models"
        print "\n===Run Similarity All At Once===="
        WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = createPrivateFolder_All_At_Once() +"\\Wise_3_LandPKS_GDAL_Highest_Similarity_Index.csv"
        result_all_at_once = calculator_similarity_cosin_vector_space_model_ALL_AT_ONCE(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE,WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE,ENTRY_PLOT_IDENTIFY,ENTRY_PLOT_DATA,DATA_TYPE)
        #print "\n===Run Similarity Multiple-Step=="
        #WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE = createPrivateFolder_Multi_Step() +"\\Wise_3_LandPKS_GDAL_Highest_Similarity_Index.csv"
        #result_multiple_step = calculator_similarity_cosin_vector_space_model_MULTI_STEP(WISE3_LANDPKS_INTPUT_CSV_STANDALIZATION_FILE,WISE3_LANDPKS_OUTPUT_CSV_SIMILARITY_INDEX_FILE,ENTRY_PLOT_IDENTIFY,ENTRY_PLOT_DATA)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
