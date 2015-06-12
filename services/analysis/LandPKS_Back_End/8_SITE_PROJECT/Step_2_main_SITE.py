# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import shutil



# define
EXTEND_FILE_OPERATIONS = ".SIT"
DAT_DIRECTORY = ""
SITECOM_DAT_FILE_NAME = "SITECOM.DAT"
site_files_folder = ""
ACTION_FLAG = 1
# Check arguments
if (len(sys.argv) < 2):
    print("Sorry, not enough arguments")
    sys.exit("Usage : python main_SITE.py -fsite <Individual Site Files Folder Path> -fdat <Dat file Folder>")

# Input requires
full_path = os.getcwd() + "\\"
# Manage arguments
if (sys.argv[1] == '-fsite') :
    if (sys.argv[2] is None) :
        sys.exit("Usage : python main_SITE.py -fsite <Individual Site Files Folder Path> -fdat <Dat file Folder>")
    else:
        print("\n---Individual Site Files SIT are in Folder %s" % (sys.argv[2]))
        site_files_folder = sys.argv[2]
        site_files_folder = site_files_folder.replace("\\\\", "\\")
elif (sys.argv[1] == '-rm'):
    ACTION_FLAG = 0
else :
    sys.exit("Usage : python main_SITE.py -fsite <Individual Site Files Folder Path> -fdat <Dat file Folder>")

if (sys.argv[3] == '-fdat'):
    if (sys.argv[4] is None) :
        sys.exit("Usage : python main_SITE.py -fsite <Individual Site Files Folder Path> -fdat <Dat file Folder>")
    else:
        DAT_DIRECTORY = sys.argv[4]
        DAT_DIRECTORY = DAT_DIRECTORY.replace("\\\\", "\\")

# Function
def checkAndCreateFolder():
    directory = full_path + "\Site_Files"
    if not os.path.exists(directory):
        os.makedirs(directory)
    datDirectory = directory + "\%s" % ("DAT_Files")
    if not os.path.exists(datDirectory):
        os.makedirs(datDirectory)
def get_files_path(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
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
def createDATFile(site_folder):
    if (site_folder is None):
        sys.exit("---[Error] : Folder that contains SIT files are NOT existed")
    if not os.path.exists(site_folder):
        sys.exit("---[Error] : Folder that contains SIT files are NOT existed")
    try:
        fo = open(os.path.join(DAT_DIRECTORY, SITECOM_DAT_FILE_NAME), "wb")
        SITFiles = get_files_path(site_folder)
        count = 0
        maxLength = getMaxLengthOfFileName(SITFiles)
        for f in SITFiles:
            uF = f.upper()
            count = count + 1
            if uF.endswith(EXTEND_FILE_OPERATIONS):
                if (getLengthString(f) == maxLength):
                    if (count == 1):
                        strContent = "    %d %s  %s" % (count, f, "additional content")
                    else:
                        if (count >= 2 and count <= 9):
                            strContent = "\r\n    %d %s  %s" % (count, f, "additional content")
                        elif (count >= 10 and count <= 99):
                            strContent = "\r\n   %d %s  %s" % (count, f, "additional content")
                        elif (count >= 100 and count <= 999):
                            strContent = "\r\n  %d %s  %s" % (count, f, "additional content")
                        elif (count >= 1000 and count <= 9999):
                            strContent = "\r\n %d %s  %s" % (count, f, "additional content")
                        elif (count >= 10000 and count <= 99999):
                            strContent = "\r\n%d %s  %s" % (count, f, "additional content")
                else:
                    numberOfSpace = maxLength - getLengthString(f)
                    strAdd = ""
                    for i in range(0, numberOfSpace):
                        strAdd = strAdd + " "
                    if (count == 1):
                        strContent = "    %d %s  %s%s" % (count, f, strAdd, "additional content")
                    else:
                        if (count >= 2 and count <= 9):
                            strContent = "\r\n    %d %s  %s%s" % (count, f, strAdd, "additional content")
                        elif (count >= 10 and count <= 99):
                            strContent = "\r\n   %d %s  %s%s" % (count, f, strAdd, "additional content")
                        elif (count >= 100 and count <= 999):
                            strContent = "\r\n  %d %s  %s%s" % (count, f, strAdd, "additional content")
                        elif (count >= 1000 and count <= 9999):
                            strContent = "\r\n %d %s  %s%s" % (count, f, strAdd, "additional content")
                        elif (count >= 10000 and count <= 99999):
                            strContent = "\r\n%d %s  %s%s" % (count, f, strAdd, "additional content")
                fo.write(strContent)
        print("---Created %s file already---" % (SITECOM_DAT_FILE_NAME))
        fo.write("\r\n")
        return 1
    except Exception, err:
        sys.stderr.write('---[Error]: Write file raised Error %s ' % (err))
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
        createDATFile(site_files_folder)
        print("-FINISH : SITECOM.DAT is created and located in %s" % (DAT_DIRECTORY))
    else:
        deleteAllFolderAndFiles()
        sys.exit("===All data files and folder are removed======")
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
