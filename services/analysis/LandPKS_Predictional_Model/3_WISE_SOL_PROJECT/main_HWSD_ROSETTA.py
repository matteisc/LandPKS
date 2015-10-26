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
    sys.exit("Usage : python main_HWSD_ROSETTA.py -d <Database File Path> -m <MU_GLOBAL> -model <Rosetta Model Application Full Path>")
        
# Input requires
message = "Usage : python main_HWSD_ROSETTA.py -d <Database File Path> -m <MU_GLOBAL> -model <Rosetta Model Application Full Path>"
db_file = ""
mu_global = ""
output_file = ""
full_path = os.getcwd() + "\\"
datDirectory = ""
solDirectory = ""
name_sol = ""

FULL_PATH_ROSETTA_APPLICATION = ""
EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION = "rosetta.exe"

FULL_PATH_RUNABLE_ROSETTA_APPLICATION = ""
FULL_PATH_WEIGHTS_FOLDER_ROSETTA = ""

OUTPUT_ROSETTA_MODEL_FILE_PATH = ""
INPUT_ROSETTA_MODEL_FILE_PATH = ""

# Manage arguments
if (sys.argv[1] == '-d') :
    if (sys.argv[2] is None) :
        sys.exit(message)
    else:
        #db_file = full_path + sys.argv[2]
        db_file = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT" + sys.argv[2]
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
        FULL_PATH_RUNABLE_ROSETTA_APPLICATION = os.path.join(FULL_PATH_ROSETTA_APPLICATION,EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION)
        FULL_PATH_WEIGHTS_FOLDER_ROSETTA = os.path.join(FULL_PATH_ROSETTA_APPLICATION,"weights")
        print("\n---[Done] : Rosetta Model Application is in Folder %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION))     
else:
    sys.exit(message)

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
                #strContent = "    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                strContent = "    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1])  + str(item[3]))
            else:
                if (count >= 2 and count <= 9):
                    #strContent = "\n    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n    %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1])  + str(item[3]))
                elif (count >= 10 and count <= 99):
                    #strContent = "\n   %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n   %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1])  + str(item[3]))
                elif (count >= 100 and count <= 999):
                    #strContent = "\n  %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n  %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1])  + str(item[3]))
                elif (count >= 1000 and count <= 9999):
                    #strContent = "\n %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
                    strContent = "\n %d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1])  + str(item[3]))
                elif (count >= 10000 and count <= 99999):
                    #strContent = "\n%d %s.SOL" % (count, str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3]))
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
    inputRosettaModel = full_path + "\Rosetta_Model_Application\Input"
    if not os.path.exists(inputRosettaModel):
        os.makedirs(inputRosettaModel)
    outputRosettaModel = full_path + "\Rosetta_Model_Application\Output"
    if not os.path.exists(outputRosettaModel):
        os.makedirs(outputRosettaModel)
def acessModelToGetValue(seq,FULL_PATH_RUNABLE_ROSETTA_APPLICATION,FULL_PATH_WEIGHTS_FOLDER_ROSETTA,INPUT_ROSETTA_MODEL_FILE_PATH,OUTPUT_ROSETTA_MODEL_FILE_PATH, sand_top, silt_top, clay_top, bulk_dens_top, tot_c_1, w3cld_1, w15ad_1, sand_sub, silt_sub, clay_sub, bulk_dens_sub, tot_c_2, w3cld_2, w15ad_2):
    values = []
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
        if (seq is None or not int(seq)):
            seq = 1
        strSeq = str(seq)
        strContent = "";
        number_space = 16 - len(strSeq)
        strContent = "%s" %(strSeq)
        for i in range(1,number_space):
            strContent = strContent + " "
        
        # Process top
        strContent = strContent + "      top"
        
        #Process hz_tp
        strContent = strContent + "        0"
        
        #Process hz_bt
        strContent = strContent + "      30"
        
        #process sand_top
        fl_sand_top = float(sand_top)
        number_space = 11 - len(str("%0.2f" %(fl_sand_top)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_sand_top)
        
         #process silt_top
        fl_silt_top = float(silt_top)
        number_space = 12 - len(str("%0.2f" %(fl_silt_top)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_silt_top)
        
         #process clay_top
        fl_clay_top = 100 - fl_sand_top - fl_silt_top
        number_space = 12 - len(str("%0.2f" %(fl_clay_top)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_clay_top)
        
        
         #process Bulk Denstity
        fl_bulk_dens_top = float(bulk_dens_top)
        number_space = 13 - len(str("%0.2f" %(fl_bulk_dens_top)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_bulk_dens_top)
        
        #process Top C 1
        fl_tot_c_1 = float(tot_c_1)
        number_space = 8 - len(str("%0.2f" %(fl_tot_c_1)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_tot_c_1)
        
        #process W3 CLD 1
        fl_w3cld_1 = float(w3cld_1)
        number_space = 8 - len(str("%0.2f" %(fl_w3cld_1)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_w3cld_1)
        
        #process Top C 1
        fl_w15ad_1 = float(w15ad_1)
        number_space = 8 - len(str("%0.2f" %(fl_w15ad_1)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_w15ad_1)
        
        fo.write(strContent)
    
        # Line 4 ============ SUB LAYER
        fo.write("\n")
        
        # Process for seq
        if (seq is None or not int(seq)):
            seq = 2
        strContent = "";
        number_space = 16 - len(strSeq)
        strContent = "%s" %(strSeq)
        for i in range(1,number_space):
            strContent = strContent + " "
        
        # Process top
        strContent = strContent + "      sub"
        
        #Process hz_tp
        strContent = strContent + "       30"
        
        #Process hz_bt
        strContent = strContent + "     100"
        
        #process sand_top
        fl_sand_sub = float(sand_sub)
        number_space = 11 - len(str("%0.2f" %(fl_sand_sub)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_sand_sub)
        
         #process silt_top
        fl_silt_sub = float(silt_sub)
        number_space = 12 - len(str("%0.2f" %(fl_silt_sub)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_silt_sub)
        
         #process clay_top
        fl_clay_sub = 100 - fl_sand_sub - fl_silt_sub
        number_space = 12 - len(str("%0.2f" %(fl_clay_sub)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_clay_sub)
        
        
         #process Bulk Denstity
        fl_bulk_dens_sub = float(bulk_dens_sub)
        number_space = 13 - len(str("%0.2f" %(fl_bulk_dens_sub)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_bulk_dens_sub)
        
        #process Top C 1
        fl_tot_c_2 = float(tot_c_2)
        number_space = 8 - len(str("%0.2f" %(fl_tot_c_2)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_tot_c_2)
        
        #process W3 CLD 1
        fl_w3cld_2 = float(w3cld_2)
        number_space = 8 - len(str("%0.2f" %(fl_w3cld_2)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_w3cld_2)
        
        #process Top C 1
        fl_w15ad_2 = float(w15ad_2)
        number_space = 8 - len(str("%0.2f" %(fl_w15ad_2)))
        for i in range(1,number_space):
            strContent = strContent + " "
        strContent = strContent + " %0.2f" %(fl_w15ad_2)
        
        fo.write(strContent)
        fo.close()
        # Finish Step 1
        
        # Start Step 2 : RUN MODEL
        command = "%s %s 3 %s %s" %(FULL_PATH_RUNABLE_ROSETTA_APPLICATION,FULL_PATH_WEIGHTS_FOLDER_ROSETTA, os.path.join(INPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_in.txt"),os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt"))
        os.system(command)
        # Start Step 3 : Read data from output of Roseta Model
        output_file = os.path.join(OUTPUT_ROSETTA_MODEL_FILE_PATH, str(seq) + "_out.txt")
        with open(output_file,'r') as file:
            data = file.readlines()
        if (len(data) <> 4):
            sys.exit("==[Error] : Output data %s is NOT correct" %(output_file))
        line_top = data[2]
        line_sub = data[3]
        ######Process Data Top
        line_top = standard_string(line_top)
        data_top = line_top.split(' ')
        str_theta_r_top = data_top[2]
        str_theta_s_top = data_top[3]
        str_theta_alpha_top = data_top[4]
        str_n_par_top = data_top[5]
        str_K_s_top = data_top[6]
        str_K_o_top = data_top[7]
        str_L_top = data_top[8]
        
        ######Check data
        if (float(str_theta_r_top) and float(str_theta_s_top) and float(str_theta_alpha_top) and float(str_n_par_top) and float(str_K_s_top) and float(str_K_o_top) and float(str_L_top)):
            fl_theta_r_top = float(str_theta_r_top)
            fl_theta_s_top = float(str_theta_s_top)
            fl_theta_alpha_top = float(str_theta_alpha_top)
            fl_n_par_top = float(str_n_par_top)
            fl_K_s_top = float(str_K_s_top)
            fl_K_o_top = float(str_K_o_top)
            fl_L_top = float(str_L_top)
        else:
            sys.exit("===[Error] : Data from output file is not correct")
        #####Calculate
        sat_hy_cond_1 = calculate_Saturated_Hydraulic_Conductivity(fl_K_s_top)
        field_capacity_1 = calculate_Field_Capacity(fl_theta_r_top, fl_theta_s_top, fl_theta_alpha_top, fl_n_par_top)
        wilting_point_1 = calculate_Wilting_Point(fl_theta_r_top, fl_theta_s_top, fl_theta_alpha_top, fl_n_par_top)
        
        
        ######Process Data SUB
        line_sub = standard_string(line_sub)
        data_sub = line_sub.split(' ')
        str_theta_r_sub = data_sub[2]
        str_theta_s_sub = data_sub[3]
        str_theta_alpha_sub = data_sub[4]
        str_n_par_sub = data_sub[5]
        str_K_s_sub = data_sub[6]
        str_K_o_sub = data_sub[7]
        str_L_sub = data_sub[8]
        
        ######Check data
        if (float(str_theta_r_sub) and float(str_theta_s_sub) and float(str_theta_alpha_sub) and float(str_n_par_sub) and float(str_K_s_sub) and float(str_K_o_sub) and float(str_L_sub)):
            fl_theta_r_sub = float(str_theta_r_sub)
            fl_theta_s_sub = float(str_theta_s_sub)
            fl_theta_alpha_sub = float(str_theta_alpha_sub)
            fl_n_par_sub = float(str_n_par_sub)
            fl_K_s_sub = float(str_K_s_sub)
            fl_K_o_sub = float(str_K_o_sub)
            fl_L_sub = float(str_L_sub)
        else:
            sys.exit("===[Error] : Data from output file is not correct")
        #####Calculate
        sat_hy_cond_2 = calculate_Saturated_Hydraulic_Conductivity(fl_K_s_sub)
        field_capacity_2 = calculate_Field_Capacity(fl_theta_r_sub, fl_theta_s_sub, fl_theta_alpha_sub, fl_n_par_sub)
        wilting_point_2 = calculate_Wilting_Point(fl_theta_r_sub, fl_theta_s_sub, fl_theta_alpha_sub, fl_n_par_sub)
        values = [wilting_point_1, field_capacity_1, sat_hy_cond_1, wilting_point_2, field_capacity_2, sat_hy_cond_2]
        
        print values
        return values
    except Exception, err:
        sys.exit(err)
def calculate_Saturated_Hydraulic_Conductivity(input_float_Ks_rosetta):
    return float(input_float_Ks_rosetta)
def calculate_Field_Capacity(float_theta_r, float_theta_s, float_alpha, float_n_par):
    try:
        import math
        sh1 = float_theta_r
        
        tu1 = float_theta_s - float_theta_r
        pt1 = (1 + math.pow((float_alpha*330),float_n_par))
        pt2 = 1 - (1/float_n_par)
        mau1 = math.pow(pt1, pt2)
        
        sh2 = tu1/mau1
        
        return sh1 + sh2
    except Exception,err:
        print err
        return 0
def calculate_Wilting_Point(float_theta_r, float_theta_s, float_alpha, float_n_par):
    try:
        import math
        sh1 = float_theta_r
        
        tu1 = float_theta_s - float_theta_r
        pt1 = (1 + math.pow((float_alpha*15000),float_n_par))
        pt2 = 1 - (1/float_n_par)
        mau1 = math.pow(pt1, pt2)
        
        sh2 = tu1/mau1
        
        return sh1 + sh2
    except Exception,err:
        print err
        return 0

def standard_string(line):
    line = line.strip()
    line = line.replace("         "," ")
    line = line.replace("        "," ")
    line = line.replace("       "," ")
    line = line.replace("      "," ")
    line = line.replace("     "," ")
    line = line.replace("    "," ")
    line = line.replace("   "," ")
    line = line.replace("  "," ")
    return line   
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
                        print item2
                        for i in range(0,len(item2)-1):
                            if (item2[i] is None):
                                item2[i] = 0
                        #name_sol = str(item[0]) + str(mu_global) + str(item[1]) + str(int(item[2])) + str(item[3])
                        name_sol = str(item[0]) + str(mu_global) + str(item[1]) + str(item[3])
                        output_model_value = []
                        output_model_value = acessModelToGetValue(item[0],FULL_PATH_RUNABLE_ROSETTA_APPLICATION,FULL_PATH_WEIGHTS_FOLDER_ROSETTA,INPUT_ROSETTA_MODEL_FILE_PATH,OUTPUT_ROSETTA_MODEL_FILE_PATH, item2[3], item2[5], item2[21], item2[17], -9.9, -9.9, -9.9, item2[4], item2[6], item2[22], item2[18], -9.9, -9.9, -9.9)
                        wiliting_point_l = output_model_value[0]
                        field_capacity_1 = output_model_value[1]
                        sat_hy_con_1 = output_model_value[2]
                        wiliting_point_2 = output_model_value[3]
                        field_capacity_2 = output_model_value[4]
                        sat_hy_con_2 = output_model_value[5]
                        createSOILFile(wise3_id, name_sol, item2[3], item2[4], item2[5], item2[6], item2[7], item2[8], item2[9], item2[10], item2[11], item2[12], item2[13], item2[14], item2[15], item2[16], item2[17], item2[18], item2[19], item2[20], wiliting_point_l, wiliting_point_2, field_capacity_1, field_capacity_2, sat_hy_con_1, sat_hy_con_2)
    except Exception, err:
        print err
        
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
