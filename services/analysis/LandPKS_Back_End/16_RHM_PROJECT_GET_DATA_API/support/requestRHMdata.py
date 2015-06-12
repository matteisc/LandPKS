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


def getSegmentStr(coverList):
    
    ##COVER_1 ("Bare"),
    ##COVER_2 ("Trees"),
    ##COVER_3 ("Shrubs"),
    ##COVER_4 ("Sub-shrubs"),
    ##COVER_5 ("Perennial grasses"),
    ##COVER_6 ("Annuals"),
    ##COVER_7 ("Herb litter"),
    ##COVER_8 ("Wood litter"),
    ##COVER_9 ("Rock");
		
    segStr = ""
    if coverList[0]:
        segStr += "Bare, "
    if coverList[1]:
        segStr += "Trees, "
    if coverList[2]:
        segStr += "Shrubs, "
    if coverList[3]:
        segStr += "Sub-shrubs, "
    if coverList[4]:
        segStr += "Perennial grasses, "
    if coverList[5]:
        segStr += "Annuals, "
    if coverList[6]:
        segStr += "Herb Litter, "
    if coverList[7]:
        segStr += "Wood Litter, "
    if coverList[8]:
        segStr += "Rock, " 

    return segStr[:len(segStr)-2]

def getRHMdata(userName, date):       
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
    api = 'transectendpoint'
    version ='v1'
    #https://silicon-bivouac-496.appspot.com/_ah/api/transectendpoint/v1/transect?afterDate=2014-11-29&otherUser=dwkimiti%40gmail.com
    encodedUserName = userName.replace("@","%40")
    discovery_url = '%s/transectendpoint/v1/transect?afterDate=%s&otherUser=%s' % (api_root,date, encodedUserName)

    service = build(
          api, version, discoveryServiceUrl=discovery_url, http=http2)

    buildRHMData(userName, json.loads(service))



def buildRHMData(userName,data):

    if "items" not in data:
        return 
    for i, item in enumerate(data["items"]): #4 segments each item     
        name = item["siteID"]
        recorder_name = userName
        transect = item["direction"]
        for _segment in item["segments"]:
            segment = _segment["range"]
            date = _segment["date"]
            canopy_height = _segment["canopyHeight"]
            canopy_gap = _segment["canopyGap"]
            basal_gap = _segment["basalGap"]
            species_1_density = _segment["species1Density"]
            species_2_density = _segment["species2Density"]

            stick_segment_0 = getSegmentStr(_segment["stickSegments"][0]["covers"])
            stick_segment_1 = getSegmentStr(_segment["stickSegments"][1]["covers"])
            stick_segment_2 = getSegmentStr(_segment["stickSegments"][2]["covers"])
            stick_segment_3 = getSegmentStr(_segment["stickSegments"][3]["covers"])
            stick_segment_4 = getSegmentStr(_segment["stickSegments"][4]["covers"])

            global result 
            result.append([name,recorder_name,transect, segment,date,canopy_height,canopy_gap,
                   basal_gap,species_1_density,species_2_density,stick_segment_0,stick_segment_1,stick_segment_2,stick_segment_3,stick_segment_4])
        
    

def getListRHMdata(recorders,date):
    global result
    result = []
    for recorder in recorders :
        getRHMdata(recorder,date)
    return result


#getListRHMdata(['corwaal@gmail.com','ericha30@gmail.com'],"20100505")
