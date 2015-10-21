# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys


from support import support_rhm_sync_data
from support import requestPlotPhotos
from __builtin__ import int, len

RECORDER_NAME = ""
LAST_DATE = ""

if (len(sys.argv) <> 5):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python Run_main_RHM_Sync_Data.py -recorder_name <Recorder Name> -date <Last Data Update>")
else:
    if (sys.argv[1] == '-recorder_name'):
        if (sys.argv[2] is not None):
            RECORDER_NAME = str(sys.argv[2])
        else:
            sys.exit("====[Error] : Error in Recorder Name")
        
        if (sys.argv[3] == '-date'):
            if (sys.argv[4] is not None):
               LAST_DATE = str(sys.argv[4])
            else:
               sys.exit("====[Error] : Error in Date")
        else:
            sys.exit("====[Error] : Error in Date") 
    else:
        sys.exit("====[Error] : Error in Recorder Name")
 
def main():
    if (RECORDER_NAME.upper() == "ALL"):
        print "Developed LandInfo Photo"
        if ((LAST_DATE is None) or (len(LAST_DATE) <> 8) or not int(LAST_DATE)):
            last_update_date = support_rhm_sync_data.get_last_update_date()
            if ((last_update_date is None) or (len(last_update_date) <> 8)):
                last_update_date = "20150101"
        else:
            last_update_date = LAST_DATE
        print "\n========================================\n"
        print "\n===Start Working====\n";
        print last_update_date
        print "\n========================================\n"
        #last_update_date = "20140102"
        # Request to Nasim get data 
        lst_records = requestPlotPhotos.getListPhotoUrls(last_update_date)
        #print last_update_date
        # For loop all result of Nasim to insert our database
        for  record in lst_records:
            try:
                print ("===Consider : %s \n" %(last_update_date));
                print record
                print ("\n")
                landinfor_name = str(record[0])
                landinfor_recorder_name = str(record[1])
                landinfor_landscapeNorthPhotoURL = str(record[4])
                landinfor_landscapeEastPhotoURL = str(record[5])
                landinfor_landscapeSouthPhotoURL = str(record[6])
                landinfor_landscapeWestPhotoURL = str(record[7])
                landinfor_soilPitPhotoURL = str(record[2])
                landinfor_soilSamplesPhotoURL = str(record[3])
                result = support_rhm_sync_data.update_photos_landinfo(landinfor_name,landinfor_recorder_name, landinfor_landscapeNorthPhotoURL, landinfor_landscapeEastPhotoURL, landinfor_landscapeSouthPhotoURL, landinfor_landscapeWestPhotoURL, landinfor_soilPitPhotoURL, landinfor_soilSamplesPhotoURL)
                if (result == 1):
                         print "\n ===Update successfully==="
                else:
                         print "\n ===Error ----"     
                
            except:
                pass
            
      
    else:
        print "Does not support now !"
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
