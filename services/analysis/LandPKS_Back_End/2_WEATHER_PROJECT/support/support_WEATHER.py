# Author : Thanh Nguyen
# 05/23/2014
# ?/usr/local/bin
__version__ = "1"
from __builtin__ import len


def check_exit_record(ID, dly_file_name):
   try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
   except:
       sys.exit("Please install MySQLLib for Python") 
   try: 
       cur = db.cursor()
       sql = "SELECT COUNT(1) FROM landpks_map_input_files WHERE ID = %s and dly_file_name = '%s'" % (ID , dly_file_name)
       cur.execute(sql)
       results = cur.fetchone()[0]
       if (results):
           return 1
       return 0
   except Exception, err:
       print err
       db.close()
       return 0
   finally:
       db.close()
     
def insert_data_X_Y_dly_name(ID, Y, X, dly_file_name):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python") 
    try:
       dly_file_name = dly_file_name.strip()
       if (check_exit_record(ID, dly_file_name) == 0):
           print "insert data"
           cur = db.cursor()
           str_ID = str(ID)
           str_X = str(X)
           str_Y = str(Y)
           str_dly_file_name = str(dly_file_name)
           cur.execute("INSERT INTO landpks_map_input_files VALUES (%s,%s,%s,%s,%s)" % (str_ID, str_ID, str_Y, str_X, str_dly_file_name))
           db.commit()
       else:
          print "===Record existed"
    except Exception, err:
        print err
        db.rollback()
        pass
    finally:
        db.close() 
def get_coordinate_follow_dly_file_name(str_dly_file_name):
    try:
       import MySQLdb
       db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="apex")
    except:
       sys.exit("Please install MySQLLib for Python") 
    try:
       cur = db.cursor()
       str_dly_file_name = str_dly_file_name.strip()
       sql = "SELECT longitude, latitude FROM landpks_map_input_files WHERE dly_file_name = '%s'" % (str_dly_file_name)
       cur.execute(sql)
       results = cur.fetchone()
       if (results):
           X = results[0]
           Y = results[1]
           return str(X) + "|" + str(Y)
       return None
    except Exception, err:
        print err
        db.rollback()
        return None
        pass
    finally:
        db.close() 

