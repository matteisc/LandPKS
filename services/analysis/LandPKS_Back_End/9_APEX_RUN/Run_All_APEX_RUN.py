# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
import os
import sys
X_COOR = 0.0
Y_COOR = 0.0
ID = ""

if (sys.argv[1] == '-x'):
   if (float(sys.argv[2])):
       X_COOR = float(sys.argv[2])
else:
   sys.exit("===[Error] : Not enough values")
if (sys.argv[3] == '-y'):
     if (float(sys.argv[4])):
       Y_COOR = float(sys.argv[4])
else:
   sys.exit("===[Error] : Not enough values")

if (sys.argv[5] == '-ID'):
   ID = sys.argv[6]
else:
   sys.exit("===[Error] : Not enough values")


os.system("python Step_1_preprocessing_APEX_RUN_real_time.py -x %f -y %f -id %s -tif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" %(X_COOR,Y_COOR,str(ID)))
