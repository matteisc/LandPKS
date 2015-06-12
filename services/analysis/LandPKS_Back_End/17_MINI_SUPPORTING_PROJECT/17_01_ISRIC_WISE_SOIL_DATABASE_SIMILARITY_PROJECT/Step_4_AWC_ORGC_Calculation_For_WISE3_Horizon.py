
__version__ = "1"

import struct, os, csv, codecs, cStringIO, sys
import shutil
from __builtin__ import str, len
from __builtin__ import int
import datetime
import time
from support import support_SIMILARITY

# Server AWC Running
FULL_PATH_ROSETTA_APPLICATION = ""
EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION = "rosetta.exe"
FULL_PATH_RUNABLE_ROSETTA_APPLICATION = ""
FULL_PATH_WEIGHTS_FOLDER_ROSETTA = ""
OUTPUT_ROSETTA_MODEL_FILE_PATH = ""
INPUT_ROSETTA_MODEL_FILE_PATH = ""
full_path = os.getcwd() + "\\"
NUMBER_LAYERS_SOL_FILE = 7
LAYER_1 = [0,1]
LAYER_2 = [1,10]
LAYER_3 = [10,20]
LAYER_4 = [20,50]
LAYER_5 = [50,70]
LAYER_6 = [70,100]
LAYER_7 = [100,120]
ID = 0
# End AWC Running
WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\ISRIC_WISE_DATABASE\\WISE3_HORIZON.csv"
WISE3_LANDPKS_OUTPUT_CSV_AWC_ORGC_CALCULATION = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_HORIZON_AWC_ORGC_DATA.csv"

mess = "Usage : Step_4_AWC_ORGC_Calculation_For_WISE3_Horizon.py -input_wise3_horizon_csv <Full Path to Input> -output_wise3_landpks_awc_orgc_csv <Full Path to Output> -model <Path to folder of Rosetta model>"
if (len(sys.argv) < 8):
    print("\n Using default value \n WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA = %s" %(WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA))
    print("\n Using default value \n WISE3_LANDPKS_OUTPUT_CSV_AWC_ORGC_CALCULATION = %s" %(WISE3_LANDPKS_OUTPUT_CSV_AWC_ORGC_CALCULATION))
    
    if (not os.path.exists("C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\Rosetta_Model_Application\\Rosetta\\")):
        sys.exit("==[Error] : Folder contains Rosetta Model is NOT Existed")
    else:
        FULL_PATH_ROSETTA_APPLICATION = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\Rosetta_Model_Application\\Rosetta\\" 
        FULL_PATH_RUNABLE_ROSETTA_APPLICATION = os.path.join(FULL_PATH_ROSETTA_APPLICATION, EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION)
        FULL_PATH_WEIGHTS_FOLDER_ROSETTA = os.path.join(FULL_PATH_ROSETTA_APPLICATION, "weights")
        print("\n---[Done] : Rosetta Model Application is in Folder %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION)) 
else:

    if (sys.argv[1] == '-input_wise3_horizon_csv'):
        if (sys.argv[2] is not None):
            WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
    if (sys.argv[3] == '-output_wise3_landpks_awc_orgc_csv'):
        if (sys.argv[4] is not None):
            WISE3_LANDPKS_OUTPUT_CSV_AWC_ORGC_CALCULATION = sys.argv[4].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
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
            sys.exit("====[Error] : No defined Model")    
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
def prepareDistinguish_Input_Output_Folder_PerEachProcess(folder_name):
    #current = time.time()
    output_direction = full_path + "\Rosetta_Model_Application\Output\%s" % str(folder_name)
    if not os.path.exists(output_direction):
        os.makedirs(output_direction)
    input_direction = full_path + "\Rosetta_Model_Application\Input\%s" % str(folder_name)
    if not os.path.exists(input_direction):
        os.makedirs(input_direction)
    return str(folder_name)
def acessModelToGetValue_Wise(seq,NUMBER_LAYER,TOP_DEP,BOT_DEP,FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, INPUT_ROSETTA_MODEL_FILE_PATH, OUTPUT_ROSETTA_MODEL_FILE_PATH, SAND_LIST, SILT_LIST, CLAY_LIST, BULK_DENSITY_LIST, TOT_C_LIST, W3CLD_LIST, W15AD_LIST):
    values = []
    
    SAT_HY_COND_LIST = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
    FIELD_CAPACITY_LIST = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
    WILTING_POINT_LIST = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
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
        for j in range(0, NUMBER_LAYER):
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
            top_dep = TOP_DEP[j] / 100
            bot_dep = BOT_DEP[j] / 100
            if (j >= 0):
                # Process hz_tp
                strContent = strContent + "     %0.2f" %(top_dep)
                # Process hz_bt
                strContent = strContent + "     %0.2f" %(bot_dep)
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
        command = "%s %s 2 %s %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, os.path.join(INPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_in.txt"), os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt"))
        os.system(command)
        # Start Step 3 : Read data from output of Roseta Model
        output_file = os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt")
        with open(output_file, 'r') as file:
            data = file.readlines()
        #if (len(data) > 9):
        #    sys.exit("==[Error] : Output data %s is NOT correct" % (output_file))
            
        for j in range(0, NUMBER_LAYER):
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
                else:
                    SAT_HY_COND_LIST[j] = -999
                    FIELD_CAPACITY_LIST[j] = -999
                    WILTING_POINT_LIST[j] = -999
        
        BIG_LIST_CAL = [SAT_HY_COND_LIST, FIELD_CAPACITY_LIST, WILTING_POINT_LIST]
        print BIG_LIST_CAL
        return BIG_LIST_CAL
    except Exception, err:
        sys.exit(err)
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
def read_Soil_Data_From_Wise3_Horizon_File(in_csv):
    WISE_HORIZON_RECORD = []
    WISE_HORIZON_DATA_LIST_RECORD = []
    WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD = []
    try:
       f = open(in_csv, "rb")
       l = UnicodeReader(f)
       l.next()
       consider_id = "" 
       for row in l:
           WISE3_ID = str(row[0]).upper()
           WISE3_honu = str(row[1]).upper().strip()
           if (str(row[3]).strip() is not None and str(row[3]).strip() != ""):
                   WISE3_topdep = float(row[3])
           else:
                   WISE3_topdep = float(0)
           if (str(row[4]).strip() is not None and str(row[4]).strip() != ""):
                   WISE3_botdep = float(row[4])
           else:        
                   WISE3_botdep = float(0)
           if (str(row[7]).strip() is not None and str(row[7]).strip() != ""):
                   WISE3_orgc = float(row[7])
           else:
                   WISE3_orgc = float(-9.9)
           if (str(row[23]).strip() is not None and str(row[23]).strip() != ""):
                   WISE3_sand = float(row[23])
           else:
                   WISE3_sand = float(-9.9)
           if (str(row[24]).strip() is not None and str(row[24]).strip() != ""):
                   WISE3_silt = float(row[24])
           else:
                   WISE3_silt = float(-9.9)
           if (str(row[25]).strip() is not None and str(row[25]).strip() != ""):
                   WISE3_clay = float(row[25])
           else:
                   WISE3_clay = float(-9.9)    
            
           if (str(row[27]).strip() is not None and str(row[27]).strip() != ""):
                   WISE3_bulkdens = float(row[27])
           else:
                   WISE3_bulkdens = float(-9.9)
                   
                   
           if (WISE3_ID != consider_id):
               if (WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD is not None and len(WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD) > 0):
                   WISE_HORIZON_DATA_LIST_RECORD.append(WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD)
               WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD = []
               consider_id = WISE3_ID
               WISE_HORIZON_RECORD = [WISE3_ID,WISE3_honu,WISE3_topdep,WISE3_botdep,WISE3_orgc,WISE3_sand,WISE3_silt,WISE3_clay,WISE3_bulkdens]
               WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD.append(WISE_HORIZON_RECORD)
           else:
               WISE_HORIZON_RECORD = [WISE3_ID,WISE3_honu,WISE3_topdep,WISE3_botdep,WISE3_orgc,WISE3_sand,WISE3_silt,WISE3_clay,WISE3_bulkdens]
               WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD.append(WISE_HORIZON_RECORD)
         
       if (WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD is not None and len(WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD) > 0):
           WISE_HORIZON_DATA_LIST_RECORD.append(WISE_HORIZON_DATA_LIST_LAYER_BY_RECORD)
       return  WISE_HORIZON_DATA_LIST_RECORD   
    except Exception, err:
       print err
       return -1
def print_test_data(out_csv,list_records):
    #Standard data before
    out_csvfile = open(out_csv, 'wb')
    out = UnicodeWriter(out_csvfile)
    out.writerow(['WISE3_ID', 'HONU', 'TOP_DEP', 'BOT_DEP', 'ORGC', 'SAND', 'SILT','CLAY','BULK_DENS','ORIGINAL_AWC','CENTIMETER_AWC','SOIL_PROFILE_AWC','ORGC_I_Layer','ORGC_I_RECORD'])
    ID = ""
    for list_layer in list_records:
        out.writerow(["Consider ID : " + list_layer[0][0]])
        for record in list_layer:
            if (record[0] != ID):
                ID = record[0]
                out.writerow([record[0], str(record[1]), str(record[2]), str(record[3]), str(record[4]), str(record[5]), str(record[6]),str(record[7]),str(record[8]),str(record[9]),str(record[10]),str(record[11]),str(record[12]),str(record[13])])
            else:
                out.writerow([record[0], str(record[1]), str(record[2]), str(record[3]), str(record[4]), str(record[5]), str(record[6]),str(record[7]),str(record[8]),str(record[9]),str(record[10]),"",str(record[12]),""])
def print_result_data_after_calculation(out_csv,list_records):
    #Standard data before
    out_csvfile = open(out_csv, 'wb')
    out = UnicodeWriter(out_csvfile)
    out.writerow(['WISE3_ID', 'HONU', 'TOP_DEP', 'BOT_DEP', 'ORGC', 'SAND', 'SILT','CLAY','BULK_DENS','ORIGINAL_AWC','CENTIMETER_AWC','SOIL_PROFILE_AWC','ORGC_I_Layer','ORGC_I_RECORD'])
    ID = ""
    for list_layer in list_records:
        for record in list_layer:
            #if (record[0] != ID):
                ID = record[0]
                out.writerow([record[0], str(record[1]), str(record[2]), str(record[3]), str(record[4]), str(record[5]), str(record[6]),str(record[7]),str(record[8]),str(record[9]),str(record[10]),str(record[11]),str(record[12]),str(record[13])])
            #else:
            #    out.writerow([record[0], str(record[1]), str(record[2]), str(record[3]), str(record[4]), str(record[5]), str(record[6]),str(record[7]),str(record[8]),str(record[9]),str(record[10]),"",str(record[12]),""])  
def calculate_AWC_data(WISE_HORIZON_DATA_LIST_RECORD):
    try:
        seq = 0
        for LIST_LAYER in WISE_HORIZON_DATA_LIST_RECORD:
             folder_name = LIST_LAYER[0][0]
             print "Consider " + folder_name
             folder_name = prepareDistinguish_Input_Output_Folder_PerEachProcess(folder_name)
             OUTPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Output\%s" % str(folder_name)
             INPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Input\%s" % str(folder_name)
             output_model_value = []
             seq = seq + 1
             NUMBER_LAYER = len(LIST_LAYER)
             TOP_DEP = []
             BOT_DEP = []
             SAND_LIST = []
             SILT_LIST = []
             CLAY_LIST = []
             BULK_DENSITY_LIST = []
             TOT_C_LIST = []
             W3CLD_LIST = []
             W15AD_LIST = []
             ORGC_LIST = []
             for soil_record in LIST_LAYER:
                 TOP_DEP.append(soil_record[2])
                 BOT_DEP.append(soil_record[3])
                 ORGC_LIST.append(soil_record[4])
                 SAND_LIST.append(soil_record[5])
                 SILT_LIST.append(soil_record[6])
                 CLAY_LIST.append(soil_record[7])
                 BULK_DENSITY_LIST.append(soil_record[8])
                 TOT_C_LIST.append(-9.9)
                 W3CLD_LIST.append(-9.9)
                 W15AD_LIST.append(-9.9)
             output_model_value = acessModelToGetValue_Wise(seq,NUMBER_LAYER,TOP_DEP,BOT_DEP,FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, INPUT_ROSETTA_MODEL_FILE_PATH, OUTPUT_ROSETTA_MODEL_FILE_PATH, SAND_LIST, SILT_LIST, CLAY_LIST, BULK_DENSITY_LIST, TOT_C_LIST, W3CLD_LIST, W15AD_LIST)
             FIELD_CAPACITY_LIST = output_model_value[1]
             WILTING_POINT_LIST = output_model_value[2]
             EXAMPLE_AWC = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
             CENTIMES_AWC = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
             ORGC_LIST_I_LAYER = [-999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999, -999]
             soil_profile_awc = 0
             organic_carbon_record = 0
             for i in range(0, NUMBER_LAYER):
                 if (FIELD_CAPACITY_LIST[i] != -999 and FIELD_CAPACITY_LIST[i] != "-999" and WILTING_POINT_LIST[i] != "-999" and WILTING_POINT_LIST[i] != -999):
                     EXAMPLE_AWC[i] = FIELD_CAPACITY_LIST[i] - WILTING_POINT_LIST[i]
                     LIST_LAYER[i].append(EXAMPLE_AWC[i])
                     if (BOT_DEP[i] <= 120 and TOP_DEP[i] <= 120 and BOT_DEP[i] > TOP_DEP[i]):
                         CENTIMES_AWC[i] = (BOT_DEP[i] - TOP_DEP[i])*EXAMPLE_AWC[i]
                     elif (BOT_DEP[i] > 120 and TOP_DEP[i] <= 120):
                         BOT_DEP[i] = 120
                         CENTIMES_AWC[i] = (BOT_DEP[i] - TOP_DEP[i])*EXAMPLE_AWC[i]
                     elif (BOT_DEP[i] > 120 and TOP_DEP[i] > 120):
                         BOT_DEP[i] = 120
                         TOP_DEP[i] = 120
                         CENTIMES_AWC[i] = (BOT_DEP[i] - TOP_DEP[i])*EXAMPLE_AWC[i]
                     else:
                         CENTIMES_AWC[i] = -999
                     LIST_LAYER[i].append(CENTIMES_AWC[i])
                     soil_profile_awc = float(soil_profile_awc) + CENTIMES_AWC[i]
                 else:
                     LIST_LAYER[i].append(-999)
                     LIST_LAYER[i].append(-999)
                     
             for i in range(0, NUMBER_LAYER):
                 LIST_LAYER[i].append(soil_profile_awc)

             for i in range(0, NUMBER_LAYER):
                 if (ORGC_LIST[i] is not None and ORGC_LIST[i] != "" and ORGC_LIST[i] != -9.9 and ORGC_LIST[i] != "-9.9"):
                     ORGC_LIST_I_LAYER[i] = ((BOT_DEP[i] - TOP_DEP[i]) / 120)*ORGC_LIST[i]
                     LIST_LAYER[i].append(ORGC_LIST_I_LAYER[i])
                     organic_carbon_record = float(organic_carbon_record) + ORGC_LIST_I_LAYER[i]
                 else:
                     LIST_LAYER[i].append(-999)
                     
             for i in range(0, NUMBER_LAYER):
                 LIST_LAYER[i].append(organic_carbon_record)
                         
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
        return WISE_HORIZON_DATA_LIST_RECORD
    except Exception, err:
       print err
       return -1
def main():
    WISE_HORIZON_DATA_LIST_RECORD = []
    # Check source data
    if (not os.path.exists(WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA)):
        print "==Error 405 : File WISE3_HORIZON.csv was not existed==="
        sys.exit()
    if (not os.path.exists(FULL_PATH_RUNABLE_ROSETTA_APPLICATION)):
        print "==Error 404 : Rosetta Model was not existed==="
        sys.exit()
    if (not os.path.exists(FULL_PATH_WEIGHTS_FOLDER_ROSETTA)):
        print "==Error 401 : Rosetta Weoghts was not existed==="
        sys.exit() 
    
    print "=== Step 1 : Read Soil Data from WISE3_HORIZON ==="
    WISE_HORIZON_DATA_LIST_RECORD = read_Soil_Data_From_Wise3_Horizon_File(WISE3_LANDPKS_INTPUT_CSV_HORIZON_DATA)
    if (WISE_HORIZON_DATA_LIST_RECORD == -1):
        sys.exit("==Error 300 : Something wrongs===")
    print "=== Step 2 : Calculate AWC Data. Update to List ==="
    WISE_HORIZON_DATA_LIST_RECORD = calculate_AWC_data(WISE_HORIZON_DATA_LIST_RECORD)
    
    #Test data 
    #print_test_data("C:\\xampp\\htdocs\\APEX\\Python_APEX\\17_MINI_SUPPORTING_PROJECT\\17_01_ISRIC_WISE_SOIL_DATABASE_SIMILARITY_PROJECT\\LANDPKS_WISE_DATA\\WISE3_LANDPKS_HORIZON_AWC_ORGC_CALCULATION.csv", WISE_HORIZON_DATA_LIST_RECORD)
    print "=== Step 3 : Export all calculated data to File in  ==="
    print_result_data_after_calculation(WISE3_LANDPKS_OUTPUT_CSV_AWC_ORGC_CALCULATION, WISE_HORIZON_DATA_LIST_RECORD)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
