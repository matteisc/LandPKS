# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
if (len(sys.argv) < 6):
    os.system("python Step_1_preprocessing_SITE.py -in C:/xampp/htdocs/APEX/Python_APEX/8_SITE_PROJECT/map_location.csv -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/")
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
        
    os.system("python Step_1_preprocessing_SITE_real_time.py -x %f -y %f -id %s -tif E:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" %(X_Coor,Y_Coor,ID))
