# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import shutil
import fileinput
import datetime
import time
import subprocess

from support import support_AWC
from __builtin__ import int

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
ACTION_FLAG = 1

if (len(sys.argv) <> 10 and len(sys.argv) <> 2):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Run_main_AWC.py -x <X Coordinate> -y <Y Coordinate> -mode <Path to folder of Rosetta model> -ID <Record ID>")
else:
    if (sys.argv[1] == '-run' and sys.argv[2] == '-x'):
        ACTION_FLAG = 1
        if (float(sys.argv[3])):
            X_Coor = float(sys.argv[3])
        else:
            sys.exit("====[Error] : Error in X")
        
        if (sys.argv[4] == '-y'):
            if (float(sys.argv[5])):
               Y_Coor = float(sys.argv[5])
            else:
               sys.exit("====[Error] : Error in Y")
        else:
            sys.exit("====[Error] : Error in Y")
        
                   
       
        if (sys.argv[6] == '-model'):
            if (sys.argv[7] is None) :
               sys.exit(message)
            else:
               if (os.path.exists(sys.argv[7])):
                   FULL_PATH_ROSETTA_APPLICATION = sys.argv[7]
               else:
                   sys.exit("==[Error] : Folder contains Rosetta Model is NOT Existed") 
               FULL_PATH_RUNABLE_ROSETTA_APPLICATION = os.path.join(FULL_PATH_ROSETTA_APPLICATION, EXECUTABLE_EXE_FILE_ROSETTA_APPLICATION)
               FULL_PATH_WEIGHTS_FOLDER_ROSETTA = os.path.join(FULL_PATH_ROSETTA_APPLICATION, "weights")
               print("\n---[Done] : Rosetta Model Application is in Folder %s" % (FULL_PATH_RUNABLE_ROSETTA_APPLICATION))     
        else:
            sys.exit("====[Error] : No defined Model")   
            
        if (sys.argv[8] == '-ID'):
            if (sys.argv[9] is None) :
               sys.exit(message)
            else:
               ID = str(sys.argv[9])    
               
    elif (sys.argv[1] == '-rm_real_time'):
        ACTION_FLAG = 0
    elif (sys.argv[1] == '-rm_all'):
        ACTION_FLAG = 2
    else:
        sys.exit("====[Error] : Error in X")
 
# Manage arguments
# Function
def prepareDistinguish_Input_Output_Folder_PerEachProcess():
    current = time.time()
    output_direction = full_path + "\Rosetta_Model_Application\Output\%s" % str(current)
    if not os.path.exists(output_direction):
        os.makedirs(output_direction)
    input_direction = full_path + "\Rosetta_Model_Application\Input\%s" % str(current)
    if not os.path.exists(input_direction):
        os.makedirs(input_direction)
    return str(current)
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
    if (ACTION_FLAG == 1):
       # Get Rock Fragment Value
       ROCK_FRAGMENT_LIST = [0,0,0,0,0,0,0]
       ROCK_FRAGMENT_LIST = support_AWC.get_list_value_of_rock_fragment(ID)
       
       TEXTURE_SOIL_LAYER = support_AWC.get_values_texture_for_soil_horizon(ID)
       if (TEXTURE_SOIL_LAYER is None):
            sys.exit("====[ERROR 303] : Cannot find any data about Soil Layer Texture]")
   
       BIG_LIST = support_AWC.get_collection_value_from_all_layer_texture(TEXTURE_SOIL_LAYER)
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
        
       folder_name = prepareDistinguish_Input_Output_Folder_PerEachProcess()
       OUTPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Output\%s" % str(folder_name)
       INPUT_ROSETTA_MODEL_FILE_PATH = full_path + "\Rosetta_Model_Application\Input\%s" % str(folder_name)
       output_model_value = []
       output_model_value = acessModelToGetValue(ID, FULL_PATH_RUNABLE_ROSETTA_APPLICATION, FULL_PATH_WEIGHTS_FOLDER_ROSETTA, INPUT_ROSETTA_MODEL_FILE_PATH, OUTPUT_ROSETTA_MODEL_FILE_PATH, SAND_LIST, SILT_LIST, CLAY_LIST, BULK_DENSITY_LIST, TOT_C_LIST, W3CLD_LIST, W15AD_LIST)
       FIELD_CAPACITY_LIST = output_model_value[1]
       WILTING_POINT_LIST = output_model_value[2]
       EXAMPLE_AWC = [-9.9,-9.9,-9.9,-9.9,-9.9,-9.9,-9.9]
       CENTIMES_AWC = [-9.9,-9.9,-9.9,-9.9,-9.9,-9.9,-9.9]
       soil_profile_awc = 0
       for i in range(0, NUMBER_LAYERS_SOL_FILE):
           EXAMPLE_AWC[i] = FIELD_CAPACITY_LIST[i] - WILTING_POINT_LIST[i]   
           if (i==0):
               depth_layer_cm = LAYER_1[1] - LAYER_1[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_1[1] - LAYER_1[0])
           elif (i==1):
               depth_layer_cm = LAYER_2[1] - LAYER_2[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_2[1] - LAYER_2[0])
           elif (i==2):
               depth_layer_cm = LAYER_3[1] - LAYER_3[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_3[1] - LAYER_3[0])
           elif (i==3):
               depth_layer_cm = LAYER_4[1] - LAYER_4[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_4[1] - LAYER_4[0])
           elif (i==4):
               depth_layer_cm = LAYER_5[1] - LAYER_5[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_5[1] - LAYER_5[0])
           elif (i==5):
               depth_layer_cm = LAYER_6[1] - LAYER_6[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_6[1] - LAYER_6[0])
           elif (i==6):
               depth_layer_cm = LAYER_7[1] - LAYER_7[0]
               soil_depth_cm =  depth_layer_cm - (depth_layer_cm*ROCK_FRAGMENT_LIST[i])
               CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(soil_depth_cm)
               #CENTIMES_AWC[i] = EXAMPLE_AWC[i]*(LAYER_7[1] - LAYER_7[0])
           print ("\n Da chay gia tri moi : rock_fragment : %s ; example_awc : %s ; centimes_awc : %s " %(str(ROCK_FRAGMENT_LIST[i]),str(EXAMPLE_AWC[i]),str(CENTIMES_AWC[i])))
           soil_profile_awc = float(soil_profile_awc) + CENTIMES_AWC[i]    
       result = support_AWC.insert_rosetta_value_awc_output(ID, '', Y_Coor, X_Coor, FIELD_CAPACITY_LIST, WILTING_POINT_LIST,EXAMPLE_AWC, CENTIMES_AWC, soil_profile_awc) 
       
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
    elif (ACTION_FLAG == 0):
       print "Thanh Nguyen"
    elif (ACTION_FLAG == 2):
       print "Thanh Nguyen" 
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
