# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys


from support import support_rhm_sync_data
from support import requestRHMdata
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
        print "Developed"
        recorder_name_list = support_rhm_sync_data.get_list_recorder_name_from_landpks()
        if ((LAST_DATE is None) or (len(LAST_DATE) <> 8) or not int(LAST_DATE)):
            last_update_date = support_rhm_sync_data.get_last_update_date()
            if ((last_update_date is None) or (len(last_update_date) <> 8)):
                last_update_date = "20140102"
        else:
            last_update_date = LAST_DATE
            
        print "\n========================================\n"
        print "\n===Start Working====\n";
        print last_update_date
        print "\n"
        print recorder_name_list
        print "\n========================================\n"
        #last_update_date = "20140102"
        # Request to Nasim get data 
        lst_records = requestRHMdata.getListRHMdata(recorder_name_list,last_update_date)
        #print last_update_date
        # For loop all result of Nasim to insert our database
        for  record in lst_records:
            try:
                print ("===Consider : %s \n" %(last_update_date));
                print record
                print ("\n")
                rhm_name = str(record[0])
                rhm_recorder_name = str(record[1])
                rhm_transect = str(record[2])
                rhm_dominant_woody_species = str(record[3])
                rhm_dominant_nonwoody_species = str(record[4])
                rhm_species_of_interest_1 = str(record[5])
                rhm_species_of_interest_2 = str(record[6])                                    
                rhm_segment = str(record[7])
                rhm_date = str(record[8])
                rhm_canopy_height = str(record[9])
                rhm_canopy_gap = str(record[10])
                rhm_basal_gap = str(record[11])
                rhm_species_1_density = int(record[12])
                rhm_species_2_density = int(record[13])
                rhm_species_of_interest_1_count = int(record[14])
                rhm_species_of_interest_2_count = int(record[15])
                rhm_stick_segment_0 = str(record[16])
                rhm_stick_segment_1 = str(record[17])
                rhm_stick_segment_2 = str(record[18])
                rhm_stick_segment_3 = str(record[19])
                rhm_stick_segment_4 = str(record[20])
                if (not support_rhm_sync_data.check_exit_rhm_record(rhm_name,rhm_recorder_name,rhm_transect,rhm_segment)):
                    result = support_rhm_sync_data.insert_rhm_data_to_rhm_store(rhm_name,rhm_recorder_name, rhm_transect,rhm_dominant_woody_species,rhm_dominant_nonwoody_species,rhm_species_of_interest_1,rhm_species_of_interest_2, rhm_segment, rhm_date, rhm_canopy_height, rhm_canopy_gap, rhm_basal_gap,rhm_species_1_density,rhm_species_2_density,rhm_species_of_interest_1_count,rhm_species_of_interest_2_count, "", rhm_stick_segment_0, rhm_stick_segment_1 , rhm_stick_segment_2, rhm_stick_segment_3 ,rhm_stick_segment_4)
                    if (result == 1):
                         print "\n ===Insert successfully==="
                    else:
                         print "\n ===Error ----"     
                else:
                    print "\n ===Record existed==="
            except:
                pass
            
      
    else:
        list_recorder_name = [RECORDER_NAME]
        if ((LAST_DATE is None) or (len(LAST_DATE) <> 8) or not int(LAST_DATE)):
            last_update_date = support_rhm_sync_data.get_last_update_date_follow_recorder_name(RECORDER_NAME)
            if ((last_update_date is None) or (len(last_update_date) <> 8)):
                last_update_date = "20140102"
        else:
            last_update_date = LAST_DATE
            
        print "\n========================================\n"
        print "\n===Start Working====\n";
        print last_update_date
        print "\n"
        print list_recorder_name
        print "\n========================================\n"    
            
        lst_results = requestRHMdata.getListRHMdata(list_recorder_name,last_update_date)
        for record in lst_results:
            try:
                print ("===Consider : %s \n" %(last_update_date));
                print record
                print ("\n")
                rhm_name = str(record[0])
                rhm_recorder_name = str(record[1])
                rhm_transect = str(record[2])
                rhm_dominant_woody_species = str(record[3])
                rhm_dominant_nonwoody_species = str(record[4])
                rhm_species_of_interest_1 = str(record[5])
                rhm_species_of_interest_2 = str(record[6])                                    
                rhm_segment = str(record[7])
                rhm_date = str(record[8])
                rhm_canopy_height = str(record[9])
                rhm_canopy_gap = str(record[10])
                rhm_basal_gap = str(record[11])
                rhm_species_1_density = int(record[12])
                rhm_species_2_density = int(record[13])
                rhm_species_of_interest_1_count = int(record[14])
                rhm_species_of_interest_2_count = int(record[15])
                rhm_stick_segment_0 = str(record[16])
                rhm_stick_segment_1 = str(record[17])
                rhm_stick_segment_2 = str(record[18])
                rhm_stick_segment_3 = str(record[19])
                rhm_stick_segment_4 = str(record[20])
                if (not support_rhm_sync_data.check_exit_rhm_record(rhm_name,rhm_recorder_name,rhm_transect,rhm_segment)):
                    result = support_rhm_sync_data.insert_rhm_data_to_rhm_store(rhm_name,rhm_recorder_name, rhm_transect,rhm_dominant_woody_species,rhm_dominant_nonwoody_species,rhm_species_of_interest_1,rhm_species_of_interest_2, rhm_segment, rhm_date, rhm_canopy_height, rhm_canopy_gap, rhm_basal_gap,rhm_species_1_density,rhm_species_2_density,rhm_species_of_interest_1_count,rhm_species_of_interest_2_count, "", rhm_stick_segment_0, rhm_stick_segment_1 , rhm_stick_segment_2, rhm_stick_segment_3 ,rhm_stick_segment_4)
                    if (result == 1):
                         print "\n ===Insert successfully==="
                    else:
                         print "\n ===Error ----"     
                else:
                    print "\n ===Record existed==="
            except:
                pass
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
