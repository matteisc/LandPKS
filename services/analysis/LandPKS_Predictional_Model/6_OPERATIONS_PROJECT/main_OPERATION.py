﻿# Author : Thanh Nguyen
# 05/23/2014
#?/usr/local/bin
__version__ = "1"
import os
import sys
import shutil

#define
EXTEND_FILE_OPERATIONS = ".OPS"
DAT_DIRECTORY = "Operation_Files\DAT_Files"
OPSCCOM_DAT_FILE_NAME = "OPSCCOM.DAT"
operation_files_folder = ""
ACTION_FLAG = 1
# Check arguments
if (len(sys.argv) < 2):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python main_OPERATION.py -f <Individual Operations Files Folder Path>")

# Input requires
full_path = os.getcwd() + "\\"
operation_files_folder = ""
# Manage arguments
if (sys.argv[1] == '-f') :
    if (sys.argv[2] is None) :
        sys.exit("Usage : python main_OPERATION.py -f <Individual Operations Files Folder Path>")
    else:
        print("\n---Individual Operations Files OPS are in Folder %s" %(sys.argv[2]))
        operation_files_folder = full_path     +       sys.argv[2]
        operation_files_folder = operation_files_folder.replace("\\\\","\\")
elif (sys.argv[1] == '-rm'):
    ACTION_FLAG = 0
else :
    sys.exit("Usage : python main_OPERATION.py -f <Individual Operations Files Folder Path>")

#Function
def checkAndCreateFolder():
    directory = full_path + "\Operation_Files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory =  directory + "\%s" %("DAT_Files")
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
def get_files_path(directory):
    file_paths = []
    for root, directories,files in os.walk(directory):
        for filename in files:
            file_path = filename
            file_paths.append(file_path)
    return file_paths
def getMaxLengthOfFileName(files):
    max = 0
    for f in files:
        uF = f.upper()
        if (uF.endswith(EXTEND_FILE_OPERATIONS)):
            sizeF = len(f.strip())
            if (sizeF > max):
                max = sizeF
    return max
def getLengthString(str):
    if (str is None):
        return 0
    str = str.strip()
    return len(str)
def createDATFile(operation_folder):
    if (operation_folder is None):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    if not os.path.exists(operation_folder):
        sys.exit("---[Error] : Folder that contains DLY files are NOT existed")
    try:
        fo = open(os.path.join(DAT_DIRECTORY,OPSCCOM_DAT_FILE_NAME),"wb")
        OPSFiles = get_files_path(operation_folder)
        count = 0
        maxLength = getMaxLengthOfFileName(OPSFiles)
        for f in OPSFiles:
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_OPERATIONS):
                if (getLengthString(f) == maxLength):
                    if (count == 1):
                        strContent = "    %d %s  %s" %(count,f,"additional content")
                    else:
                        if (count >= 2 and count <= 9):
                            strContent = "\r\n    %d %s  %s" %(count,f,"additional content")
                        elif (count >= 10 and count <= 99):
                            strContent = "\r\n   %d %s  %s" %(count,f,"additional content")
                        elif (count >= 100 and count <= 999):
                            strContent = "\r\n  %d %s  %s" %(count,f,"additional content")
                        elif (count >= 1000 and count <= 9999):
                            strContent = "\r\n %d %s  %s" %(count,f,"additional content")
                        elif (count >= 10000 and count <= 99999):
                            strContent = "\r\n%d %s  %s" %(count,f,"additional content")
                else:
                    numberOfSpace = maxLength - getLengthString(f)
                    strAdd = ""
                    for i in range(0,numberOfSpace):
                        strAdd = strAdd + " "
                    if (count == 1):
                        strContent = "    %d %s  %s%s" %(count,f,strAdd,"additional content")
                    else:
                        if (count >= 2 and count <= 9):
                            strContent = "\r\n    %d %s  %s%s" %(count,f,strAdd,"additional content")
                        elif (count >= 10 and count <= 99):
                            strContent = "\r\n   %d %s  %s%s" %(count,f,strAdd,"additional content")
                        elif (count >= 100 and count <= 999):
                            strContent = "\r\n  %d %s  %s%s" %(count,f,strAdd,"additional content")
                        elif (count >= 1000 and count <= 9999):
                            strContent = "\r\n %d %s  %s%s" %(count,f,strAdd,"additional content")
                        elif (count >= 10000 and count <= 99999):
                            strContent = "\r\n%d %s  %s%s" %(count,f,strAdd,"additional content")
                fo.write(strContent)
        print("---Created %s file already---" %(OPSCCOM_DAT_FILE_NAME))
        fo.write("\r\n")
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' %(err))
    finally :
        # close the cursor and connection
        fo.close()
def deleteAllFolderAndFiles():
    if os.path.exists(DAT_DIRECTORY):
        try:
            shutil.rmtree(DAT_DIRECTORY)
        except OSError:
            pass
def main():
    if (ACTION_FLAG == 1):
        print("-PREPROCESSING : Create Folders--")
        checkAndCreateFolder()
        print("-START Step 1 : Create OPSCCOM.DAT File")
        createDATFile(operation_files_folder)
        print("-FINISH : OPSCCOM.DAT is created and located in %s" %(full_path + DAT_DIRECTORY))
    else:
        deleteAllFolderAndFiles()
        sys.exit("===All data files and folder are removed======")
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()