""" Logging service for background tasks """

import os, time
from time import localtime as tm

BLUE = "\u001b[38;5;87m"
YELLOW = "\u001b[1;33m"
RESET = "\u001b[0m"

def log_event(message:str, DATAPATH:str, severity=1):
    """ Append a message to the end of the log file.
        ### The following are the accepted SEVERITY levels:
        * 1 = Info (INFO)
        * 2 = Warning (WARN)
        * 3 = Error (ERROR)
        * 4 = Catastrophic error (FATAL)\n
     """

    currentTime = str(tm()[1]) + "/" + str(tm()[2]) + "/" + str(tm()[0]) + ", " + str(tm()[3]) + ":" + str(tm()[4])
    
    if not (os.path.isfile(DATAPATH + "/services.log")):
        lf = open(DATAPATH + "/services.log", "x")
        lf.write("%s -- %s: %s\n"%(currentTime, "INFO", "Log file created"))
        lf.close()

    ## Convert SEVERITY to string format ##
    if severity==1:severity="INFO"
    elif severity==2:severity="WARN"
    elif severity==3:severity="ERROR"
    elif severity==4:severity="FATAL"
    else:severity="-"

    ## Log to the file
    logFile = open(DATAPATH + "/services.log", "a")
    logFile.write("%s -- %s: %s\n"%(currentTime, severity, message))
    logFile.close()

def dump_log_to_terminal(DATAPATH):
    print(YELLOW + "Dumping log to terminal" + RESET)
    log_event("Dumping log contents", DATAPATH)

    logFile = open(DATAPATH + "/services.log", "r")

    print(logFile.read())
    logFile.close()