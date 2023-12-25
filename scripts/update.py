from io import BytesIO
import os
import shutil

from urllib import request as requests
from zipfile import ZipFile

from resources.colour import *
from resources.config import *
from scripts.log import log_event

def get_updates(local_version, auto):
	if not os.path.isfile(DATAPATH + "/config/runtime_flags/updates") and auto: return -1

	log_event("Started an update", 1)

	if not auto: print(YELLOW + "Checking for updates...")

	if not check_updates(local_version):
		log_event("Already up to date", 1)
		if not auto: print(SEAFOAM + "WinLine is up to date" + RESET)

	else:
		if not auto: print(YELLOW + "Downloading update...")

		STAGE_PATH = DRIVELETTER + ":/ProgramData/winline_staging"

		try: shutil.rmtree(STAGE_PATH)
		except: NotImplemented
		finally: os.mkdir(STAGE_PATH)

		with requests.urlopen(SERVER_URL + "/winline.zip") as server:
			with ZipFile(BytesIO(server.read())) as package:
				package.extractall(STAGE_PATH)

		if not auto: print(YELLOW + "Installing update..." + RESET)

		try: 
			shutil.copytree(STAGE_PATH, DATAPATH, dirs_exist_ok=True)
			if not auto: print(SEAFOAM + "Update complete! " + YELLOW + "Restart WinLine to see new features" + RESET)

			shutil.rmtree(STAGE_PATH)
		except Exception as err:
			if not auto: print(RED + "Failed to install update")
			log_event(str(err), 3)

def check_updates(local_version):
	try: 
		latest_version = str(requests.urlopen(SERVER_URL + "/version").read(), "'UTF-8'")

		return (local_version < latest_version)

	except Exception as err:
		log_event("UPDATE_CHECK_FAILED: %s"%str(err), 3)
		return False
		