# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
import os
os.system("python Step_2_main_SUBAREA.py -f Subarea_Files\Original_Subarea_Files")
os.system("python Step_1_preprocessing_SUBAREA.py -in C:/xampp/htdocs/APEX/Python_APEX/7_SUBAREA_PROJECT/map_location_subarea.csv -tif D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/")
