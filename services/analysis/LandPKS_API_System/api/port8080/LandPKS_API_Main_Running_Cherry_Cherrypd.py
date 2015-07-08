'''
Created on Apr 21, 2015

@author: Thanh Nguyen Hai
'''
import cherrypy
from version.v0_1 import API_Running_V_0_1
import time
import datetime
import json
from version.v0_1.auth import AuthController, require, member_of, name_is, check_credentials

'''
Configuration
'''
ACCESS_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/LandPKS_API_System/api/port8080=cherrypd_server+cherrypy_framework/log/%s_8080_access_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))
ERROR_LOG_CHERRYPY_8080 = "C:/xampp/htdocs/LandPKS_API_System/api/port8080=cherrypd_server+cherrypy_framework/log/%s_8080_error_log.log" %(str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d')))

LASTEST_VERSION_API = 0.1

class LandPKS_API(object):
    _cp_config = {
        'tools.sessions.on': True,
        'tools.auth.on': True
    }    
    auth = AuthController()
    def index(self):
        return "Server is running. Listening : 128.123.177.251:8080"
   
    def query(self,**request_data):
        version = 0.0
        try:
            version = float(str(request_data['version']).strip());
        except:
            version = LASTEST_VERSION_API
            pass
        
        if (version == LASTEST_VERSION_API):
            return API_Running_V_0_1.Running_API_V_0_1(request_data)
        else:
            cherrypy.response.headers['Content-Type'] = "application/json"
            cherrypy.response.headers['Retry-After']=60
            cherrypy.response.status = 400
            message = {'error':'This version has not suppported yet'}
            return json.dumps(message)
            
    #Public /index
    index.exposed = True
    #publci /query
    query.exposed = True

if __name__ == '__main__':
    #Configure Server
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            'log.error_file':ERROR_LOG_CHERRYPY_8080,
                            'log.access_file':ACCESS_LOG_CHERRYPY_8080
                          })
    #Starting Server
    cherrypy.quickstart(LandPKS_API())
    #cherrypy.engine.start()
