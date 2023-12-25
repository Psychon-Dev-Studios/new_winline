import os, time
from time import localtime as tm

datapath = ""

def configureLogging(dpath):
	global datapath
	 
	datapath = dpath
	log_event("Logging module ready")

def log_event(message:str, severity=1):
	""" Append a message to the end of the log file.

		Available severity levels:
		  * 1 = Info (INFO)
		  * 2 = Warning (WARN)
		  * 3 = Error (ERROR)
		  * 4 = Catastrophic error (FATAL)\n
	"""
	  
	global datapath
	DATAPATH = datapath

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
	else:severity="SEVERITY.%s"%severity

	 ## Log to the file
	try:
		logFile = open(DATAPATH + "/winline.log", "a")
		logFile.write("%s -- %s: %s\n"%(currentTime, severity, message))
		logFile.close()
	except: NotImplemented