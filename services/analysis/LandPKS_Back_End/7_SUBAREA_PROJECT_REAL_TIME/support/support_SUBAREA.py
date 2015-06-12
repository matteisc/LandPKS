# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"

try:
    from osgeo import gdal, ogr
    import numpy
    import struct, os, csv, codecs, cStringIO, sys
except Exception, err:
    print err
    sys.exit("Please install GDAL for Python")


try:
   import MySQLdb
except:
   sys.exit("Please install MySQLLib for Python")

db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="", db="apex")

PARSER_PERCENTAGE = '%'
PARSER_LEFT_PARENTHESIS = '('
PARSER_SPLASH = '-'


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

def get_soil_file_name_closest_user_input(similarity_file_path):
    if (not os.path.exists(similarity_file_path)):
        return None
    
    f = open(similarity_file_path, "rb")
    l = UnicodeReader(f)
    l.next()
    try:
       max_cosine = -1 
       selected_soil_name = ""
       
       for row in l:
           if (float(row[23])):
               current_cosin = float(row[23])
               if (current_cosin > max_cosine):
                   max_cosine = current_cosin
                   selected_soil_name =  str(row[0])
               else:
                   continue
           else:
               continue
       return [selected_soil_name + ".SOL",max_cosine]
    except:
       return None
def count_number_sol_file_in_class(SOL_FILE_LIST):
    count = 0
    for f in SOL_FILE_LIST:
        if "VRe" in f:
            count = count + 1
        elif "VRd" in f:
            count = count + 1
        elif "VRk" in f:
            count = count + 1
        elif "VRy" in f:
            count = count + 1
    return count
def get_soil_file_name_in_classes(SOL_FILE_LIST):
    for f in SOL_FILE_LIST:
        if "VRe" in f:
            return f
        elif "VRd" in f:
            return f
        elif "VRk" in f:
            return f
        elif "VRy" in f:
            return f
    return SOL_FILE_LIST[0]
def get_surface_craking_from_id(IDapex):
   cur = db.cursor() 
   cur.execute("SELECT surface_cracking FROM landpks_input_data WHERE ID = %d" %(int(IDapex)))
   for row in cur.fetchall() :
       if (row[0] is not None):
           return row[0].strip()
       else:
           return None
   return None 
def get_slope_value_from_id(IDapex):
   cur = db.cursor() 
   cur.execute("SELECT slope FROM landpks_input_data WHERE ID = %d" %(IDapex))
   for row in cur.fetchall() :
       if (row[0] is not None):
           return row[0]
       else:
           return ""
def check_is_number(string):
    try:
        float(string)
        return 1
    except:
        return -1
def get_float_percentage_number_of_slope_value(strSlope):
    #2
    if (strSlope is None):
        return 0.00
    if (strSlope == ""):
        return 0.00
    if (strSlope.strip() == ""):
        return 0.00
    if (strSlope == "0"):
        return 0.00

    try:
        if (float(strSlope)):
           return float(strSlope)
    except:
        pass
  
    int_index_percent = strSlope.index(PARSER_PERCENTAGE)
    
    if (int_index_percent >= 0 and int_index_percent <= len(strSlope)):
        before_percentage = strSlope[:int_index_percent]
        before_percentage = before_percentage.strip()
        if (check_is_number(before_percentage) == 1):
          if (float(before_percentage)):
              return float(before_percentage) / 100
          else:
              return 0.00
        else:
            int_index_lparent = before_percentage.index(PARSER_LEFT_PARENTHESIS)
            after_lparent = before_percentage[int_index_lparent+1:]
            after_lparent = after_lparent.strip()
            int_index_splash = after_lparent.index(PARSER_SPLASH)
            below_value = after_lparent[:int_index_splash]
            above_value = after_lparent[int_index_splash + 1:]
            float_below_value = 0.0
            float_above_value = 0.0
            try:
                float_above_value = float(above_value.strip())
                float_below_value = float(below_value.strip())
                float_middle_value = (float_above_value + float_below_value)/2
                return float(float_middle_value) / 100
            except:
                return 0.00
          
            return 0.00
    else:
        return 0.00
def get_slope_length_from_slope_range(slope_range):
    if (not float(slope_range)):
        return 5
    if (float(slope_range) >= 0.00 and float(slope_range) <= 0.02):
        return 50
    elif (float(slope_range) > 0.02 and float(slope_range) <= 0.05):
        return 35
    elif (float(slope_range) > 0.05 and float(slope_range) <= 0.08):
        return 20
    elif (float(slope_range) > 0.08 and float(slope_range) <= 0.16):
        return 10
    elif (float(slope_range) > 0.16 and float(slope_range) <= 0.3):
        return 7.5
    else:
        return 5
def getRasterValue_ThanhNH(srcfile, mx, my):  
    try:# # Return the value of a raster at the point that is passed to it
        src_ds = gdal.Open(srcfile) 
        gt = src_ds.GetGeoTransform() 
    
        # Convert from map to pixel coordinates.
        px = int((mx - gt[0]) / gt[1])  # x pixel
        py = int((my - gt[3]) / gt[5])  # y pixel
    
        rb = src_ds.GetRasterBand(1)
        structval = rb.ReadAsArray(px, py, 1, 1).astype(numpy.integer)
        return structval[0][0]
    except Exception,err:
        return -1
