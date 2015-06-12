# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import struct, os, csv, codecs, cStringIO, sys
import urllib2
from urllib2 import Request
from support import support_Apex_Sensitivity
import time
from __builtin__ import len
RECORD_NAME = ""

APEX_OUT_FILE_FOLDER = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\0_APEX_RUNTIME_MODEL\\Private\\"
tif_HWSD = 'soil_texture/HWSD_soil.tif'
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'
TIF_FOLDER = 'E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/'
APEX_TYPE = ""
mess = "Usage : python Run_main_Apex_Sensitivity_Analysis.py -recorder_name <Record Name want to collect data>"
if (len(sys.argv) < 4):
    print("Sorry, not enough arguments")
    sys.exit(mess)
else:
    if (sys.argv[1] == '-recorder_name'):
        if (sys.argv[2] is not None):
            RECORD_NAME = sys.argv[2].strip()
        else:
            sys.exit(mess)
        
        if (sys.argv[3] == '-type'):
            APEX_TYPE = sys.argv[4].upper()
            if (APEX_TYPE <> 'M' and APEX_TYPE <> 'G'):
                sys.exit(mess)
        else:
            sys.exit(mess)    
    else:
        sys.exit(mess)
        
FILE_NAME = int(round(time.time() * 1000))
PRIVATE_FOLDER_RESULT_CSV_FILE = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\11_APEX_SENSITIVITY_ANALYSIS\\Result\\%s.csv" % (str(FILE_NAME))

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
def checking_key(key, value):
    key = key.strip()
    key = key.upper()
    key = key.replace("_","")
    key = key.replace("-","")
    key = key.strip()
    if (key == value):
        return 1
    else:
        return 0
def find_data_2(data,key):
    try:
        intLength = len(data)
        for i in range(0, intLength-3):
            line = data[i]
            if (line is None or len(line) < 40):
                continue
            line = line[0:40]
            if (checking_key(line, key) == 1):
                return [line,i]
        return None
    except Exception, err:
        print err
        pass
def find_data(data, key):
    try:
        intLength = len(data)
        for i in range(0, intLength-3):
            line = data[i]
            #line = support_Apex_Sensitivity.standard_string(line)
            if (line is None or line == ""):
                continue
            if (checking_key(line, key) == 1):
                #print "Da phat hien : " + str(line) + " : " + str(i)
                return [line,i]
        return None
    except Exception, err:
        print err
        pass
def check_data_soil(data,key,index):
    value = data[index]
    
    value = value.strip()
    value = value.upper()
    if (value==key):
        return 1
    else:
        return 0
def check_data(data,key):
    value = data[0]
    value = value.strip()
    value = value.upper()
    if (value==key):
        return 1
    else:
        return 0
def find_line_data_fit(data,begin,end,key):
    for i in range(begin,end):
        line = data[i]
        line = support_Apex_Sensitivity.standard_string(line)
        data_con = line.split(" ")
        if (checking_key(data_con[1], key)):
            return line
    return None
         
def get_subarea_fields(SUBAREA_FILE_LOCAL):
    try:
        line_2 = ""
        line_3 = ""
        with open(SUBAREA_FILE_LOCAL, 'r') as file:
            data = file.readlines()
        
        line_2 = data[2]
        line_3 = data[3]
       
        line_2 = support_Apex_Sensitivity.standard_string(line_2)
        line_3 = support_Apex_Sensitivity.standard_string(line_3)
        
        data_line_2 = line_2.split(" ")
        data_line_3 = line_3.split(" ")

        aspect_value = data_line_2[4]
        slope_value = data_line_3[5]
    
        print aspect_value
        print slope_value    
        return [aspect_value,slope_value]
    except Exception, err:
        print err
        return [0,0]   
def get_soil_chemical_fields(APEX_OUT_FILE_LOCAL):
    line_10_ph_org = ""
    line_50_ph_org = ""
    line_100_ph_org= ""
    with open(APEX_OUT_FILE_LOCAL, 'r') as file:
        data = file.readlines()
    
    if (APEX_TYPE == 'G'):    
        consider_index_line = 275
    elif (APEX_TYPE == 'M'):
        consider_index_line = 381
    else:
        consider_index_line = 275
        
    line_checking = data[consider_index_line]
    if (checking_key(line_checking, "SOIL CHEMICAL DATA") == 1 and len(data) >= 400):
       print "===[Good] : Find line contain data Soil Chemical fast => Read immediately" 
       #line_10_ph_org = data[consider_index_line + 6]
       line_10_ph_org = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.10")
       #line_50_ph_org = data[consider_index_line + 11]
       line_50_ph_org = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.50")
       #line_100_ph_org = data[consider_index_line + 13]
       line_100_ph_org = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "1.00")
       line_root =  data[consider_index_line + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line)
       [line_checking,index] = find_data(data, "SOIL CHEMICAL DATA")
       if (checking_key(line_checking, "SOIL CHEMICAL DATA") == 1):
           print "===Retry to find data" 
           #line_10_ph_org = data[index + 6]
           #line_50_ph_org = data[index + 11]
           #line_100_ph_org = data[index + 13]
           line_10_ph_org = find_line_data_fit(data, index + 4, index + 15, "0.10")
           line_50_ph_org = find_line_data_fit(data, index + 4, index + 15, "0.50")
           line_100_ph_org = find_line_data_fit(data, index + 4, index + 15, "1.00")
           line_root =  data[index + 3]
       else:
           sys.exit("Error : Please check output data file. System cannot find Soil Data")    
    
    
    line_root = support_Apex_Sensitivity.standard_string(line_root)
    data_root = line_root.split(" ")
    
    if (line_10_ph_org is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Chemical")
        value_ph_10 = 0.0
        value_org_10 = 0.0
        value_cec_10 = 0.0
    else:
        line_10_ph_org = support_Apex_Sensitivity.standard_string(line_10_ph_org)
        print "==10 Ph ORG : " + line_10_ph_org + "\n"
        data_10_ph_org = line_10_ph_org.split(" ")
        if (check_data_soil(data_root,"PH",2) == 1):
            value_ph_10 = data_10_ph_org[2]
            value_org_10 = data_10_ph_org[14]
            value_cec_10 = data_10_ph_org[4]
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Chemical====")
        print "=============Ph , ORG C 10, CEC 10  : %s , %s, %s" %(str(value_ph_10), str(value_org_10), str(value_cec_10))
    
    
    if (line_50_ph_org is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Chemical")
        value_ph_50 = 0.0
        value_org_50 = 0.0
        value_cec_50 = 0.0
    else:
        line_50_ph_org = support_Apex_Sensitivity.standard_string(line_50_ph_org)
        print "==50 Ph ORG : " + line_50_ph_org + "\n"
        data_50_ph_org = line_50_ph_org.split(" ")
        if (check_data_soil(data_root,"PH",2) == 1):
            value_ph_50 = data_50_ph_org[2]
            value_org_50 = data_50_ph_org[14]
            value_cec_50 = data_50_ph_org[4]
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Chemical====")
        print "=============Ph , ORG C , CEC 50  : %s , %s , %s" %(str(value_ph_50), str(value_org_50), str(value_cec_50))       
    
    if (line_100_ph_org is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Chemical")
        value_ph_100 = 0.0
        value_org_100 = 0.0
        value_cec_100 = 0.0
    else:
        line_100_ph_org = support_Apex_Sensitivity.standard_string(line_100_ph_org)
        print "==100 Ph ORG : " + line_100_ph_org + "\n"
        data_100_ph_org = line_100_ph_org.split(" ")
        if (check_data_soil(data_root,"PH",2) == 1):
            value_ph_100 = data_100_ph_org[2]
            value_org_100 = data_100_ph_org[14]
            value_cec_100 = data_100_ph_org[4]
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Chemical====")
        print "=============Ph , ORG C , CEC 100  : %s , %s , %s" %(str(value_ph_100), str(value_org_100), str(value_cec_100))
    return [value_ph_10, value_org_10, value_ph_50, value_org_50, value_ph_100, value_org_100, value_cec_10, value_cec_50, value_cec_100]     


def get_soil_data_fields(APEX_OUT_FILE_LOCAL):
    line_10_sand_clay = ""
    line_10_ph_org = ""
    line_50_sand_clay = ""
    line_50_ph_org = ""
    line_100_sand_clay = ""
    line_100_ph_org= ""
    
    #Additional data
    line_1_data = ""
    line_15_data = ""
    line_20_data = ""
    line_28_data = ""
    line_35_data = ""
    line_43_data = ""
    line_70_data = ""
    line_120_data = ""
    
    with open(APEX_OUT_FILE_LOCAL, 'r') as file:
        data = file.readlines()
    
    if (APEX_TYPE == 'G'):    
        consider_index_line = 245
    elif (APEX_TYPE == 'M'):
        consider_index_line = 351
    else:
        consider_index_line = 245
        
    line_checking = data[consider_index_line]
    if (checking_key(line_checking, "SOIL PHYSICAL DATA") == 1 and len(data) >= 400):
       print "===[Good] : Find line contain data Soil Data fast => Read immediately" 
       #line_10_sand_clay = data[consider_index_line + 6]
       line_10_sand_clay = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.10")
       #line_50_sand_clay = data[consider_index_line + 11]
       line_50_sand_clay = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.50")
       #line_100_sand_clay = data[consider_index_line + 13]
       line_100_sand_clay = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "1.00")
       
       #Additinal data
       line_1_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.01")
       line_15_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.15")
       line_20_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.20")
       line_28_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.28")
       line_35_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.35")
       line_43_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.43")
       line_70_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.70")
       line_120_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "1.20")
       
       line_root =  data[consider_index_line + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line)
       [line_checking,index] = find_data(data, "SOIL PHYSICAL DATA")
       if (checking_key(line_checking, "SOIL PHYSICAL DATA") == 1):
           print "===Retry to find data" 
           #line_10_sand_clay = data[index + 6]
           line_10_sand_clay = find_line_data_fit(data, index + 4, index + 15, "0.10")
           #line_50_sand_clay = data[index + 11]
           line_50_sand_clay = find_line_data_fit(data, index + 4, index + 15, "0.50")
           #line_100_sand_clay = data[index + 13]
           line_100_sand_clay = find_line_data_fit(data, index + 4, index + 15, "1.00")
           
           #Additinal data
           line_1_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.01")
           line_15_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.15")
           line_20_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.20")
           line_28_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.28")
           line_35_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.35")
           line_43_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.43")
           line_70_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "0.70")
           line_120_data = find_line_data_fit(data, consider_index_line + 4, consider_index_line + 15, "1.20")
           
           line_root =  data[index + 3]
       else:
           sys.exit("Error : Please check output data file. System cannot find Soil Data")
   
    #Get Data Line 10 Sand Clay
    line_root = support_Apex_Sensitivity.standard_string(line_root)
    data_root = line_root.split(" ")
    
    
    #ADDITIONAL DATA
    # Layer 1: 0.01 m
    if (line_1_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_1 = 0.0
    else:
        line_1_data = support_Apex_Sensitivity.standard_string(line_1_data)
        print "==1 Sand Clay : " + line_1_data + "\n"
        data_1_data = line_1_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_1 = float(data_1_data[3]) - float(data_1_data[4])
            except Exception,err:
                value_awc_1 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 1  : %s " %(str(value_awc_1))
    # Layer 3: 0.15 m
    if (line_15_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_15 = 0.0
    else:
        line_15_data = support_Apex_Sensitivity.standard_string(line_15_data)
        print "==15 Sand Clay : " + line_15_data + "\n"
        data_15_data = line_15_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_15 = float(data_15_data[3]) - float(data_15_data[4])
            except Exception,err:
                value_awc_15 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 15  : %s " %(str(value_awc_15))
    # Layer 3: 0.20 m
    if (line_20_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_20 = 0.0
    else:
        line_20_data = support_Apex_Sensitivity.standard_string(line_20_data)
        print "==20 Sand Clay : " + line_20_data + "\n"
        data_20_data = line_20_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_20 = float(data_20_data[3]) - float(data_20_data[4])
            except Exception,err:
                value_awc_20 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 15  : %s " %(str(value_awc_20))
    # Layer 4: 0.28 m
    if (line_28_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_28 = 0.0
    else:
        line_28_data = support_Apex_Sensitivity.standard_string(line_28_data)
        print "==28 Sand Clay : " + line_28_data + "\n"
        data_28_data = line_28_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_28 = float(data_28_data[3]) - float(data_28_data[4])
            except Exception,err:
                value_awc_28 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 15  : %s " %(str(value_awc_28))  
    # Layer 4: 0.35 m
    if (line_35_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_35 = 0.0
    else:
        line_35_data = support_Apex_Sensitivity.standard_string(line_35_data)
        print "==35 Sand Clay : " + line_35_data + "\n"
        data_35_data = line_35_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_35 = float(data_35_data[3]) - float(data_35_data[4])
            except Exception,err:
                value_awc_35 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 35  : %s " %(str(value_awc_35)) 
    # Layer 4: 0.43 m
    if (line_43_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_43 = 0.0
    else:
        line_43_data = support_Apex_Sensitivity.standard_string(line_43_data)
        print "==43 Sand Clay : " + line_43_data + "\n"
        data_43_data = line_43_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_43 = float(data_43_data[3]) - float(data_43_data[4])
            except Exception,err:
                value_awc_43 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 43  : %s " %(str(value_awc_43))
    # Layer 7: 1.20 m
    if (line_70_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_70 = 0.0
    else:
        line_70_data = support_Apex_Sensitivity.standard_string(line_70_data)
        print "==43 Sand Clay : " + line_70_data + "\n"
        data_70_data = line_70_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_70 = float(data_70_data[3]) - float(data_70_data[4])
            except Exception,err:
                value_awc_70 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 43  : %s " %(str(value_awc_70))
    # Layer 5: 0.70 m
    if (line_120_data is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_awc_120 = 0.0
    else:
        line_120_data = support_Apex_Sensitivity.standard_string(line_120_data)
        print "==120 Sand Clay : " + line_120_data + "\n"
        data_120_data = line_120_data.split(" ")
        if (check_data_soil(data_root,"FC",3) == 1) and (check_data_soil(data_root,"WP",4) == 1):
            try:
                value_awc_120 = float(data_120_data[3]) - float(data_120_data[4])
            except Exception,err:
                value_awc_120 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============AWC 43  : %s " %(str(value_awc_120))             
    #END
    
    if (line_10_sand_clay is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_sand_10 = 0.0
        value_clay_10 = 0.0
        value_rock_10 = 0.0
        value_bulk_den_ov_dry_10 = 0.0
        value_awc_10 = 0.0
    else:
        line_10_sand_clay = support_Apex_Sensitivity.standard_string(line_10_sand_clay)
        print "==10 Sand Clay : " + line_10_sand_clay + "\n"
        data_10_sand_clay = line_10_sand_clay.split(" ")
        if (check_data_soil(data_root,"SAND",11) == 1):
            value_sand_10 = data_10_sand_clay[10]
            value_clay_10 = data_10_sand_clay[12]
            value_rock_10 = data_10_sand_clay[13]
            value_bulk_den_ov_dry_10 = data_10_sand_clay[9]
            try:
                value_awc_10 = float(data_10_sand_clay[3]) - float(data_10_sand_clay[4])
            except Exception,err:
                value_awc_10 = 0.0    
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============Sand , Clay, Rock, Bulk Den OV Dry , AWC 10  : %s , %s , %s  , %s , %s" %(str(value_sand_10), str(value_clay_10), str(value_rock_10),str(value_bulk_den_ov_dry_10), str(value_awc_10))   
        
    #Get Data Line 50 Sand Clay
    if (line_50_sand_clay is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_sand_50 = 0.0
        value_clay_50 = 0.0
        value_rock_50 = 0.0
        value_bulk_den_ov_dry_50 = 0.0
        value_awc_50 = 0.0
    else:
        line_50_sand_clay = support_Apex_Sensitivity.standard_string(line_50_sand_clay)
        print "==50 Sand Clay : " + line_50_sand_clay + "\n"
        data_50_sand_clay = line_50_sand_clay.split(" ")
        if (check_data_soil(data_root,"SAND",11) == 1):
            value_sand_50 = data_50_sand_clay[10]
            value_clay_50 = data_50_sand_clay[12]
            value_rock_50 = data_50_sand_clay[13]
            value_bulk_den_ov_dry_50 = data_50_sand_clay[9]
            try:
                value_awc_50 = float(data_50_sand_clay[3]) - float(data_50_sand_clay[4])
            except Exception,err:
                value_awc_50 = 0.0
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============Sand , Clay, Rock, Bulkd Dev OV Dry , AWC  50  : %s , %s, %s , %s , %s " %(str(value_sand_50), str(value_clay_50), str(value_rock_50), str(value_bulk_den_ov_dry_50), str(value_awc_50)) 
        
    #Get Data Line 100 Sand Clay
    if (line_100_sand_clay is None):
        #sys.exit("Error : Please check output data file. System cannot find Soil Data")
        value_sand_100 = 0.0
        value_clay_100 = 0.0
        value_rock_100 = 0.0
        value_bulk_den_ov_dry_100 = 0.0
        value_awc_100 = 0.0
    else:
        line_100_sand_clay = support_Apex_Sensitivity.standard_string(line_100_sand_clay)
        print "==100 Sand Clay : " + line_100_sand_clay + "\n"
        data_100_sand_clay = line_100_sand_clay.split(" ")
        if (check_data_soil(data_root,"SAND",11) == 1):
            value_sand_100 = data_100_sand_clay[10]
            value_clay_100 = data_100_sand_clay[12]
            value_rock_100 = data_100_sand_clay[13]
            value_bulk_den_ov_dry_100 = data_100_sand_clay[9]
            try:
                value_awc_100 = float(data_100_sand_clay[3]) - float(data_100_sand_clay[4])
            except Exception,err:
                value_awc_100 = 0.0
        else:
            sys.exit("Error : Please check output data file. System cannot find Soil Data====")
        print "=============Sand , Clay, Rock, Bulkd Dev OV Dry , AWC 100  : %s , %s, %s , %s , %s" %(str(value_sand_100), str(value_clay_100), str(value_rock_100), str(value_bulk_den_ov_dry_100), str(value_awc_100))
        
    return [value_sand_10,value_clay_10,value_sand_50,value_clay_50,value_sand_100,value_clay_100,value_rock_10,value_bulk_den_ov_dry_10,value_rock_50,value_bulk_den_ov_dry_50,value_rock_100,value_bulk_den_ov_dry_100,value_awc_10,value_awc_50,value_awc_100,value_awc_1,value_awc_15,value_awc_20,value_awc_28,value_awc_35,value_awc_43,value_awc_70,value_awc_120]    
          
def get_weather_data_fields(APEX_OUT_FILE_LOCAL):
    line_TMX = ""
    line_TMN = ""
    line_PRCP = ""
    line_DAYP = ""
    line_SRAD = ""

    
    with open(APEX_OUT_FILE_LOCAL, 'r') as file:
        data = file.readlines()
        
        
    if (APEX_TYPE == 'G'):    
        consider_index_line = 108
    elif (APEX_TYPE == 'M'):
        consider_index_line = 214
    else:
        consider_index_line = 108
        
    line_checking = data[consider_index_line]
    if (checking_key(line_checking, "WEATHER DATA") == 1 and len(data) >= 240):
       print "===[Good] : Find line contain data Weather Data fast => Read immediately" 
       line_TMX = data[consider_index_line + 11]
       line_TMN = data[consider_index_line + 12]
       line_PRCP = data[consider_index_line + 15]
       line_DAYP = data[consider_index_line + 20]
       line_SRAD = data[consider_index_line + 22]
       
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line)
       [line_checking,index] = find_data(data, "WEATHER DATA")
       if (checking_key(line_checking, "WEATHER DATA") == 1):
           print "===Retry to find data" 
           line_TMX = data[index + 11]
           line_TMN = data[index + 12]
           line_PRCP = data[index + 15]
           line_DAYP = data[index + 20]
           line_SRAD = data[index + 22]
       else:
           sys.exit("Error : Please check output data file. System cannot find Weather Data")
    #Get Data TMX
    if (line_TMX is None):
        sys.exit("Error : Please check output data file. System cannot find Weather Data")
    else:
        line_TMX = support_Apex_Sensitivity.standard_string(line_TMX)
        print line_TMX + "\n"
        data_TMX = line_TMX.split(" ")
        if (check_data(data_TMX,"TMX") == 1):
            value_TMX_year = data_TMX[len(data_TMX)-2]
        else:
            sys.exit("Error : Please check output data file. System cannot find Weather Data")
        print "=============TMX value  :" + value_TMX_year
    #Get Data TMN
    if (line_TMN is None):
        sys.exit("Error : Please check output data file. System cannot find Weather Data")
    else:
        line_TMN = support_Apex_Sensitivity.standard_string(line_TMN)
        print line_TMN + "\n"
        data_TMN = line_TMN.split(" ")
        if (check_data(data_TMN,"TMN") == 1):
            value_TMN_year = data_TMN[len(data_TMN)-2]
        else:
            sys.exit("Error : Please check output data file. System cannot find Weather Data")
        print "=============TMN value  :" + value_TMN_year
    
    #Get data PRCP
    if (line_PRCP is None):
        sys.exit("Error : Please check output data file. System cannot find Weather Data")
    else:
        line_PRCP = support_Apex_Sensitivity.standard_string(line_PRCP)
        print line_PRCP + "\n"
        data_PRCP = line_PRCP.split(" ")
        if (check_data(data_PRCP,"PRCP") == 1):
            value_PRCP_year = data_PRCP[len(data_PRCP)-2]
        else:
            sys.exit("Error : Please check output data file. System cannot find Weather Data")
        print "=============PRCP value  :" + value_PRCP_year
    
    #Get data DAYP
    if (line_DAYP is None):
        sys.exit("Error : Please check output data file. System cannot find Weather Data")
    else:
        line_DAYP = support_Apex_Sensitivity.standard_string(line_DAYP)
        print line_DAYP + "\n"
        data_DAYP = line_DAYP.split(" ")
        if (check_data(data_DAYP,"DAYP") == 1):
            value_DAYP_year = data_DAYP[len(data_DAYP)-2]
        else:
            sys.exit("Error : Please check output data file. System cannot find Weather Data")
        print "=============DAYP value  :" + value_DAYP_year
   
    #Get Data SRAD
    if (line_SRAD is None):
        sys.exit("Error : Please check output data file. System cannot find Weather Data")
    else:
        line_SRAD = support_Apex_Sensitivity.standard_string(line_SRAD)
        print line_SRAD + "\n"
        data_SRAD = line_SRAD.split(" ")
        if (check_data(data_SRAD,"SRAD") == 1):
            value_SRAD_year = data_SRAD[len(data_SRAD)-2]
        else:
            sys.exit("Error : Please check output data file. System cannot find Weather Data")
        print "=============SRAD value  :" + value_SRAD_year
    return [value_TMX_year,value_TMN_year,value_PRCP_year,value_DAYP_year,value_SRAD_year]  
def find_index(data,key):
    for i in range(0,13):
        if (data[i].strip().upper() == key):
            return i
    return None


def get_grass_scenarion_data(OUT_G_FILE):
    line_forageyield_YLDF = ""
    line_Q_Y = ""
    with open(OUT_G_FILE, 'r') as file:
        data = file.readlines()
          
    #YLDG
    if (len(data) > 7160):
       consider_index_line_YLDF = 7160
    else:
       consider_index_line_YLDF = 0 
    line_checking = data[consider_index_line_YLDF]
    if (checking_key(line_checking[0:40], "AVE ANNUAL CROP YLD DATA") == 1):
       print "===[Good] : Find line contain data GRASS SCENARIO - YLDF fast => Read immediately" 
       line_root_YLDF = data[consider_index_line_YLDF + 1]
       line_forageyield_YLDF = data[consider_index_line_YLDF + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line_YLDF)
       [line_checking,index] = find_data_2(data, "AVE ANNUAL CROP YLD DATA")
       if (checking_key(line_checking[0:40], "AVE ANNUAL CROP YLD DATA") == 1):
           print "===Retry to find data===" 
           line_root_YLDF = data[index + 1]
           line_forageyield_YLDF = data[index + 3]
       else:
           #sys.exit("Error : Please check output data file. System cannot find Weather Data")
           value_forage_yield_YLDF = 0.0
      
    #Q - Y Runoff
    if (len(data) >= 7218):   
       consider_index_line_Q_Y = 7218
    else:
       consider_index_line_Q_Y = 0 
    
    line_checking = data[consider_index_line_Q_Y]
    if (checking_key(line_checking, "AVE ANNUAL DATA") == 1):
       print "===[Good] : Find line contain data GRASS SCENARIO - Q and Y fast => Read immediately" 
       line_root_Q_Y = data[consider_index_line_Q_Y + 1]
       line_Q_Y = data[consider_index_line_Q_Y + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line_Q_Y)
       [line_checking,index] = find_data(data, "AVE ANNUAL DATA")
       if (checking_key(line_checking, "AVE ANNUAL DATA") == 1):
           print "===Retry to find data===" 
           line_root_Q_Y = data[index + 1]
           line_Q_Y = data[index + 3]
       else:
           #sys.exit("Error : Please check output data file. System cannot find Weather Data")
           value_Q = 0.0
           value_Y = 0.0
    
    #Get Data YLDG
    if (line_root_YLDF is None):
        value_forage_yield_YLDF = 0.0
    else:
        line_root_YLDF = support_Apex_Sensitivity.standard_string(line_root_YLDF)
        data_root_YLDF = line_root_YLDF.split(" ")
    
    if (line_forageyield_YLDF is None):
        value_forage_yield_YLDF = 0.0
    else:
        line_forageyield_YLDF = support_Apex_Sensitivity.standard_string(line_forageyield_YLDF)
        print line_forageyield_YLDF + "\n"
        data_YLDF = line_forageyield_YLDF.split(" ")
        if (data_root_YLDF[2].strip().upper() == "YLDF"):
            value_forage_yield_YLDF = data_YLDF[2].strip()
        else:
            value_forage_yield_YLDF = 0.0
            index_yldf = find_index(data_root_YLDF, "YLDF")
            if (index_yldf is None):
                value_forage_yield_YLDF = 0.0
            else:
                value_forage_yield_YLDF = data_YLDF[index_yldf].strip()
                    
        value_forage_yield_YLDF = value_forage_yield_YLDF.replace('/','')
        print "=============Grass YLDG value  :" + value_forage_yield_YLDF
    
    
    #Get Data Q Y
    if (line_root_Q_Y is None):
        value_Q = 0.0
        value_Y = 0.0
    else:
        line_root_Q_Y = support_Apex_Sensitivity.standard_string(line_root_Q_Y)
        data_root_Q_Y = line_root_Q_Y.split(" ")
    
    if (line_Q_Y is None):
        value_Q = 0.0
        value_Y = 0.0
    else:
        line_Q_Y = support_Apex_Sensitivity.standard_string(line_Q_Y)
        print line_Q_Y + "\n"
        data_Q_Y = line_Q_Y.split(" ")
        if (data_root_Q_Y[3].strip().upper() == "Q"):
            value_Q = data_Q_Y[5].strip()
        else:
            value_Q = 0.0
            index_Q = find_index(data_root_Q_Y, "Q")
            if (index_Q is None):
                value_Q = 0.0
            else:
                value_Q = data_Q_Y[index_Q + 2].strip()              
        print "=============Grass Q value  :" + value_Q 
        if (data_root_Q_Y[8].strip().upper() == "Y"):
            value_Y = data_Q_Y[10].strip()
        else:
            value_Y = 0.0
            index_Y = find_index(data_root_Q_Y, "Y")
            if (index_Y is None):
                index_Y = 0.0
            else:
                value_Y = data_Q_Y[index_Y + 2].strip()
        print "=============Grass Q value  :" + value_Y
    
    return [value_forage_yield_YLDF,value_Q,value_Y]


def get_crop_scenarion_data(OUT_M_FILE):
    line_cropyield_YLDG = ""
    line_Q_Y = ""
    with open(OUT_M_FILE, 'r') as file:
        data = file.readlines()
          
    #YLDG
    if (len(data) > 7644):
       consider_index_line_YLDG = 7644
    else:
       consider_index_line_YLDG = 0 
    line_checking = data[consider_index_line_YLDG]
    if (checking_key(line_checking[0:40], "AVE ANNUAL CROP YLD DATA") == 1):
       print "===[Good] : Find line contain data CROP SCENARIO - YLDG fast => Read immediately" 
       line_root_YLDG = data[consider_index_line_YLDG + 1]
       line_cropyield_YLDG = data[consider_index_line_YLDG + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line_YLDG)
       [line_checking,index] = find_data_2(data, "AVE ANNUAL CROP YLD DATA")
       if (checking_key(line_checking[0:40], "AVE ANNUAL CROP YLD DATA") == 1):
           print "===Retry to find data===" 
           line_root_YLDG = data[index + 1]
           line_cropyield_YLDG = data[index + 3]
       else:
           #sys.exit("Error : Please check output data file. System cannot find Weather Data")
           value_crop_yield_YLDG = 0.0
      
    #Q - Y Runoff
    if (len(data) >= 7703):   
       consider_index_line_Q_Y = 7703
    else:
       consider_index_line_Q_Y = 0 
    
    line_checking = data[consider_index_line_Q_Y]
    if (checking_key(line_checking, "AVE ANNUAL DATA") == 1):
       print "===[Good] : Find line contain data CROP SCENARIO - Q and Y fast => Read immediately" 
       line_root_Q_Y = data[consider_index_line_Q_Y + 1]
       line_Q_Y = data[consider_index_line_Q_Y + 3]
    else:
       print "===[Warning] : Line %d does not contain data => Need to loop all line" % (consider_index_line_Q_Y)
       [line_checking,index] = find_data(data, "AVE ANNUAL DATA")
       if (checking_key(line_checking, "AVE ANNUAL DATA") == 1):
           print "===Retry to find data===" 
           line_root_Q_Y = data[index + 1]
           line_Q_Y = data[index + 3]
       else:
           #sys.exit("Error : Please check output data file. System cannot find Weather Data")
           value_Q = 0.0
           value_Y = 0.0
    
    #Get Data YLDG
    if (line_root_YLDG is None):
        value_crop_yield_YLDG = 0.0
    else:
        line_root_YLDG = support_Apex_Sensitivity.standard_string(line_root_YLDG)
        data_root_YLDG = line_root_YLDG.split(" ")
    
    if (line_cropyield_YLDG is None):
        value_crop_yield_YLDG = 0.0
    else:
        line_cropyield_YLDG = support_Apex_Sensitivity.standard_string(line_cropyield_YLDG)
        print line_cropyield_YLDG + "\n"
        data_YLDG = line_cropyield_YLDG.split(" ")
        if (data_root_YLDG[1].strip().upper() == "YLDG"):
            value_crop_yield_YLDG = data_YLDG[1].strip()
        else:
            value_crop_yield_YLDG = 0.0
            index_yldg = find_index(data_root_YLDG, "YLDG")
            if (index_yldg is None):
                value_crop_yield_YLDG = 0.0
            else:
                value_crop_yield_YLDG = data_YLDG[index_yldg].strip()
                    
        value_crop_yield_YLDG = value_crop_yield_YLDG.replace('/','')
        print "=============Crop YLDG value  :" + value_crop_yield_YLDG
    
    
    #Get Data Q Y
    if (line_root_Q_Y is None):
        value_Q = 0.0
        value_Y = 0.0
    else:
        line_root_Q_Y = support_Apex_Sensitivity.standard_string(line_root_Q_Y)
        data_root_Q_Y = line_root_Q_Y.split(" ")
    
    if (line_Q_Y is None):
        value_Q = 0.0
        value_Y = 0.0
    else:
        line_Q_Y = support_Apex_Sensitivity.standard_string(line_Q_Y)
        print line_Q_Y + "\n"
        data_Q_Y = line_Q_Y.split(" ")
        if (data_root_Q_Y[3].strip().upper() == "Q"):
            value_Q = data_Q_Y[5].strip()
        else:
            value_Q = 0.0
            index_Q = find_index(data_root_Q_Y, "Q")
            if (index_Q is None):
                value_Q = 0.0
            else:
                value_Q = data_Q_Y[index_Q + 2].strip()              
        print "=============Crop Q value  :" + value_Q 
        if (data_root_Q_Y[8].strip().upper() == "Y"):
            value_Y = data_Q_Y[10].strip()
        else:
            value_Y = 0.0
            index_Y = find_index(data_root_Q_Y, "Y")
            if (index_Y is None):
                index_Y = 0.0
            else:
                value_Y = data_Q_Y[index_Y + 2].strip()
        print "=============Crop Q value  :" + value_Y
    
    return [value_crop_yield_YLDG,value_Q,value_Y]
def get_MU_globalID(X_COOR, Y_COOR):
    print "%s   |    %s" %(str(X_COOR),str(Y_COOR))
    return support_Apex_Sensitivity.getRasterValue(TIF_FOLDER + tif_HWSD,X_COOR,Y_COOR) 
def get_slate_weather(X_COOR, Y_COOR):
    print "%s   |    %s" %(str(X_COOR),str(Y_COOR))
    return support_Apex_Sensitivity.getRasterValue_ThanhNguyen_TIF(TIF_FOLDER + tif_slate_weather,X_COOR,Y_COOR)   
def main():
    try:
       csvfile = open(PRIVATE_FOLDER_RESULT_CSV_FILE, 'wb')
       out = UnicodeWriter(csvfile)
       out.writerow(['ID','RECORDER_NAME', 'PLOT_NAME', 'LATITUDE','LONGITUDE','TIME','MU_GLOBAL','SLATE_WEATHER','ORGANIZATION','TMX','TMN','PRCP','DAYP','SRAD','10 SAND',
                     '10 CLAY','10 ROCK','10 BULK DEV OV DRY','10 PH','10 ORGC','10 CEC','50 SAND','50 CLAY','50 ROCK','50 BULK DEV OV DRY','50 PH','50 ORGC','50 CEC','100 SAND','100 CLAY','100 ROCK','100 BULK DEV OV DRY','100 PH','100 ORGC',
                     '100 CEC','SLP','AZM','CROP-YLDG','CROP-Q','CROP-Y','GRASS-YLDF','GRASS-Q','GRASS-Y','0.1 AWC','0.5 AWC','1.0 AWC','0.01 AWC','0.15 AWC','0.20 AWC','0.28 AWC','0.35 AWC','0.43 AWC','0.70 AWC','1.20 AWC']) 
       print "====================================================="
       print "==Step 1 : Select all plots comes from %s" %(RECORD_NAME)
       list_records = support_Apex_Sensitivity.get_collection_data_from_record_name(RECORD_NAME)
       print "==Step 2 : Get data per each record=================="
       for item in list_records:
           ID = item[0]
           mu_global = get_MU_globalID(item[4],item[3])
           slate_weather = get_slate_weather(float(item[4]),float(item[3]))
           print "=====Get data from %s.Out file==========================" %(str(ID))
           if (APEX_TYPE == 'G'):
               APEX_OUT_FILE = os.path.join(APEX_OUT_FILE_FOLDER,"%s\\%sG.OUT" %(str(ID),str(ID)))
           elif (APEX_TYPE == 'M'):
               APEX_OUT_FILE = os.path.join(APEX_OUT_FILE_FOLDER,"%s\\%sM.OUT" %(str(ID),str(ID)))
           if (not os.path.exists(APEX_OUT_FILE)):
               print("Error : File %sG.OUT is NOT Existed !" %(str(ID)))
               weather_fields = [0.0,0.0,0.0,0.0,0.0]  
               soil_fields = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
               soil_chemicals = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
           else:
               try:   
                   weather_fields = get_weather_data_fields(APEX_OUT_FILE)
                   soil_fields = get_soil_data_fields(APEX_OUT_FILE)
                   soil_chemicals = get_soil_chemical_fields(APEX_OUT_FILE)
               except Exception, err:
                   pass
           
           SUBAREA_FILE_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\7_SUBAREA_PROJECT_REAL_TIME\\Subarea_Files\\Private\\%s\\Modified_Subarea_Files\\SUBS1.SUB" %(str(ID))
           subarea_fields = get_subarea_fields(SUBAREA_FILE_PATH)
           
           #Get data CROP version M-Version
           APEX_OUT_M_FILE = os.path.join(APEX_OUT_FILE_FOLDER,"%s\\%sM.OUT" %(str(ID),str(ID)))
           APEX_OUT_G_FILE = os.path.join(APEX_OUT_FILE_FOLDER,"%s\\%sG.OUT" %(str(ID),str(ID)))
           if (not os.path.exists(APEX_OUT_M_FILE) or not os.path.exists(APEX_OUT_G_FILE)):
               print("Error : File %sM.OUT is NOT Existed !" %(str(ID)))
               crop_scenarion = [0.0,0.0,0.0]
               print("Error : File %sM.OUT is NOT Existed !" %(str(ID)))
               grass_scenarion = [0.0,0.0,0.0]
           else:
               try:
                   crop_scenarion = get_crop_scenarion_data(APEX_OUT_M_FILE)
                   grass_scenarion = get_grass_scenarion_data(APEX_OUT_G_FILE)
               except Exception, err:
                   pass
           
          
           out.writerow([str(ID),str(item[2]),str(item[1]),str(item[3]),str(item[4]),str(item[5]),str(mu_global),str(slate_weather),str(item[6]),str(weather_fields[0]),
                         str(weather_fields[1]),str(weather_fields[2]),str(weather_fields[3]),str(weather_fields[4])
                         ,str(soil_fields[0]),str(soil_fields[1]),str(soil_fields[6]),str(soil_fields[7]),str(soil_chemicals[0]),str(soil_chemicals[1]),str(soil_chemicals[6]),str(soil_fields[2]),
                         str(soil_fields[3]),str(soil_fields[8]),str(soil_fields[9]),str(soil_chemicals[2]),str(soil_chemicals[3]),str(soil_chemicals[7]),str(soil_fields[4]),str(soil_fields[5])
                         ,str(soil_fields[10]),str(soil_fields[11]),str(soil_chemicals[4]),str(soil_chemicals[5]),str(soil_chemicals[8]),str(subarea_fields[1]),str(subarea_fields[0]),str(crop_scenarion[0])
                         ,str(crop_scenarion[1]),str(crop_scenarion[2]),str(grass_scenarion[0]),str(grass_scenarion[1]),str(grass_scenarion[2]),str(soil_fields[12]),str(soil_fields[13]),str(soil_fields[14])
                         ,str(soil_fields[15]),str(soil_fields[16]),str(soil_fields[17]),str(soil_fields[18]),str(soil_fields[19]),str(soil_fields[20]),str(soil_fields[21]),str(soil_fields[22])])
    except Exception, err:
        print err
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()    
    
