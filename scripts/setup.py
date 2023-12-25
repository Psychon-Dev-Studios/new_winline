# SCRIPT RESPONSIBLE FOR HANDLING FIRST-TIME SETUP

import os
import shutil

from resources.colour import *


def run(DATAPATH):
	print(YELLOW + "Welcome to WinLine!")
	print("Before you get started, we need to finish up a few things" + RESET)

	try:os.mkdir(DATAPATH + "/config")
	except:NotImplemented
	try:os.mkdir(DATAPATH + "/config/runtime_flags")
	except:NotImplemented
	try:os.mkdir(DATAPATH + "/addons")
	except:NotImplemented

	uname = input(BLUE + "Enter your desired username > " + RESET)
	enable_updates = input(BLUE + "Would you like automatic updates? [Y/N] > " + RESET)

	uname_file = open(DATAPATH + "/config/username", "x")
	uname_file.write(uname)
	uname_file.close()

	if enable_updates.lower() == "y":
		open(DATAPATH + "/config/runtime_flags/updates", "x").close()


def check(DATAPATH):
	if not os.path.isfile(DATAPATH + "/config/username"): run(DATAPATH)