# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
ID = ""
APPROACH = ""
METHOD = ""
DATA_TYPE = ""
if (len(sys.argv) != 9):
    sys.exit("====[Error] : NOT ENOUGH ARGUMENT")
else:
  if (sys.argv[1] == '-ID'):
      if (sys.argv[2] is not None):
          ID = str(sys.argv[2]).strip()
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
      
  if (sys.argv[5] == '-method'):
      if (sys.argv[6] is not None):
          METHOD = str(sys.argv[6]).strip()
      else:
          sys.exit("====[Error] : Error Method")
  else:
      sys.exit("====[Error] : Error Method")
   
  if (sys.argv[7] == '-data_type'):
      if (sys.argv[8] is not None):
          DATA_TYPE = str(sys.argv[8]).strip()
      else:
          DATA_TYPE = 1
  else:
      sys.exit("====[Error] : Error Data Type")
      
  if (APPROACH == "ALL_AT_ONCE"):    
       cmd = "python Step_3_1_Run_Stage_1_Similarity_Model_All_At_One_Calculation.py -record_id %s -method %s -data_type %s" %(str(ID),str(METHOD),str(DATA_TYPE))    #print cmd
       os.system(cmd)
       cmd = "python Step_5_1_Run_Stage_2_Similarity_Model_UserInput_vs_Horizon_AWC_ORGC_Data_Follow_All_At_Once_Result.py -record_id %s -method %s" %(str(ID),str(METHOD))    #print cmd
       os.system(cmd)
  elif (APPROACH == "MULTI_STEP"):
       cmd = "python Step_3_2_Run_Stage_1_Similarity_Model_Multi_Step_Calculation.py -record_id %s -method %s -data_type %s" %(str(ID),str(METHOD),str(DATA_TYPE))    #print cmd
       os.system(cmd)
       cmd = "python Step_5_2_Run_Stage_2_Similarity_Model_UserInput_vs_Horizon_AWC_ORGC_Data_Follow_Multi_Step_Result.py -record_id %s -method %s" %(str(ID),str(METHOD))    #print cmd
       os.system(cmd) 
  else:
       sys.exit("====[Error] : Error Approach")
       
       
# Try to run : python Run_main_ISRIC_WISE_SOIL_Similarity_Project.py -ID <your id> -approach all_at_once -method cosine_vector_space_model
# or : python Run_main_ISRIC_WISE_SOIL_Similarity_Project.py -ID <your id> -approach multi_step -method cosine_vector_space_model