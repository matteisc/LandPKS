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
# Check arguments
if (len(sys.argv) < 4):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python createDATscript.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel Application Folder>")


from win32com.client import Dispatch

try: 
    excel = win32com.client.GetActiveObject("Excel.Application")
    print("Running Excel instance found, returning object => CLOSE this => Ready to Run Script")
    excel.Application.Quit()
except:
    print("No running Excel instances => Ready to Start Services")
    
def checkExcelApplicationIsRunning():
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        try:
           index_exe = line.index(' ')
           app = line[:index_exe]
           if (app == 'excel.exe' or app == "EXCEL.exe" or app == "Excel.exe" or app == "EXCEL.EXE"):
               return 1
        except:
            continue
    return 0
if (checkExcelApplicationIsRunning()==1):
    print "Kill Excel Project"
    os.system("taskkill /f /im excel.exe")

xlApp = Dispatch("Excel.Application")
xlApp.Visible = 0
        
# Input requires
db_file = ""
mu_global = ""
output_file = ""
full_path = os.getcwd() + "\\"
datDirectory = ""
solDirectory = ""
name_sol = ""

FULL_PATH_EXCEL_APPLICATION = ""
REAL_PATH_EXCEL_APPLICATION = ""
REAL_RUNABLE_EXCEL_FOLDER = ""
EXECUTABLE_EXE_FILE_EXCEL_APPLICATION = "LPKS_SPAW.xlsx"

# Manage arguments
if (sys.argv[1] == '-d') :
    if (sys.argv[2] is None) :
        sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")
    else:
        db_file = full_path + sys.argv[2]
        db_file = db_file.replace("\\\\", "\\")
else :
    sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")

if (sys.argv[3] == '-m') :
    if (sys.argv[4] is None) :
        sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")
    else:
        mu_global = sys.argv[4]
else :
    sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")
    
if (sys.argv[5] == '-model'):
    if (sys.argv[6] is None) :
        sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")
    else:
        if (os.path.exists(sys.argv[6])):
            FULL_PATH_EXCEL_APPLICATION = sys.argv[6]
        else:
            sys.exit("==[Error] : Folder contains SPAW Excel Model is NOT Existed") 
        print("\n---[Done] : SPAW Excel Application is in Folder %s" % (FULL_PATH_EXCEL_APPLICATION))
else:
    sys.exit("Usage : python main_HWSD_SPAW.py -d <Database File Path> -m <MU_GLOBAL> -model <Excel File Path Model Application>")

# Set Up MSAccess Driver
user = ''
password = ''
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s' % \
                (db_file, user, password)

# Function

def copyFile(From, To):
    shutil.copy2(From, To)
def prepareFacingModels():
    current = time.time()
    model_directory = full_path + "\Model_Application\Sub_request\%s" % str(current)
    REAL_RUNABLE_EXCEL_FOLDER = model_directory
    if not os.path.exists(model_directory):
        os.makedirs(model_directory)
    copyFile(FULL_PATH_EXCEL_APPLICATION, REAL_RUNABLE_EXCEL_FOLDER)
    # REAL_RUNABLE_EXCEL_FOLDER = os.path.join(REAL_RUNABLE_EXCEL_FOLDER, EXECUTABLE_EXE_FILE_EXCEL_APPLICATION)
    return REAL_RUNABLE_EXCEL_FOLDER
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
                strContent = "    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
            else:
                if (count >= 2 and count <= 9):
                    strContent = "\n    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                elif (count >= 10 and count <= 99):
                    strContent = "\n   %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                elif (count >= 100 and count <= 999):
                    strContent = "\n  %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                elif (count >= 1000 and count <= 9999):
                    strContent = "\n %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                elif (count >= 10000 and count <= 99999):
                    strContent = "\n%d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
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
        sql = "SELECT SEQ, SHARE, SU_SYM90, T_SAND, S_SAND, T_SILT, S_SILT, T_PH_H2O, S_PH_H2O, T_OC, S_OC, T_CACO3, S_CACO3, T_CEC_SOIL, S_CEC_SOIL, T_GRAVEL, S_GRAVEL, T_REF_BULK_DENSITY, S_REF_BULK_DENSITY, T_ECE, S_ECE FROM HWSD_DATA WHERE ID = %d AND MU_GLOBAL = %d" % (int(wise3_id), int(mu_global))

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
def createSOILFile(wise3_id, name_sol, t_sand, s_sand, t_silt, s_silt, t_ph_h2o, s_ph_h2o, t_oc, s_oc, t_caco3, s_caco3, t_cec_soil, s_cec_soil, t_gravel, s_gravel, t_ref_bulk_density, s_ref_bulk_density, t_ece, s_ece, wiliting_point_1, wiliting_point_2, field_capacity_1, field_capacity_2, saturated_hydraulic_con_1,saturated_hydraulic_con_2):
    try:
        # fo=open(wise3_id +".SOL","wb")
        fo = open(os.path.join("Result_HWSD/SOLFiles/%s/" % (str(mu_global)), name_sol + ".SOL"), "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SOIL property to File %s.SOL" % (name_sol))
        # Line 1
        fo.write("            %s" % (name_sol))
        # Line 2
        field_2_line_2 = 0.0
        if (saturated_hydraulic_con_1 > 254):
            field_2_line_2 = 1
        elif (saturated_hydraulic_con_1 >= 84 and saturated_hydraulic_con_1 <= 254):
            field_2_line_2 = 2
        elif (saturated_hydraulic_con_1 >= 8.4 and saturated_hydraulic_con_1 <= 84):
            field_2_line_2 = 3
        elif (saturated_hydraulic_con_1 >= 0 and saturated_hydraulic_con_1 < 8.4):
            field_2_line_2 = 4
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (0.15, field_2_line_2, 0, 0, 0, 0, 0, 0, 0, 0))
        # Line 3
        #fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" % (10, 0, 50, 2, 0.1, 0.1, 0.1, 0, 0, 0))
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
        strContent = "    %0.2f    %0.2f" % (0.3, 1.0)
        fo.write(strContent)
        # Line 5 - Dry Bulk Density % - T_REF_BULK_DENSITY and S_REF_BULK_DENSITY - 0 -> 2.0
        fo.write("\n")
        if (t_ref_bulk_density >= 0 and t_ref_bulk_density < 10):
            strContent = "    %0.2f" % (t_ref_bulk_density)
        elif (t_ref_bulk_density > 9 and t_ref_bulk_density < 100):
            strContent = "   %0.2f" % (t_ref_bulk_density)
        fo.write(strContent)
        if (s_ref_bulk_density >= 0 and s_ref_bulk_density < 10):
            strContent = "    %0.2f" % (s_ref_bulk_density)
        elif (s_ref_bulk_density > 9 and s_ref_bulk_density < 100):
            strContent = "   %0.2f" % (s_ref_bulk_density)
        fo.write(strContent)
        # Line 6 - Water content at PWP - 0.01 - 0.5
        fo.write("\n")
        if (wiliting_point_1 >= 0 and wiliting_point_1 < 10):
            strContent = "    %0.2f" % (wiliting_point_1)
        elif (wiliting_point_1 > 9 and wiliting_point_1 < 100):
            strContent = "   %0.2f" % (wiliting_point_1)
        fo.write(strContent)
        if (wiliting_point_2 >= 0 and wiliting_point_2 < 10):
            strContent = "    %0.2f" % (wiliting_point_2)
        elif (wiliting_point_2 > 9 and wiliting_point_2 < 100):
            strContent = "   %0.2f" % (wiliting_point_2)
        fo.write(strContent)
        # Line 7 - Water Content at FC - 0.1 - 0.6
        fo.write("\n")
        if (field_capacity_1 >= 0 and field_capacity_1 < 10):
            strContent = "    %0.2f" % (field_capacity_1)
        elif (field_capacity_1 > 9 and field_capacity_1 < 100):
            strContent = "   %0.2f" % (field_capacity_1)
        fo.write(strContent)
        if (field_capacity_2 >= 0 and field_capacity_2 < 10):
            strContent = "    %0.2f" % (field_capacity_2)
        elif (field_capacity_2 > 9 and field_capacity_2 < 100):
            strContent = "   %0.2f" % (field_capacity_2)
        fo.write(strContent)
        # Line 8 - Sand Content - T_SAND and S_SAND - 1 -> 99
        fo.write("\n")
        if (t_sand >= 0 and t_sand < 10):
            strContent = "    %0.2f" % (t_sand)
        elif (t_sand > 9 and t_sand < 100):
            strContent = "   %0.2f" % (t_sand)
        fo.write(strContent)
        if (s_sand >= 0 and s_sand < 10):
            strContent = "    %0.2f" % (s_sand)
        elif (s_sand > 9 and s_sand < 100):
            strContent = "   %0.2f" % (s_sand)
        fo.write(strContent)
		# Line 9 - Silt Content - T_SILT and S_SILT - 1 -> 99
        fo.write("\n")
        if (t_silt >= 0 and t_silt < 10):
            strContent = "    %0.2f" % (t_silt)
        elif (t_silt > 9 and t_silt < 100):
            strContent = "   %0.2f" % (t_silt)
        fo.write(strContent)
        if (s_silt >= 0 and s_silt < 10):
            strContent = "    %0.2f" % (s_silt)
        elif (s_silt > 9 and s_silt < 100):
            strContent = "   %0.2f" % (s_silt)
        fo.write(strContent)
		# Line 10 - Initial Organic N - 100 -> 5000 ppm
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		# Line 11 - Soil PH - T_PH_H2O and S_PH_H2O - 3 -> 9
        fo.write("\n")
        if (t_ph_h2o >= 0 and t_ph_h2o < 10):
            strContent = "    %0.2f" % (t_ph_h2o)
        elif (t_ph_h2o > 9 and t_ph_h2o < 100):
            strContent = "   %0.2f" % (t_ph_h2o)
        fo.write(strContent)
        if (s_ph_h2o >= 0 and s_ph_h2o < 10):
            strContent = "    %0.2f" % (s_ph_h2o)
        elif (s_ph_h2o > 9 and s_ph_h2o < 100):
            strContent = "   %0.2f" % (s_ph_h2o)
        fo.write(strContent)
		# Line 12 - Sum of bases - 0 -> 150
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		# Line 13 - Organic C Conc % - T_OC and S_OC - 0.1 -> 10
        fo.write("\n")
        if (t_oc >= 0 and t_oc < 10):
            strContent = "    %0.2f" % (t_oc)
        elif (t_oc > 9 and t_oc < 100):
            strContent = "   %0.2f" % (t_oc)
        fo.write(strContent)
        if (s_oc >= 0 and s_oc < 10):
            strContent = "    %0.2f" % (s_oc)
        elif (s_oc > 9 and s_oc < 100):
            strContent = "   %0.2f" % (s_oc)
        fo.write(strContent)
		# Line 14 - Calcium Carbonat Content % - T_CACO3 and S_CACO3 - 0 -> 99
        fo.write("\n")
        if (t_caco3 >= 0 and t_caco3 < 10):
            strContent = "    %0.2f" % (t_caco3)
        elif (t_caco3 > 9 and t_caco3 < 100):
            strContent = "   %0.2f" % (t_caco3)
        fo.write(strContent)
        if (s_caco3 >= 0 and s_caco3 < 10):
            strContent = "    %0.2f" % (s_caco3)
        elif (s_caco3 > 9 and s_caco3 < 100):
            strContent = "   %0.2f" % (s_caco3)
        fo.write(strContent)
		# Line 15 - CEC - T_CEC_SOIL and S_CEC_SOIL - 0 -> 150
        fo.write("\n")
        if (t_cec_soil >= 0 and t_cec_soil < 10):
            strContent = "    %0.2f" % (t_cec_soil)
        elif (t_cec_soil > 9 and t_cec_soil < 100):
            strContent = "   %0.2f" % (t_cec_soil)
        elif (t_cec_soil > 99 and t_cec_soil < 1000):
            strContent = "  %0.2f" % (t_cec_soil)
        fo.write(strContent)
        if (s_cec_soil >= 0 and s_cec_soil < 10):
            strContent = "    %0.2f" % (s_cec_soil)
        elif (s_cec_soil > 9 and s_cec_soil < 100):
            strContent = "   %0.2f" % (s_cec_soil)
        elif (s_cec_soil > 99 and s_cec_soil < 1000):
            strContent = "  %0.2f" % (s_cec_soil)
        fo.write(strContent)
		
		# Line 16 - Coarse Fragment % - T_GRAVEL and S_GRAVEL - 0 -> 99
        fo.write("\n")
        if (t_gravel >= 0 and t_gravel < 10):
            strContent = "    %0.2f" % (t_gravel)
        elif (t_gravel > 9 and t_gravel < 100):
            strContent = "   %0.2f" % (t_gravel)
        fo.write(strContent)
        if (s_gravel >= 0 and s_gravel < 10):
            strContent = "    %0.2f" % (s_gravel)
        elif (s_gravel > 9 and s_gravel < 100):
            strContent = "   %0.2f" % (s_gravel)
        fo.write(strContent)
		# Line 17 - Initial Soluble N
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		# Line 18 - Initial Soluble P
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		# Line 19 - Crop Residue - 0 - 20
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		
		# Line 20 - Moist bulk density - 0.5 - 2.5
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
        # Line 21 - Phosphorous sorption ratio - 0 -> 0.9
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
        # Line 22 - Saturated conductivity 0.00001-100
        fo.write("\n")
        if (saturated_hydraulic_con_1 >= 0 and saturated_hydraulic_con_1 < 10):
            strContent = "    %0.2f" % (saturated_hydraulic_con_1)
        elif (saturated_hydraulic_con_1 > 9 and saturated_hydraulic_con_1 < 100):
            strContent = "   %0.2f" % (saturated_hydraulic_con_1)
        fo.write(strContent)
        if (saturated_hydraulic_con_2 >= 0 and saturated_hydraulic_con_2 < 10):
            strContent = "    %0.2f" % (saturated_hydraulic_con_2)
        elif (saturated_hydraulic_con_2 > 9 and saturated_hydraulic_con_2 < 100):
            strContent = "   %0.2f" % (saturated_hydraulic_con_2)
        fo.write(strContent)
        # Line 23 - Lateral Hydraulic 0.00001-10
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
        # Line 24 - Initial Organic P conc 50 - 1000
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
        # Line 25 - Exchangeable K conc
        fo.write("\n    %0.2f    %0.2f" % (0, 0))
		
        # Line 26 - Electrical Conductivity 0 - 50
        fo.write("\n")
        if (t_ece >= 0 and t_ece < 10):
            strContent = "    %0.2f" % (t_ece)
        elif (t_ece > 9 and t_ece < 100):
            strContent = "   %0.2f" % (t_ece)
        fo.write(strContent)
        if (s_ece >= 0 and s_ece < 10):
            strContent = "    %0.2f" % (s_ece)
        elif (s_ece > 9 and s_ece < 100):
            strContent = "   %0.2f" % (s_ece)
        fo.write(strContent)

        # Line 27 -> 45
        for i in range(27, 46):
            fo.write("\n    %0.2f    %0.2f" % (0, 0))

    except Exception, err:
        sys.exit("Error : %s" % (err))
    finally:
        fo.close()
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
def acessModelToGetValue(xlBook, REAL_PATH_EXCEL_APPLICATION, sand_1, clay_1, organic_matter_1, gravel_1, sand_2, clay_2, organic_matter_2, gravel_2):
    
    values = []
    try:
            
            fl_sand_1 = 0.0
            fl_clay_1 = 0.0
            fl_organic_matter_1 = 0.0
            fl_gravel_1 = 0.0
        # Process for Layer 1    
            if (float(sand_1)):
                fl_sand_1 = float(sand_1) / 100
            if (float(clay_1)):
                fl_clay_1 = 1 - fl_sand_1 - (float(clay_1) / 100)
            if (float(organic_matter_1)):
                fl_organic_matter_1 = float(organic_matter_1) * 2
            if (float(gravel_1)):
                fl_gravel_1 = float(gravel_1) / 100
            print "Receive Input Level 1 : Sand = %s | Clay = %s | Organic Matter = %s | Gravel = %s" % (str(sand_1), str(clay_1), str(organic_matter_1), str(gravel_1))
            print "Receive Input Level 1 : Sand = %s | Clay = %s | Organic Matter = %s | Gravel = %s" % (str(fl_sand_1), str(fl_clay_1), str(fl_organic_matter_1), str(fl_gravel_1))
            
            xlSheet = xlBook.Sheets(1)
            xlSheet.Cells(5, 3).Value = fl_sand_1
            xlSheet.Cells(5, 4).Value = fl_clay_1
            xlSheet.Cells(5, 5).Value = fl_organic_matter_1
            xlSheet.Cells(5, 7).Value = fl_gravel_1
            
            wiliting_point_1 = xlSheet.Cells(5, 10).Value
            if (wiliting_point_1 == '' or wiliting_point_1 is None):
                wiliting_point_1 = 0.0
            print "Wiliting Point Level 1 (J) = " + str(wiliting_point_1)
            wp_1 = float(wiliting_point_1) / 100
            field_capacity_1 = xlSheet.Cells(5, 11).Value
            if (field_capacity_1 == '' or field_capacity_1 is None):
                field_capacity_1 = 0.0
            print "Field Capacity Level 1 (K) = " + str(field_capacity_1)
            fc_1 = float(field_capacity_1) / 100
            sat_hy_con_1 = xlSheet.Cells(5, 14).Value
            if (sat_hy_con_1 == '' or sat_hy_con_1 is None):
                sat_hy_con_1 = 0.0
            print "Saturated Hydraulic Conductivity Level 1 (N) = " + str(sat_hy_con_1)
            sa_1 = float(sat_hy_con_1)
            
            print "========================="
            # Process Level 2
            fl_sand_2 = 0.0
            fl_clay_2 = 0.0
            fl_organic_matter_2 = 0.0
            fl_gravel_2 = 0.0
        # Process for Layer 1    
            if (float(sand_2)):
                fl_sand_2 = float(sand_2) / 100
            if (float(clay_2)):
                fl_clay_2 = 1 - fl_sand_2 - (float(clay_2) / 100)
            if (float(organic_matter_2)):
                fl_organic_matter_2 = float(organic_matter_2) * 2
            if (float(gravel_2)):
                fl_gravel_2 = float(gravel_2) / 100
            print "Receive Input Level 2 : Sand = %s | Clay = %s | Organic Matter = %s | Gravel = %s" % (str(sand_2), str(clay_2), str(organic_matter_2), str(gravel_2))
            print "Receive Input Level 2 : Sand = %s | Clay = %s | Organic Matter = %s | Gravel = %s" % (str(fl_sand_2), str(fl_clay_2), str(fl_organic_matter_2), str(fl_gravel_2))
            xlSheet.Cells(6, 3).Value = fl_sand_2
            xlSheet.Cells(6, 4).Value = fl_clay_2
            xlSheet.Cells(6, 5).Value = fl_organic_matter_2
            xlSheet.Cells(6, 7).Value = fl_gravel_2
            
            wiliting_point_2 = xlSheet.Cells(6, 10).Value
            if (wiliting_point_2 == '' or wiliting_point_2 is None):
                wiliting_point_2 = 0.0
            print "Wiliting Point Level 2 (J) = " + str(wiliting_point_2)
            wp_2 = float(wiliting_point_2) / 100
            field_capacity_2 = xlSheet.Cells(6, 11).Value
            if (field_capacity_2 == '' or field_capacity_2 is None):
                field_capacity_2 = 0.0
            print "Field Capacity Level 2 (K) = " + str(field_capacity_2)
            fc_2 = float(field_capacity_2) / 100
            sat_hy_con_2 = xlSheet.Cells(6, 14).Value
            if (sat_hy_con_2 == '' or sat_hy_con_2 is None):
                sat_hy_con_2 = 0.0
            print "Saturated Hydraulic Conductivity Level 1 (N) = " + str(sat_hy_con_2)
            sa_2 = float(sat_hy_con_2)
            print "========================="
            values = [wp_1, fc_1, sa_1, wp_2, fc_2, sa_2]
            return values
    except Exception, err:
        xlBook.Close(SaveChanges=0)
        xlApp.Quit()
        sys.exit(err)      
def main():
    checkAndCreateFolder()
    print("-PREPROCESSING :")
    REAL_RUNABLE_EXCEL_FOLDER = prepareFacingModels()
    REAL_PATH_EXCEL_APPLICATION = os.path.join(REAL_RUNABLE_EXCEL_FOLDER, EXECUTABLE_EXE_FILE_EXCEL_APPLICATION)
    print("---Real Excel File is %s" % (REAL_PATH_EXCEL_APPLICATION))
    print("-START Step 1:")
    result = queryIDfollow_MU_GLOBAL()
    intRecord = recordsDATFile(result)
    if (intRecord == 1):
        print("-DONE Step 1---")
    else:
        print("----Problems----")
   
    print("-START Step 2 :")
    try:
        xlBook.Close()
    except:
        pass
    xlBook = xlApp.Workbooks.Open(REAL_PATH_EXCEL_APPLICATION)
    try:
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
                        name_sol = str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3])
                        output_model_value = []
                        output_model_value = acessModelToGetValue(xlBook, REAL_PATH_EXCEL_APPLICATION, item2[3], item2[5], item2[9], item2[15], item2[4], item2[6], item2[10], item2[16])
                        wiliting_point_l = output_model_value[0]
                        field_capacity_1 = output_model_value[1]
                        sat_hy_con_1 = output_model_value[2]
                        wiliting_point_2 = output_model_value[3]
                        field_capacity_2 = output_model_value[4]
                        sat_hy_con_2 = output_model_value[5]
                        print output_model_value
                        createSOILFile(wise3_id, name_sol, item2[3], item2[4], item2[5], item2[6], item2[7], item2[8], item2[9], item2[10], item2[11], item2[12], item2[13], item2[14], item2[15], item2[16], item2[17], item2[18], item2[19], item2[20], wiliting_point_l, wiliting_point_2, field_capacity_1, field_capacity_2, sat_hy_con_1, sat_hy_con_2)
    except Exception, err:
        print err
        xlBook.Close(SaveChanges=0)
        
    xlBook.Close(SaveChanges=0)
    xlApp.Quit()
    
    print("-DONE Step 2 :")
    print("-DAT File is located in %s" % (full_path + "Result" + "\\" + "DATFiles\<MU_GLOBAL>"))
    print("-SOL Files are located in %s" % (full_path + "Result" + "\\" + "SOLFiles\<MU_GLOBAL>"))
    print("-DELETE Temp Excel Model File")
    if (os.path.exists(REAL_RUNABLE_EXCEL_FOLDER)):
        try:
            shutil.rmtree(REAL_RUNABLE_EXCEL_FOLDER)
        except OSError:
            pass
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
