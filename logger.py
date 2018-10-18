from singleton import *
import logging.config

class Logger(Singleton):
    def __init__( self ):
        # Singleton
        self.logger_ = logging.getLogger("dummy")
        self.logger_.setLevel(logging.DEBUG)
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # add formatter to ch
        ch.setFormatter(formatter)
        # add ch to logger
        self.logger_.addHandler(ch)
        pass
    
    def init( self, *args ):
        qualname = args[0]

        # qualname, log_output, log_file
        if len(args) == 3:
            log_output = args[1]
            log_file = args[2]

            # Store args, maybe we need them later
            self.log_output = log_output
            self.log_file = log_file

            # First, create a logger and set base log level
            self.logger_ = logging.getLogger( qualname )
            self.logger_.setLevel( logging.DEBUG )

            # Now check what handler should we use
            if self.log_output == "file":
                if self.log_file:
                    self.logger_handler = logging.FileHandler(self.log_file, 'a')
                else:
                    self.logger_handler = logging.handlers.SysLogHandler('/dev/log')
            elif self.log_output == "console":
                self.logger_handler = logging.StreamHandler()
            else:
                self.logger_handler = logging.handlers.SysLogHandler('/dev/log')

            # Now we set the handler log level
            self.logger_handler.setLevel(logging.DEBUG)

            # Create a formatter
            self.logger_formatter = logging.Formatter("%(asctime)s %(name)s[%(process)d]: %(levelname)s: %(message)s")

            # Add formatter to handler
            self.logger_handler.setFormatter( self.logger_formatter )

            # Add handler to logger
            self.logger_.addHandler( self.logger_handler )

        # qualname, config_file
        elif len(args) == 2:
            config_file = args[1]
            logging.config.fileConfig(config_file)

        # qualname
        elif len(args) == 1:
            logging.config.fileConfig('common/logger.conf')

        self.logger_ = logging.getLogger( qualname )
    def debug(self, msg, *args, **kwargs):
        self.logger_.debug( msg, *args, **kwargs )
    def info(self, msg, *args, **kwargs):
        self.logger_.info( msg, *args, **kwargs )
    def warning(self, msg, *args, **kwargs):
        self.logger_.warn( msg, *args, **kwargs )
    def error(self, msg, *args, **kwargs):
        self.logger_.error( msg, *args, **kwargs )
    def critical(self, msg, *args, **kwargs):
        self.logger_.critical( msg, *args, **kwargs )
        
    def setLogLevel(self, level):
        self.logger_.setLevel(level)
    

logger = Logger()
logger.setLogLevel( logging.DEBUG )