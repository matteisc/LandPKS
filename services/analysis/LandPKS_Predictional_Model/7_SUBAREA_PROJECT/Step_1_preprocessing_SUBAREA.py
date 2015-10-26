# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import csv
import codecs
import struct

from osgeo import gdal, ogr
import numpy

in_locs = ""

# define
SUB_FILE_ORIGINAL_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\7_SUBAREA_PROJECT\\Subarea_Files\\Original_Subarea_Files"
SOI_FILE_ORIGINAL_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT\\Result_HWSD\\SOLFiles\\"
DLY_FILE_ORIGINAL_PATH = "C:\\xampp\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT\\Weather_Files\\Daily_Weather_Files\\"
DLY_DAT_FILE = "C:\\xampp\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT\\Weather_Files\\DATFiles\\WDLSTCOM.DAT"
PRE_SOICOM_DAT_FILE_PATH = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\3_WISE_SOL_PROJECT\\Result_HWSD\\DATFiles\\"
POS_SOICOM_DAT_FILE_PATH = "\\SOILCOM.DAT"

TIF_FOLDER_COLLECTION = ""
TIF_HWSD = 'soil_texture/HWSD_soil.tif'
tif_slate_weather = 'SLATE_Weather/tif/SLATE_raster1.tif'

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

def getRasterValue(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadRaster(px, py, 1, 1, buf_type=gdal.GDT_UInt16)  # Assumes 16 bit int aka 'short'
    intval = struct.unpack('h' , structval)  # use the 'short' format code (2 bytes) not int (4 bytes)
    return(intval[0])
def getRasterValue_ThanhNH(srcfile, mx, my):  # # Return the value of a raster at the point that is passed to it
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 

    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel

    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
    return structval[0][0]
if (len(sys.argv) < 4):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_SUBAREA.py -in <Input CSV File contains X and Y and name of SubFile> -tif <Folder path of TIF File>")
if (sys.argv[1] == '-in'):
    if (sys.argv[2] is None):
        sys.exit("Usage : python Step_1_preprocessing_SUBAREA.py -in <Input CSV File contains X and Y and name of SubFile> -tif <Folder path of TIF File>")
    else:
        in_locs = sys.argv[2]
        if (not os.path.exists(in_locs)):
            sys.exit("===[Error] : CSV Input File is NOT existed")
else:
    sys.exit("Usage : python Step_1_preprocessing_SUBAREA.py -in <Input CSV File contains X and Y and name of SubFile> -tif <Folder path of TIF File>")

if (sys.argv[3] == '-tif'):
    if (sys.argv[4] is None):
        sys.exit("Usage : python Step_1_preprocessing_SUBAREA.py -in <Input CSV File contains X and Y and name of SubFile> -tif <Folder path of TIF File>")
    else:
        TIF_FOLDER_COLLECTION = sys.argv[4]
        if (not os.path.exists(in_locs)):
            sys.exit("===[Error] : TIF Folder Collection is NOT existed")
else:
    sys.exit("Usage : python Step_1_preprocessing_SUBAREA.py -in <Input CSV File contains X and Y and name of SubFile> -tif <Folder path of TIF File>")

def main():
    f = open(in_locs, "rb")
    l = UnicodeReader(f)
    l.next()
    try:
        for row in l:
            id = row[0]
            if (id is None or id == ""):
                sys.exit("==[Error 21] : File CSV contains not enought data")
            if (float(row[2]) and float(row[1])):
                mx, my = float(row[2]), float(row[1])
            if (row[3] is None or row[3].strip() == ''):
                sys.exit("==[Error 21] : File CSV contains not enought data")

            sub_file_name = row[3].strip()
            full_path = os.path.join(SUB_FILE_ORIGINAL_PATH, sub_file_name)
            if (not os.path.exists(full_path)):
                sys.exit("==[Error 21] : One Sub File is Not existed" + str(full_path))
                
            mu_global = getRasterValue(os.path.join(TIF_FOLDER_COLLECTION, TIF_HWSD), mx, my)
            soil_file_name = row[4].strip()
            full_path_soil = os.path.join(SOI_FILE_ORIGINAL_PATH + "\\%s" % (str(mu_global)), soil_file_name)
            if (not os.path.exists(full_path_soil)):
                sys.exit("==[Error 21] : One SOIL File is Not existed" + str(full_path_soil))
                
            dly_name = getRasterValue_ThanhNH(os.path.join(TIF_FOLDER_COLLECTION, tif_slate_weather), mx, my)
            dly_name = str(dly_name) + "%s" %(".DLY")
            full_path_dly = os.path.join(DLY_FILE_ORIGINAL_PATH , dly_name)
            if (not os.path.exists(full_path_dly)):
                sys.exit("==[Error 21] : One DLY File is Not existed == " + str(full_path_dly))
            print "================================================="
            
    
            command = "python Step_2_main_SUBAREA.py -m %s -s %s %s%s%s -o 2_shortgrass.ops -default -d %s %s -x %f -y %f -tif %s -IDapex %s" % (sub_file_name, soil_file_name, PRE_SOICOM_DAT_FILE_PATH, str(mu_global), POS_SOICOM_DAT_FILE_PATH,dly_name, DLY_DAT_FILE,mx, my, TIF_FOLDER_COLLECTION, id)
            print("====Command : %s" % (command))
            os.system(command)
    except Exception, err:
        print err
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
