# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"

import struct, os, csv, codecs, cStringIO, sys
from support import support_SIMILARITY
RECORD_ID = ""
APPROACH = ""
WISE_SITE_FILE_CSV = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\ISRIC_WISE_DATABASE\\WISE3_SITE.csv"
WISE_HORIZON_FILE_CSV = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\ISRIC_WISE_DATABASE\\WISE3_HORIZON.csv"
WISE_FILE_DETAIL_RESULT_CSV = ""
print "Run"
if (len(sys.argv) != 9):
    sys.exit("====[Error] : NOT ENOUGH ARGUMENT")
else:
  if (sys.argv[1] == '-ID'):
      if (sys.argv[2] is not None):
          RECORD_ID = str(sys.argv[2]).strip()
      else:
          sys.exit("====[Error] : Error ID")
  else:
      sys.exit("====[Error] : Error ID")

  if (sys.argv[3] == '-approach'):
      if (sys.argv[4] is not None):
          APPROACH = str(sys.argv[4]).strip().upper()
      else:
          sys.exit("====[Error] : Error Approach")
  else:
      sys.exit("====[Error] : Error Approach")
      
  if (sys.argv[5] == '-wise_site_file'):
      if (sys.argv[6] is not None and os.path.exists(sys.argv[6])):
          WISE_SITE_FILE_CSV = str(sys.argv[6]).strip()
  else:
      sys.exit("====[Error] : Error Method")
   
  if (sys.argv[7] == '-wise_horizon_file'):
      if (sys.argv[8] is not None and os.path.exists(sys.argv[8])):
          WISE_HORIZON_FILE_CSV = str(sys.argv[8]).strip()
  else:
      sys.exit("====[Error] : Error Wise Horizon File")
APPROACH_FOLDER = ""
if (APPROACH == "ALL_AT_ONCE" or APPROACH == "all_at_once"):
    APPROACH_FOLDER = "All_At_Once"
else:
    APPROACH_FOLDER = "Multi_Step"

WISE_FILE_DETAIL_RESULT_CSV = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\Private\\%s\\%s\\Wise_3_LandPKS_Final_Detail_Result.csv" %(RECORD_ID,APPROACH_FOLDER)
WISE_FILE_FINAL_RESULT_SIMILARITY = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\Private\\%s\\%s\\Wise_3_LandPKS_Highest_Similarity_Stage_2_Site_Awc_Soil.csv" %(RECORD_ID,APPROACH_FOLDER)
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
def read_Data_From_Wise_Site_File(in_csv):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       WISE_SITE_RECORD = []
       WISE_SITE_LIST = []
       for row in l:
           WISE3_ID = str(row[0]).upper()
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
           WISE3_Country = str(row[35])
           WISE3_Soldep = str(row[5])
           WISE3_fao74 = str(row[9])
           WISE3_uscl = str(row[12])
           WISE3_slope = str(row[28])
           WISE_SITE_RECORD =[WISE3_ID,latitude_decimal,longitude_decimal,WISE3_Country,WISE3_Soldep,WISE3_fao74,WISE3_uscl,WISE3_slope]
           WISE_SITE_LIST.append(WISE_SITE_RECORD)
       return WISE_SITE_LIST    
    except Exception, err:
       print err
       return -1
def read_Data_From_Final_Result_Similarity(in_csv):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       WISE_FINAL_RECORD = []
       WISE_FINAL_LIST = []
       for row in l:
           WISE3_ID = str(row[0]).upper()
           similarity_stage_1 = float(row[1])
           similarity_stage_2 = float(row[15])
           soil_profile_awc = float(row[12])
           WISE_FINAL_RECORD =[WISE3_ID,similarity_stage_1,similarity_stage_2,soil_profile_awc]
           WISE_FINAL_LIST.append(WISE_FINAL_RECORD)
       return WISE_FINAL_LIST    
    except Exception, err:
       print err
       return -1
def read_Data_From_Wise_Horizon_File(in_csv):
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       WISE_HORIZON_RECORD = []
       WISE_HORIZON_LIST = []
       for row in l:
           WISE3_ID = str(row[0]).upper()
           horizon_number = row[1]
           horizon_topdep = row[3]
           horizon_botdep = row[4]
           horizon_orgc = row[7]
           horizon_totn = row[8]
           horizon_caco3 = row[9]
           horizon_gypsum = row[10]
           horizon_phh2o = row[11]
           horizon_phkcl = row[12]
           horizon_phcacl2 = row[13]
           horizon_ece = row[14]
           horizon_exca = row[15]
           horizon_exmg = row[16]
           horizon_exna = row[17]
           horizon_exk = row[18]
           horizon_exalum = row[19]
           horizon_exacid = row[20]
           horizon_cecsoil = row[21]
           horizon_bsat = row[22]
           horizon_sand = row[23]
           horizon_silt = row[24]
           horizon_clay = row[25]
           horizon_gravel = row[26]
           horizon_bulkdens = row[27]
           horizon_vmc1 = row[28]
           horizon_vmc2 = row[29]
           horizon_vmc3 = row[30]
           
           WISE_HORIZON_RECORD =[WISE3_ID,horizon_number,horizon_topdep,horizon_botdep,horizon_orgc,horizon_totn,horizon_caco3,horizon_gypsum,horizon_phh2o,horizon_phkcl,horizon_phcacl2,horizon_ece,
                                 horizon_exca,horizon_exmg,horizon_exna,horizon_exk,horizon_exalum,horizon_exacid,horizon_cecsoil,horizon_bsat,horizon_sand,horizon_silt,horizon_clay,
                                 horizon_gravel,horizon_bulkdens,horizon_vmc1,horizon_vmc2,horizon_vmc3]
           WISE_HORIZON_LIST.append(WISE_HORIZON_RECORD)
       return WISE_HORIZON_LIST    
    except Exception, err:
       print err
       return -1
def export_to_file(WISE_FINAL_RESULT_LIST,WISE_SITE_DATA_LIST,WISE_HORIZON_DATA_LIST,WISE_FILE_DETAIL_RESULT_CSV,USER_DATA_INPUT):
    try:
        out_csvfile = open(WISE_FILE_DETAIL_RESULT_CSV, 'wb')
        out = UnicodeWriter(out_csvfile)
        # Print User Input data from Mobile
        out.writerow(['USER_ID','NAME','LATITUDE','LONGITUDE','SLOPE','SLOPE_SHAPE','texture_for_soil_horizon_1','texture_for_soil_horizon_2','texture_for_soil_horizon_3','texture_for_soil_horizon_4','texture_for_soil_horizon_5','texture_for_soil_horizon_6','texture_for_soil_horizon_7','SOIL_PROFILE_AWC'])
        out.writerow([str(USER_DATA_INPUT[0]),str(USER_DATA_INPUT[1]),str(USER_DATA_INPUT[2]),str(USER_DATA_INPUT[3]),str(USER_DATA_INPUT[4]),str(USER_DATA_INPUT[5]),str(USER_DATA_INPUT[6]),str(USER_DATA_INPUT[7]),str(USER_DATA_INPUT[8]),str(USER_DATA_INPUT[9]),str(USER_DATA_INPUT[10]),str(USER_DATA_INPUT[11]),str(USER_DATA_INPUT[12]),str(USER_DATA_INPUT[14])])
        out.writerow(['','','','','','','SAND   :  ' + str(USER_DATA_INPUT[13][0]),'','','','','',''])
        out.writerow(['','','','','','','SILT   :  ' + str(USER_DATA_INPUT[13][1]),'','','','','',''])
        out.writerow(['','','','','','','CLAY   :  ' + str(USER_DATA_INPUT[13][2]),'','','','','',''])
        out.writerow(['','','','','','','BULK   :  ' + str(USER_DATA_INPUT[13][3]),'','','','','',''])
        out.writerow([''])
        out.writerow([''])
        # WISE_SITE_Data and WISE_HORIZON_DATA
        out.writerow(['WISE3_ID','LATITUDE','LONGITUDE','COUNTRY','SOLDEP','FAO_74','USCL','SLOPE','SIM_STAGE_1','SIM_STAGE_2','HONU','TOPDEP','BOTDEP','ORGC','TOTN','CACO3','GYPSUM','PHH2O','PHKCL','PHCACL2','ECE','EXCA','EXMG','EXNA','EXK','EXALUM','EXACID','CECSOIL','BSAT','SAND','SILT','CLAY','GRAVEL','BULKDENS','VMC1','VMC2','VMC3','PROFILE_AWC'])
        for final_result_record in WISE_FINAL_RESULT_LIST:
            
            for site_record in WISE_SITE_DATA_LIST:
                if (final_result_record[0] == site_record[0]):
                    out.writerow([str(final_result_record[0]),str(site_record[1]),str(site_record[2]),str(site_record[3]),str(site_record[4]),str(site_record[5]),str(site_record[6]),str(site_record[7]),str(final_result_record[1]),str(final_result_record[2])])
            for horizon_record in WISE_HORIZON_DATA_LIST:
                if (final_result_record[0] == horizon_record[0]):
                        out.writerow(['','','','','','','','','','',str(horizon_record[1]),str(horizon_record[2]),str(horizon_record[3]),str(horizon_record[4]),str(horizon_record[5]),str(horizon_record[6]),str(horizon_record[7]),
                                      str(horizon_record[8]),str(horizon_record[9]),str(horizon_record[10]),str(horizon_record[11]),str(horizon_record[12]),str(horizon_record[13]),
                                      str(horizon_record[14]),str(horizon_record[15]),str(horizon_record[16]),str(horizon_record[17]),str(horizon_record[18]),str(horizon_record[19]),str(horizon_record[20]),str(horizon_record[21]),
                                      str(horizon_record[22]),str(horizon_record[23]),str(horizon_record[24]),str(horizon_record[25]),str(horizon_record[26]),str(horizon_record[27]),str(final_result_record[3])])
        return 1
    except Exception, err:
        print err
        return -1
def main():
    print "==Reading Site Data ===" 
    WISE_SITE_DATA_LIST = read_Data_From_Wise_Site_File(WISE_SITE_FILE_CSV)
    WISE_FINAL_RESULT_LIST = read_Data_From_Final_Result_Similarity(WISE_FILE_FINAL_RESULT_SIMILARITY)
    print "==Reading Horizon Data ==="
    WISE_HORIZON_DATA_LIST = read_Data_From_Wise_Horizon_File(WISE_HORIZON_FILE_CSV)
    print "==Reading User Input Data from Database ==="
    USER_DATA_INPUT = support_SIMILARITY.get_record_user_data_by_record_id(RECORD_ID)
    print "==Final : Extract Data to : %s " %(WISE_FILE_DETAIL_RESULT_CSV)
    export_to_file(WISE_FINAL_RESULT_LIST,WISE_SITE_DATA_LIST,WISE_HORIZON_DATA_LIST,WISE_FILE_DETAIL_RESULT_CSV,USER_DATA_INPUT)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()  