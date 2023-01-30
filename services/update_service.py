""" Update service for WinLine """

import shutil, os, time
from zipfile import ZipFile
from urllib import request as urlRequest
from io import BytesIO
import services.service_logging as logging

# Colors
BLUE = "\u001b[38;5;87m"
DRIVES = "\u001b[1;38;5;202m"
SPECIALDRIVE = "\u001b[1;38;5;120m"
SEAFOAM = "\u001b[1;38;5;85m"
RED = "\u001b[1;31m"
MAGENTA = "\u001b[1;35m"
DULLYELLOW = "\u001b[1;38;5;142m"
YELLOW = "\u001b[1;33m"
DEV_COLOR = "\u001b[1;38;5;201m"
RESET = "\u001b[0m"

def update_winline(winConfig, REMOTE_SERVER, NON_WIN, DRIVELETTER, DATAPATH, VERSION_ID, OLD_VERSIONS, Appversion, VALID_CHANNELS):
    if (winConfig.REQUIRE_HTTPS and "https://" in REMOTE_SERVER.lower()) or not winConfig.REQUIRE_HTTPS:
        print(YELLOW + "Contacting server and checking for updates..." + RESET)
        if not NON_WIN:
                stage_path = DRIVELETTER + ":/ProgramData/wlstage"
        else:
                stage_path = "/tmp/wlstage"
        keepTrying = True
        failed = 0
        okay = True
        while keepTrying == True:
            try:
                chanfile = open(DATAPATH + "/channel", "r")
                channel = chanfile.read()
                CHANNEL = channel if channel in VALID_CHANNELS else "stable"
                chanfile.close()

                if CHANNEL == "stable":
                    server_version = str(urlRequest.urlopen(REMOTE_SERVER  + "/latest_version").read(), "'UTF-8'")
                else:
                    server_version = str(urlRequest.urlopen(REMOTE_SERVER  + "/latest_version_" + CHANNEL).read(), "'UTF-8'")
                # print(BLUE + "Current version: %s"%VERSION_ID + RESET)
                # print(YELLOW + "Latest version: %s"%server_version + RESET)
                keepTrying = False
            except:
                failed += 1
                time.sleep(1)

                if failed > 3:
                    keepTrying = False
                    okay = False
                    
    else:
        print(RED + "The current configuration requires an HTTPS connection, but an HTTP URL has been specified" + RESET)
        okay = False

    if okay:
        server_version = server_version.split("\n")[0]
        if (server_version != VERSION_ID) and not server_version in OLD_VERSIONS:
            print(YELLOW + "You are currently using WinLine " + SEAFOAM + Appversion + YELLOW + ", and version " + SEAFOAM + server_version + YELLOW + " is available" + RESET)
            print(DEV_COLOR + "The update will be pulled from the " + SPECIALDRIVE + CHANNEL + DEV_COLOR + " channel")
            cinst = input(BLUE + "Do you want to update? [Y/N] > " + RESET).capitalize()

            if cinst == "Y":
                print(YELLOW + "\nDownloading update..." + RESET)
                try:
                    os.mkdir(stage_path)
                except:
                    shutil.rmtree(stage_path)
                    os.mkdir(stage_path)
                everythingIsOkay = True
                keepTrying = True
                failed = 0

                try:
                    if CHANNEL == "stable":remFile = REMOTE_SERVER  + "/winline.dat"
                    else:remFile = REMOTE_SERVER  + "/winline_%s.dat"%CHANNEL

                    with urlRequest.urlopen(remFile) as remote_archive:
                        with ZipFile(BytesIO(remote_archive.read())) as update_package:
                            update_package.extractall(stage_path)
                    keepTrying = False
                except Exception as err:
                    failed += 1

                    if failed > 5:
                        everythingIsOkay = False
                        reason = str(err)
                        keepTrying = False

                if everythingIsOkay:
                    print(YELLOW + "Updating core files..." + RESET)
                    try:
                        shutil.copy(stage_path + "/terminal.py", DATAPATH + "/terminal.py")
                        shutil.copy(stage_path + "/utilities.py", DATAPATH + "/utilities.py")
                    except Exception as err:
                        print(RED + "Core files could not be updated: " + str(err) + ". Trying again may fix the issue"+ RESET)


                    print(YELLOW + "Downloading service files..." + RESET)
                    keepTrying = True
                    failed = 0
                    good = True
                    try:
                        with urlRequest.urlopen(REMOTE_SERVER  + "/winline_services.dat") as remote_archive:
                            with ZipFile(BytesIO(remote_archive.read())) as update_package:
                                update_package.extractall(DRIVELETTER + ":/ProgramData/wlstage")
                        keepTrying = False
                    except:
                        failed += 1
                        if failed > 5:
                            keepTrying = False
                            good = False

                    if good:
                        print(YELLOW + "Updating services..." + RESET)
                        try:
                            shutil.copy(stage_path + "/service_logging.py", DATAPATH + "/services/service_logging.py")
                            shutil.copy(stage_path + "/uninstall.py", DATAPATH + "/services/uninstall.py")
                            shutil.copy(stage_path + "/update_service.py", DATAPATH + "/services/update_service.py")
                            print(SPECIALDRIVE + "Update complete! Please restart WinLine to use the new version" + RESET)
                        except Exception as err:
                            print(RED + "Core files could not be updated: " + str(err) + ". Trying again may fix the issue"+ RESET)
                    else:
                        print(RED + "Failed to download service files" + RESET)

                    shutil.rmtree(stage_path, True)

                else:
                    print(RED + "Update failed: " + reason + ". Trying again may fix the issue"+ RESET)

        else:
            print(YELLOW + "WinLine is already up-to-date" + RESET)
            print(DEV_COLOR + "Current channel: " + SPECIALDRIVE + CHANNEL + RESET)
                        
    else:
        print(RED + "Unable to connect to server" + RESET)

    print("")
    try: shutil.rmtree(stage_path, True)
    except:NotImplemented

def update_winline_no_prompt(winConfig, REMOTE_SERVER, NON_WIN, DRIVELETTER, DATAPATH, VERSION_ID, OLD_VERSIONS, Appversion, VALID_CHANNELS):
    if (winConfig.REQUIRE_HTTPS and "https://" in REMOTE_SERVER.lower()) or not winConfig.REQUIRE_HTTPS:
        logging.log_event("Automatically checking for update...", DATAPATH, 1)
        if not NON_WIN:
                stage_path = DRIVELETTER + ":/ProgramData/wlstage"
        else:
                stage_path = "/tmp/wlstage"
        keepTrying = True
        failed = 0
        okay = True
        while keepTrying == True:
            try:
                chanfile = open(DATAPATH + "/channel", "r")
                channel = chanfile.read()
                CHANNEL = channel if channel in VALID_CHANNELS else "stable"
                chanfile.close()

                if CHANNEL == "stable":
                    server_version = str(urlRequest.urlopen(REMOTE_SERVER  + "/latest_version").read(), "'UTF-8'")
                else:
                    server_version = str(urlRequest.urlopen(REMOTE_SERVER  + "/latest_version_" + CHANNEL).read(), "'UTF-8'")
                # print(BLUE + "Current version: %s"%VERSION_ID + RESET)
                # print(YELLOW + "Latest version: %s"%server_version + RESET)
                keepTrying = False
            except:
                failed += 1
                time.sleep(1)

                if failed > 3:
                    keepTrying = False
                    okay = False
                    
    else:
        logging.log_event("Unable to download update, HTTPS is required, got HTTP", DATAPATH, 2)
        okay = False

    if okay:
        server_version = server_version.split("\n")[0]
        if (server_version != VERSION_ID) and not server_version in OLD_VERSIONS:
            cinst = "Y"

            if cinst == "Y":
                # print(YELLOW + "\nDownloading update..." + RESET)
                logging.log_event("Downloading update", DATAPATH, 1)
                try:
                    os.mkdir(stage_path)
                except:
                    shutil.rmtree(stage_path)
                    os.mkdir(stage_path)
                everythingIsOkay = True
                keepTrying = True
                failed = 0

                try:
                    if CHANNEL == "stable":remFile = REMOTE_SERVER  + "/winline.dat"
                    else:remFile = REMOTE_SERVER  + "/winline_%s.dat"%CHANNEL

                    with urlRequest.urlopen(remFile) as remote_archive:
                        with ZipFile(BytesIO(remote_archive.read())) as update_package:
                            update_package.extractall(stage_path)
                    keepTrying = False
                except Exception as err:
                    failed += 1

                    if failed > 5:
                        everythingIsOkay = False
                        reason = str(err)
                        keepTrying = False

                if everythingIsOkay:
                    # print(YELLOW + "Updating core files..." + RESET)
                    logging.log_event("Installing update", DATAPATH, 1)
                    try:
                        shutil.copy(stage_path + "/terminal.py", DATAPATH + "/terminal.py")
                        shutil.copy(stage_path + "/utilities.py", DATAPATH + "/utilities.py")
                    except Exception as err:
                        logging.log_event("Failed to update core files: " + str(err), DATAPATH, 3)
                        # print(RED + "Core files could not be updated: " + str(err) + ". Trying again may fix the issue"+ RESET)


                    # print(YELLOW + "Downloading service files..." + RESET)
                    logging.log_event("Downloading service files", DATAPATH, 1)
                    keepTrying = True
                    failed = 0
                    good = True
                    try:
                        with urlRequest.urlopen(REMOTE_SERVER  + "/winline_services.dat") as remote_archive:
                            with ZipFile(BytesIO(remote_archive.read())) as update_package:
                                update_package.extractall(DRIVELETTER + ":/ProgramData/wlstage")
                        keepTrying = False
                    except:
                        failed += 1
                        if failed > 5:
                            keepTrying = False
                            good = False

                    if good:
                        print(YELLOW + "Updating services..." + RESET)
                        try:
                            shutil.copy(stage_path + "/service_logging.py", DATAPATH + "/services/service_logging.py")
                            shutil.copy(stage_path + "/uninstall.py", DATAPATH + "/services/uninstall.py")
                            shutil.copy(stage_path + "/update_service.py", DATAPATH + "/services/update_service.py")
                            # print(SPECIALDRIVE + "Update complete! Please restart WinLine to use the new version" + RESET)
                            logging.log_event("Update complete", DATAPATH, 1)
                        except Exception as err:
                            # print(RED + "Core files could not be updated: " + str(err) + ". Trying again may fix the issue"+ RESET)
                            logging.log_event("Failed to update services: " + str(err), DATAPATH, 3)
                    else:
                        # print(RED + "Failed to download service files" + RESET)
                        logging.log_event("Failed to download service files", DATAPATH, 3)

                    shutil.rmtree(stage_path, True)

                else:
                    # print(RED + "Update failed: " + reason + ". Trying again may fix the issue"+ RESET)
                    logging.log_event("Update failed: " + reason, DATAPATH, 3)

        else:
            logging.log_event("No updates available", DATAPATH, 1)
            # print(YELLOW + "WinLine is already up-to-date" + RESET)
            # print(DEV_COLOR + "Current channel: " + SPECIALDRIVE + CHANNEL + RESET)
                        
    else:
        # print(RED + "Unable to connect to server" + RESET)
        logging.log_event("Unable to connect to server", DATAPATH, 1)

    # print("")
    try: shutil.rmtree(stage_path, True)
    except:NotImplemented