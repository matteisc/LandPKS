'''
Created on Apr 21, 2015

@author: Thanh Nguyen Hai
'''
import cherrypy
import json
from database_layer import LandPKS_Database_Driver
from utility import LandPKS_Ultility
from object import LandPKS_LandCover, LandPKS_LandInfo
from mhlib import isnumeric
from numpy.distutils.fcompiler import vast
import os
import sys
from urllib import urlencode
import types
from numpy.oldnumeric.linear_algebra import determinant
import time
import datetime

from auth import AuthController, require, member_of, name_is, check_credentials
SESSION_KEY = '_cp_username'

CURRENT_VERSION = 0.1
'''
Configuration
'''
ACCESS_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/LandPKS_API_System/api/port8080=cherrypd_server+cherrypy_framework/log/%s_8080_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/LandPKS_API_System/api/port8080=cherrypd_server+cherrypy_framework/log/%s_8080_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))


CORE_BACK_END_MAIN_LANPKS = "C:/xampp/htdocs/APEX/Python_APEX/1_CONTROLLER_PROJECT/"
def prepare_response(data,format="JSON"):
    return "Da converted"
def return_response_error(code,type,mess,format="JSON"):
    if (format=="JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.headers['Retry-After']=60
        cherrypy.response.status = code
        message = {type:mess}
        return json.dumps(message)
    else:
        return "Not support yet"
def return_success_response_put(code,id,object,name,recorder_name,status,version,detail):
    cherrypy.response.headers['Content-Type'] = "application/json"
    cherrypy.response.headers['Retry-After']=60
    cherrypy.response.status = code
    message = {'id':id, 'object':object,'name':name,'recorder_name':recorder_name,'status':status,'version':version,'detail':detail}
    return json.dumps(message)
def return_success_get(landinfo_list):
    cherrypy.response.headers['Content-Type'] = "application/json"
    cherrypy.response.headers['Retry-After']=60
    cherrypy.response.status = 200
    return json.dumps(landinfo_list,indent=4)
def get_parameter(request_data,field_name,mandatory):
    try:
           field_name = str(request_data[field_name]).strip()
           return field_name
    except:
        if (mandatory == True):
           return -9999
        else:
           return ''
def get_ip_adress():
    return cherrypy.request.remote.ip
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
def running_model(record_id,recorder_name,latitude,longitude):
    try:
       mess = "cd %s && python Run_main_Controller.py -x %s -y %s -ID %s -name %s" % (str(CORE_BACK_END_MAIN_LANPKS),str(longitude), str(latitude), str(record_id),str(recorder_name))
       print "THANH NGUYEN " + mess
       os.system(mess)
       return 1
    except Exception,err:
       print err 
       return -1
def check_auth_thanhnh(*args, **kwargs):
    #conditions = cherrypy.request.config.get('auth.require', None)
    conditions = []
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    #raise cherrypy.HTTPRedirect("/auth/login")
                    return False
            return True    
        else:
            #raise cherrypy.HTTPRedirect("/auth/login")
            #return return_response_error(401,'error','Authenticated key is missing or invalid',format="JSON")
            return False
def Running_API_V_0_1(request_data):
    try:
       object = str(request_data['object']).strip().upper();
       action = str(request_data['action']).strip().upper();
    except:
       return return_response_error(400,"error","Missing parameters action or object","JSON")
    if (object is None or object == ""):
        return return_response_error(400,"error","Invalid or missing object field","JSON")
    if (action is None or action == ""):
        return return_response_error(400,"error","Invalid or missing action field","JSON")
    else:
        if (object == 'LANDINFO'):
            
            '''
              Work with Object LandInfo
            '''
            if (action == "PUT"):
                '''
                 Check authentication
                '''
                if (not check_auth_thanhnh()):
                    return return_response_error(401,'error','Authentication key is missing or invalid',format="JSON")
                try:
                    from osgeo import gdal, ogr
                    import numpy
                except Exception, err:
                    print err
                    return return_response_error(500,"error","Internal Error. Geo-spatial (Libray) data is missing","JSON")
                
                '''
                    PUT Object LandInfo + Running Model + Response
                '''
                try:
                   plot_data = {} 
                   name = get_parameter(request_data, 'name', True)
                   if (name == -9999):
                       return return_response_error(400,"error","Invalid or missing name field","JSON")
                   if (not name or name == "" or name is None):
                       return return_response_error(400,"error","Invalid or missing name field","JSON")
                   plot_data['name'] = str(name)
                                          
                   recorder_name = get_parameter(request_data, 'recorder_name', True)
                   if (recorder_name == -9999):
                       return return_response_error(400,"error","Invalide or missing recorder_name field","JSON")
                   if (not recorder_name or recorder_name == '' or recorder_name is None):
                       return return_response_error(400,"error","Invalid or missing recorder_name field","JSON")
                   plot_data['recorder_name'] = str(recorder_name)
                   
                   #Check map with LandInfo Record
                   existd_landinfor_id = LandPKS_Database_Driver.get_plot_id_land_info(name,recorder_name)
                   if (existd_landinfor_id <> 0):
                       return return_response_error(400,"error","[Recorder_name + name] pair is existed in system. Please select another ","JSON")
                   
                   test_plot = get_parameter(request_data, 'test_plot', True)
                   if (test_plot == -9999):
                       return return_response_error(400,"error","Invalid or missing test_plot field","JSON")
                   if (not test_plot or test_plot == '' or test_plot is None):
                       test_plot = "TRUE"
                   plot_data['test_plot'] = test_plot
                   
                   
                   test_plot = test_plot.strip().upper()   
                   if (test_plot == "TRUE"):
                       b_test_plot = 1
                   elif (test_plot == "FALSE"):
                       b_test_plot = 0
                   else:
                       test_plot = "TRUE"
                       b_test_plot = 1
                   plot_data['boolean_test_plot'] = b_test_plot
                        
                   organization = get_parameter(request_data, 'organization', False)
                   plot_data['organization'] = str(organization)
                   
                   latitude = get_parameter(request_data, 'latitude', True)
                   if (latitude == -9999):
                       return return_response_error(400,"error","Invalid or missing latitude field","JSON")
                   if (is_Float(latitude) == False):
                       return return_response_error(400,"error","Invalid or missing latitude field","JSON")
                   plot_data['latitude'] = latitude
                   
                   longitude = get_parameter(request_data, 'longitude', True)
                   if (longitude == -9999):
                       return return_response_error(400,"error","Invalid or missing longitude field","JSON")
                   if (is_Float(longitude) == False):
                       return return_response_error(400,"error","Invalid or missing longitude field","JSON")
                   plot_data['longitude'] = longitude
                    
                   city = get_parameter(request_data, 'city', False)
                   plot_data['city'] = str(city)
                   
                   notes = get_parameter(request_data, 'notes', False)
                   plot_data['notes'] = str(notes)
                   
                   modified_date = get_parameter(request_data, 'modified_date', False)
                   plot_data['modified_date'] = str(modified_date)
                   
                   land_cover = get_parameter(request_data, 'land_cover', False)
                   plot_data['land_cover'] = str(land_cover)
                   
                   grazed = get_parameter(request_data, 'grazed', False)
                   if (not grazed or grazed == '' or grazed is None):
                       grazed = "FALSE"
                   grazed = grazed.strip().upper()   
                   if (grazed == "TRUE"):
                       b_grazed = 1
                   elif (grazed == "FALSE"):
                       b_grazed = 0
                   else:
                       grazed = "FALSE"
                       b_grazed = 0
                   plot_data['grazed'] = grazed
                   plot_data['boolean_grazed'] = b_grazed
                   
                   grazing = get_parameter(request_data, 'grazing', False)
                   plot_data['grazing'] = str(grazing)
                        
                   flooding = get_parameter(request_data, 'flooding', False)
                   if (not flooding or flooding == '' or flooding is None):
                       flooding = "FALSE"
                   flooding = flooding.strip().upper()   
                   if (flooding == "TRUE"):
                       b_flooding = 1
                   elif (flooding == "FALSE"):
                       b_flooding = 0
                   else:
                       flooding = "FALSE"
                       b_flooding = 0
                   plot_data['flooding'] = grazed
                   plot_data['boolean_flooding'] = b_flooding
                       
                   slope = get_parameter(request_data, 'slope', True)
                   if (slope == -9999):
                       return return_response_error(400,"error","Invalid or missing slope field","JSON")
                   if (not slope or slope == '' or slope is None):
                       return return_response_error(400,"error","Invalid or missing slope field","JSON")
                   plot_data['slope'] = str(slope)
                   
                   slope_shape = get_parameter(request_data, 'slope_shape', True)
                   if (slope_shape == -9999):
                       return return_response_error(400,"error","Invalid or missing slope_shape field","JSON")
                   if (not slope_shape or slope_shape == '' or slope_shape is None):
                       return return_response_error(400,"error","Invalid or missing slope_shape field","JSON")
                   plot_data['slope_shape'] = str(slope_shape)
                   
                   bedrock_depth = get_parameter(request_data, 'bedrock_depth', False)
                   plot_data['bedrock_depth'] = str(bedrock_depth)
                   stopped_digging_depth = get_parameter(request_data, 'stopped_digging_depth', False)
                   plot_data['stopped_digging_depth'] = str(stopped_digging_depth)
                   
                   rock_fragment_for_soil_horizon_1 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_1', False)
                   rock_fragment_for_soil_horizon_1 = rock_fragment_for_soil_horizon_1.strip()
                   if (rock_fragment_for_soil_horizon_1 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_1 field","JSON")
                    
                   rock_fragment_for_soil_horizon_2 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_2', False)
                   rock_fragment_for_soil_horizon_2 = rock_fragment_for_soil_horizon_2.strip()
                   if (rock_fragment_for_soil_horizon_2 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_2 field","JSON")
                    
                   rock_fragment_for_soil_horizon_3 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_3', False)
                   rock_fragment_for_soil_horizon_3 = rock_fragment_for_soil_horizon_3.strip()
                   if (rock_fragment_for_soil_horizon_3 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_3 field","JSON")
                    
                   rock_fragment_for_soil_horizon_4 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_4', False)
                   rock_fragment_for_soil_horizon_4 = rock_fragment_for_soil_horizon_4.strip()
                   if (rock_fragment_for_soil_horizon_4 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_4 field","JSON")
                    
                   rock_fragment_for_soil_horizon_5 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_5', False)
                   rock_fragment_for_soil_horizon_5 = rock_fragment_for_soil_horizon_5.strip()
                   if (rock_fragment_for_soil_horizon_5 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_5 field","JSON")
                    
                    
                   rock_fragment_for_soil_horizon_6 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_6', False)
                   rock_fragment_for_soil_horizon_6 = rock_fragment_for_soil_horizon_6.strip()
                   if (rock_fragment_for_soil_horizon_6 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_6 field","JSON")
                    
                    
                   rock_fragment_for_soil_horizon_7 = get_parameter(request_data, 'rock_fragment_for_soil_horizon_7', False)
                   rock_fragment_for_soil_horizon_7 = rock_fragment_for_soil_horizon_7.strip()
                   if (rock_fragment_for_soil_horizon_7 not in LandPKS_LandInfo.ROCK_FRAGMENT_SOIL_SET):
                        return return_response_error(400,"error","Wrong data in rock_fragment_for_soil_horizon_7 field","JSON")
                    
                    
                   plot_data['rock_fragment_for_soil_horizon_1'] = str(rock_fragment_for_soil_horizon_1)
                   plot_data['rock_fragment_for_soil_horizon_2'] = str(rock_fragment_for_soil_horizon_2)
                   plot_data['rock_fragment_for_soil_horizon_3'] = str(rock_fragment_for_soil_horizon_3)
                   plot_data['rock_fragment_for_soil_horizon_4'] = str(rock_fragment_for_soil_horizon_4)
                   plot_data['rock_fragment_for_soil_horizon_5'] = str(rock_fragment_for_soil_horizon_5)
                   plot_data['rock_fragment_for_soil_horizon_6'] = str(rock_fragment_for_soil_horizon_6)
                   plot_data['rock_fragment_for_soil_horizon_7'] = str(rock_fragment_for_soil_horizon_7)
                   
                   color_for_soil_horizon_1 = get_parameter(request_data, 'color_for_soil_horizon_1', False)
                   color_for_soil_horizon_2 = get_parameter(request_data, 'color_for_soil_horizon_2', False)
                   color_for_soil_horizon_3 = get_parameter(request_data, 'color_for_soil_horizon_3', False)
                   color_for_soil_horizon_4 = get_parameter(request_data, 'color_for_soil_horizon_4', False)
                   color_for_soil_horizon_5 = get_parameter(request_data, 'color_for_soil_horizon_5', False)
                   color_for_soil_horizon_6 = get_parameter(request_data, 'color_for_soil_horizon_6', False)
                   color_for_soil_horizon_7 = get_parameter(request_data, 'color_for_soil_horizon_7', False)
                   plot_data['color_for_soil_horizon_1'] = str(color_for_soil_horizon_1)
                   plot_data['color_for_soil_horizon_2'] = str(color_for_soil_horizon_2)
                   plot_data['color_for_soil_horizon_3'] = str(color_for_soil_horizon_3)
                   plot_data['color_for_soil_horizon_4'] = str(color_for_soil_horizon_4)
                   plot_data['color_for_soil_horizon_5'] = str(color_for_soil_horizon_5)
                   plot_data['color_for_soil_horizon_6'] = str(color_for_soil_horizon_6)
                   plot_data['color_for_soil_horizon_7'] = str(color_for_soil_horizon_7)
                   
                   texture_for_soil_horizon_1 = get_parameter(request_data, 'texture_for_soil_horizon_1', False)
                   texture_for_soil_horizon_1 = texture_for_soil_horizon_1.upper().strip()
                   
                   if (texture_for_soil_horizon_1 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_1 field","JSON")
                   
                   texture_for_soil_horizon_2 = get_parameter(request_data, 'texture_for_soil_horizon_2', False)
                   texture_for_soil_horizon_2 = texture_for_soil_horizon_2.upper().strip()
                   
                   if (texture_for_soil_horizon_2 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_2 field","JSON")
                   
                   texture_for_soil_horizon_3 = get_parameter(request_data, 'texture_for_soil_horizon_3', False)
                   texture_for_soil_horizon_3 = texture_for_soil_horizon_3.upper().strip()
                   
                   if (texture_for_soil_horizon_3 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_3 field","JSON")
                   
                   texture_for_soil_horizon_4 = get_parameter(request_data, 'texture_for_soil_horizon_4', False)
                   texture_for_soil_horizon_4 = texture_for_soil_horizon_4.upper().strip()
                   
                   if (texture_for_soil_horizon_4 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_4 field","JSON")
                   
                   texture_for_soil_horizon_5 = get_parameter(request_data, 'texture_for_soil_horizon_5', False)
                   texture_for_soil_horizon_5 = texture_for_soil_horizon_5.upper().strip()
                   
                   if (texture_for_soil_horizon_5 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_5 field","JSON")
                   
                   texture_for_soil_horizon_6 = get_parameter(request_data, 'texture_for_soil_horizon_6', False)
                   texture_for_soil_horizon_6 = texture_for_soil_horizon_6.upper().strip()
                   
                   if (texture_for_soil_horizon_6 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_6 field","JSON")
                   
                   texture_for_soil_horizon_7 = get_parameter(request_data, 'texture_for_soil_horizon_7', False)
                   texture_for_soil_horizon_7 = texture_for_soil_horizon_7.upper().strip()
                   
                   if (texture_for_soil_horizon_7 not in LandPKS_LandInfo.TEXTURE_SOIL_SET):
                        return return_response_error(400,"error","Wrong data format in texture_for_soil_horizon_7 field","JSON")
                   
                   plot_data['texture_for_soil_horizon_1'] = str(texture_for_soil_horizon_1)
                   plot_data['texture_for_soil_horizon_2'] = str(texture_for_soil_horizon_2)
                   plot_data['texture_for_soil_horizon_3'] = str(texture_for_soil_horizon_3)
                   plot_data['texture_for_soil_horizon_4'] = str(texture_for_soil_horizon_4)
                   plot_data['texture_for_soil_horizon_5'] = str(texture_for_soil_horizon_5)
                   plot_data['texture_for_soil_horizon_6'] = str(texture_for_soil_horizon_6)
                   plot_data['texture_for_soil_horizon_7'] = str(texture_for_soil_horizon_7)
                   
                   
                   surface_cracking = get_parameter(request_data, 'surface_cracking', False)
                   if (not surface_cracking or surface_cracking == '' or surface_cracking is None):
                       surface_cracking = "FALSE"
                   surface_cracking = surface_cracking.strip().upper()   
                   if (surface_cracking == "TRUE"):
                       b_surface_cracking = 1
                   elif (surface_cracking == "FALSE"):
                       b_surface_cracking = 0
                   else:
                       surface_cracking = "FALSE"
                       b_surface_cracking = 0
                   plot_data['surface_cracking'] = surface_cracking
                   plot_data['boolean_surface_cracking'] = b_surface_cracking    
                   
                   surface_salt = get_parameter(request_data, 'surface_salt', False)
                   if (not surface_salt or surface_salt == '' or surface_salt is None):
                       surface_salt = "FALSE"
                   surface_salt = surface_salt.strip().upper()   
                   if (surface_salt == "TRUE"):
                       b_surface_salt = 1
                   elif (surface_salt == "FALSE"):
                       b_surface_salt = 0
                   else:
                       surface_salt = "FALSE"
                       b_surface_salt = 0
                   plot_data['surface_salt'] = surface_salt
                   plot_data['boolean_surface_salt'] = b_surface_salt     
                
                   soil_pit_photo_url = get_parameter(request_data, 'soil_pit_photo_url', False)
                   soil_samples_photo_url = get_parameter(request_data, 'soil_samples_photo_url', False)
                   landscape_north_photo_url = get_parameter(request_data, 'landscape_north_photo_url', False)
                   landscape_east_photo_url = get_parameter(request_data, 'landscape_east_photo_url', False)
                   landscape_south_photo_url = get_parameter(request_data, 'landscape_south_photo_url', False)
                   landscape_west_photo_url = get_parameter(request_data, 'landscape_west_photo_url', False)
                   
                   plot_data['soil_pit_photo_url'] = str(soil_pit_photo_url)
                   plot_data['soil_samples_photo_url'] = str(soil_samples_photo_url)
                   plot_data['landscape_north_photo_url'] = str(landscape_north_photo_url)
                   plot_data['landscape_east_photo_url'] = str(landscape_east_photo_url)
                   plot_data['landscape_south_photo_url'] = str(landscape_south_photo_url)
                   plot_data['landscape_west_photo_url'] = str(landscape_west_photo_url)
                   client_ip = get_ip_adress()
                   plot_data['client_ip'] = str(client_ip)
                   
                   #Insert plot
                   plot_id = -1
                   plot_id = LandPKS_Database_Driver.insert_new_plot_LandInfo_MySQL_Database(plot_data)
                   if (plot_id == -1 or plot_id == 0 or plot_id is None):
                       return return_response_error(500,"error","Cannot insert new LandInfo Plot. Please check your data","JSON")
                   else:
                       # Running Model
                       result_model = running_model(plot_id, recorder_name, latitude, longitude)
                       check_predicted_data = LandPKS_Database_Driver.check_exist_predicted_data_MySQL_Database(plot_id)
                       if(result_model == 1 and check_predicted_data == 1):
                            return return_success_response_put(201, plot_id, object, name, recorder_name, 1, CURRENT_VERSION, 'LandInfo plot is created and predicted data is ready')
                       elif (result_model == 1 and check_predicted_data == 0):
                            return return_success_response_put(201, plot_id, object, name, recorder_name, 0, CURRENT_VERSION, 'LandInfo plot is created')
                       elif  (result_model == 1 and check_predicted_data == -1):
                           return return_success_response_put(201, plot_id, object, name, recorder_name, -1, CURRENT_VERSION, 'LandInfo plot is created, but cannot create predicted data')
                       else:
                            return return_response_error(500,"error","Cannot run prediction model and Back-End","JSON")
                except Exception, err:
                    print err
                    return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
            elif (action == "DELETE"):
                '''
                   Delete LandInfo + Running Model + Response
                '''
                '''
                 Check authentication
                '''
                if (not check_auth_thanhnh()):
                    return return_response_error(401,'error','Authentication key is missing or invalid',format="JSON")
                try:
                   id = get_parameter(request_data, 'id', True)
                   if ((id == -9999) or (not id) or (id == "") or (id is None)):
                       name = get_parameter(request_data, 'name', True)
                       if (name == -9999):
                           return return_response_error(400,"error","Invalide or missing ID field or [Recorder_name + name] pair","JSON")
                       if (not name or name == "" or name is None):
                           return return_response_error(400,"error","Invalide or missing ID field or [Recorder_name + name] pair","JSON")                       
                       recorder_name = get_parameter(request_data, 'recorder_name', True)
                       if (recorder_name == -9999):
                           return return_response_error(400,"error","Invalide or missing ID field or [Recorder_name + name] pair","JSON")
                       if (not recorder_name or recorder_name == '' or recorder_name is None):
                           return return_response_error(400,"error","Invalide or missing ID field or [Recorder_name + name] pair","JSON")
                       id = LandPKS_Database_Driver.get_plot_id_land_info(name,recorder_name)
                       if (id == 0 or id == -1 or id == "0" or id == "-1"):
                           return return_response_error(404,"error","Plot with [Recorder_Name and Name] pair is not existed or has been deleted","JSON")
                       else:
                           check_delete = LandPKS_Database_Driver.check_be_able_deleted_before_delete_MySQL_Database(id)
                           if (check_delete == 1):
                               result_delete = LandPKS_Database_Driver.delete_land_info_plot_MySQL_Database(id)
                               if (result_delete == 1):
                                   message = {'id':id,'status':'deleted','version':CURRENT_VERSION,'object':object}
                                   cherrypy.response.headers['Content-Type'] = "application/json"
                                   cherrypy.response.headers['Retry-After']=60
                                   cherrypy.response.status = 200
                                   return json.dumps(message)
                               else:
                                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
                           else:
                               return return_response_error(404,"error","ID " + str(id) + " is not existed or has been deleted","JSON")
                   else:
                       #print ids
                       id = str(id).strip()
                       if (not is_Int(id)):
                           return return_response_error(400,"error","Invalid or missing ID field","JSON")
                       check_delete = LandPKS_Database_Driver.check_be_able_deleted_before_delete_MySQL_Database(id)
                       if (check_delete == 1):
                           result_delete = LandPKS_Database_Driver.delete_land_info_plot_MySQL_Database(id)
                           if (result_delete == 1):
                               message = {'id':id,'status':'deleted','version':CURRENT_VERSION,'object':object}
                               cherrypy.response.headers['Content-Type'] = "application/json"
                               cherrypy.response.headers['Retry-After']=60
                               cherrypy.response.status = 200
                               return json.dumps(message)
                       else:
                           return return_response_error(300,"error","ID " + str(id) + " is not existed or has been deleted","JSON")
                except Exception,err:
                   print err
                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
            elif (action == "GET"):
                '''
                 GET
                '''
                try:
                   b_params = LandPKS_Ultility.checkParams(request_data)
                   
                   if (b_params['id'] == True and b_params['recorder_name'] == False and b_params['name'] == False 
                       and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                       and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                       and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                       and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                       
                       ids = get_parameter(request_data, 'id', False)
                       if ((ids == -9999) or (not ids) or (ids == "") or (ids is None)):
                           return return_response_error(400,"error","Missing filtering ID or IDs","JSON")
                       else:
                           '''
                             Conduct method GET by ID or IDs
                           '''
                           delimiter = get_parameter(request_data, 'delimiter', False)
                           if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                               delimiter = " "
                               
                           display = get_parameter(request_data, 'display', False)
                           if ((display == -9999) or (not display) or (display == "") or (display is None)):
                               display = ''
                           display_set = set()
                           if (display == ''):
                               display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                           else:
                               list_display = str(display).strip().upper().split(delimiter)
                               new_list_display = []
                               for element in list_display:
                                   element = str(element).strip().upper()
                                   new_list_display.append(element)
                               display_set = set(new_list_display)
                    
                           list_id = str(ids).strip().split(delimiter)
                           str_list_id = ""
                           str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                           land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                           return return_success_get(land_info_list)
                   elif (b_params['id'] == False and b_params['recorder_name'] == True and b_params['name'] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                           recorder_name = get_parameter(request_data, 'recorder_name', False)
                           if ((recorder_name == -9999) or (not recorder_name) or (recorder_name == "") or (recorder_name is None)):
                               return return_response_error(400,"error","Missing filtering recorder_name","JSON")
                           else:
                               '''
                                  Conduct method GET by OWNERs : Recorder_Name
                               '''
                               delimiter = get_parameter(request_data, 'delimiter', False)
                               if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                                     delimiter = " "
                               display = get_parameter(request_data, 'display', False)
                               if ((display == -9999) or (not display) or (display == "") or (display is None)):
                                   display = ''
                               display_set = set()
                               if (display == ''):
                                   display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                               else:
                                   list_display = str(display).strip().upper().split(delimiter)
                                   new_list_display = []
                                   for element in list_display:
                                       element = str(element).strip().upper()
                                       new_list_display.append(element)
                                   display_set = set(new_list_display)
                               
                               list_id = LandPKS_Database_Driver.get_land_info_IDs_by_Recorder_Name_MySQL_Database(recorder_name)
                               str_list_id = ""
                               str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                               land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                               return return_success_get(land_info_list)
                   elif (b_params['id'] == False and b_params['recorder_name'] == True and b_params['name'] == True
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                           recorder_name = get_parameter(request_data, 'recorder_name', False)
                           if ((recorder_name == -9999) or (not recorder_name) or (recorder_name == "") or (recorder_name is None)):
                               return return_response_error(400,"error","Missing filtering recorder_name","JSON")
                           name = get_parameter(request_data, 'name', False)
                           if ((name == -9999) or (not name) or (name == "") or (name is None)):
                               return return_response_error(400,"error","Missing filtering name","JSON")
                           
                           '''
                              Conduct method GET by OWNERs : Recorder_Name + name
                           '''
                           delimiter = get_parameter(request_data, 'delimiter', False)
                           if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                                 delimiter = " "
                           display = get_parameter(request_data, 'display', False)
                           if ((display == -9999) or (not display) or (display == "") or (display is None)):
                               display = ''
                           display_set = set()
                           if (display == ''):
                               display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                           else:
                               list_display = str(display).strip().upper().split(delimiter)
                               new_list_display = []
                               for element in list_display:
                                   element = str(element).strip().upper()
                                   new_list_display.append(element)
                               display_set = set(new_list_display)
                           
                           list_id = LandPKS_Database_Driver.get_plot_id_land_info(name,recorder_name)
                           str_list_id = ""
                           str_list_id = str(list_id) + ",0"
                           land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                           return return_success_get(land_info_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_ID] == False and b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == True 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == True
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == True
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == True
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                         
                         minlat = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MIN_LAT, False)
                         if ((minlat == -9999) or (not is_Float(minlat)) or (minlat == "") or (minlat is None)):
                               return return_response_error(400,"error","Missing or invalid filtering minlat (minimum latitude)","JSON")
                         minlong = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MIN_LONG, False)
                         if ((minlong == -9999) or (not is_Float(minlong)) or (minlong == "") or (minlong is None)):
                               return return_response_error(400,"error","Missing or invalid filtering minlong (minimum longitude)","JSON")
                         maxlat = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MAX_LAT, False)
                         if ((maxlat == -9999) or (not is_Float(maxlat)) or (maxlat == "") or (maxlat is None)):
                               return return_response_error(400,"error","Missing or invalid filtering maxlat (maximum latitude)","JSON")
                         maxlong = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MAX_LONG, False)
                         if ((maxlong == -9999) or (not is_Float(maxlong)) or (maxlong == "") or (maxlong is None)):
                               return return_response_error(400,"error","Missing or invalid filtering maxlong (maximum longitude)","JSON")
                         '''
                          Conduct method GET by POLYGON
                         '''
                         delimiter = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DELIMITER, False)
                         if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                             delimiter = " "
                         display = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DISPLAY, False)
                         if ((display == -9999) or (not display) or (display == "") or (display is None)):
                             display = ''
                         display_set = set()
                         if (display == ''):
                             display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                         else:
                             list_display = str(display).strip().upper().split(delimiter)
                             new_list_display = []
                             for element in list_display:
                                 element = str(element).strip().upper()
                                 new_list_display.append(element)
                             display_set = set(new_list_display)
                         
                         list_id = LandPKS_Database_Driver.get_land_info_IDs_by_Polygon_MySQL_Database(None,minlat,minlong,maxlat,maxlong)
                         str_list_id = ""
                         str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                         land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                         return return_success_get(land_info_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_ID] == False and b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == True and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == True 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == True
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == True
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == True
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                         
                         minlat = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MIN_LAT, False)
                         if ((minlat == -9999) or (not is_Float(minlat)) or (minlat == "") or (minlat is None)):
                               return return_response_error(400,"error","Missing or invalid filtering minlat (minimum latitude)","JSON")
                         minlong = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MIN_LONG, False)
                         if ((minlong == -9999) or (not is_Float(minlong)) or (minlong == "") or (minlong is None)):
                               return return_response_error(400,"error","Missing or invalid filtering minlong (minimum longitude)","JSON")
                         maxlat = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MAX_LAT, False)
                         if ((maxlat == -9999) or (not is_Float(maxlat)) or (maxlat == "") or (maxlat is None)):
                               return return_response_error(400,"error","Missing or invalid filtering maxlat (maximum latitude)","JSON")
                         maxlong = get_parameter(request_data, LandPKS_LandInfo.PARAMS_MAX_LONG, False)
                         if ((maxlong == -9999) or (not is_Float(maxlong)) or (maxlong == "") or (maxlong is None)):
                               return return_response_error(400,"error","Missing or invalid filtering maxlong (maximum longitude)","JSON")
                         recorder_name = get_parameter(request_data, LandPKS_LandInfo.PARAMS_RECORDER_NAME, False)
                         if ((recorder_name == -9999) or (not recorder_name) or (recorder_name == "") or (recorder_name is None)):
                               return return_response_error(400,"error","Missing filtering recorder_name","JSON") 
                         '''
                          Conduct method GET by POLYGON
                         '''
                         delimiter = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DELIMITER, False)
                         if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                             delimiter = " "
                         display = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DISPLAY, False)
                         if ((display == -9999) or (not display) or (display == "") or (display is None)):
                             display = ''
                         display_set = set()
                         if (display == ''):
                             display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                         else:
                             list_display = str(display).strip().upper().split(delimiter)
                             new_list_display = []
                             for element in list_display:
                                 element = str(element).strip().upper()
                                 new_list_display.append(element)
                             display_set = set(new_list_display)
                         
                         list_id = LandPKS_Database_Driver.get_land_info_IDs_by_Polygon_MySQL_Database(recorder_name,minlat,minlong,maxlat,maxlong)
                         str_list_id = ""
                         str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                         land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                         return return_success_get(land_info_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_ID] == False and b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == True):
                         
                         after_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_AFTER_DATE, False)
                         if ((after_date == -9999)  or (after_date == "") or (after_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering after_date","JSON")
                         if (len(after_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON") 
                         '''
                          Conduct method GET by POLYGON
                         '''
                         delimiter = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DELIMITER, False)
                         if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                             delimiter = " "
                         display = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DISPLAY, False)
                         if ((display == -9999) or (not display) or (display == "") or (display is None)):
                             display = ''
                         display_set = set()
                         if (display == ''):
                             display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                         else:
                             list_display = str(display).strip().upper().split(delimiter)
                             new_list_display = []
                             for element in list_display:
                                 element = str(element).strip().upper()
                                 new_list_display.append(element)
                             display_set = set(new_list_display)
                         
                         list_id = LandPKS_Database_Driver.get_land_info_IDs_by_After_Before_Date_MySQL_Database(None,None,after_date)
                         str_list_id = ""
                         str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                         land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                         return return_success_get(land_info_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_ID] == False and b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == True
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                         
                         before_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_BEFORE_DATE, False)
                         if ((before_date == -9999)  or (before_date == "") or (before_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering before_date","JSON")
                         if (len(before_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON") 
                         '''
                          Conduct method GET by BEFORE DATE
                         '''
                         delimiter = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DELIMITER, False)
                         if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                             delimiter = " "
                         display = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DISPLAY, False)
                         if ((display == -9999) or (not display) or (display == "") or (display is None)):
                             display = ''
                         display_set = set()
                         if (display == ''):
                             display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                         else:
                             list_display = str(display).strip().upper().split(delimiter)
                             new_list_display = []
                             for element in list_display:
                                 element = str(element).strip().upper()
                                 new_list_display.append(element)
                             display_set = set(new_list_display)
                         
                         list_id = LandPKS_Database_Driver.get_land_info_IDs_by_After_Before_Date_MySQL_Database(None,before_date,None)
                         str_list_id = ""
                         str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                         land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                         return return_success_get(land_info_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_ID] == False and b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LAT] == False 
                         and b_params[LandPKS_LandInfo.PARAMS_MIN_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LAT] == False
                         and b_params[LandPKS_LandInfo.PARAMS_MAX_LONG] == False
                         and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == True
                         and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == True):
                       
                       
                         before_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_BEFORE_DATE, False)
                         if ((before_date == -9999)  or (before_date == "") or (before_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering before_date","JSON")
                         if (len(before_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON")
                         
                         after_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_AFTER_DATE, False)
                         if ((after_date == -9999)  or (after_date == "") or (after_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering after_date","JSON")
                         if (len(before_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON") 
                         '''
                          Conduct method GET by After DATE
                         '''
                         delimiter = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DELIMITER, False)
                         if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                             delimiter = " "
                         display = get_parameter(request_data, LandPKS_LandInfo.PARAMS_DISPLAY, False)
                         if ((display == -9999) or (not display) or (display == "") or (display is None)):
                             display = ''
                         display_set = set()
                         if (display == ''):
                             display_set = LandPKS_LandInfo.LAND_INFO_DISPLAY_SET
                         else:
                             list_display = str(display).strip().upper().split(delimiter)
                             new_list_display = []
                             for element in list_display:
                                 element = str(element).strip().upper()
                                 new_list_display.append(element)
                             display_set = set(new_list_display)
                         
                         list_id = LandPKS_Database_Driver.get_land_info_IDs_by_After_Before_Date_MySQL_Database(None,before_date,after_date)
                         str_list_id = ""
                         str_list_id = LandPKS_Ultility.build_up_str_list_id(list_id)
                         land_info_list = LandPKS_Database_Driver.get_list_landinfo_predicted_data_by_IDs_MySQL_Database(str_list_id,display_set)
                         return return_success_get(land_info_list)
                   else:
                       return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                  
                except Exception,err:
                   print err
                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")   
            else:
                return return_response_error(400,"error","Invalide action field","JSON")
        elif (object == 'LANDCOVER'):
            '''
              Work with Object LandCover
            '''
            if (action == "PUT"):
                '''
                 PUT landcover
                '''
                '''
                 Check authentication
                '''
                if (not check_auth_thanhnh()):
                    return return_response_error(401,'error','Authentication key is missing or invalid',format="JSON")
                try:
                   landcover_data = {} 
                   name = get_parameter(request_data, 'name', True)
                   if (name == -9999):
                       return return_response_error(404,"error","Invalid or missing name field","JSON")
                   if (not name or name == "" or name is None):
                       return return_response_error(404,"error","Invalid or missing name field","JSON")
                   landcover_data['name'] = str(name)
                   
                   recorder_name = get_parameter(request_data, 'recorder_name', True)
                   if (recorder_name == -9999):
                       return return_response_error(404,"error","Invalid or missing recorder_name field","JSON")
                   if (not recorder_name or recorder_name == '' or recorder_name is None):
                       return return_response_error(404,"error","Invalid or missing recorder_name field","JSON")
                   landcover_data['recorder_name'] = str(recorder_name)
                   
                   #Check map with LandInfo Record
                   landinfor_id = LandPKS_Database_Driver.get_plot_id_land_info(name,recorder_name)
                   if (landinfor_id == 0):
                       return return_response_error(400,"error","This LandCover Record does not match with any LandInfo Plot. Please verify your name and recorder_name","JSON")
                   landcover_data['landinfor_id'] = landinfor_id
                   
                   
                   transect = get_parameter(request_data, 'transect', True)
                   if (transect == -9999):
                       return return_response_error(404,"error","Invalid or missing transect field","JSON")
                   if (not transect or transect == '' or transect is None):
                       return return_response_error(404,"error","Invalid or missing transect field","JSON")
                   transect = str(transect).strip().upper();
                   if (transect != "WEST" and transect != "SOUTH" and transect != "NORTH" and transect != "EAST"):
                       return return_response_error(400,"error","Wrong format transect, only accept WEST, NORTH, SOUTH, EAST","JSON")
                   landcover_data['transect'] = str(transect).strip().upper()
                   
                   segment = get_parameter(request_data, 'segment', True)
                   if (segment == -9999):
                       return return_response_error(404,"error","Invalid or missing segment field","JSON")
                   if (not segment or segment == '' or segment is None):
                       return return_response_error(404,"error","Invalid or missing segment field","JSON")
                   segment = str(segment).strip()
                   if (segment != "5m" and segment != "10m" and segment != "15m" and segment != "20m" and segment != "25m"):
                       return return_response_error(400,"error","Wrong format segment, only accept 5m, 10m, 15m, 20m and 25m","JSON")
                   landcover_data['segment'] = segment
                   
                   canopy_height = get_parameter(request_data, 'canopy_height', True)
                   if (canopy_height == -9999):
                       return return_response_error(404,"error","Invalid or missing canopy_height field","JSON")
                   if (not canopy_height or canopy_height == '' or canopy_height is None):
                       return return_response_error(404,"error","Invalid or missing canopy_height field","JSON")
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(canopy_height,","),LandPKS_LandCover.CANOPY_HEIGHT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong format canopy_height, only accept <10cm, 10-50cm, 50cm-1m, 1-2m, 2-3m and >3m","JSON")
                   landcover_data['canopy_height'] = str(canopy_height).strip()
                   
                   canopy_gap = get_parameter(request_data, 'canopy_gap', True)
                   if (canopy_gap == -9999):
                       return return_response_error(404,"error","Invalid or missing canopy_gap field","JSON")
                   if (not canopy_gap or canopy_gap == '' or canopy_gap is None):
                       return return_response_error(404,"error","Invalid or missing canopy_gap field","JSON")
                   canopy_gap = canopy_gap.upper().strip()
                   if (canopy_gap != "TRUE" and canopy_gap != "FALSE"):
                       return return_response_error(400,"error","Wrong format canopy_gap, only accept TRUE or FALSE","JSON")
                   landcover_data['canopy_gap'] = canopy_gap
                   
                   basal_gap = get_parameter(request_data, 'basal_gap', True)
                   if (basal_gap == -9999):
                       return return_response_error(404,"error","Invalide or missing basal_gap field","JSON")
                   if (not basal_gap or basal_gap == '' or basal_gap is None):
                       return return_response_error(404,"error","Invalide or missing basal_gap field","JSON")
                   basal_gap = basal_gap.upper().strip()
                   if (basal_gap != "TRUE" and basal_gap != "FALSE"):
                       return return_response_error(400,"error","Wrong format basal_gap, only accept TRUE or FALSE","JSON")
                   landcover_data['basal_gap'] = basal_gap
                   
                   
                   species_1_density = get_parameter(request_data, 'species_1_density', False)
                   if ((not is_Int(species_1_density)) or species_1_density == '' or species_1_density is None):
                       species_1_density = 0
                   landcover_data['species_1_density'] = species_1_density
                   
                   species_2_density = get_parameter(request_data, 'species_2_density', False)
                   if ((not is_Int(species_2_density)) or species_2_density == '' or species_2_density is None):
                       species_2_density = 0
                   landcover_data['species_2_density'] = species_2_density
                   
                   
                   species_list = get_parameter(request_data, 'species_list', False)
                   landcover_data['species_list'] = species_list
                   
                   stick_segment_0 = get_parameter(request_data, 'stick_segment_0', False)
                   landcover_data['stick_segment_0'] = stick_segment_0
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(stick_segment_0,","),LandPKS_LandCover.STICK_SEGMENT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong data format in stick_segment_0 field","JSON")
                   
                   
                   stick_segment_1 = get_parameter(request_data, 'stick_segment_1', False)
                   landcover_data['stick_segment_1'] = stick_segment_1
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(stick_segment_1,","),LandPKS_LandCover.STICK_SEGMENT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong data format in stick_segment_1 field","JSON")
                   
                   stick_segment_2 = get_parameter(request_data, 'stick_segment_2', False)
                   landcover_data['stick_segment_2'] = stick_segment_2
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(stick_segment_2,","),LandPKS_LandCover.STICK_SEGMENT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong data format in stick_segment_2 field","JSON")
                   
                   stick_segment_3 = get_parameter(request_data, 'stick_segment_3', False)
                   landcover_data['stick_segment_3'] = stick_segment_3
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(stick_segment_3,","),LandPKS_LandCover.STICK_SEGMENT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong data format in stick_segment_3 field","JSON")
                   
                   stick_segment_4 = get_parameter(request_data, 'stick_segment_4', False)
                   landcover_data['stick_segment_4'] = stick_segment_4
                   check_satisfy = LandPKS_Ultility.checkIsSubset(LandPKS_Ultility.convertStringToSet(stick_segment_4,","),LandPKS_LandCover.STICK_SEGMENT_SET)
                   if (not check_satisfy):
                       return return_response_error(400,"error","Wrong data format in stick_segment_4 field","JSON")
                   
                   stick_segment_string = stick_segment_0.strip() + " | " + stick_segment_1.strip() + " | " + stick_segment_2.strip() + " | " + stick_segment_3.strip() + " | " + stick_segment_4.strip()
                   stick_segment_string = stick_segment_string.upper().strip()
                   
                   int_bare_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.BARE.upper(), stick_segment_string)
                   int_trees_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.TREES.upper(), stick_segment_string)
                   int_shrubs_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.SHRUBS.upper(), stick_segment_string)
                   int_sub_shrubs_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.SUB_SHRUBS.upper(), stick_segment_string)
                   int_perennial_grasses_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.PER_GRASS.upper(), stick_segment_string)
                   int_annuals_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.ANNUAL.upper(), stick_segment_string)
                   int_herb_litter_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.HERB_LITTER.upper(), stick_segment_string)
                   int_wood_litter_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.WOOD_LITTER.upper(), stick_segment_string)
                   int_rock_total = LandPKS_Ultility.count_value_in_string(LandPKS_LandCover.ROCK.upper(), stick_segment_string)
                   
                   landcover_data['int_bare_total'] = int_bare_total
                   landcover_data['int_trees_total'] = int_trees_total
                   landcover_data['int_shrubs_total'] = int_shrubs_total
                   landcover_data['int_sub_shrubs_total'] = int_sub_shrubs_total
                   landcover_data['int_perennial_grasses_total'] = int_perennial_grasses_total
                   landcover_data['int_annuals_total'] = int_annuals_total
                   landcover_data['int_herb_litter_total'] = int_herb_litter_total
                   landcover_data['int_wood_litter_total'] = int_wood_litter_total
                   landcover_data['int_rock_total'] = int_rock_total
                   
                   client_ip = get_ip_adress()
                   landcover_data['client_ip'] = str(client_ip)
                   if (not LandPKS_Database_Driver.check_exit_landcover_record_MySQL_Database(name,recorder_name,transect,segment)):
                          result_id = LandPKS_Database_Driver.insert_LandCover_Object_MySQL_Database(landcover_data)
                          if (result_id <> -1):
                              cherrypy.response.headers['Content-Type'] = "application/json"
                              cherrypy.response.headers['Retry-After']=60
                              cherrypy.response.status = 200
                              message = {'id':result_id,'landinfo_plot_id':landinfor_id ,'object':object,'name':name,'recorder_name':recorder_name,'status':1,'version':CURRENT_VERSION,'detail':'LandCover Record is created'}
                              return json.dumps(message)    
                   else:
                       return return_response_error(400,"error","This LandCover (Transect - Segment - Name - Recorder_name) has been existed in system. Please try another","JSON")
                   
                except Exception, err:
                   print err
                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")    
            elif (action == "DELETE"):
                '''
                 Delete landcover
                '''
                '''
                 Check authentication
                '''
                if (not check_auth_thanhnh()):
                    return return_response_error(401,'error','Authentication key is missing or invalid',format="JSON")
                try:
                   id = get_parameter(request_data, 'id', True)
                   if ((id == -9999) or (not id) or (id == "") or (id is None)):
                       name = get_parameter(request_data, 'name', True)
                       if (name == -9999):
                           return return_response_error(400,"error","Invalide or missing ID field or (Recorder_name and name) pair","JSON")
                       if (not name or name == "" or name is None):
                           return return_response_error(400,"error","Invalide or missing ID field or (Recorder_name and name) pair","JSON")                       
                       recorder_name = get_parameter(request_data, 'recorder_name', True)
                       if (recorder_name == -9999):
                           return return_response_error(400,"error","Invalide or missing ID field or (Recorder_name and name) pair","JSON")
                       if (not recorder_name or recorder_name == '' or recorder_name is None):
                           return return_response_error(400,"error","Invalide or missing ID field or (Recorder_name and name) pair","JSON")
                       
                       if (LandPKS_Database_Driver.get_land_cover_id_from_key_pair_MySQL_Database(name, recorder_name) != 1):
                           return return_response_error(400,"error","LandCover with (Recorder_name and name) pair has been deleted already or does not exist in System","JSON")
                       
                       result_delete = LandPKS_Database_Driver.delete_land_cover_record_name_recorder_name_MySQL_Database(name, recorder_name)
                       if (result_delete == 1):
                               message = {'name':name,'recorder_name':recorder_name,'status':'deleted','version':CURRENT_VERSION,'object':object}
                               cherrypy.response.headers['Content-Type'] = "application/json"
                               cherrypy.response.headers['Retry-After']=60
                               cherrypy.response.status = 200
                               return json.dumps(message)
                       else:
                           return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
                   else:
                       #print ids
                       id = str(id).strip()
                       if (not is_Int(id)):
                           return return_response_error(404,"error","Wrong format ID field","JSON")
                       check_delete = LandPKS_Database_Driver.check_be_able_deleted_LANDCOVER_before_delete_MySQL_Database(id)
                       if (check_delete == 1):
                           result_delete = LandPKS_Database_Driver.delete_land_cover_record_MySQL_Database(id)
                           if (result_delete == 1):
                               message = {'id':id,'status':'deleted','version':CURRENT_VERSION,'object':object}
                               cherrypy.response.headers['Content-Type'] = "application/json"
                               cherrypy.response.headers['Retry-After']=60
                               cherrypy.response.status = 200
                               return json.dumps(message)
                       else:
                           return return_response_error(300,"error","ID " + str(id) + " is not existed in database or has been deleted","JSON")
                except Exception,err:
                   print err
                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
            elif (action == "GET"):
                '''
                 GET landcover
                '''
                try:
                   b_params = LandPKS_Ultility.checkParams(request_data)
                   if (b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == True and b_params[LandPKS_LandInfo.PARAMS_NAME] == True
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                       
                       
                       name = get_parameter(request_data, 'name', False)
                       if ((name == -9999) or (not name) or (name == "") or (name is None)):
                           return return_response_error(400,"error","Missing filtering name","JSON")
                       recorder_name = get_parameter(request_data, 'recorder_name', False)
                       if ((recorder_name == -9999) or (not recorder_name) or (recorder_name == "") or (recorder_name is None)):
                           return return_response_error(400,"error","Missing filtering recorder_name","JSON")
                       
                       delimiter = get_parameter(request_data, 'delimiter', False)
                       if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                           delimiter = " "
                      
                       land_cover_list = LandPKS_Database_Driver.get_list_landcover_data_by_IDs_MySQL_Database(name,recorder_name)
                       if (land_cover_list == -1):
                           return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                       else:
                           return return_success_get(land_cover_list)
                   elif (b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == True and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):
                       
                       recorder_name = get_parameter(request_data, 'recorder_name', False)
                       if ((recorder_name == -9999) or (not recorder_name) or (recorder_name == "") or (recorder_name is None)):
                           return return_response_error(400,"error","Missing filtering recorder_name","JSON")
                       
                       delimiter = get_parameter(request_data, 'delimiter', False)
                       if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                           delimiter = " "
                       BIG_LIST = []
                       list_name = LandPKS_Database_Driver.get_list_name_landcover_by_recorder_name_MySQL_Database(recorder_name)
                       
                       for name in list_name:
                           land_cover_list = LandPKS_Database_Driver.get_list_landcover_data_by_IDs_MySQL_Database(name,recorder_name)
                           if (land_cover_list == -1):
                                return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                           else:
                                BIG_LIST.append(land_cover_list)
                       return return_success_get(BIG_LIST)
                   elif (b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == False
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == True):   
                       '''
                         Time
                       '''
                       after_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_AFTER_DATE, False)
                       if ((after_date == -9999)  or (after_date == "") or (after_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering after_date","JSON")
                       if (len(after_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON")
                       
                       delimiter = get_parameter(request_data, 'delimiter', False)
                       if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                           delimiter = " "
                       BIG_LIST = []
                       list_key = LandPKS_Database_Driver.get_key_pair_landcover_MySQL_Database(None,after_date,None)
                       
                       for key in list_key:
                           land_cover_list = LandPKS_Database_Driver.get_list_landcover_data_by_IDs_MySQL_Database(key[0],key[1])
                           if (land_cover_list == -1):
                                return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                           else:
                                BIG_LIST.append(land_cover_list)
                       return return_success_get(BIG_LIST)
                   elif (b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == True
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == False):   
                       '''
                         Time
                       '''
                       before_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_BEFORE_DATE, False)
                       if ((before_date == -9999)  or (before_date == "") or (before_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering before date","JSON")
                       if (len(before_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON")
                       
                       delimiter = get_parameter(request_data, 'delimiter', False)
                       if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                           delimiter = " "
                       BIG_LIST = []
                       list_key = LandPKS_Database_Driver.get_key_pair_landcover_MySQL_Database(None,None,before_date)
                       
                       for key in list_key:
                           land_cover_list = LandPKS_Database_Driver.get_list_landcover_data_by_IDs_MySQL_Database(key[0],key[1])
                           if (land_cover_list == -1):
                                return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                           else:
                                BIG_LIST.append(land_cover_list)
                       return return_success_get(BIG_LIST)
                   elif (b_params[LandPKS_LandInfo.PARAMS_RECORDER_NAME] == False and b_params[LandPKS_LandInfo.PARAMS_NAME] == False
                       and b_params[LandPKS_LandInfo.PARAMS_BEFORE_DATE] == True
                       and b_params[LandPKS_LandInfo.PARAMS_AFTER_DATE] == True):   
                       '''
                         Time
                       '''
                       after_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_AFTER_DATE, False)
                       if ((after_date == -9999)  or (after_date == "") or (after_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering after_date","JSON")
                       if (len(after_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON")
                        
                       before_date = get_parameter(request_data, LandPKS_LandInfo.PARAMS_BEFORE_DATE, False)
                       if ((before_date == -9999)  or (before_date == "") or (before_date is None)):
                            return return_response_error(400,"error","Missing or invalid filtering before date","JSON")
                       if (len(before_date) != 10):
                            return return_response_error(400,"error","Data Format is not correct yyyy-mm-dd","JSON")
                       
                       delimiter = get_parameter(request_data, 'delimiter', False)
                       if ((delimiter == -9999) or (not delimiter) or (delimiter == "") or (delimiter is None)):
                           delimiter = " "
                       BIG_LIST = []
                       list_key = LandPKS_Database_Driver.get_key_pair_landcover_MySQL_Database(None,after_date,before_date)
                       
                       for key in list_key:
                           land_cover_list = LandPKS_Database_Driver.get_list_landcover_data_by_IDs_MySQL_Database(key[0],key[1])
                           if (land_cover_list == -1):
                                return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                           else:
                                BIG_LIST.append(land_cover_list)
                       return return_success_get(BIG_LIST)
                   else:
                       return return_response_error(404,"error","GET Method has not supported these filtering parameters yet","JSON")
                           
                except Exception,err:
                   print err
                   return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
            else:
                return return_response_error(404,"error","Invalide action field","JSON")
        elif (object == 'CLIMATE'):
            if (action == "GET"):
                try:      
                    from model_support import geospatial_functions
                except Exception,err:
                    print err
                    return return_response_error(500,"error","Something went wrong. Please try it again","JSON")
                
                latitude = get_parameter(request_data, LandPKS_LandInfo.PARAMS_LAT, True)
                if (latitude == -9999):
                    return return_response_error(400,"error","Invalid or missing latitude field","JSON")
                if (is_Float(latitude) == False):
                    return return_response_error(400,"error","Invalid or missing latitude field","JSON")
                fl_latitude = float(latitude)
                   
                longitude = get_parameter(request_data, LandPKS_LandInfo.PARAMS_LONG, True)
                if (longitude == -9999):
                    return return_response_error(400,"error","Invalid or missing longitude field","JSON")
                if (is_Float(longitude) == False):
                    return return_response_error(400,"error","Invalid or missing longitude field","JSON")
                fl_longitude= float(longitude)
                
                data_source = ""
                data_source = get_parameter(request_data, 'data_source', False)
                if ((data_source == -9999) or (not data_source) or (data_source == "") or (data_source is None)):
                    data_source = ""
                CLIMATE_DATA_SOURCE = "CRU"
                if (data_source != ""):
                   CLIMATE_DATA_SOURCE = data_source.strip().upper()
                print CLIMATE_DATA_SOURCE
                climate_data = geospatial_functions.get_climate_data_set(fl_longitude,fl_latitude,CLIMATE_DATA_SOURCE)
                return return_success_get(climate_data)
            else:
                return return_response_error(404,"error","Invalide action field","JSON")
        else:
            return return_response_error(404,"error","Invalide object field","JSON")
