'''
Created on Apr 21, 2015

@author: Thanh Nguyen Hai
'''
import cherrypy
import time
import datetime
import json
from support import support_API
'''
Configuration
'''
ACCESS_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/APEX/Python_APEX/18_MINI_ADDITIONAL_API_FUNCTION/log/%s_8080_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/APEX/Python_APEX/18_MINI_ADDITIONAL_API_FUNCTION/log/%s_8080_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

LASTEST_VERSION_API = 0.1

#CLIMATE_DATA_SOURCE = "WORLD_CLIM"
CLIMATE_DATA_SOURCE = "AGMERRA_TIF"

def return_response_error(code,type,mess,format="JSON"):
    if (format=="JSON"):
        cherrypy.response.headers['Content-Type'] = "application/json"
        cherrypy.response.headers['Retry-After']=60
        cherrypy.response.status = code
        message = {type:mess}
        return json.dumps(message)
    else:
        return "Not support yet"
def return_success_get(landinfo_list):
    cherrypy.response.headers['Content-Type'] = "application/json"
    cherrypy.response.headers['Retry-After']=60
    cherrypy.response.status = 200
    return json.dumps(landinfo_list,indent=4)
class LandPKS_API(object):
    def index(self):
        return "Server is running. Listening : 128.123.177.13:8081. \n To get quick-climate data set : http://128.123.177.13:8081/quick_climate?latitude={}&longitude={}"
    def quick_climate(self,**request_data):
        try:
            latitude = float(str(request_data['latitude']).strip());
        except:
            return return_response_error(400,"error","Invalid or missing latitude data","JSON")
        
        try:
            longitude = float(str(request_data['longitude']).strip());
        except:
            return return_response_error(400,"error","Invalid or missing longitude data","JSON")
        
        data_source = ""
        try:
            data_source = str(request_data['data_source']).strip();
        except:
            pass
        
        if (data_source != "" and (data_source.strip().upper() == "AGMERRA_TIF" or data_source.strip().upper() == "CRU")):
            CLIMATE_DATA_SOURCE = data_source.strip().upper()
        else:
            CLIMATE_DATA_SOURCE = "AGMERRA_TIF"
            
        climate_data = support_API.get_climate_data_set(longitude,latitude,CLIMATE_DATA_SOURCE)
        return return_success_get(climate_data)
            
    #Public /index
    index.exposed = True
    #publci /query
    quick_climate.exposed = True

if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8081,
                            'log.error_file':ERROR_LOG_CHERRYPY_8080,
                            'log.access_file':ACCESS_LOG_CHERRYPY_8080
                          })
    #Starting Server
    cherrypy.quickstart(LandPKS_API())
    #cherrypy.engine.start()
