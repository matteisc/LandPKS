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

mess = "Usage : python Run_main_RHM_Insert_Collection.py -input_csv <Full Path to Input CSV File>"
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
    #l.next()
    try:
       for row in l:
           name = row[0]
           record_name = row[1]
           transect = row[2]
           segment = row[3]
           date = row[4]
           canopy_height = row[5]
           canopy_gap = row[6]
           basal_gap = row[7]
           species_1_density = row[8]
           species_2_density = row[9]
           species_list = row[10]
           stick_0 = row[11]
           stick_1 = row[12]
           stick_2 = row[13]
           stick_3 = row[14]
           stick_4 = row[15]
           bare_total = row[16]
           trees_total = row[17]
           shrubs_total = row[18]
           sub_shrubs_total = row[19]
           grasses = row[20]
           annual = row[21]
           herb = row[22]
           wood = row[23]
           rock = row[24]
           
           
           print "================================================="
           request = "https://127.0.0.1/APEX/RHMSummary?name=%s&recorder_name=%s&transect=%s&segment=%s&date=%s&canopy_height=%s&canopy_gap=%s&basal_gap=%s&species_1_density=%s&species_2_density=%s&species_list=%s&stick_segment_0=%s&stick_segment_1=%s&stick_segment_2=%s&stick_segment_3=%s&stick_segment_4=%s&bare_total=%s&trees_total=%s&shrubs_total=%s&sub_shrubs_total=%s&perennial_grasses_total=%s&annuals_total=%s&herb_litter_total=%s&wood_litter_total=%s&rock_total=%s" %(str(name), str(record_name), str(transect), str(segment), str(date), str(canopy_height), str(canopy_gap), str(basal_gap), str(species_1_density), str(species_2_density), str(species_list), str(stick_0), str(stick_1), str(stick_2), str(stick_3), str(stick_4), str(bare_total), str(trees_total), str(shrubs_total), str(sub_shrubs_total), str(grasses), str(annual), str(herb), str(wood), str(rock)) 
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
    
