1. Require Python 2.7.3 or above

2. Extract Weather_Files.zip project and cop Weather_Files folder in to your workspace such as ..\Working

2. DLY files are put in ..\Working\2_WEATHER_PROJECT\Weather_Files\Daily_Weather_Files

3. Run script by command line 
Run Step 1 : python Step_1_preprocessing_WEATHER.py -in C:\xampp\htdocs\APEX\Python_APEX\2_WEATHER_PROJECT\Weather_Files\map_location.csv -ou Weather_Files\complete_map_location.csv -tif D:\ThanhNguyen_Working\Python_APEX\TIF_FILE_COLLECTION\
 
Run Step 2 : python Step_2_convert_wtg_to_dly_WEATHER.py -Fwtg D:\ThanhNguyen_Working\Python_APEX\TIF_FILE_COLLECTION\SLATE_Weather\wtg\ -Fdly D:\ThanhNguyen_Working\Python_APEX\TIF_FILE_COLLECTION\SLATE_Weather\dly\
  
Run Step 3 : python Step_3_main_WEATHER.py -f \Weather_Files\Daily_Weather_Files

Run Step 4 : python Step_4_postprocessing_WEATHER.py -Fcsv C:\xampp\htdocs\APEX\Python_APEX\2_WEATHER_PROJECT\Weather_Files\complete_map_location.csv -Fwp1 C:\xampp\htdocs\APEX\Python_APEX\2_WEATHER_PROJECT\Weather_Files\Complete_WP1_Files -Ftif D:\ThanhNguyen_Working\Python_APEX\TIF_FILE_COLLECTION\global_wind_tifs\ -Wyear 2001

If you want to delete old data file, run command :  python Step_3_main_WEATHER.py -rm


4. Waiting for a moment for script running

5. After complete with main_ISRIC, all dat file (WXPMRUN.DAT and WP1MO.DAT) will be located in : ..\Working\2_WEATHER_PROJECT\Weather_Files\DATFiles
                                   all raw DLY files locates in : ..\Working\Weather_Project\Weather_Files\Daily_Weather_Files
								   all modified DLY files locates in : ....\Working\2_WEATHER_PROJECT\Weather_Files\Temp_DLY_Files
								   all WP1 files locates in  : ..\Working\2_WEATHER_PROJECT\Weather_Files\WP1_Files
								   all INP files locates in  : ..\Working\2_WEATHER_PROJECT\Weather_Files\INP_OUT_Files
								   all OUT files locates in  : ..\Working\2_WEATHER_PROJECT\Weather_Files\INP_OUT_Files
								 
