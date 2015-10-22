1. Require Python 2.7.3 or above

2. Extract 7_SUBAREA_PROJECT.zip project and cop 7_SUBAREA_PROJECT folder in to your workspace such as ..\Working

2. SUB files are put in ..\Working\7_SUBAREA_PROJECT\Subarea_Files\Original_Subare_Files

3. How to run 

   Step 1: Run command : python -t Step_2_main_SUBAREA.py -f Subarea_Files\Original_Subarea_Files
   
           Output result : SUBACOM.DAT was created in \Working\7_SUBAREA_PROJECT\Subarea_Files\DAT_Files
   
   Step 2: Modify SUB File with the data about : Subarea number, operation number, daily weather numer.
           Run command : python -t Step_2_main_SUBAREA.py -m SUBS2.SUB -s 1343312188410LPq.SOL -default -o 2_shortgrass.ops -default -d 1268999999.Dly -default
           In which, SUBS2.SUB is file you want to modify
		             1343312188410LPq.SOL : Soil data file
					 -default : means that SOILCOM.DAT file was located in default Folder. In which it is : \Working\3_WISE_SOL_PROJECT\Result_HWSD\DATFiles
					    You can change default folder in file Step_2_main_SUBAREA.py
					    If you do not want to use default file, replace -default by your directory. Such as :  \Working\3_WISE_SOL_PROJECT\Result_HWSD\DATFiles\SOILCOM.DAT
                     2_shortgrass.ops : Operation File
					  -default : means that OPSCCOM.DAT file was located in default Folder. In which it is : \Working\6_OPERATIONS_PROJECT\Operation_Files\DAT_Files
					    You can change default folder in file Step_2_main_SUBAREA.py
					    If you do not want to use default file, replace -default by your directory. Such as :  \Working\6_OPERATIONS_PROJECT\Operation_Files\DAT_Files\OPSCCOM.DAT
					 1268999999.Dly : DLY File
					  -default : means that WDLSTCOM.DAT file was located in default Folder. In which it is : \Working\2_WEATHER_PROJECT\Weather_Files\DATFiles
					    You can change default folder in file Step_2_main_SUBAREA.py
					    If you do not want to use default file, replace -default by your directory. Such as :  \Working\2_WEATHER_PROJECT\Weather_Files\DATFiles\WDLSTCOM.DAT
		   After Running this script. 
		       Outputs are the modified SUB files, they are located in : ..\Working\7_SUBAREA_PROJECT\Subarea_Files\Modified_Subarea_Files
If you want to delete old data file, run command :  python main_WEATHER.py -rm
   
   Step 3: If you want to process many SUB file, write new code 
                 os.system("Step_2_main_SUBAREA.py -m SUBS1.SUB -s 1343112188230LVh.SOL -default -o 1_maize.ops -default -d 126435.Dly -default")
		   into Step_1_preprocessing_SUBAREA.py and change your parameters you want.
		   
		   Run command : python -t Step_1_preprocessing_SUBAREA.py


4. Waiting for a moment for script running

5. After complete with . SUBACOM.DAT was created in \Working\7_SUBAREA_PROJECT\Subarea_Files\DAT_Files
                         modified SUB files, they are located in : ..\Working\7_SUBAREA_PROJECT\Subarea_Files\Modified_Subarea_Files
								 
