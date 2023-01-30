""" Uninstallation service file for WinLine """

import shutil, os, time

# Colors
BLUE = "\u001b[38;5;87m"
DRIVES = "\u001b[1;38;5;202m"
SPECIALDRIVE = "\u001b[1;38;5;120m"
SEAFOAM = "\u001b[1;38;5;85m"
RED = "\u001b[1;31m"
MAGENTA = "\u001b[1;35m"
DULLYELLOW = "\u001b[1;38;5;142m"
YELLOW = "\u001b[1;33m"
RESET = "\u001b[0m"

def uninstall_winline(DATAPATH):
    print("Waiting for WinLine to exit...")
    time.sleep(3)
    print(YELLOW + "\nWinLine Uninstaller")
    print(YELLOW + "Please select an option:")
    print(RED + "1. Uninstall and erase data\n2. Uninstall and keep data\n3. Cancel"+RESET)
                    
    selectActive = True
    while selectActive:
        option = input(BLUE + "Enter choice > " + RESET)
        selectActive = False

    if option == "1":
        print(YELLOW + "Fully uninstalling and purging data..." + RESET)
        try:
            shutil.rmtree(DATAPATH)
            print(RED + "WinLine has been fully uninstalled" + RESET)
            print(SPECIALDRIVE + "\nThanks for using WinLine! We're sad to be parting, but we understand your choice\nThis window will close momentarily" + RESET)
            os.abort()
        except Exception as err:
            print(RED + "WARNING: Uninstallation failed! Error: " + str(err) + RESET)

    elif option == "2":
        print(YELLOW + "Removing core files..." + RESET)
        os.remove(DATAPATH + "/terminal.py")
        os.remove(DATAPATH + "/utilities.py")
        shutil.rmtree(DATAPATH + "__pycache__", ignore_errors=True)
        print(SPECIALDRIVE + "\nThanks for using WinLine! We're sad to be parting, but we understand your choice\nThis window will close momentarily" + RESET)

    else:
        print(YELLOW + "Cancelled" + RESET)
        time.sleep(5)