# Author : Thanh Nguyen
# 05/21/2014
#?/usr/local/bin
__version__ = "1"
import os
import pyodbc
import sys

# Check arguments
if (len(sys.argv) < 5):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python createDATscript.py -d <Database File Path> -c <Country Name> -o <Output File>")

# Input requires
db_file = ""
strCountry = ""
output_file = ""
full_path = os.getcwd() + "\\"
datDirectory = ""
solDirectory = ""

# Manage arguments
if (sys.argv[1] == '-d') :
    if (sys.argv[2] == "") :
        sys.exit("Usage : python createDATscript.py -d <Database File Path> -c <Country Name> -o <Output File>")
    else:
        db_file = full_path     +       sys.argv[2]
        db_file = db_file.replace("\\\\","\\")
else :
    sys.exit("Usage : python createDATscript.py -d <Database File Path> -c <Country Name> -o <Output File>")

if (sys.argv[3] == '-c') :
    if (sys.argv[4] == "") :
        sys.exit("Usage : python createDATscript.py -d <Database File Path> -c <Country Name> -o <Output File>")
    else:
        strCountry =  sys.argv[4]
else :
    sys.exit("Usage : python createDATscript.py -d <Database File Path> -c <Country Name> -o <Output File>")

# Set Up MSAccess Driver
user = ''
password = ''
odbc_conn_str = 'DRIVER={Microsoft Access Driver (*.mdb)};DBQ=%s;UID=%s;PWD=%s' % \
                (db_file, user, password)

#Function
def queryIDfollowCountry():
    try :
        conn = pyodbc.connect(odbc_conn_str)
        print("---Connected database successfully---")
        # create a cursor
        cur = conn.cursor()

        # extract all the data
        sql = "select WISE3_id from WISE3_SITE WHERE UCASE(WISE3_SITE.COUNTRY) LIKE '%" + strCountry.upper() + "%'"

        #print(sql)
        cur.execute(sql)

        # show the result
        result = cur.fetchall()

        # Preprocess checking
        numItems = len(result)

        if (numItems <= 0) :
            sys.exit("There is no any records for this country")
        else:
            print("---Select data successfully---")
        return result
    except Exception, err:
        sys.stderr.write('Please check correctness of database file %s' %(err))
    finally :
        # close the cursor and connection
        #fo.close()
        cur.close()
        conn.close()

def recordsDATFile(result):
    try:
        fo = open(os.path.join("Result/DATFiles/","SOILCOM.DAT"),"wb")
        count = 0
        print("---Write data to file SOILCOM.DAT---")
        for item in result:
            count += 1
            if (count == 1):
                strContent = "    %d %s.SOL" %(count,item[0])
            else:
                if (count >= 2 and count <= 9):
                   strContent = "\n    %d %s.SOL" %(count,item[0])
                elif (count >= 10 and count <= 99):
                   strContent = "\n   %d %s.SOL" %(count,item[0])
                elif (count >= 100 and count <= 999):
                   strContent = "\n  %d %s.SOL" %(count,item[0])
                elif (count >= 1000 and count <= 9999):
                   strContent = "\n %d %s.SOL" %(count,item[0])
                elif (count >= 10000 and count <= 99999):
                   strContent = "\n%d %s.SOL" %(count,item[0])
            fo.write(strContent)
        return 1
    finally :
        # close the cursor and connection
        fo.close()
def querySoilPropertyFollowWise3_ID(wise3_id):
    try :
        conn = pyodbc.connect(odbc_conn_str)
        print("---Query soil property from ID %s---" %(wise3_id))
        # create a cursor
        cur = conn.cursor()

        # extract all the data
        sql = "SELECT WISE3_ID, HONU, BOTDEP, SAND, SILT, PHH2O, ORGC, CACO3, CECSOIL, GRAVEL, BULKDENS FROM WISE3_HORIZON WHERE UCASE(WISE3_HORIZON.WISE3_ID) = '" + wise3_id.upper() + "' ORDER BY HONU ASC"

        #print(sql)
        cur.execute(sql)

        # show the result
        result = cur.fetchall()

        # Preprocess checking
        numItems = len(result)

        if (numItems <= 0):
            sys.exit("There is no any records for this ID")
        else:
            print("---Query Soil property successfully---")
        return result
    except Exception, err:
        sys.stderr.write('Please check correctness of database file %s' %(err))
    finally:
        cur.close()
        conn.close()
def createSOILFile(wise3_id,soilResult):
    try:
        #fo=open(wise3_id +".SOL","wb")
        fo = open(os.path.join("Result/SOLFiles/",wise3_id +".SOL"),"wb")
        print("---Write SOIL property to File %s.SOL" %(wise3_id))
        # Line 1
        fo.write("            %s" %(wise3_id))
        # Line 2
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 3
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 4 - BOTDEP col 5 - 0.01 - 10
        fo.write("\n")
        for item in soilResult:
            if (item[2] is not None):
                if (item[2] >= 0 and item[2] < 1000):
                    value = float (item[2]) / 100
                    strContent = "    %0.2f" %(value)
                else:
                    value = float (item[2]) / 100
                    strContent = "   %0.2f" %(value)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 5 - Moist bulk density - 0.5 - 2.5
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 6 - Water content at PWP - 0.01 - 0.5
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 7 - Water Content at FC - 0.1 - 0.6
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 8 - Sand Content - Col 24 - 1 - 99
        fo.write("\n")
        for item in soilResult:
            if (item[3] is not None):
                value = item[3]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 9 - Silt Content - Col 25 - 1 - 99
        fo.write("\n")
        for item in soilResult:
            if (item[4] is not None):
                value = item[4]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 10 - Initial Organic N - 100 - 5000 ppm
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 11 - Soil PH - Col 12 - 3 -> 9
        fo.write("\n")
        for item in soilResult:
            if (item[5] is not None):
                value = item[5]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 12 - Sum of Bases - 0 -> 150
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 13 - Organic C Conc % - Col 8 - 0.1 -> 10
        fo.write("\n")
        for item in soilResult:
            if (item[6] is not None):
                value = float(item[6])*0.1
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 14 -  Calcium Carbonate Content % - Col 10 - 0 -> 99
        fo.write("\n")
        for item in soilResult:
            if (item[7] is not None):
                value = float(item[7])*0.1
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 15 -  CEC - Col 22 - 0 -> 150
        fo.write("\n")
        for item in soilResult:
            if (item[8] is not None):
                value = item[8]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                elif (value >= 100 and value < 1000):
                    strContent = "  %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 16 -  Coarse Fragment - Col 27 - 0 -> 99
        fo.write("\n")
        for item in soilResult:
            if (item[9] is not None):
                value = item[9]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                elif (value >= 100 and value < 1000):
                    strContent = "  %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 17 - Initial Soluble N
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 18 - Initial Soluble P
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 19 - Crop Residue (t/ha)
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 20 -  Dry Bulk Density - Col 28 - 0 -> 2.0
        fo.write("\n")
        for item in soilResult:
            if (item[10] is not None):
                value = item[10]
                if (value >= 0 and value < 10):
                    strContent = "    %0.2f" %(value)
                elif (value >= 10 and value < 100):
                    strContent = "   %0.2f" %(value)
                elif (value >= 100 and value < 1000):
                    strContent = "  %0.2f" %(value)
                else:
                    strContent = "    %0.2f" %(0)
            else:
                strContent = "    %0.2f" %(0)
            fo.write(strContent)
        # Line 21 - Phosphorous sorption ratio - 0 -> 0.9
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 22 - Saturated conductivity 0.00001-100
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 23 - Lateral Hydraulic 0.00001-10
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 24 - Initial Organic P conc 50 - 1000
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 25 - Exchangeable K conc
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))
        # Line 26 - Electrical conductivity 0 - 50
        fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))

        # Line 27 -> 45
        for i in range(27,46):
            fo.write("\n    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f    %0.2f"  %(0,0,0,0,0,0,0,0,0,0))

    except Exception, err:
        sys.exit("Error : %s" %(err))
    finally:
        fo.close()
def checkAndCreateFolder():
    directory = full_path + "Result"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory =  directory + "\\" + "DATFiles"
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
    solDirectory = directory + "\\" + "SOLFiles"
    if not os.path.exists(solDirectory):
        os.makedirs(solDirectory)
def main():
    checkAndCreateFolder()
    print("-START Step 1:")
    result = queryIDfollowCountry()
    intRecord = recordsDATFile(result)
    if (intRecord == 1):
        print("-DONE Step 1---")
    else:
        print("----Problems----")
    print("-START Step 2 :")
    for item in result:
        if (item is None):
            continue
        else :
            if (item[0] is None):
                continue
            else:
                wise3_id = item[0].strip()
                soilResult = querySoilPropertyFollowWise3_ID(wise3_id)
                createSOILFile(wise3_id,soilResult)
    print("-DONE Step 2 :")
    print("-DAT File is located in %s" %(full_path + "Result" + "\\" + "DATFiles"))
    print("-SOL Files are located in %s" %(full_path + "Result" + "\\" + "SOLFiles"))
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
