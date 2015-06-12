# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
import os
import sys
import struct, os, csv, codecs, cStringIO, sys
import urllib2
from urllib2 import Request

CSV_INPUT_FILE = ""

mess = "Usage : python Run_main_CONTROLLER_collection.py -input_csv <Full Path to Input CSV File>"
if (len(sys.argv) < 2):
    print("Sorry, not enough arguments")
    sys.exit(mess)
else:
    if (sys.argv[1] == '-input_csv'):
        if (sys.argv[2] is not None):
            CSV_INPUT_FILE = sys.argv[2].strip()
        else:
            sys.exit(mess)
    else:
        sys.exit(mess)
        
class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")

class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
def main():
    f = open(CSV_INPUT_FILE, "rb")
    l = UnicodeReader(f)
    l.next()
    l.next()
    try:
       for row in l:
           name = row[0]
           mx, my = float(row[4]), float(row[3])
           record_name = row[1]
           slope = row[10]
           slope_shape = row[11]
           if (slope_shape is not None):
             slope_shape = slope_shape.upper()
           rockFrag_1 = row[12]
           rockFrag_2 = row[13]
           rockFrag_3 = row[14]
           rockFrag_4 = row[15]
           rockFrag_5 = row[16]
           rockFrag_6 = row[17]
           rockFrag_7 = row[18]
           text_1 = row[25]
           if (text_1 is not None):
               text_1 = text_1.strip().upper()
           text_2 = row[26]
           if (text_2 is not None):
               text_2 = text_2.strip().upper()
           text_3 = row[27]
           if (text_3 is not None):
               text_3 = text_3.strip().upper()
           text_4 = row[28]
           if (text_4 is not None):
               text_4 = text_4.strip().upper()
           text_5 = row[29]
           if (text_5 is not None):
               text_5 = text_5.strip().upper()
           text_6 = row[30]
           if (text_6 is not None):
               text_6 = text_6.strip().upper()
           text_7 = row[31]
           if (text_7 is not None):
               text_7 = text_7.strip().upper()
           print "================================================="
           print "Request : Name = %s ; X = %s; Y = %s ; Slope = %s, Slope Shape = %s , rock 1 = %s, rock_2 = %s, rock_3 = %s , rock_4 = %s, rock 5 = %s , rock_6 = %s, rock_7 = %s ; text 1 = %s , text 2 = %s , text_3 = %s, text_4 = %s , text_5 = %s, text_6 = %s , text_7 = %s " %(str(name),str(mx),str(my),str(slope),str(slope_shape),str(rockFrag_1),str(rockFrag_2),str(rockFrag_3),str(rockFrag_4),str(rockFrag_5),str(rockFrag_6),str(rockFrag_7),str(text_1),str(text_2),str(text_3),str(text_4),str(text_5),str(text_6),str(text_7))
           request = "https://127.0.0.1/APEX/SiteAnalysis?name=%s&recorder_name=%s&organization=&latitude=%s&longitude=%s&city=&modified_date=&land_cover=&grazed=&flooding=&slope=%s&slope_shape=%s&rock_fragment_for_soil_horizon_1=%s&rock_fragment_for_soil_horizon_2=%s&rock_fragment_for_soil_horizon_3=%s&rock_fragment_for_soil_horizon_4=%s&rock_fragment_for_soil_horizon_5=%s&rock_fragment_for_soil_horizon_6=%s&rock_fragment_for_soil_horizon_7=%s&color_for_soil_horizon_1=&color_for_soil_horizon_2=&color_for_soil_horizon_3=&color_for_soil_horizon_4=&color_for_soil_horizon_5=&color_for_soil_horizon_6=&texture_for_soil_horizon_1=%s&texture_for_soil_horizon_2=%s&texture_for_soil_horizon_3=%s&texture_for_soil_horizon_4=%s&texture_for_soil_horizon_5=%s&texture_for_soil_horizon_6=%s&texture_for_soil_horizon_7=%s&surface_cracking=false&surface_salt=false" %(str(name),str(record_name),str(my),str(mx),str(slope),str(slope_shape),str(rockFrag_1),str(rockFrag_2),str(rockFrag_3),str(rockFrag_4),str(rockFrag_5),str(rockFrag_6),str(rockFrag_7),str(text_1),str(text_2),str(text_3),str(text_4),str(text_5),str(text_6),str(text_7))
           request = request.replace(" ", "%20")
           print "HTTP : %s" %(request)
           content = urllib2.urlopen(request).read()
           print "Response : %s" %(content) 
    except Exception, err:
           print err
           print 1
#################################################
####MAIN
#################################################
if __name__ == '__main__':
    main()    
    
