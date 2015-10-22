# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"




try:
   import MySQLdb
except:
   sys.exit("Please install MySQLLib for Python")

db = MySQLdb.connect(host="127.0.0.1",user="root",passwd="", db="apex")

PARSER_PERCENTAGE = '%'
PARSER_LEFT_PARENTHESIS = '('
PARSER_SPLASH = '-'


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

