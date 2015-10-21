# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import time
import datetime
import sys
import os

from object import LandPKS_LandInfo

def is_Float(str):
    try:
        float(str)
        return True
    except ValueError:
        return False
def is_Int(str):
    try:
        int(float(str))
        return True
    except ValueError:
        return False
def occurrences(string, sub):
    try:
        count = start = 0
        while True:
            start = string.find(sub, start) + 1
            if start > 0:
                count+=1
            else:
                return count
    except:
        return 0
def count_value_in_string(value, string):
    return occurrences(string, value)

def convertStringToSet(string,deter):
    list = (str(string).upper()).split(deter)
    result_list = []
    for element in list:
        element = str(element).strip()
        result_list.append(element)
    return set(result_list) 
def checkIsSubset(smallSet, BigSet):
    if (smallSet.issubset(BigSet)):
        return True
    return False
def build_up_str_list_id(list_id):
    str_list_id = ""
    for id in list_id:
        id = str(id).strip()
        if (is_Int(id)):
             str_list_id = str_list_id + id + ","
    str_list_id = str_list_id + "0"
    return str_list_id
def checkParams(request_data):
     b_params = {}
     b_ids = False
     b_recorder_name = False
     b_name = False
     b_minlat = False
     b_minlong = False
     b_maxlat = False
     b_maxlong = False
     b_before_date = False
     b_after_date = False
     
     try:
         ids = str(request_data[LandPKS_LandInfo.PARAMS_ID]).strip().upper();
         b_ids = True
     except:
         b_ids = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_ID] = b_ids
     
     try:
         b_recorder_name = str(request_data[LandPKS_LandInfo.PARAMS_RECORDER_NAME]).strip().upper();
         b_recorder_name = True
     except:
         b_recorder_name = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] = b_recorder_name
     
     try:
         b_name = str(request_data[LandPKS_LandInfo.PARAMS_NAME]).strip().upper();
         b_name = True
     except:
         b_name = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_NAME] = b_name
     
     try:
         b_minlat = str(request_data[LandPKS_LandInfo.PARAMS_MIN_LAT]).strip().upper();
         b_minlat = True
     except:
         b_minlat = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] = b_minlat
     
     try:
         b_minlong = str(request_data[LandPKS_LandInfo.PARAMS_MIN_LONG]).strip().upper();
         b_minlong = True
     except:
         b_minlong = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] = b_minlong
     
     
     try:
         b_maxlat = str(request_data[LandPKS_LandInfo.PARAMS_MAX_LAT]).strip().upper();
         b_maxlat = True
     except:
         b_maxlat = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] = b_maxlat
     
     
     try:
         b_maxlong = str(request_data[LandPKS_LandInfo.PARAMS_MAX_LONG]).strip().upper();
         b_maxlong = True
     except:
         b_maxlong = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] = b_maxlong
     
     try:
         b_before_date = str(request_data[LandPKS_LandInfo.PARAMS_BEFORE_DATE]).strip().upper();
         b_before_date = True
     except:
         b_before_date = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] = b_before_date
     
     try:
         b_after_date = str(request_data[LandPKS_LandInfo.PARAMS_AFTER_DATE]).strip().upper();
         b_after_date = True
     except:
         b_after_date = False
         pass
     b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] = b_after_date
     
     return b_params
