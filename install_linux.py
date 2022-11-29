import os, sys, subprocess, time, shutil
from threading import Thread as td
from zipfile import ZipFile

os.system("title WinLine - Linux Installer")

BLUE = "\u001b[38;5;87m"
GREEN = "\u001b[1;38;5;120m"
RED = "\u001b[1;31m"
YELLOW = "\u001b[1;33m"
RESET = "\u001b[0m"

PATH = sys.path[0]
DATAPATH = "/home/%s/.winline"%os.getlogin()

if (os.path.isfile(PATH + "/winline.dat")):INSTALLABLE = True
else:INSTALLABLE = False

print(YELLOW + "### WinLine - Linux Installer ###" + RESET)

if not INSTALLABLE:
    print(RED + "Cannot find " + BLUE + "winline.dat" + RED + ". Make sure the file is in this directory: " + BLUE + PATH + RESET)

    time.sleep(5)
    os.abort()

else:
    os.system('clear')
    print(GREEN + "Installing WinLine" + RESET)
    print(YELLOW + "[                        ] " + RED + "0%" + RESET)

    try:os.mkdir(DATAPATH)
    except:shutil.rmtree(DATAPATH);os.mkdir(DATAPATH)
    with ZipFile(PATH + "/winline.dat") as data:
        data.extractall(DATAPATH)
        data.close()

    time.sleep(1)
    os.system("clear")
    print(GREEN + "Installing WinLine" + RESET)
    print(YELLOW + "[############             ] " + RED + "50%" + RESET)

    try:
        with ZipFile(sys.path[0] + "/winline_docs.dat") as data:
            data.extractall(DATAPATH + "/man")
            data.close()
    except Exception as err:NotImplemented
    if not os.path.isdir(DATAPATH + "/components"):
        try:
            with ZipFile(sys.path[0] + "/winline_components.dat") as data:
                data.extractall(DATAPATH + "/components")
                data.close()
        except Exception as err:NotImplemented

    time.sleep(1.3)
    os.system("clear")
    print(GREEN + "Installing WinLine" + RESET)
    print(YELLOW + "[#####################     ] " + RED + "80%" + RESET)

    print(YELLOW + "\nTo enable command-line support, we need to add a few files to your system. Some operating systems will require an administrator password to continue. Please enter it if prompted, or installation might not complete!" + RESET)

    datastring = """python3 %s/terminal.py"""%DATAPATH

    os.system("echo '%s' | sudo tee /bin/winline"%datastring)
    os.system("sudo chmod 777 /bin/winline")

    os.system('clear')
    print(GREEN + "Installing WinLine" + RESET)
    print(YELLOW + "[##########################] " + RED + "100%" + RESET)
    print(YELLOW + "\nInstallation complete! You can run WinLine by typing " + GREEN + "winline" + YELLOW + " into the terminal" + RESET)