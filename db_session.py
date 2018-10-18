import mysql.connector
from mysql.connector import Error
from logger import *
from traceback_info import *
import sys

ERR_ENDCOMMCHANNEL        =  3113
ERR_NOTCONNECTED2ORACLE   =  3114
ERR_CONNLOSTCONTACT       =  3135
ERR_SESSIONKILLED         =    28
ERR_DISCONNECTIONFORCED   =  1092
ERR_NOTLOGGEDON           =  1012
ERR_SVC_HND_NOT_INIT_ORA  = 24324
ERR_CONNMUSTROLLBACK      = 25402

class DB_Session:

    def __init__(self, username, password, db_id):
        logger.debug(  "DB_Session::__init__()" )
        self.username_ = username
        self.password_ = password
        self.db_id_ = db_id
        self.connection_ = None
        self.cursor_ = None

    def connect(self):
        logger.debug(  "DB_Session::connect()" )
        try:
				self.connection_ = mysql.connector.connect(host='localhost', database=self.db_id_, user=self.username_, password=self.password_)
				self.cursor_ = self.connection_.cursor()
				#self.cursor_.arraysize = 300
				if self.connection_.is_connected():
					logger.debug(  "DB_Session::connect() -> connected." )
					return True
        except Error as ex:
            logger.error(  "DB_Session::connect() -> "
                           "MySQLException: %s" % (ex) )
        return False

    def disconnect(self):
        try:
                self.connection_.close()
        except Error, ex:
            logger.error(  "DB_Session::disconnect() -> "
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
        logger.debug( "DB_Session::commit()" )
        ret = 0
        try:
            self.connection_.commit()
        except Error, ex:
            logger.error(  "DB_Session::commit() -> "
                           "MySQLException: %s" % (ex) )
            ret = -1
        return ret

    def execute( self, db_operation ):
        logger.debug(  "DB_Session::execute()" )
        reconnect_tries = 5
        retry = True
        ret = 0
        while retry:
            try:
                logger.debug(  "DB_Session::execute() -> "
                               "executing %s query." % db_operation.tag())
                ret = db_operation.execute( self.cursor_ )
                retry = False
            except Error, ex:
                retry = self.handle_exception( ex, reconnect_tries)
                reconnect_tries -= 1
                ret = -1
            except:
                logger.error( "DB_Session::execute() -> "
                              "unhandled exception executing %s." % db_operation.tag() )
                logger.error( traceback_info() )
                retry = False
                ret = -1
        return ret
    def handle_exception(self, exception, retries):
        logger.error(  "DB_Session::handle_exception() -> "
                       "MySQLException:  %s %s" % (exception, self.cursor_.statement ) )
        code = exception.args[0].code
        if not self.must_reconnect( code ) and \
           not self.must_rollback( code ):
                logger.error(  "DB_Session::handle_exception() -> "
                               "Unable to handle exception." )
                self.rollback()
                return False
        retries -= 1
        if retries < 0:
            logger.warning( "DB_Session::handle_exception() -> "
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
        return code == ERR_ENDCOMMCHANNEL or\
               code == ERR_NOTCONNECTED2ORACLE or\
               code == ERR_CONNLOSTCONTACT or\
               code == ERR_SESSIONKILLED  or\
               code == ERR_DISCONNECTIONFORCED or\
               code == ERR_NOTLOGGEDON or\
               code == ERR_SVC_HND_NOT_INIT_ORA

    def must_rollback(self, code):
        return code == ERR_CONNMUSTROLLBACK


    
        

