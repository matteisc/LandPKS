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
        #recorder_name_list = support_rhm_sync_data.get_list_recorder_name_from_landpks()
        if ((LAST_DATE is None) or (len(LAST_DATE) <> 8) or not int(LAST_DATE)):
            last_update_date = support_rhm_sync_data.get_last_update_date()
            if ((last_update_date is None) or (len(last_update_date) <> 8)):
                last_update_date = "20140102"
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
                landinfor_landscapeNorthPhotoURL = str(record[2])
                landinfor_landscapeEastPhotoURL = str(record[3])
                landinfor_landscapeSouthPhotoURL = str(record[4])
                landinfor_landscapeWestPhotoURL = str(record[5])
                landinfor_soilPitPhotoURL = str(record[6])
                landinfor_soilSamplesPhotoURL = str(record[7])
                #result = support_rhm_sync_data.insert_rhm_data_to_rhm_store(rhm_name,rhm_recorder_name, rhm_transect, rhm_segment, rhm_date, rhm_canopy_height, rhm_canopy_gap, rhm_basal_gap,rhm_species_1_density,rhm_species_2_density, "", rhm_stick_segment_0, rhm_stick_segment_1 , rhm_stick_segment_2, rhm_stick_segment_3 ,rhm_stick_segment_4)
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
