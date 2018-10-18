import mysql.connector
from mysql.connector import Error
from logger import *
from traceback_info import *
import sys

ERR_1 = 1
ERR_2 = 2
ERR_FATAL = 3

class DB_Session_MySQL:

    def __init__(self, username, password, db_id):
        logger.debug(  "DB_Session_MySQL::__init__()" )
        self.username_ = username
        self.password_ = password
        self.db_id_ = db_id
        self.connection_ = None
        self.cursor_ = None

    def connect(self):
        logger.debug(  "DB_Session_MySQL::connect()" )
        try:
				self.connection_ = mysql.connector.connect(host='localhost', database=self.db_id_, user=self.username_, password=self.password_)
				self.cursor_ = self.connection_.cursor()
				#self.cursor_.arraysize = 300
				if self.connection_.is_connected():
					logger.debug(  "DB_Session_MySQL::connect() -> connected." )
					return True
        except Error as ex:
            logger.error(  "DB_Session_MySQL::connect() -> "
                           "MySQLException: %s" % (ex) )
        return False

    def disconnect(self):
        try:
                self.connection_.close()
        except Error, ex:
            logger.error(  "DB_Session_MySQL::disconnect() -> "
                           "MySQLException: %s" % (ex) )

    def rollback(self):
        try:
            self.connection_.rollback()
        except:
            return -1
        return 0

    def reconnect(self):
        self.disconnect()
        return self.connect()    

    def commit(self):
        logger.debug( "DB_Session_MySQL::commit()" )
        ret = 0
        try:
            self.connection_.commit()
        except Error, ex:
            logger.error(  "DB_Session_MySQL::commit() -> "
                           "MySQLException: %s" % (ex) )
            ret = -1
        return ret

    def execute( self, db_operation ):
        logger.debug(  "DB_Session_MySQL::execute()" )
        reconnect_tries = 5
        retry = True
        ret = 0
        while retry:
            try:
                logger.debug(  "DB_Session_MySQL::execute() -> "
                               "executing %s query." % db_operation.tag())
                ret = db_operation.execute( self.cursor_ )
                retry = False
            except Error, ex:
                retry = self.handle_exception( ex, reconnect_tries)
                reconnect_tries -= 1
                ret = -1
            except:
                logger.error( "DB_Session_MySQL::execute() -> "
                              "unhandled exception executing %s." % db_operation.tag() )
                logger.error( traceback_info() )
                retry = False
                ret = -1
        return ret
    def handle_exception(self, exception, retries):
        logger.error(  "DB_Session_MySQL::handle_exception() -> "
                       "MySQLException:  %s %s" % (exception, self.cursor_.statement ) )
        code = exception.args[0].code
        if not self.must_reconnect( code ) and \
           not self.must_rollback( code ):
                logger.error(  "DB_Session_MySQL::handle_exception() -> "
                               "Unable to handle exception." )
                self.rollback()
                return False
        retries -= 1
        if retries < 0:
            logger.warning( "DB_Session_MySQL::handle_exception() -> "
                            "Maximum number if retrue exceeded." )
            return False
        if self.must_reconnect( code ):
            logger.warning( "Attempting to reconnect current session.")
            self.reconnect()
            return True
        if self.must_rollback( code ):
            logger.warning( "Performing Rollback in current session.")
            self.rollback()
            return True
        return False

    def must_reconnect(self, code):
        return code == ERR_1 or code == ERR_2

    def must_rollback(self, code):
        return code == ERR_FATAL

    def driver_name(self):
        return "DB_Session_MySQL"
    
        

