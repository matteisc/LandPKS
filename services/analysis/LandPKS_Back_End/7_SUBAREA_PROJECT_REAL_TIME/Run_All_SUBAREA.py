# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
import os
import sys

from support import support_SUBAREA
tif_countries = 'countryrastermap/Countries_Raster.tif'
if (len(sys.argv) <>  7):
   print("Not enough arguments")
   sys.exit("Usage : python Run_All_SUBAREA -x <Longtitude X Coordinate> -y <Latitude Y Coordinate> -ID <Record ID User Input>")
else:
    X_Coor = 0.00
    Y_Coor = 0.00
    ID = ""
    if (sys.argv[1] == '-x'):
        if (float(sys.argv[2])):
            X_Coor = float(sys.argv[2])
        else:
            sys.exit("====[Error] : Error in X")
    else:
        sys.exit("====[Error] : Error in X")
    
    if (sys.argv[3] == '-y'):
        if (float(sys.argv[4])):
            Y_Coor = float(sys.argv[4])
        else:
            sys.exit("====[Error] : Error in Y")
    else:
        sys.exit("====[Error] : Error in Y")
        
    if (sys.argv[5] == '-ID'):
        if (sys.argv[6] is not None):
            ID = str(sys.argv[6])
        else:
            sys.exit("====[Error] : Error in Folder")
    else:
        sys.exit("====[Error] : Error in Folder")

    os.system("python Step_2_main_SUBAREA_Real_Time.py -f Subarea_Files\Original_Subarea_Files -x %f -y %f -ID %s" %(X_Coor,Y_Coor,ID))
    country_identify = support_SUBAREA.getRasterValue_ThanhNH("E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" + tif_countries, X_Coor, Y_Coor)
    print "bat dau test " + str(country_identify)
    if (country_identify == 209 or str(country_identify) == '209'): #Kenya
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS1.SUB -opsname KY_Maize_HI.ops"%(X_Coor,Y_Coor,ID))
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS2.SUB -opsname KY_Grass.ops"%(X_Coor,Y_Coor,ID))
    elif (country_identify == 228 or str(country_identify) == '228'):#Namibia
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS1.SUB -opsname NM_Millet_HI.ops"%(X_Coor,Y_Coor,ID))
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS2.SUB -opsname NM_Grass.ops"%(X_Coor,Y_Coor,ID))
    elif (country_identify == 223 or str(country_identify) == '223'):#Angola
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS1.SUB -opsname NM_Millet_HI.ops"%(X_Coor,Y_Coor,ID))
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS2.SUB -opsname NM_Grass.ops"%(X_Coor,Y_Coor,ID))
    elif (country_identify == 205 or str(country_identify) == '205'):#Angola
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS1.SUB -opsname NM_Millet_HI.ops"%(X_Coor,Y_Coor,ID))
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS2.SUB -opsname NM_Grass.ops"%(X_Coor,Y_Coor,ID))
    else:
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS1.SUB -opsname NM_Millet_HI.ops"%(X_Coor,Y_Coor,ID))
        os.system("python Step_1_preprocessing_SUBAREA_Real_Time.py -x %f -y %f -ID %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/ -subname SUBS2.SUB -opsname NM_Grass.ops"%(X_Coor,Y_Coor,ID))
