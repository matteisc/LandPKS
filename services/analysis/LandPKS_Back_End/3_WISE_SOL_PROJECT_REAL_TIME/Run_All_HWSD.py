# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import pyodbc
import sys
import time
import shutil
import subprocess
import math
import struct, os, csv, codecs, cStringIO
from support import support_SOIL
# Check arguments

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


if (len(sys.argv) < 4):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python main_HWSD_ROSETTA.py -d <Database File Path> -m <MU_GLOBAL> -model <Rosetta Model Application Full Path> -ID <User Input Record ID>")
        
# Input requires
message = "Usage : python main_HWSD_ROSETTA.py -d <Database File Path> -m <MU_GLOBAL> -model <Rosetta Model Application Full Path> -ID <User Input Record ID>"
db_file = ""
mu_global = ""
output_file = ""
full_path = os.getcwd() + "\\"
datDirectory = ""
solDirectory = ""
name_sol = ""
ID = ""
FULL_PATH_ROSETTA_APPLICATION = ""
EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION = "rosetta.exe"

FULL_PATH_RUNABLE_ROSETTA_APPLICATION = ""
FULL_PATH_WEIGHTS_FOLDER_ROSETTA = ""

OUTPUT_ROSETTA_MODEL_FILE_PATH = ""
INPUT_ROSETTA_MODEL_FILE_PATH = ""


NUMBER_LAYERS_SOL_FILE = 7
SAND_LIST = []
SILK_LIST = []
CLAY_LIST = []
BULK_DENSITY_LIST = []
TOT_C_LIST = []
W3CLD_LIST = [] 
W15AD_LIST = []
ROCK_FRAGMENT_LIST = []

SAT_HY_COND_LIST_FULL = []
FIELD_CAPACITY_LIST_FULL = []
WILITING_POINT_LIST_FULL = []



# Manage arguments
if (sys.argv[1] == '-d') :
    if (sys.argv[2] is None) :
        sys.exit(message)
    else:
        # db_file = full_path + sys.argv[2]
        db_file = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT_REAL_TIME" + sys.argv[2]
        db_file = db_file.replace("\\\\", "\\")
else :
    sys.exit(message)

if (sys.argv[3] == '-m') :
    if (sys.argv[4] is None) :
        sys.exit(message)
    else:
        mu_global = sys.argv[4]
else :
    sys.exit(message)
    
if (sys.argv[5] == '-model'):
    if (sys.argv[6] is None) :
        sys.exit(message)
    else:
        if (os.path.exists(sys.argv[6])):
            FULL_PATH_ROSETTA_APPLICATION = sys.argv[6]
        else:
            sys.exit("==[Error] : Folder contains Rosetta Model is NOT Existed") 
        FULL_PATH_RUNABLE_ROSETTA_APPLICATION = os.path.join(FULL_PATH_ROSETTA_APPLICATION, EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION)
        FULL_PATH_WEIGHTS_FOLDER_ROSETTA = os.path.join(FULL_PATH_ROSETTA_APPLICATION, "weights")
        print("\n---[Done] : Rosetta Model Application is in Folder %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION))     
else:
    sys.exit(message)
    
if (sys.argv[7] == '-ID'):
    if (sys.argv[8] is None):
        sys.exit(message)
    else:
        ID = str(sys.argv[8])
else:
    sys.exit(message)


NUMBER_LAYERS_SOL_FILE = support_SOIL.get_number_layers(ID)

PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT_REAL_TIME\\Result_HWSD\\Private\\%s" % (str(ID)), "SIMILARITY\\%s.csv" %(str(ID)))
# Set Up MSAccess Driver
user = ''
password = ''
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s' % \
                (db_file, user, password)

# Function

def copyFile(From, To):
    shutil.copy2(From, To)
def prepareDistinguish_Input_Output_Folder_PerEachProcess():
    current = time.time()
    output_direction = full_path + "\Rosetta_Model_Application\Output\%s" % str(current)
    if not os.path.exists(output_direction):
        os.makedirs(output_direction)
    input_direction = full_path + "\Rosetta_Model_Application\Input\%s" % str(current)
    if not os.path.exists(input_direction):
        os.makedirs(input_direction)
    return str(current)
def queryIDfollow_MU_GLOBAL():
    try :
        conn = pyodbc.connect(odbc_conn_str)
        print("---Connected database successfully---")
        # create a cursor
        cur = conn.cursor()

        # extract all the data
        sql = "SELECT ID, SEQ, SHARE, SU_SYM90 FROM HWSD_DATA WHERE MU_GLOBAL = %d " % (int(mu_global))

        # print(sql)
        cur.execute(sql)

        # show the result
        result = cur.fetchall()

        # Preprocess checking
        numItems = len(result)

        if (numItems <= 0) :
            sys.exit("There is no any records for this MU_GLOBAL")
        else:
            print("---Select data successfully---")
        return result
    except Exception, err:
        sys.stderr.write('Please check correctness of database file %s' % (err))
    finally :
        # close the cursor and connection
        # fo.close()
        cur.close()
        conn.close()

def recordsDATFile(result):
    try:
        fo = open(os.path.join("Result_HWSD/DATFiles/%s/" % (mu_global), "SOILCOM.DAT"), "wb")
        count = 0
        print("---Write data to file SOILCOM.DAT---")
        for item in result:
            count += 1
            if (count == 1):
                # strContent = "    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                strContent = "    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
            else:
                if (count >= 2 and count <= 9):
                    # strContent = "\n    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
                elif (count >= 10 and count <= 99):
                    # strContent = "\n   %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n   %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
                elif (count >= 100 and count <= 999):
                    # strContent = "\n  %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n  %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
                elif (count >= 1000 and count <= 9999):
                    # strContent = "\n %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
                elif (count >= 10000 and count <= 99999):
                    # strContent = "\n%d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n%d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(item[3]))
            fo.write(strContent)
        return 1
    finally :
        fo.close()
        
def querySoilPropertyFollowWise3_ID(wise3_id):
    try :
        conn = pyodbc.connect(odbc_conn_str)
        print("--Query sold property from HWSD_DATA with ID = %d" % (wise3_id))
        # create a cursor
        cur = conn.cursor()

        # extract all the data
        sql = "SELECT SEQ, SHARE, SU_SYM90, T_SAND, S_SAND, T_SILT, S_SILT, T_PH_H2O, S_PH_H2O, T_OC, S_OC, T_CACO3, S_CACO3, T_CEC_SOIL, S_CEC_SOIL, T_GRAVEL, S_GRAVEL, T_REF_BULK_DENSITY, S_REF_BULK_DENSITY, T_ECE, S_ECE, T_CLAY, S_CLAY FROM HWSD_DATA WHERE ID = %d AND MU_GLOBAL = %d" % (int(wise3_id), int(mu_global))

        # print(sql)
        cur.execute(sql)

        # show the result
        result = cur.fetchall()

        # Preprocess checking
        numItems = len(result)

        if (numItems <= 0):
            sys.exit("There is no any records for this ID")
        else:
            print("---Query Soil property successfully---")
        return result
    except Exception, err:
        sys.stderr.write('Please check correctness of database file %s' % (err))
    finally:
        cur.close()
        conn.close()
#######################################################################################################################################
#######################################################################################################################################
def createSOILFile_V2(wise3_id, name_sol, SAND_LIST, SILK_LIST, t_ph_h2o, s_ph_h2o, t_oc, s_oc, t_caco3, s_caco3, t_cec_soil, s_cec_soil, ROCK_FRAGMENT_LIST, t_ref_bulk_density, s_ref_bulk_density, t_ece, s_ece, WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL):
    try:
        fo = open(os.path.join("Result_HWSD/SOLFiles/%s/" % (str(mu_global)), name_sol + ".SOL"), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SOIL property to File %s.SOL" % (name_sol))
        # Line 1
        fo.write("            %s" % (name_sol))
        # Line 2
        field_2_line_2 = 0.0
        shc = SAT_HY_COND_LIST_FULL[0] + SAT_HY_COND_LIST_FULL[1] + SAT_HY_COND_LIST_FULL[2] + SAT_HY_COND_LIST_FULL[3]
        if (shc > 254):
            field_2_line_2 = 1
        elif (shc >= 84 and shc <= 254):
            field_2_line_2 = 2
        elif (shc >= 8.4 and shc <= 84):
            field_2_line_2 = 3
        elif (shc >= 0 and shc < 8.4):
            field_2_line_2 = 4
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.15, field_2_line_2, 0, 0, 0, 0, 0, 0, 0, 0))
        
        # Line 3
        # fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (10, 0, 50, 2, 0.1, 0.1, 0.1, 0, 0, 0))
        field_1 = 10
        field_2 = 0
        field_3 = 50
        field_4 = 2
        field_5 = 0.1
        field_6 = 0.1
        field_7 = 0.1
        field_8 = 0
        field_9 = 0
        field_10 = 0
        fo.write("\n")
        if (field_1 >= 0 and field_1 < 10):
            strContent = "    %0.2f" % (field_1)
        elif (field_1 > 9 and field_1 < 100):
            strContent = "   %0.2f" % (field_1)
        fo.write(strContent)
        
        if (field_2 >= 0 and field_2 < 10):
            strContent = "    %0.2f" % (field_2)
        elif (field_2 > 9 and field_2 < 100):
            strContent = "   %0.2f" % (field_2)
        fo.write(strContent)
        
        if (field_3 >= 0 and field_3 < 10):
            strContent = "    %0.2f" % (field_3)
        elif (field_3 > 9 and field_3 < 100):
            strContent = "   %0.2f" % (field_3)
        fo.write(strContent)
        
        if (field_4 >= 0 and field_4 < 10):
            strContent = "    %0.2f" % (field_4)
        elif (field_4 > 9 and field_4 < 100):
            strContent = "   %0.2f" % (field_4)
        fo.write(strContent)
        
        if (field_5 >= 0 and field_5 < 10):
            strContent = "    %0.2f" % (field_5)
        elif (field_5 > 9 and field_5 < 100):
            strContent = "   %0.2f" % (field_5)
        fo.write(strContent)
        
        if (field_6 >= 0 and field_6 < 10):
            strContent = "    %0.2f" % (field_6)
        elif (field_6 > 9 and field_6 < 100):
            strContent = "   %0.2f" % (field_6)
        fo.write(strContent)
        
        if (field_7 >= 0 and field_7 < 10):
            strContent = "    %0.2f" % (field_7)
        elif (field_7 > 9 and field_7 < 100):
            strContent = "   %0.2f" % (field_7)
        fo.write(strContent)
        
        if (field_8 >= 0 and field_8 < 10):
            strContent = "    %0.2f" % (field_8)
        elif (field_8 > 9 and field_8 < 100):
            strContent = "   %0.2f" % (field_8)
        fo.write(strContent)
        
        if (field_9 >= 0 and field_9 < 10):
            strContent = "    %0.2f" % (field_9)
        elif (field_9 > 9 and field_9 < 100):
            strContent = "   %0.2f" % (field_9)
        fo.write(strContent)
        
        if (field_10 >= 0 and field_10 < 10):
            strContent = "    %0.2f" % (field_10)
        elif (field_10 > 9 and field_10 < 100):
            strContent = "   %0.2f" % (field_10)
        fo.write(strContent)
        # Line 4 - Depth to bottom of layer - 0.01 - 10
        fo.write("\n")
        strContent = ""
        strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2)
        fo.write(strContent)
        
        # Line 5 - Dry Bulk Density % - T_REF_BULK_DENSITY and S_REF_BULK_DENSITY - 0 -> 2.0
        fo.write("\n")
        if (t_ref_bulk_density >= 0 and t_ref_bulk_density < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
        elif (t_ref_bulk_density > 9 and t_ref_bulk_density < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
        fo.write(strContent)
        
        weighted_average_ref_bulk_density = (float(t_ref_bulk_density) + float(s_ref_bulk_density)) / 2
        if (weighted_average_ref_bulk_density >= 0 and weighted_average_ref_bulk_density < 10):
            strContent = "    %0.2f" % (weighted_average_ref_bulk_density)
        elif (weighted_average_ref_bulk_density > 9 and weighted_average_ref_bulk_density < 100):
            strContent = "   %0.2f" % (weighted_average_ref_bulk_density)    
        fo.write(strContent)    
        
        if (s_ref_bulk_density >= 0 and s_ref_bulk_density < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
        elif (s_ref_bulk_density > 9 and s_ref_bulk_density < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
        fo.write(strContent)
        # Line 6 - Water content at PWP - 0.01 - 0.5
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (WILITING_POINT_LIST_FULL[i] >= 0 and WILITING_POINT_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (WILITING_POINT_LIST_FULL[i])
            elif (WILITING_POINT_LIST_FULL[i] > 9 and WILITING_POINT_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (WILITING_POINT_LIST_FULL[i])
        fo.write(strContent)
          
        # Line 7 - Water Content at FC - 0.1 - 0.6
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (FIELD_CAPACITY_LIST_FULL[i] >= 0 and FIELD_CAPACITY_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
            elif (FIELD_CAPACITY_LIST_FULL[i] > 9 and FIELD_CAPACITY_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
        fo.write(strContent)
        
        # Line 8 - Sand Content - T_SAND and S_SAND - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SAND_LIST[i] >= 0 and SAND_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (SAND_LIST[i])
            elif (SAND_LIST[i] > 9 and SAND_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (SAND_LIST[i])
        fo.write(strContent)
        
        # Line 9 - Silt Content - T_SILT and S_SILT - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SILK_LIST[i] >= 0 and SILK_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (SILK_LIST[i])
            elif (SILK_LIST[i] > 9 and SILK_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (SILK_LIST[i])
        fo.write(strContent)
        
        # Line 10 - Initial Organic N - 100 -> 5000 ppm
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        
        # Line 11 - Soil PH - T_PH_H2O and S_PH_H2O - 3 -> 9
        fo.write("\n")
        strContent = ""
        if (t_ph_h2o >= 0 and t_ph_h2o < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
        elif (t_ph_h2o > 9 and t_ph_h2o < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
        fo.write(strContent)
        weighted_average_ph_h2o = (float(t_ph_h2o) + float(s_ph_h2o)) / 2
        if (weighted_average_ph_h2o >= 0 and weighted_average_ph_h2o < 10):
            strContent = "    %0.2f" % (weighted_average_ph_h2o)
        elif (weighted_average_ph_h2o > 9 and weighted_average_ph_h2o < 100):
            strContent = "   %0.2f" % (weighted_average_ph_h2o)    
        fo.write(strContent)    
        if (s_ph_h2o >= 0 and s_ph_h2o < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o)
        elif (s_ph_h2o > 9 and s_ph_h2o < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o)
        fo.write(strContent)
        
        # Line 12 - Sum of bases - 0 -> 150
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 13 - Organic C Conc % - T_OC and S_OC - 0.1 -> 10
        fo.write("\n")
        if (t_oc >= 0 and t_oc < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_oc, t_oc, t_oc)
        elif (t_oc > 9 and t_oc < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_oc, t_oc, t_oc)
        fo.write(strContent)
        
        weighted_average_t_oc = (float(t_oc) + float(s_oc)) / 2
        if (weighted_average_t_oc >= 0 and weighted_average_t_oc < 10):
            strContent = "    %0.2f" % (weighted_average_t_oc)
        elif (weighted_average_t_oc > 9 and weighted_average_t_oc < 100):
            strContent = "   %0.2f" % (weighted_average_t_oc)    
        fo.write(strContent)    
        
        if (s_oc >= 0 and s_oc < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_oc, s_oc, s_oc)
        elif (s_oc > 9 and s_oc < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_oc, s_oc, s_oc)
        fo.write(strContent)
        
        # Line 14 - Calcium Carbonat Content % - T_CACO3 and S_CACO3 - 0 -> 99
        fo.write("\n")
        if (t_caco3 >= 0 and t_caco3 < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3)
        elif (t_caco3 > 9 and t_caco3 < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3)
        fo.write(strContent)
        
        weighted_average_t_caco3 = (float(t_caco3) + float(s_caco3)) / 2
        if (weighted_average_t_caco3 >= 0 and weighted_average_t_caco3 < 10):
            strContent = "    %0.2f" % (weighted_average_t_caco3)
        elif (weighted_average_t_caco3 > 9 and weighted_average_t_caco3 < 100):
            strContent = "   %0.2f" % (weighted_average_t_caco3)    
        fo.write(strContent)
        
        if (s_caco3 >= 0 and s_caco3 < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
        elif (s_caco3 > 9 and s_caco3 < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
        fo.write(strContent)
        # Line 15 - CEC - T_CEC_SOIL and S_CEC_SOIL - 0 -> 150
        fo.write("\n")
        if (t_cec_soil >= 0 and t_cec_soil < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
        elif (t_cec_soil > 9 and t_cec_soil < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
        elif (t_cec_soil > 99 and t_cec_soil < 1000):
            strContent = "  %0.2f  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
        fo.write(strContent)
        
        
        weighted_average_cec_soil = (float(t_cec_soil) + float(s_cec_soil)) / 2
        if (weighted_average_cec_soil >= 0 and weighted_average_cec_soil < 10):
            strContent = "    %0.2f" % (weighted_average_cec_soil)
        elif (weighted_average_cec_soil > 9 and weighted_average_cec_soil < 100):
            strContent = "   %0.2f" % (weighted_average_cec_soil)    
        fo.write(strContent)
        
        if (s_cec_soil >= 0 and s_cec_soil < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
        elif (s_cec_soil > 9 and s_cec_soil < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
        elif (s_cec_soil > 99 and s_cec_soil < 1000):
            strContent = "  %0.2f  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
        fo.write(strContent)
        
        # Line 16 - Coarse Fragment % 
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (ROCK_FRAGMENT_LIST[i] >= 0 and ROCK_FRAGMENT_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (ROCK_FRAGMENT_LIST[i])
           elif (ROCK_FRAGMENT_LIST[i] > 9 and ROCK_FRAGMENT_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (ROCK_FRAGMENT_LIST[i])
        fo.write(strContent)
        # Line 17 - Initial Soluble N
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 18 - Initial Soluble P
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 19 - Crop Residue - 0 - 20
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        
        # Line 20 - Moist bulk density - 0.5 - 2.5
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 21 - Phosphorous sorption ratio - 0 -> 0.9
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 22 - Saturated conductivity 0.00001-100
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (SAT_HY_COND_LIST_FULL[i] >= 0 and SAT_HY_COND_LIST_FULL[i] < 10):
               strContent = strContent + "    %0.2f" % (SAT_HY_COND_LIST_FULL[i])
           elif (SAT_HY_COND_LIST_FULL[i] > 9 and SAT_HY_COND_LIST_FULL[i] < 100):
               strContent = strContent + "   %0.2f" % (SAT_HY_COND_LIST_FULL[i])
        fo.write(strContent)
        
        # Line 23 - Lateral Hydraulic 0.00001-10
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 24 - Initial Organic P conc 50 - 1000
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 25 - Exchangeable K conc
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        
        # Line 26 - Electrical Conductivity 0 - 50
        fo.write("\n")
        if (t_ece >= 0 and t_ece < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece)
        elif (t_ece > 9 and t_ece < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece)
        fo.write(strContent)
        
        weighted_average_ece = (float(t_ece) + float(s_ece)) / 2
        if (weighted_average_ece >= 0 and weighted_average_ece < 10):
            strContent = "    %0.2f" % (weighted_average_ece)
        elif (weighted_average_ece > 9 and weighted_average_ece < 100):
            strContent = "   %0.2f" % (weighted_average_ece)    
        fo.write(strContent)
        
        if (s_ece >= 0 and s_ece < 10):
            strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
        elif (s_ece > 9 and s_ece < 100):
            strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
        fo.write(strContent)

        # Line 27 -> 45
        for i in range(27, 46):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
    except Exception, err:
        sys.exit("Error : %s" % (err))
    finally:
        fo.close()
###################################################################################################################################################################################        
def createSOILFile_V2_Depend_Number_Of_Layers_SOIL_GRIDS_ISRIC(wise3_id, name_sol, SAND_LIST, SILK_LIST, t_ph_h2o, s_ph_h2o, t_oc, s_oc, t_caco3, s_caco3, t_cec_soil, s_cec_soil, ROCK_FRAGMENT_LIST, t_ref_bulk_density, s_ref_bulk_density, t_ece, s_ece, WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL,ORCDRC_MAPPING_LIST,PHIHOX_MAPPING_LIST,BLD_MAPPING_LIST,CEC_MAPPING_LIST):
    try:
        fo = open(os.path.join("Result_HWSD/SOLFiles/%s/" % (str(mu_global)), name_sol + ".SOL"), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SOIL property to File %s.SOL" % (name_sol))
        # Line 1
        fo.write("            %s" % (name_sol))
        # Line 2
        field_2_line_2 = 0.0
        shc = SAT_HY_COND_LIST_FULL[0] + SAT_HY_COND_LIST_FULL[1] + SAT_HY_COND_LIST_FULL[2] + SAT_HY_COND_LIST_FULL[3]
        if (shc > 254):
            field_2_line_2 = 1
        elif (shc >= 84 and shc <= 254):
            field_2_line_2 = 2
        elif (shc >= 8.4 and shc <= 84):
            field_2_line_2 = 3
        elif (shc >= 0 and shc < 8.4):
            field_2_line_2 = 4
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.15, field_2_line_2, 0, 0, 0, 0, 0, 0, 0, 0))
        
        # Line 3
        # fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (10, 0, 50, 2, 0.1, 0.1, 0.1, 0, 0, 0))
        field_1 = 10
        field_2 = 0
        field_3 = 50
        field_4 = 2
        field_5 = 0.1
        field_6 = 0.1
        field_7 = 0.1
        field_8 = 0
        field_9 = 0
        field_10 = 0
        fo.write("\n")
        if (field_1 >= 0 and field_1 < 10):
            strContent = "    %0.2f" % (field_1)
        elif (field_1 > 9 and field_1 < 100):
            strContent = "   %0.2f" % (field_1)
        fo.write(strContent)
        
        if (field_2 >= 0 and field_2 < 10):
            strContent = "    %0.2f" % (field_2)
        elif (field_2 > 9 and field_2 < 100):
            strContent = "   %0.2f" % (field_2)
        fo.write(strContent)
        
        if (field_3 >= 0 and field_3 < 10):
            strContent = "    %0.2f" % (field_3)
        elif (field_3 > 9 and field_3 < 100):
            strContent = "   %0.2f" % (field_3)
        fo.write(strContent)
        
        if (field_4 >= 0 and field_4 < 10):
            strContent = "    %0.2f" % (field_4)
        elif (field_4 > 9 and field_4 < 100):
            strContent = "   %0.2f" % (field_4)
        fo.write(strContent)
        
        if (field_5 >= 0 and field_5 < 10):
            strContent = "    %0.2f" % (field_5)
        elif (field_5 > 9 and field_5 < 100):
            strContent = "   %0.2f" % (field_5)
        fo.write(strContent)
        
        if (field_6 >= 0 and field_6 < 10):
            strContent = "    %0.2f" % (field_6)
        elif (field_6 > 9 and field_6 < 100):
            strContent = "   %0.2f" % (field_6)
        fo.write(strContent)
        
        if (field_7 >= 0 and field_7 < 10):
            strContent = "    %0.2f" % (field_7)
        elif (field_7 > 9 and field_7 < 100):
            strContent = "   %0.2f" % (field_7)
        fo.write(strContent)
        
        if (field_8 >= 0 and field_8 < 10):
            strContent = "    %0.2f" % (field_8)
        elif (field_8 > 9 and field_8 < 100):
            strContent = "   %0.2f" % (field_8)
        fo.write(strContent)
        
        if (field_9 >= 0 and field_9 < 10):
            strContent = "    %0.2f" % (field_9)
        elif (field_9 > 9 and field_9 < 100):
            strContent = "   %0.2f" % (field_9)
        fo.write(strContent)
        
        if (field_10 >= 0 and field_10 < 10):
            strContent = "    %0.2f" % (field_10)
        elif (field_10 > 9 and field_10 < 100):
            strContent = "   %0.2f" % (field_10)
        fo.write(strContent)
        # Line 4 - Depth to bottom of layer - 0.01 - 10
        fo.write("\n")
        strContent = ""
        if (NUMBER_LAYERS_SOL_FILE == 7):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2)
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0)
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7)
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5)
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           strContent = "    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2)
        elif (NUMBER_LAYERS_SOL_FILE == 2):      
           strContent = "    %0.2f    %0.2f" % (0.01, 0.1)
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           strContent = "    %0.2f" % (0.01)
        else:
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2)
        fo.write(strContent)
        
        # Line 5 - Dry Bulk Density % - T_REF_BULK_DENSITY and S_REF_BULK_DENSITY - 0 -> 2.0
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (BLD_MAPPING_LIST[i] >= 0 and BLD_MAPPING_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (BLD_MAPPING_LIST[i])
            elif (BLD_MAPPING_LIST[i] > 9 and BLD_MAPPING_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (BLD_MAPPING_LIST[i])
        fo.write(strContent)
        
        # Line 6 - Water content at PWP - 0.01 - 0.5
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (WILITING_POINT_LIST_FULL[i] >= 0 and WILITING_POINT_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (WILITING_POINT_LIST_FULL[i])
            elif (WILITING_POINT_LIST_FULL[i] > 9 and WILITING_POINT_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (WILITING_POINT_LIST_FULL[i])
        fo.write(strContent)
          
        # Line 7 - Water Content at FC - 0.1 - 0.6
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (FIELD_CAPACITY_LIST_FULL[i] >= 0 and FIELD_CAPACITY_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
            elif (FIELD_CAPACITY_LIST_FULL[i] > 9 and FIELD_CAPACITY_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
        fo.write(strContent)
        
        # Line 8 - Sand Content - T_SAND and S_SAND - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SAND_LIST[i] >= 0 and SAND_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (SAND_LIST[i])
            elif (SAND_LIST[i] > 9 and SAND_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (SAND_LIST[i])
        fo.write(strContent)
        
        # Line 9 - Silt Content - T_SILT and S_SILT - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SILK_LIST[i] >= 0 and SILK_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (SILK_LIST[i])
            elif (SILK_LIST[i] > 9 and SILK_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (SILK_LIST[i])
        fo.write(strContent)
        
        # Line 10 - Initial Organic N - 100 -> 5000 ppm
        if (NUMBER_LAYERS_SOL_FILE == 7):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 5):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 4):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 3):
            fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
            fo.write("\n    %0.2f    %0.2f" % (0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 1):
            fo.write("\n    %0.2f" % (0))
        else:
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))    
        
        # Line 11 - Soil PH - T_PH_H2O and S_PH_H2O - 3 -> 9
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (PHIHOX_MAPPING_LIST[i] >= 0 and PHIHOX_MAPPING_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (PHIHOX_MAPPING_LIST[i])
            elif (PHIHOX_MAPPING_LIST[i] > 9 and PHIHOX_MAPPING_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (PHIHOX_MAPPING_LIST[i])
        fo.write(strContent)
        
        # Line 12 - Sum of bases - 0 -> 150
        if (NUMBER_LAYERS_SOL_FILE == 7):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 5):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 4):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 3):
            fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
            fo.write("\n    %0.2f    %0.2f" % (0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 1):
            fo.write("\n    %0.2f" % (0))
        else:    
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            
            
        # Line 13 - Organic C Conc % - T_OC and S_OC - 0.1 -> 10
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (ORCDRC_MAPPING_LIST[i] >= 0 and ORCDRC_MAPPING_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (ORCDRC_MAPPING_LIST[i])
            elif (ORCDRC_MAPPING_LIST[i] > 9 and ORCDRC_MAPPING_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (ORCDRC_MAPPING_LIST[i])
        fo.write(strContent)
        
        # Line 14 - Calcium Carbonat Content % - T_CACO3 and S_CACO3 - 0 -> 99
        fo.write("\n")
        if (t_caco3 >= 0 and t_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3) 
        elif (t_caco3 > 9 and t_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3)
        fo.write(strContent)
        
        weighted_average_t_caco3 = (float(t_caco3) + float(s_caco3)) / 2
        if (weighted_average_t_caco3 >= 0 and weighted_average_t_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
              strContent = "    %0.2f" % (weighted_average_t_caco3)
            else:
              strContent = ""
        elif (weighted_average_t_caco3 > 9 and weighted_average_t_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
              strContent = "   %0.2f" % (weighted_average_t_caco3)
            else:
              strContent = ""
        fo.write(strContent)
        
        if (s_caco3 >= 0 and s_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (s_caco3, s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
        elif (s_caco3 > 9 and s_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (s_caco3, s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
        fo.write(strContent)
        
        
        # Line 15 - CEC - T_CEC_SOIL and S_CEC_SOIL - 0 -> 150
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (CEC_MAPPING_LIST[i] >= 0 and CEC_MAPPING_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (CEC_MAPPING_LIST[i])
            elif (CEC_MAPPING_LIST[i] > 9 and CEC_MAPPING_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (CEC_MAPPING_LIST[i])
        fo.write(strContent)
        
        # Line 16 - Coarse Fragment % 
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (ROCK_FRAGMENT_LIST[i] >= 0 and ROCK_FRAGMENT_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (ROCK_FRAGMENT_LIST[i])
           elif (ROCK_FRAGMENT_LIST[i] > 9 and ROCK_FRAGMENT_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (ROCK_FRAGMENT_LIST[i])
        fo.write(strContent)
       
        
        # Line 17 - Initial Soluble N
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            
        # Line 18 - Initial Soluble P
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
        # Line 19 - Crop Residue - 0 - 20
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        
        # Line 20 - Moist bulk density - 0.5 - 2.5
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 21 - Phosphorous sorption ratio - 0 -> 0.9
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 22 - Saturated conductivity 0.00001-100
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (SAT_HY_COND_LIST_FULL[i] >= 0 and SAT_HY_COND_LIST_FULL[i] < 10):
               strContent = strContent + "    %0.2f" % (SAT_HY_COND_LIST_FULL[i])
           elif (SAT_HY_COND_LIST_FULL[i] > 9 and SAT_HY_COND_LIST_FULL[i] < 100):
               strContent = strContent + "   %0.2f" % (SAT_HY_COND_LIST_FULL[i])
        fo.write(strContent)
        
        
        # Line 23 - Lateral Hydraulic 0.00001-10
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
           
        # Line 24 - Initial Organic P conc 50 - 1000
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
           
        # Line 25 - Exchangeable K conc
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
        
        # Line 26 - Electrical Conductivity 0 - 50
        fo.write("\n")
        if (t_ece >= 0 and t_ece < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece) 
        elif (t_ece > 9 and t_ece < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece)
        fo.write(strContent)
        
        weighted_average_ece = (float(t_ece) + float(s_ece)) / 2
        if (weighted_average_ece >= 0 and weighted_average_ece < 10):
           if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "    %0.2f" % (weighted_average_ece)
           else:
               strContent = ""
        elif (weighted_average_ece > 9 and weighted_average_ece < 100):
           if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "   %0.2f" % (weighted_average_ece)
           else:
               strContent = ""
        fo.write(strContent)
        
        if (s_ece >= 0 and s_ece < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
        elif (s_ece > 9 and s_ece < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
        fo.write(strContent)

        # Line 27 -> 45
        for i in range(27, 46):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               fo.write("\n    %0.2f" % (0)) 
            else:
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
    except Exception, err:
        sys.exit("Error : %s" % (err))
    finally:
        fo.close() 
####################################################################################################################################################################################### 
####################################################################################################################################################################################### 
####################################################################################################################################################################################### 
####################################################################################################################################################################################### 
#######################################################################################################################################################################################         
#######################################################################################################################################################################################        
def createSOILFile_V2_Depend_Number_Of_Layers(wise3_id, name_sol, SAND_LIST, SILK_LIST, t_ph_h2o, s_ph_h2o, t_oc, s_oc, t_caco3, s_caco3, t_cec_soil, s_cec_soil, ROCK_FRAGMENT_LIST, t_ref_bulk_density, s_ref_bulk_density, t_ece, s_ece, WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL):
    try:
        fo = open(os.path.join("Result_HWSD/SOLFiles/%s/" % (str(mu_global)), name_sol + ".SOL"), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SOIL property to File %s.SOL" % (name_sol))
        # Line 1
        fo.write("            %s" % (name_sol))
        # Line 2
        field_2_line_2 = 0.0
        shc = SAT_HY_COND_LIST_FULL[0] + SAT_HY_COND_LIST_FULL[1] + SAT_HY_COND_LIST_FULL[2] + SAT_HY_COND_LIST_FULL[3]
        if (shc > 254):
            field_2_line_2 = 1
        elif (shc >= 84 and shc <= 254):
            field_2_line_2 = 2
        elif (shc >= 8.4 and shc <= 84):
            field_2_line_2 = 3
        elif (shc >= 0 and shc < 8.4):
            field_2_line_2 = 4
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.15, field_2_line_2, 0, 0, 0, 0, 0, 0, 0, 0))
        
        # Line 3
        # fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (10, 0, 50, 2, 0.1, 0.1, 0.1, 0, 0, 0))
        field_1 = 10
        field_2 = 0
        field_3 = 50
        field_4 = 2
        field_5 = 0.1
        field_6 = 0.1
        field_7 = 0.1
        field_8 = 0
        field_9 = 0
        field_10 = 0
        fo.write("\n")
        if (field_1 >= 0 and field_1 < 10):
            strContent = "    %0.2f" % (field_1)
        elif (field_1 > 9 and field_1 < 100):
            strContent = "   %0.2f" % (field_1)
        fo.write(strContent)
        
        if (field_2 >= 0 and field_2 < 10):
            strContent = "    %0.2f" % (field_2)
        elif (field_2 > 9 and field_2 < 100):
            strContent = "   %0.2f" % (field_2)
        fo.write(strContent)
        
        if (field_3 >= 0 and field_3 < 10):
            strContent = "    %0.2f" % (field_3)
        elif (field_3 > 9 and field_3 < 100):
            strContent = "   %0.2f" % (field_3)
        fo.write(strContent)
        
        if (field_4 >= 0 and field_4 < 10):
            strContent = "    %0.2f" % (field_4)
        elif (field_4 > 9 and field_4 < 100):
            strContent = "   %0.2f" % (field_4)
        fo.write(strContent)
        
        if (field_5 >= 0 and field_5 < 10):
            strContent = "    %0.2f" % (field_5)
        elif (field_5 > 9 and field_5 < 100):
            strContent = "   %0.2f" % (field_5)
        fo.write(strContent)
        
        if (field_6 >= 0 and field_6 < 10):
            strContent = "    %0.2f" % (field_6)
        elif (field_6 > 9 and field_6 < 100):
            strContent = "   %0.2f" % (field_6)
        fo.write(strContent)
        
        if (field_7 >= 0 and field_7 < 10):
            strContent = "    %0.2f" % (field_7)
        elif (field_7 > 9 and field_7 < 100):
            strContent = "   %0.2f" % (field_7)
        fo.write(strContent)
        
        if (field_8 >= 0 and field_8 < 10):
            strContent = "    %0.2f" % (field_8)
        elif (field_8 > 9 and field_8 < 100):
            strContent = "   %0.2f" % (field_8)
        fo.write(strContent)
        
        if (field_9 >= 0 and field_9 < 10):
            strContent = "    %0.2f" % (field_9)
        elif (field_9 > 9 and field_9 < 100):
            strContent = "   %0.2f" % (field_9)
        fo.write(strContent)
        
        if (field_10 >= 0 and field_10 < 10):
            strContent = "    %0.2f" % (field_10)
        elif (field_10 > 9 and field_10 < 100):
            strContent = "   %0.2f" % (field_10)
        fo.write(strContent)
        # Line 4 - Depth to bottom of layer - 0.01 - 10
        fo.write("\n")
        strContent = ""
        if (NUMBER_LAYERS_SOL_FILE == 7):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2)
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0)
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7)
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5)
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           strContent = "    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2)
        elif (NUMBER_LAYERS_SOL_FILE == 2):      
           strContent = "    %0.2f    %0.2f" % (0.01, 0.1)
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           strContent = "    %0.2f" % (0.01)
        else:
           strContent = "    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.01, 0.1, 0.2, 0.5, 0.7, 1.0, 1.2)
        fo.write(strContent)
        
        # Line 5 - Dry Bulk Density % - T_REF_BULK_DENSITY and S_REF_BULK_DENSITY - 0 -> 2.0
        fo.write("\n")
        if (t_ref_bulk_density >= 0 and t_ref_bulk_density < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)    
        elif (t_ref_bulk_density > 9 and t_ref_bulk_density < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7): 
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ref_bulk_density, t_ref_bulk_density, t_ref_bulk_density)     
        fo.write(strContent)
        
        weighted_average_ref_bulk_density = (float(t_ref_bulk_density) + float(s_ref_bulk_density)) / 2
        if (weighted_average_ref_bulk_density >= 0 and weighted_average_ref_bulk_density < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE ==1):
               strContent = "    %0.2f" % (weighted_average_ref_bulk_density)
            else:
               strContent = "" 
        elif (weighted_average_ref_bulk_density > 9 and weighted_average_ref_bulk_density < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE ==1):
               strContent = "   %0.2f" % (weighted_average_ref_bulk_density)
            else:
               strContent = ""    
        fo.write(strContent)    
        
        if (s_ref_bulk_density >= 0 and s_ref_bulk_density < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "    %0.2f" % (s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "    %0.2f" % (s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
        elif (s_ref_bulk_density > 9 and s_ref_bulk_density < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "   %0.2f" % (s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "   %0.2f" % (s_ref_bulk_density)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_ref_bulk_density, s_ref_bulk_density, s_ref_bulk_density)
        fo.write(strContent)
        
        
        # Line 6 - Water content at PWP - 0.01 - 0.5
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (WILITING_POINT_LIST_FULL[i] >= 0 and WILITING_POINT_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (WILITING_POINT_LIST_FULL[i])
            elif (WILITING_POINT_LIST_FULL[i] > 9 and WILITING_POINT_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (WILITING_POINT_LIST_FULL[i])
        fo.write(strContent)
          
        # Line 7 - Water Content at FC - 0.1 - 0.6
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (FIELD_CAPACITY_LIST_FULL[i] >= 0 and FIELD_CAPACITY_LIST_FULL[i] < 10):
                strContent = strContent + "    %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
            elif (FIELD_CAPACITY_LIST_FULL[i] > 9 and FIELD_CAPACITY_LIST_FULL[i] < 100):
                strContent = strContent + "   %0.2f" % (FIELD_CAPACITY_LIST_FULL[i])
        fo.write(strContent)
        
        # Line 8 - Sand Content - T_SAND and S_SAND - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SAND_LIST[i] >= 0 and SAND_LIST[i] < 10):
                strContent = strContent + "    %0.2f" % (SAND_LIST[i])
            elif (SAND_LIST[i] > 9 and SAND_LIST[i] < 100):
                strContent = strContent + "   %0.2f" % (SAND_LIST[i])
        fo.write(strContent)
        
        # Line 9 - Silt Content - T_SILT and S_SILT - 1 -> 99
        fo.write("\n")
        strContent = ""
        for i in range(0, NUMBER_LAYERS_SOL_FILE):
            if (SILK_LIST[i] >= 0 and SILK_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (SILK_LIST[i])
            elif (SILK_LIST[i] > 9 and SILK_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (SILK_LIST[i])
        fo.write(strContent)
        
        # Line 10 - Initial Organic N - 100 -> 5000 ppm
        if (NUMBER_LAYERS_SOL_FILE == 7):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 5):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 4):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 3):
            fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
            fo.write("\n    %0.2f    %0.2f" % (0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 1):
            fo.write("\n    %0.2f" % (0))
        else:
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))    
        
        # Line 11 - Soil PH - T_PH_H2O and S_PH_H2O - 3 -> 9
        fo.write("\n")
        strContent = ""
        if (t_ph_h2o >= 0 and t_ph_h2o < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
                strContent = "    %0.2f    %0.2f    %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
        elif (t_ph_h2o > 9 and t_ph_h2o < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
                strContent = "   %0.2f   %0.2f   %0.2f" % (t_ph_h2o, t_ph_h2o, t_ph_h2o)
        fo.write(strContent)
        weighted_average_ph_h2o = (float(t_ph_h2o) + float(s_ph_h2o)) / 2
        if (weighted_average_ph_h2o >= 0 and weighted_average_ph_h2o < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "    %0.2f" % (weighted_average_ph_h2o)
            else:
               strContent= ""
        elif (weighted_average_ph_h2o > 9 and weighted_average_ph_h2o < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "   %0.2f" % (weighted_average_ph_h2o)
            else:
               strContent= ""    
        fo.write(strContent)    
        if (s_ph_h2o >= 0 and s_ph_h2o < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (s_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o) 
        elif (s_ph_h2o > 9 and s_ph_h2o < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (s_ph_h2o) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (s_ph_h2o)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ph_h2o, s_ph_h2o, s_ph_h2o)
        fo.write(strContent)
        
        # Line 12 - Sum of bases - 0 -> 150
        if (NUMBER_LAYERS_SOL_FILE == 7):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 5):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 4):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 3):
            fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
            fo.write("\n    %0.2f    %0.2f" % (0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 1):
            fo.write("\n    %0.2f" % (0))
        else:    
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            
            
        # Line 13 - Organic C Conc % - T_OC and S_OC - 0.1 -> 10
        fo.write("\n")
        if (t_oc >= 0 and t_oc < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "    %0.2f    %0.2f    %0.2f" % (t_oc, t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "    %0.2f    %0.2f    %0.2f" % (t_oc, t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "    %0.2f    %0.2f" % (t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "    %0.2f    %0.2f" % (t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "    %0.2f" % (t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "    %0.2f" % (t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "    %0.2f    %0.2f    %0.2f" % (t_oc, t_oc, t_oc)
        elif (t_oc > 9 and t_oc < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "   %0.2f   %0.2f   %0.2f" % (t_oc, t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "   %0.2f   %0.2f   %0.2f" % (t_oc, t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "   %0.2f   %0.2f" % (t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "   %0.2f   %0.2f" % (t_oc, t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "   %0.2f" % (t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "   %0.2f" % (t_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "   %0.2f   %0.2f   %0.2f" % (t_oc, t_oc, t_oc)
        fo.write(strContent)
        
        weighted_average_t_oc = (float(t_oc) + float(s_oc)) / 2
        if (weighted_average_t_oc >= 0 and weighted_average_t_oc < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
                strContent = "    %0.2f" % (weighted_average_t_oc)
            else:
                strContent = ""
        elif (weighted_average_t_oc > 9 and weighted_average_t_oc < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
                strContent = "   %0.2f" % (weighted_average_t_oc)
            else:
                strContent = ""
        fo.write(strContent)    
        
        if (s_oc >= 0 and s_oc < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_oc, s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_oc, s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "    %0.2f    %0.2f" % (s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "    %0.2f    %0.2f" % (s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "    %0.2f" % (s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "    %0.2f" % (s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "    %0.2f    %0.2f    %0.2f" % (s_oc, s_oc, s_oc)
        elif (s_oc > 9 and s_oc < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_oc, s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_oc, s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
                strContent = "   %0.2f   %0.2f" % (s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 4):
                strContent = "   %0.2f   %0.2f" % (s_oc, s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
                strContent = "   %0.2f" % (s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 2):
                strContent = "   %0.2f" % (s_oc)
            elif (NUMBER_LAYERS_SOL_FILE == 1):
                strContent = ""
            else:
                strContent = "   %0.2f   %0.2f   %0.2f" % (s_oc, s_oc, s_oc)
        fo.write(strContent)
        
        # Line 14 - Calcium Carbonat Content % - T_CACO3 and S_CACO3 - 0 -> 99
        fo.write("\n")
        if (t_caco3 >= 0 and t_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_caco3, t_caco3, t_caco3) 
        elif (t_caco3 > 9 and t_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_caco3, t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_caco3, t_caco3, t_caco3)
        fo.write(strContent)
        
        weighted_average_t_caco3 = (float(t_caco3) + float(s_caco3)) / 2
        if (weighted_average_t_caco3 >= 0 and weighted_average_t_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
              strContent = "    %0.2f" % (weighted_average_t_caco3)
            else:
              strContent = ""
        elif (weighted_average_t_caco3 > 9 and weighted_average_t_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
              strContent = "   %0.2f" % (weighted_average_t_caco3)
            else:
              strContent = ""
        fo.write(strContent)
        
        if (s_caco3 >= 0 and s_caco3 < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (s_caco3, s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_caco3, s_caco3, s_caco3)
        elif (s_caco3 > 9 and s_caco3 < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (s_caco3, s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (s_caco3, s_caco3)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (s_caco3) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_caco3, s_caco3, s_caco3)
        fo.write(strContent)
        
        
        # Line 15 - CEC - T_CEC_SOIL and S_CEC_SOIL - 0 -> 150
        fo.write("\n")
        if (t_cec_soil >= 0 and t_cec_soil < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil) 
        elif (t_cec_soil > 9 and t_cec_soil < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
        elif (t_cec_soil > 99 and t_cec_soil < 1000):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "  %0.2f  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "  %0.2f  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "  %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "  %0.2f" % (t_cec_soil) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "  %0.2f  %0.2f  %0.2f" % (t_cec_soil, t_cec_soil, t_cec_soil)
        fo.write(strContent)
        
        
        weighted_average_cec_soil = (float(t_cec_soil) + float(s_cec_soil)) / 2
        if (weighted_average_cec_soil >= 0 and weighted_average_cec_soil < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "    %0.2f" % (weighted_average_cec_soil)
            else:
               strContent = ""
        elif (weighted_average_cec_soil > 9 and weighted_average_cec_soil < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "   %0.2f" % (weighted_average_cec_soil)
            else:
               strContent = ""
        elif (weighted_average_cec_soil > 99 and weighted_average_cec_soil < 1000):
            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "  %0.2f" % (weighted_average_cec_soil)
            else:
               strContent = ""
        fo.write(strContent)
        
        if (s_cec_soil >= 0 and s_cec_soil < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
              strContent = "    %0.2f    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
              strContent = "    %0.2f    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 5):
              strContent = "    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 4):
              strContent = "    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 3):
              strContent = "    %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 2):
              strContent = "    %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 1):
              strContent = ""  
            else:
              strContent = "    %0.2f    %0.2f    %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)      
        elif (s_cec_soil > 9 and s_cec_soil < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
              strContent = "   %0.2f   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
              strContent = "   %0.2f   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 5):
              strContent = "   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 4):
              strContent = "   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 3):
              strContent = "   %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 2):
              strContent = "   %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 1):
              strContent = ""  
            else:
              strContent = "   %0.2f   %0.2f   %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
        elif (s_cec_soil > 99 and s_cec_soil < 1000):
            if (NUMBER_LAYERS_SOL_FILE == 7):
              strContent = "  %0.2f  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
              strContent = "  %0.2f  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 5):
              strContent = "  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 4):
              strContent = "  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 3):
              strContent = "  %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 2):
              strContent = "  %0.2f" % (s_cec_soil)  
            elif (NUMBER_LAYERS_SOL_FILE == 1):
              strContent = ""  
            else:
              strContent = "  %0.2f  %0.2f  %0.2f" % (s_cec_soil, s_cec_soil, s_cec_soil)
        fo.write(strContent)
        
        # Line 16 - Coarse Fragment % 
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (ROCK_FRAGMENT_LIST[i] >= 0 and ROCK_FRAGMENT_LIST[i] < 10):
               strContent = strContent + "    %0.2f" % (ROCK_FRAGMENT_LIST[i])
           elif (ROCK_FRAGMENT_LIST[i] > 9 and ROCK_FRAGMENT_LIST[i] < 100):
               strContent = strContent + "   %0.2f" % (ROCK_FRAGMENT_LIST[i])
        fo.write(strContent)
       
        
        # Line 17 - Initial Soluble N
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            
        # Line 18 - Initial Soluble P
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
        # Line 19 - Crop Residue - 0 - 20
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        
        # Line 20 - Moist bulk density - 0.5 - 2.5
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 21 - Phosphorous sorption ratio - 0 -> 0.9
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        # Line 22 - Saturated conductivity 0.00001-100
        fo.write("\n")
        strContent = ""
        for i in range(0,NUMBER_LAYERS_SOL_FILE):
           if (SAT_HY_COND_LIST_FULL[i] >= 0 and SAT_HY_COND_LIST_FULL[i] < 10):
               strContent = strContent + "    %0.2f" % (SAT_HY_COND_LIST_FULL[i])
           elif (SAT_HY_COND_LIST_FULL[i] > 9 and SAT_HY_COND_LIST_FULL[i] < 100):
               strContent = strContent + "   %0.2f" % (SAT_HY_COND_LIST_FULL[i])
        fo.write(strContent)
        
        
        # Line 23 - Lateral Hydraulic 0.00001-10
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
           
        # Line 24 - Initial Organic P conc 50 - 1000
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
           
        # Line 25 - Exchangeable K conc
        if (NUMBER_LAYERS_SOL_FILE == 7):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 6):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 5):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 4):
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 3):
           fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
        elif (NUMBER_LAYERS_SOL_FILE == 2):
           fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
        elif (NUMBER_LAYERS_SOL_FILE == 1):
           fo.write("\n    %0.2f" % (0)) 
        else:
           fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
           
        
        # Line 26 - Electrical Conductivity 0 - 50
        fo.write("\n")
        if (t_ece >= 0 and t_ece < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (t_ece,t_ece,t_ece) 
        elif (t_ece > 9 and t_ece < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (t_ece,t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (t_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "" 
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (t_ece,t_ece,t_ece)
        fo.write(strContent)
        
        weighted_average_ece = (float(t_ece) + float(s_ece)) / 2
        if (weighted_average_ece >= 0 and weighted_average_ece < 10):
           if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "    %0.2f" % (weighted_average_ece)
           else:
               strContent = ""
        elif (weighted_average_ece > 9 and weighted_average_ece < 100):
           if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE == 5 or NUMBER_LAYERS_SOL_FILE == 3 or NUMBER_LAYERS_SOL_FILE == 1):
               strContent = "   %0.2f" % (weighted_average_ece)
           else:
               strContent = ""
        fo.write(strContent)
        
        if (s_ece >= 0 and s_ece < 10):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "    %0.2f    %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "    %0.2f    %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "    %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "    %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "    %0.2f    %0.2f    %0.2f" % (s_ece,s_ece,s_ece)
        elif (s_ece > 9 and s_ece < 100):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               strContent = "   %0.2f   %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               strContent = "   %0.2f   %0.2f" % (s_ece,s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               strContent = "   %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               strContent = "   %0.2f" % (s_ece) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               strContent = ""
            else:
               strContent = "   %0.2f   %0.2f   %0.2f" % (s_ece,s_ece,s_ece)
        fo.write(strContent)

        # Line 27 -> 45
        for i in range(27, 46):
            if (NUMBER_LAYERS_SOL_FILE == 7):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
            elif (NUMBER_LAYERS_SOL_FILE == 6):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 5):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 4):
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 3):
               fo.write("\n    %0.2f    %0.2f    %0.2f" % (0, 0, 0))
            elif (NUMBER_LAYERS_SOL_FILE == 2):
               fo.write("\n    %0.2f    %0.2f" % (0, 0)) 
            elif (NUMBER_LAYERS_SOL_FILE == 1):
               fo.write("\n    %0.2f" % (0)) 
            else:
               fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0, 0, 0, 0, 0, 0, 0))
    except Exception, err:
        sys.exit("Error : %s" % (err))
    finally:
        fo.close()        
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################
#######################################################################################################################################        
def checkAndCreateFolder():
    directory = full_path + "Result_HWSD"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\\" + "DATFiles\%s" % (str(mu_global))
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
    solDirectory = directory + "\\" + "SOLFiles\%s" % (str(mu_global))
    if not os.path.exists(solDirectory):
        os.makedirs(solDirectory)
    inputRosettaModel = full_path + "\Rosetta_Model_Application\Input"
    if not os.path.exists(inputRosettaModel):
        os.makedirs(inputRosettaModel)
    outputRosettaModel = full_path + "\Rosetta_Model_Application\Output"
    if not os.path.exists(outputRosettaModel):
        os.makedirs(outputRosettaModel)
def acessModelToGetValue(seq, FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, INPUT_ROSETTA_MODEL_FILE_PATH, OUTPUT_ROSETTA_MODEL_FILE_PATH, SAND_LIST, SILT_LIST, CLAY_LIST, BULK_DENSITY_LIST, TOT_C_LIST, W3CLD_LIST, W15AD_LIST):
    values = []
    
    SAT_HY_COND_LIST = [0, 0, 0, 0, 0, 0, 0]
    FIELD_CAPACITY_LIST = [0, 0, 0, 0, 0, 0, 0]
    WILTING_POINT_LIST = [0, 0, 0, 0, 0, 0, 0]
    try:
        # Create INPUT FILE
        fo = open(os.path.join(INPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_in.txt"), "wb")
        print("---Create Input file %s for Rosetta Model already" % (str(seq)))
        # Line 1
        fo.write("sam_id          layer_id    hz_tp   hz_bt   sand_tot    silt_tot    clay_tot    bulk_dens   tot_C   w3cld   w15ad")
        # Line 2
        fo.write("\n")
        # Line 3 ============ TOP LAYER
        fo.write("\n")
        
        # Process for seq
        for j in range(0, NUMBER_LAYERS_SOL_FILE):
            if (seq is None or not int(seq)):
                  seq = 1
            strSeq = str(seq)
            strContent = "";
            number_space = 16 - len(strSeq)
            strContent = "%s" % (strSeq)
            for i in range(1, number_space):
                 strContent = strContent + " "
            # Process top
            strContent = strContent + "       %d" % (j)
            
            if (j == 0):
                # Process hz_tp
                strContent = strContent + "     0.00"
                # Process hz_bt
                strContent = strContent + "     0.01"
            elif (j == 1):
                # Process hz_tp
                strContent = strContent + "     0.01"
                # Process hz_bt
                strContent = strContent + "     0.10"
            elif (j == 2):
                # Process hz_tp
                strContent = strContent + "     0.10"
                # Process hz_bt
                strContent = strContent + "     0.20"
            elif (j == 3):
                # Process hz_tp
                strContent = strContent + "     0.20"
                # Process hz_bt
                strContent = strContent + "     0.50"
            elif (j == 4):
                # Process hz_tp
                strContent = strContent + "     0.50"
                # Process hz_bt
                strContent = strContent + "     0.70" 
            elif (j == 5):
                # Process hz_tp
                strContent = strContent + "     0.70"
                # Process hz_bt
                strContent = strContent + "     1.00"
            elif (j == 6):
                # Process hz_tp
                strContent = strContent + "     1.00"
                # Process hz_bt
                strContent = strContent + "     1.20"
            # process sand_top
            fl_sand = float(SAND_LIST[j])
            number_space = 11 - len(str("%0.2f" % (fl_sand)))
            for i in range(1, number_space):
                 strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_sand)
        
            # process silt_top
            fl_silt = float(SILT_LIST[j])
            number_space = 12 - len(str("%0.2f" % (fl_silt)))
            for i in range(1, number_space):
                 strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_silt)
        
            # process clay_top
            fl_clay = 100 - fl_sand - fl_silt
            number_space = 12 - len(str("%0.2f" % (fl_clay)))
            for i in range(1, number_space):
                strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_clay)
        
        
            # process Bulk Denstity
            fl_bulk_dens = float(BULK_DENSITY_LIST[j])
            number_space = 13 - len(str("%0.2f" % (fl_bulk_dens)))
            for i in range(1, number_space):
                  strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_bulk_dens)
        
            # process Top C 1
            fl_tot_c = float(TOT_C_LIST[j])
            number_space = 8 - len(str("%0.2f" % (fl_tot_c)))
            for i in range(1, number_space):
                  strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_tot_c)
        
            # process W3 CLD 1
            fl_w3cld = float(W3CLD_LIST[j])
            number_space = 8 - len(str("%0.2f" % (fl_w3cld)))
            for i in range(1, number_space):
                 strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_w3cld)
        
            # process Top C 1
            fl_w15ad = float(W15AD_LIST[j])
            number_space = 8 - len(str("%0.2f" % (fl_w15ad)))
            for i in range(1, number_space):
                 strContent = strContent + " "
            strContent = strContent + " %0.2f" % (fl_w15ad)
        
            fo.write(strContent)
            fo.write("\n")
        
        fo.close()
        # Finish Step 1
        
        # Start Step 2 : RUN MODEL
        command = "%s %s 3 %s %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, os.path.join(INPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_in.txt"), os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt"))
        os.system(command)
        # Start Step 3 : Read data from output of Roseta Model
        output_file = os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt")
        with open(output_file, 'r') as file:
            data = file.readlines()
        if (len(data) > 9):
            sys.exit("==[Error] : Output data %s is NOT correct" % (output_file))
            
        for j in range(0, NUMBER_LAYERS_SOL_FILE):
            line_current = data[j + 2]
            ######Process Current Line
            line_current = standard_string(line_current)
            data_current = line_current.split(' ')
            str_theta_r_current = data_current[2].strip()
            str_theta_s_current = data_current[3].strip()
            str_theta_alpha_current = data_current[4].strip()
            str_n_par_current = data_current[5].strip()
            str_K_s_current = data_current[6].strip()
            str_K_o_current = data_current[7].strip()
            str_L_current = data_current[8].strip()
        
            ######Check data
            if (float(str_theta_r_current) and float(str_theta_s_current) and float(str_theta_alpha_current) and float(str_n_par_current) and float(str_K_s_current) and float(str_K_o_current) and float(str_L_current)):
               fl_theta_r_current = float(str_theta_r_current)
               fl_theta_s_current = float(str_theta_s_current)
               fl_theta_alpha_current = float(str_theta_alpha_current)
               fl_n_par_current = float(str_n_par_current)
               fl_K_s_current = float(str_K_s_current)
               fl_K_o_current = float(str_K_o_current)
               fl_L_currnet = float(str_L_current)
            else:
               sys.exit("===[Error] : Data from output file is not correct")
            #####Calculate
            if (fl_theta_r_current != -9.9 and fl_theta_s_current != -9.9 and fl_theta_alpha_current != -9.9 and fl_n_par_current != -9.9 and fl_K_s_current != -9.9 and fl_K_o_current != -9.9 and fl_L_currnet != -9.9):
                if (str_theta_r_current is not None and str_theta_r_current != "-9.90000" and str_theta_s_current is not None and str_theta_s_current != "-9.90000" and str_theta_alpha_current is not None and str_theta_alpha_current != "-9.90000" and str_n_par_current is not None and str_n_par_current != "-9.90000" and str_K_s_current is not None and str_K_s_current != "-9.90000" and str_K_o_current is not None and str_K_o_current != "-9.90000" and str_L_current is not None and str_L_current != "-9.90000"):    
                    SAT_HY_COND_LIST[j] = calculate_Saturated_Hydraulic_Conductivity(fl_K_s_current)
                    FIELD_CAPACITY_LIST[j] = calculate_Field_Capacity(fl_theta_r_current, fl_theta_s_current, fl_theta_alpha_current, fl_n_par_current)
                    WILTING_POINT_LIST[j] = calculate_Wilting_Point(fl_theta_r_current, fl_theta_s_current, fl_theta_alpha_current, fl_n_par_current)
        
        BIG_LIST_CAL = [SAT_HY_COND_LIST, FIELD_CAPACITY_LIST, WILTING_POINT_LIST]
        print BIG_LIST_CAL
        return BIG_LIST_CAL
    except Exception, err:
        sys.exit(err)
def calculate_Saturated_Hydraulic_Conductivity(input_float_Ks_rosetta):
    return (float(input_float_Ks_rosetta) * 10) / 24
    
def calculate_Field_Capacity(float_theta_r, float_theta_s, float_alpha, float_n_par):
    try:
        import math
        sh1 = float_theta_r
        
        tu1 = float_theta_s - float_theta_r
        pt1 = (1 + math.pow((float_alpha * 330), float_n_par))
        pt2 = 1 - (1 / float_n_par)
        mau1 = math.pow(pt1, pt2)
        
        sh2 = tu1 / mau1
        
        return sh1 + sh2
    except Exception, err:
        print err
        return 0
def calculate_Wilting_Point(float_theta_r, float_theta_s, float_alpha, float_n_par):
    try:
        import math
        sh1 = float_theta_r
        
        tu1 = float_theta_s - float_theta_r
        pt1 = (1 + math.pow((float_alpha * 15000), float_n_par))
        pt2 = 1 - (1 / float_n_par)
        mau1 = math.pow(pt1, pt2)
        
        sh2 = tu1 / mau1
        
        return sh1 + sh2
    except Exception, err:
        print err
        return 0

def standard_string(line):
    line = line.strip()
    line = line.replace("         ", " ")
    line = line.replace("        ", " ")
    line = line.replace("       ", " ")
    line = line.replace("      ", " ")
    line = line.replace("     ", " ")
    line = line.replace("    ", " ")
    line = line.replace("   ", " ")
    line = line.replace("  ", " ")
    return line

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))
def length(v):
  return math.sqrt(dotproduct(v, v))
def angle(v1, v2):
  return (dotproduct(v1, v2) / (length(v1) * length(v2)))
    
def main():
    checkAndCreateFolder()
    print("-PREPROCESSING :")
    folder_name = prepareDistinguish_Input_Output_Folder_PerEachProcess()
    OUTPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Output\%s" % str(folder_name)
    INPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Input\%s" % str(folder_name)
    if (not os.path.exists(OUTPUT_ROSETTA_MODEL_FILE_PATH)):
        sys.exit("===Particular Output Folder of Rosetta Model is NOT created")
    if (not os.path.exists(INPUT_ROSETTA_MODEL_FILE_PATH)):
        sys.exit("===Particular Output Folder of Rosetta Model is NOT created")
    
    print("---Real Rosetta Model Application File is %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION))
    print("-START Step 1:")
    result = queryIDfollow_MU_GLOBAL()
    intRecord = recordsDATFile(result)
    if (intRecord == 1):
        print("-DONE Step 1---")
    else:
        print("----Problems----")
   
    print("-START Step 2 :")
    ####THANH NGUYEN : BAT DAU SUA TU DAY
    TEXTURE_SOIL_LAYER = support_SOIL.get_values_texture_for_soil_horizon(ID)
    ROCK_FRAGMENT_LIST = support_SOIL.get_list_value_of_rock_fragment(ID)
    if (TEXTURE_SOIL_LAYER is None):
        sys.exit("====[ERROR 303] : Cannot find any data about Soil Layer Texture]")
    if (ROCK_FRAGMENT_LIST is None):
        ROCK_FRAGMENT_LIST = [0,0,0,0,0,0]
    BIG_LIST = support_SOIL.get_collection_value_from_all_layer_texture(TEXTURE_SOIL_LAYER)
    if (BIG_LIST is None):
        sys.exit("====[ERROR 304] : Cannot find any data about Soil Layer Texture]")
    else:
        SAND_LIST = BIG_LIST[0]
        SILT_LIST = BIG_LIST[1]
        CLAY_LIST = BIG_LIST[2]
        BULK_DENSITY_LIST = BIG_LIST[3]
        TOT_C_LIST = [-9.9, -9.9, -9.9, -9.9, -9.9, -9.9, -9.9]
        W3CLD_LIST = [-9.9, -9.9, -9.9, -9.9, -9.9, -9.9, -9.9]
        W15AD_LIST = [-9.9, -9.9, -9.9, -9.9, -9.9, -9.9, -9.9]
    
    
    try:
        csvfile = open(PRIVATE_FOLDER_ACCESS_SIMILARITY_FILE, 'wb')
        out = UnicodeWriter(csvfile)
        out.writerow(['sol_file', 'ui_sand_l_1', 'ui_sand_l_2','ui_sand_l_3','ui_sand_l_4','ui_sand_l_5','ui_sand_l_6','ui_sand_l_7','av_sand_1_2_3_4','av_sand_5_6_7','t_sand_hwsd','s_sand_hwsd','ui_silt_l_1', 'ui_silt_l_2','ui_silt_l_3','ui_silt_l_4','ui_silt_l_5','ui_silt_l_6','ui_silt_l_7','av_silt_1_2_3_4','av_silt_5_6_7','t_silt_hwsd','s_silt_hwsd','cosin_similarity'])
        for item in result:
            if (item is None):
                continue
            else :
                if (item[0] is None):
                    continue
                else:
                    wise3_id = item[0]
                    soilResult = querySoilPropertyFollowWise3_ID(wise3_id)
                    for item2 in soilResult:
                        print item2
                        for i in range(0, len(item2) - 1):
                            if (item2[i] is None):
                                item2[i] = 0
                        name_sol = str(item[0]) + str(mu_global) + str(item[1]) + str(item[3])
                        output_model_value = []
                        output_model_value = acessModelToGetValue(item[0], FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, INPUT_ROSETTA_MODEL_FILE_PATH, OUTPUT_ROSETTA_MODEL_FILE_PATH, SAND_LIST, SILT_LIST, CLAY_LIST, BULK_DENSITY_LIST, TOT_C_LIST, W3CLD_LIST, W15AD_LIST)
                        SAT_HY_COND_LIST_FULL = output_model_value[0]
                        FIELD_CAPACITY_LIST_FULL = output_model_value[1]
                        WILITING_POINT_LIST_FULL = output_model_value[2]
                        
                        #Update_ThanhNH_20150114 : Truy van data tu SOIL GRID
                        SOIL_GRIDS_VALUE_LIST = support_SOIL.select_isric_soilgrids_soil_modified_data(ID)
                        if SOIL_GRIDS_VALUE_LIST is None :
                            if (NUMBER_LAYERS_SOL_FILE == 7 or NUMBER_LAYERS_SOL_FILE is None):
                                createSOILFile_V2(wise3_id, name_sol, SAND_LIST, SILT_LIST , item2[7], item2[8], item2[9], item2[10], item2[11], item2[12], item2[13], item2[14], ROCK_FRAGMENT_LIST, item2[17], item2[18], item2[19], item2[20], WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL)
                            else:
                                createSOILFile_V2_Depend_Number_Of_Layers(wise3_id, name_sol, SAND_LIST, SILT_LIST , item2[7], item2[8], item2[9], item2[10], item2[11], item2[12], item2[13], item2[14], ROCK_FRAGMENT_LIST, item2[17], item2[18], item2[19], item2[20], WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL)
                        else:
                            print "RUN ISRIC SOIL GRIDS =========== !!!!!!!!!!!!!!!!! \n"
                            ORCDRC_MAPPING_LIST = SOIL_GRIDS_VALUE_LIST[0]
                            PHIHOX_MAPPING_LIST = SOIL_GRIDS_VALUE_LIST[1]
                            BLD_MAPPING_LIST = SOIL_GRIDS_VALUE_LIST[2]
                            CEC_MAPPING_LIST = SOIL_GRIDS_VALUE_LIST[3]
                            createSOILFile_V2_Depend_Number_Of_Layers_SOIL_GRIDS_ISRIC(wise3_id, name_sol, SAND_LIST, SILT_LIST , item2[7], item2[8], item2[9], item2[10], item2[11], item2[12], item2[13], item2[14], ROCK_FRAGMENT_LIST, item2[17], item2[18], item2[19], item2[20], WILITING_POINT_LIST_FULL, FIELD_CAPACITY_LIST_FULL, SAT_HY_COND_LIST_FULL,ORCDRC_MAPPING_LIST,PHIHOX_MAPPING_LIST,BLD_MAPPING_LIST,CEC_MAPPING_LIST)    
                        #End Update
                        
                        
                            
                        try:
                            avg_sand_1_2_3_4 = (float(SAND_LIST[0] + SAND_LIST[1] + SAND_LIST[2] + SAND_LIST[3])) / 4
                            avg_sand_5_6_7 = (float(SAND_LIST[4] + SAND_LIST[5] + SAND_LIST[6])) / 3
                            avg_silt_1_2_3_4 = (float(SILT_LIST[0] + SILT_LIST[1] + SILT_LIST[2] + SILT_LIST[3])) / 4
                            avg_silt_5_6_7 = (float(SILT_LIST[4] + SILT_LIST[5] + SILT_LIST[6])) / 3
                            HWSD_VECTOR = [item2[3],item2[4],item2[5],item2[6]]
                            USER_INPUT_VECTOR = [avg_sand_1_2_3_4,avg_sand_5_6_7,avg_silt_1_2_3_4,avg_silt_5_6_7]
                            cosin_angle_2_vectors = angle(HWSD_VECTOR,USER_INPUT_VECTOR)
                        except:
                            avg_sand_1_2_3_4 = 0
                            avg_sand_5_6_7 = 0
                            avg_silt_1_2_3_4 = 0
                            avg_silt_5_6_7 = 0
                        out.writerow([name_sol, str(SAND_LIST[0]), str(SAND_LIST[1]),str(SAND_LIST[2]),str(SAND_LIST[3]),str(SAND_LIST[4]),str(SAND_LIST[5]),str(SAND_LIST[6]),str(avg_sand_1_2_3_4),str(avg_sand_5_6_7),str(item2[3]), str(item2[4]),str(SILT_LIST[0]), str(SILT_LIST[1]),str(SILT_LIST[2]),str(SILT_LIST[3]),str(SILT_LIST[4]),str(SILT_LIST[5]),str(SILT_LIST[6]),str(avg_silt_1_2_3_4),str(avg_silt_5_6_7),str(item2[5]), str(item2[6]), str(cosin_angle_2_vectors)])
    except Exception, err:
        print err
    #####THANH NGUYEN : Ket thuc sua o day    
    print("-DONE Step 2 :")
    print("-DAT File is located in %s" % (full_path + "Result" + "\\" + "DATFiles\<MU_GLOBAL>"))
    print("-SOL Files are located in %s" % (full_path + "Result" + "\\" + "SOLFiles\<MU_GLOBAL>"))
    print("-DELETE Temp Input Folder and Output Folder Rosetta Model")
    if (os.path.exists(INPUT_ROSETTA_MODEL_FILE_PATH)):
        try:
            shutil.rmtree(INPUT_ROSETTA_MODEL_FILE_PATH)
        except OSError:
            pass
    if (os.path.exists(OUTPUT_ROSETTA_MODEL_FILE_PATH)):
        try:
            shutil.rmtree(OUTPUT_ROSETTA_MODEL_FILE_PATH)
        except OSError:
            pass
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
