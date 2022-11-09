VERSION_ID = "3.6"
PATCH_ID = 0
SVRMODE = 0 # Set to 1 to switch to a locally-served server on port 80

KEY_DEVMODE = "DEVELOPER.UNSTABLE.%s"%VERSION_ID
KEY_BETA = "GIT_BETA"
KEY_DISTMODE = "GIT_STABLE"

if SVRMODE == 0:
    REMOTE_SERVER = "https://psychon-dev-studios.github.io/nwl_stirehost"
else:
    REMOTE_SERVER = "http://localhost:80"

try:
    import os, sys, shutil, socket, subprocess, time, json
    from io import BytesIO
    from zipfile import ZipFile
    from urllib import request as urlRequest
    from threading import Thread as td
    from time import sleep
    if (os.name == "nt"):
        from ctypes import windll

    try:
        import utilities
    except:
        print("Warning: utility pack failed to import. Certain commands will not work correctly")
        time.sleep(5)

except Exception as err:
    import time
    try:
        import os, sys
        import shutil, socket, subprocess, json
        from zipfile import ZipFile
    except:
        NotImplemented
    print("Warning: Some modules failed to load. Some features will not work correctly")
    print("WinLine will continue startup momentarily")
    # time.sleep(999)
    time.sleep(4)

try:
    if (os.name == "nt"):osext=""
    else:NON_WIN = True;osext=" (Limited Non-Windows)"
except:osext=""

patchDisplay = "[Patch %s]"%PATCH_ID if PATCH_ID > 0 else  ""

try:
    if (sys.path[0] == "c:\\Users\\%s\\Downloads\\VisualStudioCode\\Python\\winLine"%open("C:/ProgramData/PsychonDevStudios/userKey.txt", "r").read() or sys.path[0] == "W:\\"):
        ISDEV = True
    else:
        ISDEV = False
except:ISDEV = False

try:
    if not (ISDEV):
        Appversion = VERSION_ID + " " + patchDisplay
    else:
        Appversion = KEY_DEVMODE + " " + patchDisplay
except:
    Appversion = VERSION_ID + " " + patchDisplay
loaded_components = []
enabled_components = []
found_dangerous = []

DANGEROUS_ADDONS_BUILTIN = "\nfake_dangerous"

try:os.system('title WinLine %s%s'%(Appversion,osext))
except:NotImplemented

BLUE = "\u001b[38;5;87m"
DRIVES = "\u001b[1;38;5;202m"
SPECIALDRIVE = "\u001b[1;38;5;120m"
RED = "\u001b[1;31m"
MAGENTA = "\u001b[1;35m"
DULLYELLOW = "\u001b[33m"
YELLOW = "\u001b[1;33m"
RESET = "\u001b[0m"

CRITICAL_BATTERY = "\u001b[38;5;160m"
DEV_COMPONENT = "\u001b[38;5;129m"

try:
    if os.name == "nt":
        DRIVELETTER = str(os.environ['WINDIR'].split(":\\")[0])
        DATAPATH = DRIVELETTER + ":/ProgramData/winLine"
    else:
        DRIVELETTER = ""
        DATAPATH = ""
except:
    DRIVELETTER = ""
    DATAPATH = ""

# config
try:
    config = open(DATAPATH + "/config", "r").read() # The file that the config is stored in
    version = open(DATAPATH + "/metadata/version", "r").read()
    # latest = str(urlRequest.urlopen("https://psychon-dev-studios.github.io/winline/metadata/version").read(), "'UTF-8'")
except:
    NotImplemented

ENABLEKEYBOARDINTURRUPT = "keyboardInturruptEnabled: true"
CMDLINK = "cmdLink: enabled"
ADVANCEDMODE = "advancedMode: enabled"
SYSRUN_FAILED_COMMANDS = "sysrun_failed_commands: true"
ALLOW_COMPONENTS = "allow_components: true"
EMULATE_LINUX = "emulate_linux: true"
SHOW_NAME = "display_username_win: true"
RESET_ON_ERROR = "prefer_reset_on_error: true"
ENABLE_AV_CHECK = "enable_malware_protection: true"
THREADED_AV_CHECK = "threaded_mw_protection: true"
USE_SAFE_MODE = "safe_mode: true"

try:
    if os.name == "nt" and os.path.isfile(DATAPATH + "/config"):
        if not (EMULATE_LINUX in config):NON_WIN = False;osext=""
        else:NON_WIN = True;osext=" (Linux Emulation)"
    elif not os.path.isfile(DATAPATH + "/config"):
        NON_WIN = False;osext=""
except:
    NON_WIN = True;osext=""

print("\a")

try:os.system('cls')
except:NotImplemented
if not ISDEV:
    print(DULLYELLOW + "WinLine " + Appversion + osext + RESET)
else:
    print(DEV_COMPONENT + "WinLine " + Appversion + osext + RESET)

if NON_WIN:
    print(RED + "\nThis instance of WinLine is running on a non-Windows operating system. Some features are unavailable, and some commands may not work correctly." + RESET)
    print(RED + "Configuration is only available on Windows. Some advanced features are unavailable" + RESET)

print("")

try:
    if not NON_WIN:
        location = DRIVELETTER + ":/"
        last_location = ""
        locprefix = ""
    else:
        location = "/"
        last_location = ""
        locprefix = MAGENTA + os.getlogin() + BLUE + "@" + SPECIALDRIVE + socket.gethostname() + RESET + " "
except:
    location = "/"
    last_location = ""
    locprefix = ""

def get_drives():
    if not NON_WIN:
        drives = []
        bitmask = windll.kernel32.GetLogicalDrives()
        for letter in map(chr, range(65, 91)):
            if bitmask & 1:
                drives.append(letter)
            bitmask >>= 1
        

        for letter in drives:
            if (letter == DRIVELETTER):
                print(SPECIALDRIVE + letter + ":/" + "  [Windows]" + RESET)
            else:
                print(DRIVES + letter + ":/" + RESET)
    else:
        print(RED + "This feature is only available on Windows systems" + RESET)

def doConfig():
    global config
    if not NON_WIN:
        if not (os.path.isfile(DATAPATH + "/config")) or (open(DATAPATH + "/config", "r").read() == ""):
            sleep(0.75)
            print(DULLYELLOW + "Welcome to WinLine!")
            sleep(2.5)
            print(BLUE + "Please wait for automatic setup to finish..." + RESET)
            sleep(1.5)

            try:
                os.mkdir(DATAPATH)

            except Exception as err:
                NotImplemented

            try:
                os.mkdir(DATAPATH + "/man")
            
            except Exception as err:
                NotImplemented


            try: 
                open(DATAPATH + "/setDone", "x").close()
                open(DATAPATH + "/loadedVersion", "x").close()
            except Exception as err:
                NotImplemented
            
            try:
                open(DATAPATH + "/config", "x")
                file = open(DATAPATH + "/config", "a")
                file.write("keyboardInturruptEnabled: true")
                file.write("\ncmdLink: disabled")
                file.write("\nadvancedMode: disabled")
                file.write("\nsysrun_failed_commands: false")
                file.write("\nallow_components: true")
                file.write("\nemulate_linux: false")
                file.write("\ndisplay_username_win: true")
                file.write("\nprefer_reset_on_error: false")
                file.write("\nenable_malware_protection: true")
                file.write("\nthreaded_mw_protection: true")
                file.write("\nsafe_mode: false")
                file.close()

            except:
                NotImplemented

            uname = input(BLUE + "\nWhat would you like to be called? > ")

            try:
                file = open(DATAPATH + "/owner_name", "x")
                file.write(uname)
                file.close()
            except:
                file = open(DATAPATH + "/owner_name", "w")
                file.write(uname)
                file.close()

            try:
                file = open(DATAPATH + "/development_components.txt", "x")
                file.close()
            except:NotImplemented

            # try:
            #     file = open(DATAPATH + "/loadedVersion", "x")
            #     file.write(Appversion)
            #     file.close()
            # except:
            #     NotImplemented
            
            print(BLUE + "Setup complete!\n" + RESET)

            sleep(1)
            print(DULLYELLOW + "To get started, use " + BLUE + "help " + DULLYELLOW + "to list supported commands.\n\n" + RESET)

            config = open(DATAPATH + "/config", "r").read()

        if not os.path.isdir(DATAPATH + "/components"):
            try:
                os.mkdir(DATAPATH + "/components")
            except:
                NotImplemented

        if not os.path.isdir(DATAPATH + "/components/staging"):
            try:
                os.mkdir(DATAPATH + "/components/staging")
            except:
                NotImplemented
        if not os.path.isdir(DATAPATH + "/components/disabled"):
            try:
                os.mkdir(DATAPATH + "/components/disabled")
            except:
                NotImplemented
        if not os.path.isdir(DATAPATH + "/components/unloaded"):
            try:
                os.mkdir(DATAPATH + "/components/unloaded")
            except:
                NotImplemented
        
        if not os.path.isdir(DATAPATH + "/components/packs"):
            try:
                os.mkdir(DATAPATH + "/components/unloaded")
            except:
                NotImplemented

        if not os.path.isfile(DATAPATH + "/owner_name"):
            uname = input(BLUE + "\nWhat would you like to be called? > ")
            try:
                file = open(DATAPATH + "/owner_name", "x")
                file.write(uname)
                file.close()
            except:
                file = open(DATAPATH + "/owner_name", "w")
                file.write(uname)
                file.close()

    else:
        config = "allow_components: true\nkeyboardInturruptEnabled: true\nadvancedMode: enabled\nsysrun_failed_commands: enabled\n"

doConfig()

if not (NON_WIN) and (SHOW_NAME in config):
    try:
        if os.path.isfile(DATAPATH + "/owner_name"):
            locprefix = MAGENTA + open(DATAPATH+"/owner_name", "r").read() + BLUE + "~ " + RESET
            if not ISDEV:
                print(YELLOW + "Welcome back, " + open(DATAPATH+"/owner_name", "r").read() + "!" + RESET)
            else:
                print(DEV_COMPONENT + "Welcome back, " + open(DATAPATH+"/owner_name", "r").read() + "! You're in developer mode." + RESET)
        else:
            locprefix = RED + "Local User" + BLUE + "~ " + RESET
            print(RED + "Welcome, Local User!" + RESET)
    except:
        NotImplemented

if not (USE_SAFE_MODE in config):
    if (ALLOW_COMPONENTS in config):
        if not NON_WIN:
            try:
                for add_on in os.listdir(DRIVELETTER + ":/ProgramData/WinLine/components/"):
                    if (".py" in add_on):loaded_components.append(add_on.split(".", 1)[0]);enabled_components.append(add_on.split(".", 1)[0])

                for add_on in os.listdir(DRIVELETTER + ":/ProgramData/WinLine/components/unloaded"):
                    if (".py" in add_on):enabled_components.append(add_on.split(".", 1)[0])
            except:loaded_components=[]
            try:
                if (open(DATAPATH + "/development_components.txt").read() != ""):
                    print(DEV_COMPONENT + "Developer components are installed" + RESET)
            except:NotImplemented
    else:loaded_components=[];print(RED + "Components have been disabled from the config file" + RESET);os.system("title WinLine %s (components disabled)"%Appversion)
else:
    print(YELLOW + "Safe mode is active" + RESET);os.system("title WinLine %s (safe mode)"%Appversion)

def checkForDangerousComponents():
    global found_dangerous
    dangerousCount = 0
    try:
        unsafe_components = str(urlRequest.urlopen(REMOTE_SERVER  + "/components/dangerous").read(), "'UTF-8'")
        verified_components = str(urlRequest.urlopen(REMOTE_SERVER  + "/components/official").read(), "'UTF-8'")
        unsafe_components = unsafe_components + "\n" + DANGEROUS_ADDONS_BUILTIN
    except Exception as err:
        unsafe_components = DANGEROUS_ADDONS_BUILTIN
        verified_components = ""
        if not THREADED_AV_CHECK in config:
            print(RED + "WARNING: Unable to reach A/V server. Built-in A/V may not be fully effective!" + RESET)

    try:
        for component in os.listdir(DATAPATH + "/components/disabled"):
            if component.split(".")[0] in unsafe_components:
                dangerousCount += 1
                try:
                    found_dangerous.append(component)
                except Exception as err:
                    NotImplemented
    except:
        NotImplemented

    for component in enabled_components:
        if component in unsafe_components:
            dangerousCount += 1
            try:
                shutil.move(DATAPATH + "/components/%s.py"%component, DATAPATH + "/components/disabled/")
                found_dangerous.append(component)
            except Exception as err:
                NotImplemented

    if dangerousCount != 0:
        if not THREADED_AV_CHECK in config:
            print(RED + "%s dangerous components were found and have been disabled"%dangerousCount + RESET)

def main():
    global location, last_location, cxrDevLocation, loaded_components, enabled_components, locprefix
    while True:
        try:
            command = input(locprefix + location + "> ").split(">", 1)
            command = command[0]
            command = command.strip("[")
            command = command.strip("'")
            command = command.strip("]")


            if (command.lower() == "help"):
                print(BLUE + "Supported commands: 'help', 'exit', 'clear', 'cd', 'ls', 'term', 'del', 'rmdir', 'cat', 'open', 'man', 'ipaddrs', 'ping', 'top', 'kill', 'clock', 'list-drives', stress, 'stress-2', 'monitor', 'components', 'change-name', 'user', 'battery-report', 'mount_folder', 'wldata', 'edition', 'path', 'reconfigure'")
                print("help: show this message\nexit: close the terminal\nclear: clear scrollback\ncd [path]: change directory to [path], throws exception if no path is specified\nls [path]: list files/folders in current directory, unless [path] is specified\nterm: start new instance of the terminal\ndel [path to file / file in CWD]: delete the specified file. If a path is not specified, del will try to remove a file in the CWD that matches. Aliases: 'remove'\nrmdir [path]: deletes the folder at [path] and all contained subfolders and files\ncat [path]: read the file at [path]\nopen [path]: open the file specified in [path] using the default application (which can be changed in Windows Settings)\nman [command]: get documentation about [command]\nipaddrs: get the device's IP\nping [destination] [count]: ping [destination] exactly [count] times. If [count] is not specified, [count] is assumed to be 10.\ntop: list running processes\nkill [PID]: kill a process by PID\nclock: start the clock service, use ctrl+c to resume normal operation.\nlist-drives: lists all drives currently connected to the device\nstress: run a CPU stress test, usually capable of redlining all CPU cores on reasonable systems\nstress-2: run a RAM stress test, usually capable of redlining RAM and maxing swap\nmonitor: keep track of CPU, RAM, swap, battery, and more.\ncomponents: list installed add-on components. use '--help' to see all options\nchange-name [new name]: change the user's identity\nuser: display the user's identity\nmount_folder [network drive] [local drive] [folder]: mount [folder] from [local drive] as a network drive with letter [network drive]\nunmount_folder [network drive]: unmount a network drive\nreconfigure: update the config file to work with the installed version of WinLine\nwldata: open data folder\nedition: get info about release edition\npath: print the current working directory\n" + RESET)
                # """camx [flags]: launch CamX: Rebirth if installed. use '--new' to launch in a new terminal and '--dev' to launch from a developer installation\n"""
                
                print(SPECIALDRIVE + "cmd: directly interface with Windows' command line. Exit cmd with ctrl+c or typing 'exit' to return to WinLine\npowershell: switch the current WinLine instance to a Powershell terminal. Use 'exit' to return to WinLine" + RESET)


                if (ADVANCEDMODE in config):
                    print(SPECIALDRIVE + "\nAdvanced commands: 'reset-term', 'sysRun'")
                    print("For more info, warnings, and usage examples, use " + RED + "man secretCommands" + RESET)

                if len(loaded_components) != 0:
                    print(YELLOW + "\nAddon components have added additional commands. Use the " + BLUE + "components " + YELLOW + "command to list them" + RESET)
                elif not (ALLOW_COMPONENTS in config):
                    print(RED + "\nWARNING: Components have been disabled from the config file. Additional features, including component management, are disabled" + RESET)
                

                if (NON_WIN):
                    print(RED + "Some features are only available on Windows and have been disabled automatically.\n")

                print("")


            elif (command.lower() == "exit"):
                os.abort()


            elif (command.split(maxsplit=1)[0] == "cd"):
                loc = ""
                try:
                    loc = "%s" % command.split(maxsplit=1)[1]

                    if not (loc == ".."):
                        if not (loc == DRIVELETTER + ":/"):
                            if (loc[0] == "/"):
                                loc = loc.split("/", maxsplit=1)[1]

                            if (loc[(len(loc) - 1)] == "/"):
                                loc = loc.rsplit("/", maxsplit=1)[0]

                            if (os.path.isdir(location + loc)):
                                location = location +  loc + "/"

                            elif (os.path.isdir(loc)):
                                location = loc + "/"

                            else:
                                print(RED + "No directory at " + loc + RESET)
                        
                        else:
                            location = DRIVELETTER + ":/"

                    else:
                        if (location != DRIVELETTER + ":/"):
                            try:
                                command = command.split(maxsplit=1)
                                path = location.split("/")
                                spare = path.pop()
                                spare = path.pop()
                                
                                location = ""

                                for segment in path:
                                    location = location + segment + "/"
                                
                                if (location == ""):
                                    location = DRIVELETTER + ":/"
                        
                            except Exception as err:
                                print(RED + "An unexpected problem is preventing relative navigation: " + str(err) + ". Try navigating using a full drive path (example: 'C:/users/example/desktop/examples'" + RESET)

                        else:
                            print(RED + "Can't back out of top-level drive path" + RESET)

                except Exception as err:
                    print(RED + "No path entered" + RESET)
                print("")


            elif (command.split(maxsplit=1)[0] == "ls"):
                abort = False
                try:
                    if (command.split(maxsplit=1)[1] != "/"):
                        pathToList = location + "%s" % command.split(maxsplit=1)[1]
                        dirContents = os.listdir(pathToList)
                    else:
                        print(BLUE + "Listing drives..." + RESET)
                        get_drives()
                        dirContents = ""

                except IndexError:
                    NotImplemented
                    pathToList = location
                    dirContents = os.listdir(location)

                except PermissionError:
                    print(RED + "Permission denied" + RESET)
                    abort = True

                except Exception as err:
                    print(RED + "Path not found, showing contents of " + location + RESET)
                        
                    pathToList = location
                    dirContents = os.listdir(location)
                
                if not abort:
                    try:
                        testStr = pathToList.split("/")
                        try:
                            if (testStr[len(testStr) - 1] == ""):
                                pathToList = pathToList[:-1]
                        except:
                            NotImplemented
                    
                    except Exception as err:
                        if ("BitLocker" in str(err)):
                            print(RED + "That device is protected by BitLocker. You need to unlock it through the File Explorer to continue" + RESET)


                    index = 0

                    for contents in dirContents:
                        if ((os.path.isdir(pathToList + "/" + contents)) or (os.path.isdir(location + "/" + contents))):
                            print(MAGENTA + contents + RESET)
                            index += 1
                        else:
                            print(contents)
                            index += 1
                print("")


            elif (command.lower() == "clear"):
                os.system('cls')


            elif (command.split(maxsplit=1)[0] == "term" or command.lower() == "term"):
                if (("-r" in command) or ("restart" in command)):
                    os.system('cls')
                    os.system('title ' + __file__)
                    sleep(1)
                    subprocess.call("python " + __file__)
                    sys.exit()
                    os.abort()

                else:
                    os.startfile(__file__)

            
            elif ((command.split(maxsplit=1)[0] == "del") or (command.split(maxsplit=1)[0] == "remove")):
                try:
                    pathToFile = "%s" % command.split(maxsplit=1)[1]

                    if (os.path.isfile(location + "/" + pathToFile)):
                        pathToFile = location + "/" + pathToFile

                    elif (os.path.isfile(pathToFile)):
                        pathToFile = pathToFile

                    os.remove(pathToFile)

                    print(BLUE + "File removed" + RESET)

                except Exception as err:
                    if (str(err) == "list index out of range"):
                        print(RED + "File name or path to file not provided" + RESET)

                    elif ("[WinError 2] The system cannot find the file specified" in str(err)):
                        print(RED + "File does not exist" + RESET)

                    elif ("[WinError 5] Access is denied" in str(err)):
                        print(RED + "Access to the file was denied" + RESET)

                    elif (os.path.isdir(pathToFile) or os.path.isdir(location + "/" + pathToFile)):
                        print(RED + "Specified path points to a directory. Use" + BLUE + " rmdir " + RED + "to delete a directory" + RESET)

                    else:
                        print(RED + "An unexpected error is preventing the removal of this file: " + str(err))
                print("")

            
            elif (command.split(maxsplit=1)[0] == "rmdir"):
                try:
                    try:
                        pathToFile = "%s" % command.split(maxsplit=2)[2]
                        
                        if (os.path.isdir(location + "/" + pathToFile)):
                            pathToFile = location + "/" + pathToFile

                        elif (os.path.isdir(pathToFile)):
                            pathToFile = pathToFile

                        shutil.rmtree(pathToFile)
                        print(BLUE + "Directory removed" + RESET)
                    except:
                        pathToFile = "%s" % command.split(maxsplit=1)[1]

                        if (os.path.isdir(location + "/" + pathToFile)):
                            pathToFile = location + "/" + pathToFile

                        elif (os.path.isdir(pathToFile)):
                            pathToFile = pathToFile

                        cont = input(RED + "Are you sure you want to continue? This will remove ALL files and directories contained in it! [Y/N] > " + RESET).capitalize()
                        if (cont == "Y"):
                            shutil.rmtree(pathToFile)
                            print(BLUE + "Directory removed" + RESET)
                        else:
                            print(BLUE + "Abort" + RESET)

                except Exception as err:
                    try:
                        pathToFile = pathToFile
                    except:
                        pathToFile = ""

                    # print(str(err))
                    if ("[WinError 2] The system cannot find the file specified" in str(err)):
                        print(RED + "Directory does not exist" + RESET)

                    elif (os.path.isfile(pathToFile) or os.path.isfile(location + "/" + pathToFile)):
                        print(RED + "Specified path points to a file. Use" + BLUE + " del " + RED + "to delete a file" + RESET)

                    elif ("list index out of range" in str(err)):
                        print(RED + "Directory name or path not provided" + RESET)

                    elif ("[WinError 5] Access is denied" in str(err)):
                        print(RED + "Access to the directory, subdirectories, or contained files was denied" + RESET)

                    else:
                        print(RED + "An unexpected error is preventing the removal of this directory: " + str(err) + RESET)
                print("")

            
            elif (command.split(maxsplit=1)[0] == "cat"):
                try:
                    pathToFile = "%s" % command.split(maxsplit=1)[1]

                    if (os.path.isfile(location + "/" + pathToFile)):
                        pathToFile = location + "/" + pathToFile

                    elif (os.path.isfile(pathToFile)):
                        pathToFile = pathToFile

                    file = open(pathToFile, "r").read()

                    print(file)

                except Exception as err:
                    if ("[WinError 2] The system cannot find the file specified" in str(err)):
                        print(RED + "File does not exist" + RESET)

                    elif ("list index out of range" in str(err)):
                        print(RED + "File name or path not provided" + RESET)

                    elif ("[WinError 5] Access is denied" in str(err)):
                        print(RED + "Access to the file was denied" + RESET)

                    elif ("[Errno 13] Permission denied" in str(err)):
                        print(RED + "Access to the file was denied" + RESET)

                    else:
                        print(RED + "An unexpected error is preventing the reading of the file: " + str(err) + RESET)
                print("")


            elif (command.split(maxsplit=1)[0] == "open"):
                try:
                    pathToFile = "%s" % command.split(maxsplit=1)[1]

                    if (os.path.isfile(location + "/" + pathToFile)):
                        pathToFile = location + "/" + pathToFile

                    elif (os.path.isfile(pathToFile)):
                        pathToFile = pathToFile

                    os.startfile(pathToFile)
                    print(BLUE + "Opened the file using default application" + RESET)

                except:
                    print(RED + "Unable to open the file" + RESET)
                print("")
                

            elif (command.split(maxsplit=1)[0] == "man"):
                # NotImplemented
                # print(RED + "Man pages are currently unavailable" + RESET   )

                try:
                    manReq = "%s" % command.split(maxsplit=1)[1]
                    manPage = open(DATAPATH + "/man/" + manReq + ".txt", "r").read()
                    if (manReq == "components") and not ("Warnings: COMPONENTS ARE NOT SANITIZED AND CAN POSE A SECURITY RISK." in manPage):
                        print(RED + "Component manual page has been compromised and will not be shown. WinLine will use the emergency internal page instead.")
                    print(manPage)

                except Exception as err:
                    if ("list index out of range" in str(err)):
                        print(RED + "Command not provided" + RESET)
                    else:
                        print(RED + "Unable to get manual page for '" + DULLYELLOW + command.split(maxsplit=1)[1] + RED + "'" + RESET)
                print("")


            elif (command.lower() == "about"):
                try:
                    aboutPage = open(DATAPATH + "/about.txt", "r").read()

                    print("\n")
                    print(aboutPage)

                except Exception as err:
                    print(YELLOW + "WinLine: a better terminal for Windows")
                    print(BLUE + "Developer: " + MAGENTA + "Psychon Development Studios")
                    print(BLUE + "Version: " + MAGENTA + Appversion)
                    try:
                        advmd = "ENABLED" if ADVANCEDMODE in config else "DISABLED"
                        cpn = "ENABLED" if ALLOW_COMPONENTS in config else "DISABLED"
                    except:advmd="?";cpn="?"
                    if (NON_WIN):cpn="DISALLOWED"
                    print(BLUE + "Advanced mode: " + MAGENTA + advmd)
                    print(BLUE + "Components: " + MAGENTA + cpn)
                    print(YELLOW + "\nOUR GOAL:" + RESET + "\nWinLine is intended to provide a better terminal experience, similar to the linux terminal, for Windows users. This is a fully-featured terminal emulator, with customization, addon capabilities, and more. You can even run Windows system commands by enabling SysRun in the configuration!\nWinLine will never connect to the internet unless you direct it to (such as for using ScreenCast or the ping command), and your data will never leave your device. In addition, your terminal history is immediately erased after closing the window, making sure your commands are never read." + RESET)

                    if NON_WIN:
                        print(RED + "\nThis instance of WinLine is running on a non-Windows operating system. Some features are unavailable, and some commands may not work correctly." + RESET)
                print("")


            elif ((command.lower() == "ipaddrs") or (command.lower() == "ipconf")):
                try:
                    ipaddrs = socket.gethostbyname(socket.gethostname())

                    if (ipaddrs != "127.0.0.1"):
                        print(BLUE + ipaddrs + RESET)

                    else:
                        print(BLUE + "127.0.0.1" + RESET)
                        print(RED + "A potential problem with your internet connection has been detected" + RESET)
                except Exception as err:
                    print(RED + "Error: failed to get device IP info: " + str(err) + RESET)
                print("")

            
            elif (command.split(maxsplit=2)[0] == "ping"):
                try:
                    target = command.split()[1]

                    try:
                        count = command.split()[2]
                    except:
                        count = 10

                    try:
                        subprocess.run('ping -n %s %s' % (count, target))
                    except Exception as err:
                        print(RED + str(err) + RESET)
                
                except KeyboardInterrupt:
                    print(BLUE + "Abort" + RESET)

                except Exception as err:
                    print(RED + "No IP address specified" + RESET)
                
                print("")              


            elif (command.split(maxsplit=1)[0] == "sysRun"):
                if not (USE_SAFE_MODE in config):
                    try:
                        os.system(command.split(maxsplit=1)[1])
                    except KeyboardInterrupt:
                        print("")
                else:
                    print(YELLOW + "Disabled in safe mode" + RESET)


            elif (command == "cmd"):
                if not NON_WIN:
                    os.system('title WinLine %s%s - COMMAND LINE'%(Appversion,osext))
                    subprocess.call("cmd.exe")
                    os.system('title WinLine %s%s'%(Appversion,osext))
                else:
                    print(RED + "This command is only available on Windows" + RESET)

            elif (command == "powershell"):
                if not NON_WIN:
                    os.system('title WinLine %s%s - POWERSHELL'%(Appversion,osext))
                    subprocess.call("powershell")
                    os.system('title WinLine %s%s'%(Appversion,osext))
                else:
                    print(RED + "This command is only available on Windows" + RESET)


            elif (command.split(maxsplit=1)[0] == "ssh"):
                try:
                    target = command.split(maxsplit=1)[1]

                    print("\n" + BLUE + "Attempting an SSH connection to " + target + RESET + "\n")

                    try:
                        subprocess.run("ssh " + target)
                    
                    except KeyboardInterrupt:
                        print(BLUE + "Abort" + RESET)
                    
                    except Exception as err:
                        print(RED + "Unexpected error: " + str(err))

                    finally:
                        os.system('cls')
                        subprocess.call("python " + __file__)

                except:
                    print(RED + "Hostname or IP not specified" + RESET)

            
            elif (command == "top"):
                subprocess.call("tasklist /FO TABLE")
                # subprocess.call("tasklist /?")


            elif (command.split(maxsplit=1)[0] == "kill"):
                try:
                    if (command.split(maxsplit=1)[1] != "/?"):
                        subprocess.call("taskkill /F /PID " + command.split(maxsplit=1)[1])
                    else:
                        subprocess.call("taskkill /?")
                except IndexError:
                    print(RED + "No process specified" + RESET)
                
            
            elif (command == "reset-term"):
                if not NON_WIN:
                    print("")
                    print(RED + "Warning: Resetting application data will reset all preferences and purge your data. This action CANNOT be undone. THIS WILL ERASE ALL COMPONENTS AND SCRIPTS!")
                    cont = input("Are you sure you want to continue? [Y/N] > " + RESET).capitalize()

                    if (cont == "Y"):
                        print(RED + "Deleting data..." + RESET)
                        try:
                            shutil.rmtree(DATAPATH, ignore_errors=True)
                        except Exception as err:
                            print(str(err))
                            sleep(1)

                        sleep(2.25)
                        os.system('cls')
                        subprocess.call("python " + __file__)
                        sys.exit()
                    sleep(1)
                else:
                    print(RED + "WinLine cannot be reset on this system because local data is only stored on Windows systems" + RESET)

            
            elif (command == "clock"):
                try:
                    while True:
                        datetime = time.strftime("%A, %B %d, %G, %I:%M:%S %p   ")
                        sys.stdout.write("\u001b[2K\r" + datetime)
                except:
                    print("\n")

            elif (command == "tellTheTruth"):
                sys.stdout.write(u"\x1b[1A" + u"\x1b[2K" + "\r")

            elif (command == "list-drives" or command == "ld"):
                get_drives()

            elif (command.split(maxsplit=1)[0] == "hide"):
                if not NON_WIN:
                    target = command.split(maxsplit=1)[1]

                    subprocess.call("attrib +s +h %s"%target)
                    print(SPECIALDRIVE + "Done\n" + RESET)

                else:
                    print(RED + "This feature is only available on Windows" + RESET)

            elif (command.split(maxsplit=1)[0] == "show"):
                if not NON_WIN:
                    target = command.split(maxsplit=1)[1]

                    subprocess.call("attrib -s -h %s"%target)
                    print(SPECIALDRIVE + "Done\n" + RESET)
                else:
                    print(RED + "This feature is only available on Windows" + RESET)

            elif command == "explorer.exe":
                if not NON_WIN:
                    print(RED + "Killing explorer...")
                    subprocess.call("taskkill /PID explorer.exe /F")
                    time.sleep(1)
                    print(SPECIALDRIVE + "Launching explorer..." + RESET)
                    subprocess.run("explorer.exe")
                else:
                    print(RED + "This feature is only available on Windows")

            elif command == "monitor":
                if not (USE_SAFE_MODE in config):
                    try:
                        sys.stdout.write(u"\x1b[?25l")
                        cached_battery = "okay"
                        # for level in range(0, 100, 1):
                        #     import psutil
                        #     print(utilities.colorBatteryPercentage(level, psutil.sensors_battery(), RED, YELLOW, SPECIALDRIVE, BLUE, CRITICAL_BATTERY, RESET ))
                        # time.sleep(30)
                        while True:
                            import psutil

                            cpuPercentage = psutil.cpu_percent(percpu=True)
                            cpuTime = psutil.cpu_times_percent()
                            diskUsage = psutil.disk_usage(DRIVELETTER + ":/")
                            completeCpuUsageString = ""
                            coreN = 1
                            ramPercentage = str(utilities.colorCpuUsage("", psutil.virtual_memory()[2],RED, YELLOW, SPECIALDRIVE, RESET))
                            ramUsage = (str(utilities.colorRamUsage(psutil.virtual_memory().used/(1024.0 ** 3),psutil.virtual_memory().total/(1024.0 ** 3),RED, YELLOW, SPECIALDRIVE, RESET)))
                            # ramUsage = psutil.virtual_memory()[1]
                            swapPercentage = str(utilities.colorCpuUsage("", psutil.swap_memory().percent,RED, YELLOW, SPECIALDRIVE, RESET))
                            swapUsage = str(utilities.colorRamUsage(psutil.swap_memory().used/(1024.0 ** 3),psutil.swap_memory().total/(1024.0 ** 3),RED, YELLOW, SPECIALDRIVE, RESET))
                            battery = psutil.sensors_battery()
                            batteryCharge = str(utilities.colorBatteryPercentage(int(battery.percent), battery, RED, YELLOW, SPECIALDRIVE, BLUE, CRITICAL_BATTERY, RESET))

                            try:
                                net_stat = str(psutil.net_if_stats().get("Wi-Fi").isup)
                            except:net_stat = False

                            for core in cpuPercentage:
                                completeCpuUsageString = completeCpuUsageString + utilities.colorCpuUsage(coreN, int(core), RED, YELLOW, SPECIALDRIVE, RESET) + " | "
                                coreN += 1
                        
                            completeCpuUsageString= completeCpuUsageString + utilities.colorCpuUsage("total", psutil.cpu_percent(percpu=False), RED, YELLOW, SPECIALDRIVE, RESET) + " avg"

                            completeCpuTime = "%s | %s | %s "%(utilities.colorCpuTime("User", cpuTime[0], RED, DULLYELLOW, SPECIALDRIVE, RESET),utilities.colorCpuTime("System",cpuTime[1], RED, DULLYELLOW, SPECIALDRIVE, RESET),utilities.colorCpuTimeInverse("Idle",cpuTime[2], RED, DULLYELLOW, SPECIALDRIVE, RESET))
                            
                            print(u"\x1b[0J\x1b[H")
                            sys.stdout.write(u"\x1b[?25l")
                            os.system("cls")
                            # print(u"\x1b[?25l")
                            print("CPU: " + completeCpuUsageString)
                            print("CPU: " + str(completeCpuTime))
                            print(RESET + "RAM: " + str(ramPercentage) + " | " + str(ramUsage))
                            print(RESET + "Swap: " + str(swapPercentage + " | " + swapUsage))
                            # print(RESET + "Disk: " + str(diskUsage.free/1e+9) + " GB /" + str(diskUsage.total/1e+9) + " GB (%s)"%diskUsage.percent)
                            print(RESET + "Battery: " + str(batteryCharge))
                            print(RESET + "Network: " + str(psutil.net_io_counters(pernic=False, nowrap=True).bytes_sent) + " sent, " + str(psutil.net_io_counters(pernic=False, nowrap=True).packets_recv) + " received, " + utilities.colorNetStatus(net_stat, RED, YELLOW, SPECIALDRIVE, RESET))
                            print(YELLOW + "\nLooking for a battery health report? Run the " + BLUE + "battery-report" + YELLOW + " command instead" + RESET)
                            time.sleep(1)

                    except ModuleNotFoundError:
                        sys.stdout.write(u"\x1b[?25h")
                        print(RED + "Installing dependency" + RESET)
                        try:
                            subprocess.call("pip install psutil")
                            print(DULLYELLOW + "Run " + BLUE + " term -r" + DULLYELLOW + " to finish installation")
                        except:print(RED + "Error while installing." + RESET)
                

                    except KeyboardInterrupt:
                        print("\n")
                        sys.stdout.write(u"\x1b[?25h")

                    except Exception as err:
                        print(RED + "Error: " + str(err) + RESET)
                        sys.stdout.write(u"\x1b[?25h")
                
                else:
                    print(YELLOW + "Disabled in safe mode" + RESET)

            elif command.split()[0] == "size":
                if not os.path.isdir(command.split()[1]):
                    size = os.path.getsize(command.split()[1])
                    try:
                        
                        print(str(round(size/1e+6, 3)) + " MB")
                    except Exception as err:print(str(err))
                else:print(YELLOW + "This command only works for files!\n" + RESET)

            elif command == "battery-report":
                if NON_WIN:
                    print(RED + "This feature is only supported on Windows" + RESET)
                else:
                    subprocess.call("powercfg /batteryreport /output C:/Users/" + os.getlogin() + "/Downloads/battery_report.html")
                    print("The report will be opened in your default browser momentarily.")
                    os.startfile("C:/Users/%s/Downloads/battery_report.html"%os.getlogin())

            elif ("components" in command or "component" in command or "addons" in command):
                if NON_WIN:print(RED + "Warning: Components are not supported on non-Windows systems")
                if not (ALLOW_COMPONENTS in config):print(RED + "Warning: Components have been disallowed from the configuration file\n\n" + RESET)
                if not (USE_SAFE_MODE in config):
                    try:
                        try:flags = command.split(maxsplit=1)[1]
                        except: flags = ""

                        if ("--unload" in flags):
                            try:whatToUnload = command.split(maxsplit=2)[2]
                            except:whatToUnload = "all"
                            ignore_load_status = open(DATAPATH + "/development_components.txt").read()

                            

                            if whatToUnload == "all":
                                print(RED + "Unloading all components..." + RESET)
                                while len(loaded_components) > 0:
                                    gotten = loaded_components.pop()
                                    shutil.move(DATAPATH + "/components/%s.py"%gotten, DATAPATH + "/components/unloaded/%s.py"%gotten)
                                    print(DRIVES + "Component %s unloaded"%gotten + RESET)
                                    # print(loaded_components)
                                    time.sleep(0.1)
                            else:
                                if (whatToUnload in loaded_components) and not whatToUnload in ignore_load_status:
                                    try:
                                        shutil.move(DATAPATH + "/components/%s.py"%whatToUnload, DATAPATH + "/components/unloaded/%s.py"%whatToUnload)
                                        loaded_components.remove(whatToUnload)
                                        print(DRIVES + "Component unloaded" + RESET)
                                    except:
                                        print(RED + "Unable to unload component" + RESET)

                                elif whatToUnload in ignore_load_status:
                                    print(DEV_COMPONENT + "Developer components can't be unloaded" + RESET)
                                elif (whatToUnload in enabled_components):print(RED + "Component already unloaded" + RESET)
                                
                                else:print(RED + "Component can't be loaded because it's not enabled. Restart WinLine to enable it" + RESET)

                        elif "--load" in flags:
                            if (ALLOW_COMPONENTS in config):
                                try:
                                    whatToLoad = command.split(maxsplit=2)[2]
                                    ignore_load_status = open(DATAPATH + "/development_components.txt").read()

                                    if (whatToLoad in enabled_components) and not whatToLoad in ignore_load_status:
                                        try:
                                            shutil.move(DATAPATH + "/components/unloaded/%s.py"%whatToLoad, DATAPATH + "/components/%s.py"%whatToLoad)
                                            loaded_components.append(whatToLoad)
                                            print(DRIVES + "Component loaded" + RESET)
                                        except:
                                            print(RED + "Unable to load component" + RESET)

                                    elif whatToLoad in ignore_load_status:
                                        print(DEV_COMPONENT + "Developer components are always loaded" + RESET)
                                    
                                    elif (whatToLoad in loaded_components):
                                        print(YELLOW + "Component is already loaded" + RESET)

                                    else:
                                        print(RED + "Component can't be loaded" + RESET)

                                except:
                                    loaded_components.clear()
                                    loaded_components = enabled_components
                                    print(RED + "Loading all components..." + RESET)

                                    for gotten in loaded_components:
                                        try:
                                            shutil.move(DATAPATH + "/components/unloaded/%s.py"%gotten, DATAPATH + "/components/%s.py"%gotten)
                                            print(DRIVES + "Component %s loaded"%gotten + RESET)
                                            time.sleep(0.1)
                                        except:
                                            print(RED + "Unable to unload component" + RESET)
                            else: print(RED + "Components have been disallowed from the configuration file" + RESET)

                        elif "--help" in flags or "-h" in flags:
                            print(YELLOW + "Format: components <option> <addon component>\nDo not supply any options to see a list of components and their status\n\n" + RED + "FLAGS:")
                            print(DRIVES + "'--unload <addon>' unloads the chosen module. to unload all modules, do not supply an addon name in <addon>\n--'--load <addon>' loads the chosen module, if it's unloaded and available. to load all modules, do not supply an addon name in <addon>\n'--install' opens a file picker to install new components\n'--purge <addon>' uninstalls the chosen addon" + RESET)

                        elif "--disable" in flags:
                            whatToDisable = command.split(maxsplit=2)[2]
                            if not whatToDisable in open(DATAPATH + "/development_components.txt").read():
                                try:
                                    shutil.move(DATAPATH + "/components/%s.py"%whatToDisable, DATAPATH + "/components/disabled/%s.py"%whatToDisable)
                                    enabled_components.remove(whatToDisable)
                                    loaded_components.remove(whatToDisable)
                                    print(DRIVES + "Component disabled" + RESET)
                                except:
                                    print(RED + "Unable to disable the component" + RESET)
                            else:
                                print(DEV_COMPONENT + "Developer components can't be disabled" + RESET)

                        elif "--enable" in flags:
                            if (ALLOW_COMPONENTS in config):
                                whatToEnable = command.split(maxsplit=2)[2]
                                if not whatToEnable in open(DATAPATH + "/development_components.txt").read():
                                    if not (whatToEnable in found_dangerous):
                                        try:
                                            shutil.move(DATAPATH + "/components/disabled/%s.py"%whatToEnable, DATAPATH + "/components/unloaded/%s.py"%whatToEnable)
                                            print(DRIVES + "Component enabled" + RESET)
                                            enabled_components.append(whatToEnable)
                                        except Exception as err:print(RED + "The component could not be enabled %s"%str(err) + RESET)
                                    else:
                                        print(RED + "WARNING: this component has been marked as dangerous by the development team. This usually means this component acts like malware or a virus. You should NOT enable this component." + RESET)
                                        contenable = input(BLUE + "Are you sure you want to continue? [Y/N] > " + RESET).capitalize()

                                        if contenable == "Y":
                                            try:
                                                shutil.move(DATAPATH + "/components/disabled/%s.py"%whatToEnable, DATAPATH + "/components/unloaded/%s.py"%whatToEnable)
                                                print(DRIVES + "Component enabled" + RESET)
                                                enabled_components.append(whatToEnable)
                                            except Exception as err:print(RED + "The component could not be enabled %s"%str(err) + RESET)
                                else: print(DEV_COMPONENT + "Developer components are always enabled" + RESET)
                            else:
                                print(RED + "Components have been disallowed from the configuration file" + RESET)

                        elif "--purge" in flags:
                            whatToPurge = command.split(maxsplit=2)[2]
                            if not (whatToPurge in loaded_components) and os.path.isfile(DRIVELETTER + ":/ProgramData/winLine/components/disabled/%s.py"%whatToPurge):
                                print(RED + "WARNING: Purging components will ERASE THEM FROM YOUR DEVICE. This CANNOT be undone.")
                                contin = input(YELLOW + "Are you sure you want to continue? [Y/N] > ").capitalize()

                                if contin == "Y":
                                    os.remove(DRIVELETTER + ":/ProgramData/winLine/components/disabled/%s.py"%whatToPurge)

                                    if os.path.isdir(DATAPATH + "/components/packs/%s"%whatToPurge):
                                        try:
                                            shutil.rmtree(DATAPATH + "/components/packs/%s"%whatToPurge)
                                        except:NotImplemented

                                    print(DRIVES + "The component was purged" + RESET)

                                    if (whatToPurge in enabled_components):
                                        enabled_components.remove(whatToPurge)

                                else:
                                    print(BLUE + "abort." + RESET)

                            elif not (os.path.isfile(DATAPATH + "/components/%s.py"%whatToPurge)):
                                print(RED + "Component not found" + RESET)

                            else:
                                print(RED + "The component is still loaded and cannot be purged. Please run " + BLUE + "components --disable %s"%whatToPurge + RESET)

                        elif "--install" in flags:
                                try:
                                    import tkinter.filedialog as getFile, tkinter

                                    root = tkinter.Tk()
                                    root.wm_geometry("1x1")
                                    root.grid_anchor("center")
                                    root.wm_title("")
                                    # root.iconify()

                                    fileToUpload = getFile.askopenfilename(title="Select Component / Package", filetypes=[("Component Files", ("*.py", "*.wcp")), ("Component Package", "*.wcp")])

                                    root.destroy()

                                    if (fileToUpload != "" and fileToUpload != None):select_valid = True
                                    else:select_valid = False
                                    if ".wcp" in fileToUpload:select_valid = "pack"

                                    if (select_valid == True):
                                        name = fileToUpload.split("/")[len(fileToUpload.split("/"))-1]
                                        print(YELLOW + "Installing selected component: %s"%str(name) + RESET)

                                        try:
                                            shutil.copy(fileToUpload, DATAPATH + "/components/%s"%(name))


                                            time.sleep(2)
                                            print(SPECIALDRIVE + "Component %s installed! Use the 'term -r' command to load it"%(name) + RESET)
                                        except Exception as err:
                                            print(RED + "Failed to install the component: " + YELLOW + str(err) + RESET)

                                    elif (select_valid == "pack"):
                                        packname = fileToUpload.split("/")[len(fileToUpload.split("/"))-1]
                                        stage_path = DATAPATH + "/components/staging/%s"%packname
                                        good_install = False 
                                        print(YELLOW + "Staging package: %s"%packname + RESET)

                                        try:
                                            os.mkdir(stage_path)
                                            with ZipFile(fileToUpload) as data:
                                                data.extractall(stage_path)
                                                data.close()
                                            keepInstalling = True
                                        except Exception as err:keepInstalling = False;print(RED + "Error while attempting to unpack the component package: %s"%str(err) + RESET)
                                        
                                        if keepInstalling:
                                            if os.path.isfile(stage_path + "/manifest.json"):keepInstalling = True
                                            else:keepInstalling = False;print(RED + "Package structure invalid: manifest.json not found" + RESET)

                                        if keepInstalling:
                                            rawmanifest_json = open(stage_path + "/manifest.json", "r")
                                            manifest_json = json.load(rawmanifest_json)
                                            package_name = manifest_json["package_name"]

                                            print(YELLOW + "Installing package: " + package_name + RESET)

                                            existing_files = 0
                                            if os.path.isdir(DATAPATH + "/components/%s"%package_name):
                                                for file in os.listdir(DATAPATH + "/components/%s"%package_name):
                                                    existing_files += 0

                                                if existing_files != 0:
                                                    print(RED + "Aboring installation: this folder already exists and it already includes data" + RESET)
                                                    keepInstalling = False

                                            if keepInstalling:
                                                try:
                                                    shutil.copytree(stage_path, DATAPATH + "/components/packs/%s"%package_name)
                                                    shutil.move(DATAPATH + "/components/packs/%s/%s.py"%(package_name,package_name),DATAPATH + "/components/")
                                                    good_install = True
                                                except Exception as err:
                                                    print(RED + "Failed to register package: " + str(err) + RESET)

                                            rawmanifest_json.close()
                                            shutil.rmtree(stage_path)

                                            if good_install:
                                                print(SPECIALDRIVE + "Package installed!" + RESET)



                                except ModuleNotFoundError:
                                    print(RED + "Tkinter is not currently installed. Tkinter is required for this command to work" + RESET)
                                    print(YELLOW + "You can still manually install components by copying your .py file to this directory:" + BLUE + DATAPATH + "/components" + YELLOW + ". Please make sure the files are python .py files, or they will not be detected by WinLine" + RESET)

                                except Exception as err:
                                    print(RED + "An error occurred: " + str(err) + RESET)

                        elif ("--debug" in flags):
                            pcomp = os.listdir(DATAPATH + "/components/disabled")
                            dcomp = os.listdir(DATAPATH + "/components")
                            disabled = []
                            present = []
                            dev = []
                            ignore_load_status = open(DATAPATH + "/development_components.txt").read()
                            for addon in pcomp:
                                if os.path.isfile(DATAPATH + "/components/disabled/%s"%addon) and ".py" in addon:
                                    disabled.append(addon.split(".")[0])
                            for addon in dcomp:
                                if os.path.isfile(DATAPATH + "/components/%s"%addon) and ".py" in addon:
                                    present.append(addon.split(".")[0])

                            for addon in present:
                                if (addon.split(".")[0] in ignore_load_status):
                                    dev.append(addon.split(".")[0])
                            
                            print(BLUE + "Component debug information")
                            print(YELLOW + "Developer components: " + DEV_COMPONENT + str(dev))
                            print(YELLOW + "Enabled components: " + SPECIALDRIVE + str(enabled_components))
                            print(YELLOW + "Loaded components: " + SPECIALDRIVE + str(loaded_components))
                            print(YELLOW + "Detected components: " + YELLOW + str(present))
                            print(YELLOW + "Disabled components: " + RED + str(disabled) + RESET)

                        else:
                            if not (NON_WIN):
                                print(YELLOW + "The following components are currently installed:" + RESET)
                                dev_components = []
                                disabled = []
                                for component in os.listdir(DRIVELETTER + ":/ProgramData/winLine/components/disabled/"):
                                    disabled.append(component.split(".", maxsplit=1)[0])
                                # print(loaded_components)
                                # print(disabled)
                                for component in os.listdir(DRIVELETTER + ":/ProgramData/winLine/components/"):
                                    # if ".py" in component:
                                        load_string = ""
                                        ignore_load_status = open(DATAPATH + "/development_components.txt").read()

                                        if not (component.split(".", 1)[0] in ignore_load_status) and os.path.isfile(DRIVELETTER + ":/ProgramData/winLine/components/%s"%component):
                                            if component.split(".", 1)[0] in found_dangerous:load_string="(DANGEROUS)";colorToUse=RED
                                            elif(component.split(".", 1)[0] in loaded_components and component.split(".", 1)[0] in enabled_components):load_string=SPECIALDRIVE+"(loaded)";colorToUse=BLUE
                                            elif(component.split(".", 1)[0] in disabled):load_string=RED + "(disabled)";colorToUse=DRIVES
                                            elif(component.split(".", 1)[0] in enabled_components):load_string="(unloaded)";colorToUse=DRIVES
                                            elif not (ALLOW_COMPONENTS in config):load_string=(RED + "(blacklisted)" + RESET);colorToUse=RED
                                            elif not (os.path.isfile(DRIVELETTER + ":/ProgramData/winLine/components/%s"%component)):load_string=RED+"(unsupported format)";colorToUse=DRIVES
                                            else:load_string=RED+"(restart WinLine to enable)";colorToUse=DRIVES

                                            print(colorToUse + component.split(".", 1)[0] + " " + load_string + RESET)
                                        elif os.path.isfile(DRIVELETTER + ":/ProgramData/winLine/components/%s"%component):
                                            load_string=DEV_COMPONENT+"(developer)";colorToUse=DEV_COMPONENT
                                            dev_components.append(colorToUse + component.split(".", 1)[0] + " " + load_string + RESET)

                                for component in os.listdir(DRIVELETTER + ":/ProgramData/winLine/components/unloaded"):
                                    if component in found_dangerous:load_string="(DANGEROUS)";colorToUse=RED
                                    elif(component.split(".", 1)[0] in disabled):load_string=RED + "(disabled)";colorToUse=DRIVES
                                    else:load_string="(unloaded)";colorToUse=DRIVES
                                    print(colorToUse + component.split(".", 1)[0] + " " + load_string + RESET)

                                if len(dev_components) != 0:
                                    print("")
                                    for dev_comp in dev_components:
                                        print(dev_comp)

                                print("")

                                for component in os.listdir(DRIVELETTER + ":/ProgramData/winLine/components/disabled"):
                                    if component in found_dangerous:
                                        load_string="(DANGEROUS)";colorToUse=RED
                                    elif(component.split(".", 1)[0] in disabled):load_string=RED + "(disabled)";colorToUse=DRIVES
                                    else:load_string="(unloaded)";colorToUse=DRIVES
                                    print(colorToUse + component.split(".", 1)[0] + " " + load_string + RESET)
                        
                        print("")

                    except Exception as err:
                        print(RED + "Error occured: " + str(err) + RESET)
                else:
                    print(YELLOW + "Disabled in safe mode\n" + RESET)

            
            elif (command == "config"):
                if not NON_WIN:
                    print(YELLOW + "Please select 'Notepad' or another text editor to open the file" + RESET)
                    os.startfile(DRIVELETTER + ":/ProgramData/winLine/config")
                else:
                    print(RED + "Configuration cannot be modified on non-Windows systems" + RESET)

            elif (command == "user") or (command == "name") or (command == "username"):
                try:
                    print(MAGENTA + open(DATAPATH+"/owner_name", "r").read() + YELLOW + " (%s)"%os.getlogin() + RESET + " on " + BLUE + socket.gethostname() + "\n")
                except:
                    print(RED + "Local user" + YELLOW + " (%s)"%os.getlogin() + RESET + " on " + BLUE + socket.gethostname() + "\n" + RESET)

            elif ("change-name" in command):
                if not (NON_WIN):
                    try:
                        newName = command.split(" ", maxsplit=1)[1]

                        file = open(DATAPATH+"/owner_name", "w")
                        file.write(newName)
                        file.close()

                        if (SHOW_NAME in config):
                            locprefix = MAGENTA + open(DATAPATH+"/owner_name", "r").read() + BLUE + "~ " + RESET
                            print(YELLOW + "Welcome back, " + open(DATAPATH+"/owner_name", "r").read() + "!" + RESET)
                        else:
                            print(SPECIALDRIVE + "Name changed" + RESET)

                    except IndexError:
                        print(RED + "New name not provided" + RESET)

                    except:
                        print(RED + "An error occured while setting your new user identity" + RESET)
                else:
                    print(RED + "This feature is only supported on Windows" + RESET)

                print("")
            
            elif command == "induce":os.induce()

            elif command.split(maxsplit=3)[0] == "mount_folder":
                try:
                    drive = command.split(maxsplit=3)[1]
                    sysd = command.split(maxsplit=3)[2]
                    folder = command.split(maxsplit=3)[3]
                    valid = True

                    command_string = "net use %s: \"\\\\localhost\\%s$\\%s\" /persistent:yes"%(drive,sysd,folder)
                    # print(command_string)

                except:
                    print(RED + "Invalid parameter values" + RESET)
                    print(YELLOW + "Example usage: mount_folder x c \\example\\myfolder" + RESET)
                    valid = False

                if valid:
                    subprocess.call(command_string)

            elif command.split(maxsplit=3)[0] == "unmount_folder" or command.split(maxsplit=3)[0] == "umount_folder":
                try:
                    drive = command.split(maxsplit=3)[1]

                    command_string = "net use %s: /D"%drive

                    subprocess.call(command_string)

                except:
                    print(RED + "Invalid parameter values" + RESET)
                    print(YELLOW + "Example usage: unmount_folder x" + RESET)


            elif command == "wldata":
                os.startfile(DATAPATH)

            elif command == "edition" or command == "key":
                try:
                    if sys.path[0] == "c:\\Users\\%s\\Downloads\\VisualStudioCode\\Python\\winLine"%open("C:/ProgramData/PsychonDevStudios/userKey.txt", "r").read() or sys.path[0] == "w:\\":
                        print(DEV_COMPONENT + KEY_DEVMODE + RESET)
                    else:
                        print(SPECIALDRIVE + KEY_DISTMODE + RESET)
                except:
                    print(SPECIALDRIVE + KEY_DISTMODE + RESET)

                if (USE_SAFE_MODE in config):
                    print(YELLOW + "WL Safe Mode" + RESET)
                print("")

            elif command == "path":
                print(YELLOW + "%s\n"%sys.path[0] + RESET)

            elif command == "reconfigure":
                print(RED + "Warning: Reconfiguring WinLine will reset all changes to the configuration!" + RESET)
                allow = input(BLUE + "Do you want to continue? [Y/N] > ").capitalize()

                if allow == "Y":
                    print(YELLOW + "Updating configuration...")
                    os.remove(DATAPATH + "/config")
                    doConfig()

            elif command == "uninstall":
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
                        print(RED + "WinLine has been fully uninstalled. Exiting..." + RESET)
                        os.abort()
                    except Exception as err:
                        print(RED + "WARNING: Uninstallation failed! Error: " + str(err) + RESET)

                elif option == "2":
                    print(YELLOW + "Removing core files..." + RESET)
                    os.remove(DATAPATH + "/terminal.py")
                    os.remove(DATAPATH + "/utilities.py")
                    shutil.rmtree(DATAPATH + "__pycache__", ignore_errors=True)

                else:
                    print(YELLOW + "Cancelled" + RESET)

            elif command == "recovery" or command == "restore":
                # print(YELLOW + "Entering recovery mode...")
                import tkinter.filedialog as getFile, tkinter
                root = tkinter.Tk()
                root.wm_geometry("1x1")
                root.grid_anchor("center")
                root.wm_title("")
                # root.iconify()

                fileToUpload = getFile.askopenfilename(title="Select Recovery Package", filetypes=[("Recovery Package", ("*.wlc"))])

                root.destroy()

                if (fileToUpload != "" and fileToUpload != None):select_valid = True
                else:select_valid = False

                if select_valid:
                    stage_path = DRIVELETTER + ":/ProgramData/wlstage"
                    print(YELLOW + "Staging..." + RESET)
                    if not os.path.isdir(stage_path):
                        os.mkdir(stage_path)
                    else:
                        shutil.rmtree(stage_path)
                        os.mkdir(stage_path)

                    with ZipFile(fileToUpload) as data:
                        print(YELLOW + "Extracting recovery contents..." + RESET)
                        data.extractall(stage_path)
                        data.close()
                    
                    try:
                        pv = open(stage_path + "/package_version", "r").read()

                        if (Appversion != pv):
                            print(YELLOW + "Caution: This backup was created on a different version of WinLine. Restoring from this backup might break some features." + RESET)
                            dob = input(BLUE + "Are you sure you want to continue? [Y/N] > ").capitalize()
                    except:NotImplemented


                    if dob == "Y":
                        print(YELLOW + "Restoring contents..." + RESET)
                        for file in os.listdir(stage_path):
                            print(DRIVES + "Checking " + file + RESET)

                            if os.path.isfile(stage_path + "/" + file):
                                print(DRIVES + "Name: " + file + BLUE + " Type: file" + RESET)
                                if os.path.isfile(DATAPATH + "/" + file):
                                    os.remove(DATAPATH + "/" + file)
                                print(YELLOW + "Copying " + file + RESET)
                                shutil.copy(stage_path + "/" + file, DATAPATH + "/" + file)

                            elif os.path.isdir(stage_path + "/" + file):
                                print(DRIVES + "Name: " + file + MAGENTA + " Type: directory" + RESET)
                                if os.path.isdir(DATAPATH + "/" + file):
                                    shutil.rmtree(DATAPATH + "/" + file)
                                
                                shutil.copytree(stage_path + "/" + file, DATAPATH + "/" + file)

                        shutil.rmtree(stage_path)

                        print(SPECIALDRIVE + "Recovery finished" + RESET)

            elif command == "backup":
                print(YELLOW + "Please wait, collecting files..." + RESET)
                backup = ZipFile(DATAPATH + '/winline_backup.wlc', 'w')

                try:
                    file = open(DATAPATH + "/package_version", "x")
                    file.write(Appversion)
                    file.close()
                except:
                    file = open(DATAPATH + "/package_version", "w")
                    file.write(Appversion)
                    file.close()

                try:backup.write(DATAPATH + "/owner_name", "owner_name")
                except:NotImplemented
                try:backup.write(DATAPATH + "/config", "config")
                except:NotImplemented
                try:backup.write(DATAPATH + "/development_components.txt", "development_components.txt")
                except:NotImplemented
                try:backup.write(DATAPATH + "/package_version", "/package_version")
                except:NotImplemented

                backup.close()

                try:os.rename(DATAPATH + "/backup.zip", DATAPATH + "/backup.wlc")
                except:NotImplemented # Fail silently

                print(YELLOW + "Backup created! Copying to desktop...")
                shutil.copy(DATAPATH + "/winline_backup.wlc", DRIVELETTER + ":/Users/%s/Desktop/winline_backup.wlc"%os.getlogin())

                os.remove(DATAPATH + '/winline_backup.wlc')
                print(SPECIALDRIVE + "Backup complete!" + RESET)

            elif command == "update":
                print(YELLOW + "Contacting server and checking for updates..." + RESET)
                keepTrying = True
                failed = 0
                okay = True
                while keepTrying == True:
                    try:
                        server_version = str(urlRequest.urlopen(REMOTE_SERVER  + "/latest_version").read(), "'UTF-8'")
                        # print(BLUE + "Current version: %s"%VERSION_ID + RESET)
                        # print(YELLOW + "Latest version: %s"%server_version + RESET)
                        keepTrying = False
                    except:
                        failed += 1
                        time.sleep(1)

                        if failed > 3:
                            keepTrying = False
                            okay = False

                if okay:
                    if (server_version != VERSION_ID):
                        print(YELLOW + "You are currently using WinLine " + MAGENTA + VERSION_ID + YELLOW + ", and version " + MAGENTA + server_version + YELLOW + " is available" + RESET)
                        cinst = input(BLUE + "Do you want to continue? [Y/N] > " + RESET).capitalize()

                        if cinst == "Y":
                            print(YELLOW + "\nDownloading update..." + RESET)
                            try:
                                os.mkdir(DRIVELETTER + ":/ProgramData/wlstage")
                            except:
                                shutil.rmtree(DRIVELETTER + ":/ProgramData/wlstage")
                                os.mkdir(DRIVELETTER + ":/ProgramData/wlstage")
                            everythingIsOkay = True
                            keepTrying = True
                            failed = 0

                            try:
                                with urlRequest.urlopen(REMOTE_SERVER  + "/winline.dat") as remote_archive:
                                    with ZipFile(BytesIO(remote_archive.read())) as update_package:
                                        update_package.extractall(DRIVELETTER + ":/ProgramData/wlstage")
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
                                    shutil.copy(DRIVELETTER + ":/ProgramData/wlstage/terminal.py", DRIVELETTER + ":/ProgramData/winLine/terminal.py")
                                    shutil.copy(DRIVELETTER + ":/ProgramData/wlstage/utilities.py", DRIVELETTER + ":/ProgramData/winLine/utilities.py")
                                    print(SPECIALDRIVE + "Update complete! Please restart WinLine to use the new version" + RESET)
                                except:
                                    print(RED + "Core files could not be updated" + RESET)

                                shutil.rmtree(DRIVELETTER + ":/ProgramData/wlstage", True)

                                # update_docs = input(BLUE + "Do you want to update the local documentation files? [Y/N] > ").capitalize()

                                # if update_docs == "Y":
                                #     print(YELLOW + "Downloading documentation..." + RESET)
                                #     keepTrying = True
                                #     failed = 0
                                #     good = True
                                #     try:
                                #         with urlRequest.urlopen(REMOTE_SERVER  + "/winline.dat") as remote_archive:
                                #             with ZipFile(BytesIO(remote_archive.read())) as update_package:
                                #                 update_package.extractall(DRIVELETTER + ":/ProgramData/wlstage")
                                #         keepTrying = False
                                #     except:
                                #         failed += 1
                                #         if failed > 5:
                                #             keepTrying = False
                                #             good = False

                                #     if good:
                                #         print(YELLOW + "Updating documentation..." + RESET)
                                #     else:
                                #         print(RED + "Failed to download documentation" + RESET)
                            else:
                                print(RED + "Update failed: " + reason + RESET)
                    
                else:
                    print(RED + "Unable to connect to server" + RESET)

                print("")
                shutil.rmtree(DRIVELETTER + ":/ProgramData/wlstage", True)

            else:
                if not (NON_WIN):
                    addin_commands = []
                    for add_on in os.listdir(DRIVELETTER + ":/ProgramData/WinLine/components/"):
                        if (".py" in add_on):
                            addin_commands.append(add_on.split(".", 1)[0])
                    
                    for add_on in os.listdir(DRIVELETTER + ":/ProgramData/WinLine/components/unloaded"):
                        if (".py" in add_on):
                            addin_commands.append(add_on.split(".", 1)[0])
                else:
                    addin_commands = []

                if (command in addin_commands):
                    ignore_load_status = open(DATAPATH + "/development_components.txt").read()
                    if (command in loaded_components) or (command in ignore_load_status):
                        runIndex = addin_commands.index(command)
                        runCommand = addin_commands[runIndex]
                        # print(DRIVELETTER + ":/ProgramData/winLine/components/%s.py"%runCommand)
                        subprocess.run("python3 " + DRIVELETTER + ":/ProgramData/winLine/components/%s.py"%runCommand)
                    else:
                        if ALLOW_COMPONENTS in config:
                            if not (command in enabled_components):print(RED + "That component hasn't been loaded yet. To load it, run the '" + BLUE + "term -r" + RED + "' command" + RESET)
                            else:print(RED + "That component was unloaded by the user or a script. To load it, run the '" + BLUE + "components --load %s"%command + RED + "' command" + RESET)
                            print(DRIVES + "Unloaded addon: " + command + RESET + "\n")
                        else:
                            print(RED + "Components have been disabled from the config file\n" + RESET)

                elif not (SYSRUN_FAILED_COMMANDS in config):
                    sys.stdout.write(u"\x1b[1A" + u"\x1b[2K" + "\r" + locprefix + location + "> " + "\u001b[1;41m" + command + RESET + "\n")
                    print(RED + "Unrecognized command\n" + RESET)
                else:
                    if not (USE_SAFE_MODE in config):
                        try:
                            # print(BLUE + "System: " + RESET)
                            subprocess.run(command)
                        except Exception as err:
                            print(RED + "Failed to run command: Not internal command and OS reported " + str(err) + RESET + "\n")
                    
                    else:
                        print(RED + "Failed to run command: Not internal command and safe mode is active" + RESET + "\n")
 

        except KeyboardInterrupt:
            if (ENABLEKEYBOARDINTURRUPT in config):
                sys.exit()
            else:
                print("")

        except IndexError:
                sys.stdout.write(u"\x1b[1A" + u"\x1b[2K" + "\r")

        except Exception as err:
            if ("has no attribute 'induce'" in str(err)):
                raise Exception("Crash intentionally caused by the user") 
            if (str(err) != ""):
                print(RED + "Unhandled error: " + str(err) + RESET)


if (ADVANCEDMODE in config) and not ISDEV:
    print(SPECIALDRIVE + "Advanced mode is enabled\n" + RESET)
elif ISDEV:
    print(DEV_COMPONENT + "Developer mode is enabled\n" + RESET)

if not (USE_SAFE_MODE in config):
    if ENABLE_AV_CHECK in config:
        if not THREADED_AV_CHECK in config:
            checkForDangerousComponents()
        else:
            td(target=checkForDangerousComponents, name="A/V check thread").start()
    else:
        print(DRIVES + "Warning: malware detection has been disabled from the config file. WinLine will not check for malicious components!" + RESET)

print("")

while True:
    try:
        main()
    except Exception as err:
        if not (RESET_ON_ERROR in config):
            print(YELLOW + "\n##-----------------------##"+RESET)
            print(YELLOW + "WinLine Exception Handler\n" + RESET)
            time.sleep(0.1)
            print(RED + "WinLine has experienced an error" + RESET)
            time.sleep(0.1)
            print(YELLOW + "Error message: " + str(err) + "\n" + RESET)
            print(YELLOW + "Resuming normal operation" + RESET)
            print(YELLOW + "##-----------------------##\n"+RESET)
        
        else:
            time.sleep(2)
            print(YELLOW + "\n##-----------------------##\n"+RESET)
            time.sleep(0.1)
            os.system("title WinLine Crash Handler")
            time.sleep(0.1)
            print(RED + "WinLine has experienced a fatal error" + RESET)
            time.sleep(0.1)
            print(YELLOW + "Error message: " + str(err) + "\n" + RESET)
            time.sleep(0.1)
            reboot = input(BLUE + "Do you want to restart WinLine? [Y/N] > ").capitalize()

            if reboot == ("Y"):
                os.system("cls")
                time.sleep(2)
                subprocess.call("python " + __file__)
                os.abort()
            else:
                print(YELLOW + "Exiting crash handler..." + RESET)
                time.sleep(2)
                os.abort()