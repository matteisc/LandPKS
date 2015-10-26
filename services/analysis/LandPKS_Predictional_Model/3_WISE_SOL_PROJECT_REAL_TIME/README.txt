1. Require Python 2.7.3 or above

2. Put Database File MDB is in the same folder with Python Script. 
   For example,
Python script is : ..\Working\main_ISRIC.py

and 

Python script is : ..\Working\main_HWSD.py

and database file is in : ..\Working\Database\ISRIC-WISE_ver3.mdb

and database file is in : ..\Working\Database\HWSD.mdb

3. Run script by command line
Run main_ISRIC :   python main_ISRIC.py -d \Database\ISRIC-WISE_ver3.mdb -c Afghanistan
Run main_ISRIC :   python main_HWSD.py -d \Database\HWSD.mdb -m 12188

In which Afghanistan is name of contry you want to extract data 


or 12188 is MU_GLOBAL that you want to get data

4. Waiting for a moment for script running

5. After complete with main_ISRIC, dat file will be located in : ..\Working\Result\DATFiles\SOILCOM.DAT
                                   sol files will be located in : ..\Working\Result\SOLFiles\*.SOL
								   
   After complete with main_HWSD, dat file will be located in : ..\Working\Result_HWSD\DATFiles\SOILCOM.DAT
                                  sol files will be located in : ..\Working\Result_HWSD\SOLFiles\*.SOL

