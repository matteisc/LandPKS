# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len

import urllib2
import json

def request_rest_api_ISRIC(urlRequest):
    response = urllib2.urlopen(urlRequest)
    data = json.load(response)
    
    ORCDRC_LIST = []
    ORCDRC_LIST = [0,0,0,0,0,0]
    sd1_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd1"]) / 10
    sd2_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd2"]) / 10
    sd3_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd3"]) / 10
    sd4_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd4"]) / 10
    sd5_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd5"]) / 10
    sd6_orcdrc = float(data["properties"]["ORCDRC"]["M"]["sd6"]) / 10
    
    ORCDRC_LIST = [sd1_orcdrc,sd2_orcdrc,sd3_orcdrc,sd4_orcdrc,sd5_orcdrc,sd6_orcdrc]
    
    PHIHOX_LIST = []
    PHIHOX_LIST = [0,0,0,0,0,0]
    sd1_phihox = float(data["properties"]["PHIHOX"]["M"]["sd1"]) / 10
    sd2_phihox = float(data["properties"]["PHIHOX"]["M"]["sd2"]) / 10
    sd3_phihox = float(data["properties"]["PHIHOX"]["M"]["sd3"]) / 10
    sd4_phihox = float(data["properties"]["PHIHOX"]["M"]["sd4"]) / 10
    sd5_phihox = float(data["properties"]["PHIHOX"]["M"]["sd5"]) / 10
    sd6_phihox = float(data["properties"]["PHIHOX"]["M"]["sd6"]) / 10
    
    PHIHOX_LIST = [sd1_phihox,sd2_phihox,sd3_phihox,sd4_phihox,sd5_phihox,sd6_phihox]
    
    
    BLD_LIST = []
    BLD_LIST = [0,0,0,0,0,0]
    sd1_bld = float(data["properties"]["BLD"]["M"]["sd1"]) / 1000
    sd2_bld = float(data["properties"]["BLD"]["M"]["sd2"]) / 1000
    sd3_bld = float(data["properties"]["BLD"]["M"]["sd3"]) / 1000
    sd4_bld = float(data["properties"]["BLD"]["M"]["sd4"]) / 1000
    sd5_bld = float(data["properties"]["BLD"]["M"]["sd5"]) / 1000
    sd6_bld = float(data["properties"]["BLD"]["M"]["sd6"]) / 1000
    
    BLD_LIST = [sd1_bld,sd2_bld,sd3_bld,sd4_bld,sd5_bld,sd6_bld]
    
    CEC_LIST = []
    CEC_LIST = [0,0,0,0,0,0]
    sd1_cec = float(data["properties"]["CEC"]["M"]["sd1"])
    sd2_cec = float(data["properties"]["CEC"]["M"]["sd2"])
    sd3_cec = float(data["properties"]["CEC"]["M"]["sd3"])
    sd4_cec = float(data["properties"]["CEC"]["M"]["sd4"])
    sd5_cec = float(data["properties"]["CEC"]["M"]["sd5"])
    sd6_cec = float(data["properties"]["CEC"]["M"]["sd6"])
    
    CEC_LIST = [sd1_cec,sd2_cec,sd3_cec,sd4_cec,sd5_cec,sd6_cec]
    
    DRB = ""
    TAXGWRBMajor = data["properties"]["TAXGWRBMajor"]
    TAXGOUSDAMajor = data["properties"]["TAXGOUSDAMajor"]
    
    SOIL_GRIDS_LIST = [ORCDRC_LIST,PHIHOX_LIST,BLD_LIST,CEC_LIST,DRB,TAXGWRBMajor,TAXGOUSDAMajor]   
    return SOIL_GRIDS_LIST
    
#print request_rest_api_ISRIC("http://rest.soilgrids.org/query?lon=-102.5&lat=35.68")
