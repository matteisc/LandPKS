# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import sys
import os
try:
    from osgeo import gdal, ogr
    import numpy
except Exception, err:
    print err
    sys.exit("Please install GDAL for Python")
#######################################################################################    
tif_countries = 'countryrastermap/Countries_Raster.tif'
tif_elevation = 'GLOBAL_GIS_DATA/AFRICA_DEM/SRTM_MOSAIC1.tif'
##############THANH NGUYEN#############################################################
def getRasterValue_ThanhNH_Float(srcfile, mx, my):
    try:  # # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.float)
        return structval[0][0]
    except Exception,err:
        return -1
def getRasterValue_ThanhNH(srcfile, mx, my):  
    try:# # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception,err:
        return -1
def get_elevation(X,Y):
    return  getRasterValue_ThanhNH_Float("D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" + tif_elevation, X, Y);   
def check_exit_record(ID, dly_file_name):
   try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
   except:
       sys.exit("Please install MySQLLib for Python") 
   try: 
       cur = db.cursor()
       sql = "SELECT COUNT(1) FROM landpks_map_input_files WHERE ID = %s and dly_file_name = '%s'" % (ID , dly_file_name)
       cur.execute(sql)
       results = cur.fetchone()[0]
       if (results):
           return 1
       return 0
   except Exception, err:
       print err
       db.close()
       return 0
   finally:
       db.close()
     
def insert_data_X_Y_dly_name(ID, Y, X, dly_file_name):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python") 
    try:
       dly_file_name = dly_file_name.strip()
       if (check_exit_record(ID,dly_file_name) == 0):
           cur = db.cursor()
           str_ID = str(ID)
           str_X = str(X)
           str_Y = str(Y)
           str_dly_file_name = str(dly_file_name)
           cur.execute("INSERT INTO landpks_map_input_files VALUES (%s,%s,%s,%s,%s)" % (str_ID, str_ID, str_Y, str_X, str_dly_file_name))
           db.commit()
      
         
    except Exception, err:
        print err
        db.rollback()
        pass
    finally:
        db.close() 
def get_coordinate_follow_dly_file_name(str_dly_file_name):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python") 
    try:
       cur = db.cursor()
       str_dly_file_name = str_dly_file_name.strip()
       sql = "SELECT longitude, latitude FROM landpks_map_input_files WHERE dly_file_name = '%s'" % (str_dly_file_name)
       cur.execute(sql)
       results = cur.fetchone()
       if (results):
           X = results[0]
           Y = results[1]
           return str(X) + "|" + str(Y)
       return None
    except Exception, err:
        print err
        db.rollback()
        return None
        pass
    finally:
        db.close() 
def get_country_code_for_finding_closest_station(X,Y):  
    country_identify = getRasterValue_ThanhNH("D:/ThanhNguyen_Working/Python_APEX/TIF_FILE_COLLECTION/" + tif_countries, X, Y)
    if (country_identify == 209 or country_identify == "209"):  # Kenya
        return "KE"
    elif (country_identify == 228 or str(country_identify) == '228'):
        return "WA"
    else:
        return "KE"    
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
    line = line.replace("\t"," ")
    return line
###########################################################################################
########################NASIM GHAZAN#######################################################
###########################################################################################
import math
import decimal
_dir = "c:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Station_Data\\Africa\\countryName"
dly_folder = "C:\\xampp\\htdocs\\APEX\\Python_APEX\\2_WEATHER_PROJECT_REAL_TIME\\Weather_Station_Data\\DLY_Files"
D = 0.5  #Distance between 2 points in km
R = 6378.1 
#this method returns the distance between p0,p1 in kilometers  
def distance_on_unit_sphere(p0,p1):
    lat1 = p0[0]
    long1 = p0[1]
    lat2= p1[0]
    long2 = p1[1]
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    # Multiply arc by the radius of the earth in kilometers
    return arc* 6371 
#will find and return the closest station data to the user location
def findClosestStation(Long ,Lat ,countryName):
    InventoryFileName = _dir + "\\" + countryName + "_Inventory.txt"
    closest = ""
    stationsData = open(InventoryFileName).readlines()
    p0 = Lat, Long
    minDist = float("inf")
    for i, station in enumerate(stationsData) :
        if i>0 :
            properties = station.split("\t")
            stationLat = float(properties[3])
            stationLong = float(properties[4])
            p1 =  stationLat ,stationLong
            
            dist = distance_on_unit_sphere(p0, p1)

            if dist < minDist:
                minDist = dist
                closest = station.replace("\n", "") +str(dist)
    
    return closest
#this method will create the .dly file of the given station in current directory and returns the distance in km
def formatDLY(stationData ,dlyFileName):
    stationsDirectory = _dir + "\\Stations\\"
    stProp = stationData.split("\t")
    #Daily_countryName-provinceName-stationName-startYear-endYear.txt
    fileNameStr = "Daily_" + stProp[0] + "-" + stProp[1] + "-" + stProp[2] + "-" + stProp[6] + "-" + stProp[7] + ".txt"
    stationFileName = stationsDirectory + fileNameStr
    stData = open(stationFileName).readlines()
    hasRain = True
    hasWind = True
    if not "rain" in stData[0].split("\t")[4].lower():
        hasRain = False
    if not "wind" in stData[0].split("\t")[-2].lower():
        hasWind = False
    days = ""
    for i, day in enumerate(stData) :
        if i>0 :
            days += "\n"
            
            properties = day.split("\t")
            date = properties[0].split("/")
            #YEAR   MONTH    DAY    SRAD    TMAX    TMIN  
            days += date[2].rjust(6) + date[0].rjust(4) + date[1].rjust(4) + "0.000".rjust(6) +properties[1].rjust(6) + properties[2].rjust(6)
            #   PRCP
            if (not hasRain) or properties[4] == '':
                days += "0.00".rjust(6)
            else:
                 days += str("%5.2f"% decimal.Decimal(properties[4])).rjust(6)   
            #    RH 
            days += "0.00".rjust(6)
            # WSPD
            if (not hasWind) or properties[-2] == '':
                days += "0.000".rjust(6)
            else:
                days += str("%5.2f"% decimal.Decimal(properties[-2])).rjust(6)   
    f = open(dly_folder + "\\" + dlyFileName + ".DLY",'w')
    f.writelines(days[1:].encode("UTF-8"))
    f.close()
    #returns the distance from user location to station in km
    return(stProp[-1])
#This method will find the closest station to the user location within the country
#and send the station data to formatDLY method to create the .dly file in current directory
def formatClosestStationDLY(Long ,Lat ,countryName ,dlyFileName):
    global _dir
    _dir = _dir.replace("countryName",countryName)
    stationData = findClosestStation(Long, Lat, countryName);
    formatDLY(stationData, dlyFileName)
    return stationData
#######################################################################################################################################################
#Horizontal Bearing between 2 locations
def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) \
        - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    return math.atan2(y, x)


#was defined previously ,you may need to delete this one
#this method returns the distance between p0,p1 in kilometers
def distance_on_unit_sphere(p0,p1):

    lat1 = p0[0]
    long1 = p0[1]
    lat2= p1[0]
    long2 = p1[1]
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
    
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )

    # Multiply arc by the radius of the earth in kilometers
    return arc* 6371 


#this method will find and return the next point with distance d on the same line
def getNextPoint(brng, lat1, long1):
    
    _lat2 = math.asin( math.sin(lat1)*math.cos(D/R) +
         math.cos(lat1)*math.sin(D/R)*math.cos(brng))

    _long2 = long1 + math.atan2(math.sin(brng)*math.sin(D/R)*math.cos(lat1),
                 math.cos(D/R)-math.sin(lat1)*math.sin(_lat2))
    
    return _lat2,_long2


#This method will return an array of points in between loc1 and loc2 inclusive
#and prints the max height difference between these points
#Long = x , Lat = y
#long1,lat1 is user's location
#long2,lat2 is station's location
def getElevationVector(lat1, long1, lat2, long2):


    dist = distance_on_unit_sphere((lat1, long1),(lat2, long2))#distance between 2 points
    
    lat1 = math.radians(lat1) # lat point converted to radians
    long1 = math.radians(long1) # long point converted to radians

    lat2 = math.radians(lat2) # lat point converted to radians
    long2 = math.radians(long2) # long point converted to radians


    brng = calcBearing(lat1, long1, lat2, long2) #Bearing

    #number of points between loc1 and loc2
    count = int(math.floor(dist/D))

    #first point is loc1
    points = []
    points.append([])
    points[0] = lat1,long1,get_elevation(long1,lat1)
    
    for i in range(1,count+1):
        
        point = getNextPoint(brng,lat1,long1)

        lat1 = point[0]
        long1 = point[1]
        
        points.append([])
        points[i] = lat1,long1,get_elevation(long1,lat1)

    #last point is loc2
    points.append([])
    points[count+1] = lat2,long2,get_elevation(long1,lat1)

    #radian to degree for all points
    for i in range(0,count+2):
        points[i] = math.degrees(points[i][0]),math.degrees(points[i][1]),points[i][2]

##    #print the points
##    for i in range(0,count+2):        
##        print(str(points[i][0]) +","+str(points[i][1])
##              )#+","+str(points[i][2]))

    #print the max (h) - min(h) ,maximum height difference in whatever scale the method will return.
    heights = [row[2] for row in points]
    print(max(heights) - min(heights))

    return points
#getElevationVector(32.279549, -106.728230,32.363687, -106.790371)

#######################################################################################################################################################
def get_dly_folder():
    return dly_folder
