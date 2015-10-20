# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len
import sys
import os


X_MAX = 54
X_MIN = -23
Y_MAX = 37
Y_MIN = -34
def Build_DLY_Library():
    x = X_MIN
    while (x <= X_MAX):
        y = Y_MIN
        while (y <= Y_MAX):
             print "X = %s ; Y = %s" %(str(x), str(y))
             try:
                  command = "cd C:/xampp/htdocs/APEX/Python_APEX/2_WEATHER_PROJECT_REAL_TIME/2_1_Weather_Big_Data_Sets_NASA/ && python Run_Build_DLY_File_From_NASA_Data.py -x %s -y %s -start_year 1980 -end_year 2010" % (str(x),str(y))
                  print command
                  os.system(command)
             except Exception, err:
                  pass 
             y = y + 0.25
        x = x + 0.25
def main():
    Build_DLY_Library()

#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()
