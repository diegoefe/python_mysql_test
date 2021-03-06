from db_session import *
import localconf as lc
import sys

class Show_Tables:
    def __init__(self):
        pass
    def tag(self):
        return "Show_Tables"

    def execute(self, cursor):
        cursor.execute("show tables")
        row = cursor.fetchall()
        print(row)
        '''
        while row is not None:
            print(row)
            row = cursor.fetchone()
        '''
        print "son {0} filas".format(cursor.rowcount)
        return cursor.rowcount


DB = DB_Session(lc.user, lc.password, lc.db)
if DB.connect() == False:
    print "Error connecting to DB. Aborting."
    sys.exit(1)

    
showtbs = Show_Tables()
DB.execute(showtbs)

print "Using driver '{0}'".format(DB.driver_name())
