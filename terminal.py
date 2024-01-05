# LIKE THE LICENSE SAYS, YOU'RE FREE TO MODIFY THIS CODE AND WHATNOT
# HOWEVER, PLEASE GIVE ME CREDIT BY LEAVING THIS LITTLE MESSAGE IN
# IF YOU'VE MODIFIED THE CODE: YOU MAY ADD YOUR NAME HERE

### WINLINE CONTRIBUTERS ###
# => MURDERAXOLOTL <= (ORIGINAL CREATOR)

VERSION_ID = "4.0"

# Developer keys
IGNORE_OS = True

# Imports
from genericpath import isdir
import os

# From 3.16ish onward, Linux is no longer supported ((even though I'm literally developing this in Linux))
if os.name != "nt" and not IGNORE_OS: #
	print(RED + "WinLine is only supported on Windows" + RESET)
	os.abort()

import sys, shutil, socket, subprocess, time, json, shlex
from io import BytesIO
from zipfile import ZipFile
from urllib import request as requests
from threading import Thread

from resources.colour import *
from resources.config import *

from scripts.log import configureLogging, log_event
import scripts.setup as setup
import scripts.update as update_util

# More constants
DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
DATAPATH = DRIVELETTER + ":/ProgramData/winLine"

setup.check(DATAPATH)
configureLogging(DATAPATH)

username = open(DATAPATH + "/config/username", "r").read()

os.system("cls")
print(DULLYELLOW + "WinLine %s"%VERSION_ID + RESET)
try:print(YELLOW + "Welcome back, %s!"%username)
except:
	print(YELLOW + "Welcome back!" + RESET)
	log_event("Failed to read username from disk", 3)

print("")

# Helpful variables for in-terminal shtuff
location = "C:/"
try:    iprompt = f"{MAGENTA}{username}{BLUE} %s{RESET}$ "
except: iprompt = f"{MAGENTA}User{BLUE} %s{RESET}$ "

def main():
	global location

	while True: # Terminal shouldn't ever break from this loop
		try:
			command = input(iprompt%location)

			match command.split(" ")[0]:
				case "ls": 
					try: os.system("dir %s"%command.split(" ", maxsplit=1)[1])
					except: os.system("dir")

				case "help":
					print(YELLOW + "Most commands are provided by the system. However, the ones listed here are handled by WinLine" + RESET)

					print(BLUE + """
help: show this message
raw: run raw python code
exit: close WinLine
term: start a new instance of WinLine
addons: manage addons. use \"addons help\" to learn more
username: change your username
mount_folder [drive] [folder] [mount_as]: mount [folder] as the network disk [mount_as]
unmount_folder [drive]: unmounts a virtual disk
uninstall: uninstall WinLine
""")

				case "raw": exec(command.split(" ", maxsplit=1)[1])
				case "exit" | "quit": os.abort()
				case "term":
					if "-r" in command: 
						os.system("clear")
						os.system("python %s"%__file__)
						sys.exit(); os.abort()
					else: os.startfile(__file__)

				case "addons":
					print(YELLOW + "NOT IMPLEMENTED" + RESET)

				case "mount_folder":
					try:
						drive = shlex.split(command)[3]
						sysd = shlex.split(command)[1]
						folder = shlex.split(command)[2]

						os.system("net use %s: \"\\\\localhost\\%s$\\%s\" /persistent:yes"%(drive,sysd,folder))

					except IndexError:
						print(YELLOW + "Usage: mount_folder c \"users/super epic/path\" x")

				case "unmount_folder": os.system("net use %s: /D"%command.split()[1])

				case "update": update_util.get_updates(VERSION_ID, False)

				case _: os.system(command)

			print("")

		except KeyboardInterrupt: print("")

		except Exception as err:
			print(RED + str(err) + RESET)
			log_event(str(err), 3)

try:
	if os.path.isfile(DATAPATH + "/config/updates"): Thread(name="Winline Updates", daemon=True, target=update_util.get_updates, args=(VERSION_ID, True)).start()
	main()
except Exception as err:
	print(RED + "UNCAUGHT FATAL EXCEPTION\n")
	log_event(str(err), 4)
	time.sleep(10)