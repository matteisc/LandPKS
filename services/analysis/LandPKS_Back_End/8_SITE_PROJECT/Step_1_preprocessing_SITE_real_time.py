# Author : Thanh Nguyen
# 05/23/2014
# Read X and Y coordinate => Find WTG File via GDAL and TIF File => Map between WTG FIle and DLY File
# ?/usr/local/bin
__version__ = "1"
from osgeo import gdal, ogr
import struct,os, sys
import numpy

full_path = os.getcwd() + "\\"

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

# Check arguments
PRIVATE_FOLDER_ACCESS = ""
PRIVATE_FOLDER_ACCESS_DAT = ""
PRIVATE_FOLDER_ACCESS_SOL = ""
X_COOR = 0.0
Y_COOR = 0.0
site_file_name = ""
if (len(sys.argv) < 9):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")
# Input filenames
tif_ELEVATION = 'elevation/elevation.tif'
if (sys.argv[1] == '-x'):
   if (float(sys.argv[2])):
       X_COOR = float(sys.argv[2])
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")
if (sys.argv[3] == '-y'):
     if (float(sys.argv[4])):
       Y_COOR = float(sys.argv[4])
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")

if (sys.argv[5]== '-id'):
   site_file_name = sys.argv[6]
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")

if (sys.argv[7]== '-tif'):
   src_dir = sys.argv[8]
else:
   sys.exit("Usage : python Step_1_preprocessing_SITE_real_time.py -x <X Longtitude> -y <Y Latitude> -id <name and ID> -tif <Directory to Folder contain all TIF Files>")
def createPrivateFolder_DAT():
   PRIVATE_FOLDER_ACCESS_DAT = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\8_SITE_PROJECT\\Site_Files\\Private\\%s" % (str(site_file_name)), "DAT")
   if (not os.path.exists(PRIVATE_FOLDER_ACCESS_DAT)):
        os.makedirs(PRIVATE_FOLDER_ACCESS_DAT)
   return PRIVATE_FOLDER_ACCESS_DAT 
def createPrivateFolder_SOL():
   PRIVATE_FOLDER_ACCESS_SOL = os.path.join("C:\\xampp\\htdocs\\APEX\\Python_APEX\\8_SITE_PROJECT\\Site_Files\\Private\\%s" % (str(site_file_name)), "SITE")
   if (not os.path.exists(PRIVATE_FOLDER_ACCESS_SOL)):
        os.makedirs(PRIVATE_FOLDER_ACCESS_SOL)
   return PRIVATE_FOLDER_ACCESS_SOL 
def checkAndCreateFolder():
    directory = full_path + "\Site_Files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\%s" % ("DAT_Files")
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
    siteDirectory = directory + "\%s" % ("Site_Files")
    if not os.path.exists(siteDirectory):
        os.makedirs(siteDirectory)    
def createSOILFile(site_file_name,elevation,X,Y,PRIVATE_FOLDER_ACCESS_SOL):
    try:
        path = PRIVATE_FOLDER_ACCESS_SOL + "\%s.SIT" %("SITE_" + str(site_file_name))
        #print path
        #fo = open(os.path.join(PRIVATE_FOLDER_ACCESS_SOL,"%s.SIT" %("SITE_" + str(site_file_name)), "wb"))
        fo = open(path, "wb")
        # print("Tham khao %d  %d" %(t_caco3,s_caco3))
        print("---Write SIT property to File %s.SIT" % (str(site_file_name)))
        # Line 1
        length = len(site_file_name)
        space_number = 81 - length
        strContent = ""
        for i in range(1, space_number):
            strContent = strContent + " "
        strContent = strContent + site_file_name
        fo.write(strContent)
        # Line 2
        full_site_file_name = site_file_name + ".SIT"
        length = len(full_site_file_name)
        space_number = 81 - length
        strContent = ""
        for i in range(1, space_number):
            strContent = strContent + " "
        strContent = strContent + full_site_file_name
        fo.write("\n" + strContent)
        # Line 3
        fo.write("\n                                                                        %s" % ("OUTLET 1"))
        # Line 4 
        fo.write("\n")
          #Field 1  Y Coor
        if (Y >= 0 and Y < 10):
            strContent = "    %0.2f" % (Y)
        elif (Y >= 10 and Y < 100):
            strContent = "   %0.2f" % (Y)
        elif (Y >= 100 and Y < 1000):
            strContent = "  %0.2f" % (Y)
        elif (Y >= 1000 and Y < 10000):
            strContent = " %0.2f" % (Y)
        elif (Y >= 10000 and Y < 100000):
            strContent = "%0.2f" % (Y)
        elif (Y < 0 and Y > -10):
            strContent = "   %0.2f" % (Y)
        elif (Y <= -10 and Y > -100):
            strContent = "  %0.2f" % (Y)
        elif (Y <= -100 and Y > -1000):
            strContent = " %0.2f" % (Y)
        elif (Y <= -1000 and Y > -10000):
            strContent = "0.2f" % (Y)
        fo.write(strContent)
           #Field 2  X Coor
        if (X >= 0 and X < 10):
            strContent = "    %0.2f" % (X)
        elif (X >= 10 and X < 100):
            strContent = "   %0.2f" % (X)
        elif (X >= 100 and X < 1000):
            strContent = "  %0.2f" % (X)
        elif (X >= 1000 and X < 10000):
            strContent = " %0.2f" % (X)
        elif (X >= 10000 and X < 100000):
            strContent = "%0.2f" % (X)
        elif (X < 0 and X > -10):
            strContent = "   %0.2f" % (X)
        elif (X <= -10 and X > -100):
            strContent = "  %0.2f" % (X)
        elif (X <= -100 and X > -1000):
            strContent = " %0.2f" % (X)
        elif (X <= -1000 and X > -10000):
            strContent = "0.2f" % (X)
        fo.write(strContent)
        
          #Field 3  Elevation
        if (elevation >= 0 and elevation < 10):
            strContent = "    %0.2f" % (elevation)
        elif (elevation >= 10 and elevation < 100):
            strContent = "   %0.2f" % (elevation)
        elif (elevation >= 100 and elevation < 1000):
            strContent = "  %0.2f" % (elevation)
        elif (elevation >= 1000 and elevation < 10000):
            strContent = " %0.2f" % (elevation)
        elif (elevation >= 10000 and elevation < 100000):
            strContent = "%0.2f" % (elevation)
        elif (elevation < 0 and elevation > -10):
            strContent = "   %0.2f" % (elevation)
        elif (elevation <= -10 and elevation > -100):
            strContent = "  %0.2f" % (elevation)
        elif (elevation <= -100 and elevation > -1000):
            strContent = " %0.2f" % (elevation)
        elif (elevation <= -1000 and elevation > -10000):
            strContent = "0.2f" % (elevation)
        fo.write(strContent)
        
          #Field 4  
        fo.write("    %0.2f" % (1))
          #Field 5  n
        fo.write("    %0.2f" % (0))
          #Field 6  n
        fo.write("    %0.2f" % (0))
          #Field 7  n
        fo.write("    %0.2f" % (0.8))
          #Field 8  n
        fo.write("    %0.2f" % (0))
          #Field 9  n
        fo.write("    %0.2f" % (0))
        
        #Line 5
        fo.write("\n                                                                                ")
        #Line 6
        fo.write("\n                                                                                ")
        #Line 7
        fo.write("\n       %d       %d       %d       %d       %d       %d       %d       %d       %d       %d" %(0,0,0,0,0,0,0,0,0,0))
        #Line 8
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f" %(0,0,0,0,0,0,0,0,0,0))
        #Line 9
        fo.write("\n\n");
        #Line 10
        fo.write("                                                                                \n")
        fo.close()
    except Exception, err:
        fo.close()
        sys.exit("Error : %s" % (err))
    finally:
        print("Done")
        fo.close()
def getRasterValue_ThanhNH(srcfile, mx, my):
    src_ds = gdal.Open(srcfile) 
    gt = src_ds.GetGeoTransform() 
    # Convert from map to pixel coordinates.
    px = int((mx - gt[0]) / gt[1])  # x pixel
    py = int((my - gt[3]) / gt[5])  # y pixel
    rb = src_ds.GetRasterBand(1)
    structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
    return structval[0][0]           
def main():
   try:
       PRIVATE_FOLDER_ACCESS_DAT = createPrivateFolder_DAT()
       PRIVATE_FOLDER_ACCESS_SOL = createPrivateFolder_SOL()
       print PRIVATE_FOLDER_ACCESS_SOL
       print "================================================="
       elevation = getRasterValue_ThanhNH(src_dir + tif_ELEVATION, X_COOR, Y_COOR)
       print "X = " + str(X_COOR)
       print "Y = " + str(Y_COOR)
       print "Elevation = " + str(elevation)
       
       print("-PREPROCESSING : Create Folders--")
       checkAndCreateFolder()
       print("-Create File and Folder already")
       print("-Create SITE Files")
       createSOILFile(site_file_name,elevation,X_COOR,Y_COOR,PRIVATE_FOLDER_ACCESS_SOL) 
       print("-Site File is created already")
       print "python Step_2_main_SITE.py -fsite %s -fdat %s" %(PRIVATE_FOLDER_ACCESS_SOL,PRIVATE_FOLDER_ACCESS_DAT)
       os.system("python Step_2_main_SITE.py -fsite %s -fdat %s" %(PRIVATE_FOLDER_ACCESS_SOL,PRIVATE_FOLDER_ACCESS_DAT))
   except Exception,err:
       sys.exit(err)
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
