import sys
import traceback

def traceback_info():
    filename, linenumber, module, variable = traceback.extract_tb(sys.exc_info()[2])[0] 
    return "File \"%s\", line %d, in %s\n%s: %s" % \
           (filename, linenumber, module, 
            sys.exc_info()[0].__name__, sys.exc_info()[1])

