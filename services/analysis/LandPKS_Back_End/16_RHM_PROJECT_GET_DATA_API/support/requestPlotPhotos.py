import json
from pprint import pprint

import argparse
import pprint
import sys

from googleapiclient.discovery import build
import httplib2
import oauth2client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.tools import run
from oauth2client.client import OAuth2WebServerFlow


result = []

def getPlotData(date):       
    date=date[0:4]+'-'+date[4:6]+'-'+date[6:8]
    SCOPES = ['https://www.googleapis.com/auth/userinfo.email',
                      'https://www.googleapis.com/auth/userinfo.profile']

    storage = Storage('RHM.dat')
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flow = OAuth2WebServerFlow(client_id='410858290704-pjirleeo4m55hme1ammq00fsbeb8nk33.apps.googleusercontent.com',
                               client_secret='V75kZtpAn-AEUnY0BZs6TFBN',
                               scope=SCOPES,
                               redirect_uri='http://google.com')
        
        credentials = run(flow, storage)

    http = httplib2.Http()
    http2 = credentials.authorize(http)

    api_root = 'https://silicon-bivouac-496.appspot.com/_ah/api'
    api = 'plotendpoint'
    version ='v1'
    #https://silicon-bivouac-496.appspot.com/_ah/api/plotendpoint/v1/plot?afterDate=2014-03-15&allUsers=true
    discovery_url = '%s/plotendpoint/v1/plot?afterDate=%s&allUsers=true' % (api_root,date)

    service = build(
          api, version, discoveryServiceUrl=discovery_url, http=http2)
    buildPhotoUrls(json.loads(service))

def getUrl(item,photoName):
    if(photoName in item.keys()):
        return(item[photoName])
    else:
        return ""
            
def buildPhotoUrls(data):

    if "items" not in data:
        return 
    for i, item in enumerate(data["items"]): #4 segments each item     
        name = item["name"]
        recorder_name = item["recorderName"]   
        landscapeNorthPhotoURL = getUrl(item,"landscapeNorthPhotoURL")
        landscapeEastPhotoURL = getUrl(item,"landscapeEastPhotoURL")
        landscapeSouthPhotoURL = getUrl(item,"landscapeSouthPhotoURL")
        landscapeWestPhotoURL = getUrl(item,"landscapeWestPhotoURL")
        soilPitPhotoURL = getUrl(item,"soilPitPhotoURL")
        soilSamplesPhotoURL = getUrl(item,"soilSamplesPhotoURL")

        global result 
        result.append([name,
                       recorder_name,
                       soilPitPhotoURL,
                       soilSamplesPhotoURL,
                       landscapeNorthPhotoURL,
                       landscapeEastPhotoURL,
                       landscapeSouthPhotoURL,
                       landscapeWestPhotoURL])

def getListPhotoUrls(date):
    global result
    result = []
    getPlotData(date)
    return (result)

#print getListPhotoUrls("20150513")

