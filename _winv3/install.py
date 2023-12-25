import os, sys, subprocess, time
from threading import Thread as td
from zipfile import ZipFile

os.system("cls")

WINDRIVE = str(os.environ['WINDIR'].split(":\\")[0])
PATH = sys.path[0]
DoNotInstallWinLine = False
installable = []
installed = []
core_only = False

if os.path.isfile(PATH + "/winline.dat"):installable.append("WinLine")

BLUE = "\u001b[34;1m" # The color blue
YELLOW = "\u001b[33;1m" # The color yellow
RED = "\u001b[31;1m" # The color red
GREEN = "\u001b[32;1m"
RESET = "\u001b[0m" # Reset to default color

def installWinLine():
    global installable

    try:
        from win32com.client import Dispatch
        dispatch_needed = False
    except: dispatch_needed = True

    if (dispatch_needed):
        print(YELLOW + "Step 1\nInstalling Dispatch")
        subprocess.call("pip install pywin32")
        os.startfile(__file__)
        os.abort()

    else:print(YELLOW + "Skipping step 1: requirement already met!")
    time.sleep(0.7)

    print(YELLOW + "Step 2\nCreating directories")
    time.sleep(0.3)
    try:os.mkdir(WINDRIVE + ":/ProgramData/winLine")
    except:print(RED + "Warning: directory already exists. Only unpacking core files\n");core_only = True
    try:os.mkdir(WINDRIVE + ":/ProgramData/winLine/man")
    except:NotImplemented
    try:os.mkdir(WINDRIVE + ":/ProgramData/winLine/components")
    except:NotImplemented

    os.system("cls")

    print(YELLOW + "Step 3\nUnpacking winLine")
    unpackErrors = 0
    unpackaged = False
    while unpackaged == False:
        try:
            with ZipFile(sys.path[0] + "/winline.dat") as data:
                if not core_only:
                    data.extractall(WINDRIVE + ":/ProgramData/winLine")
                    try:data.extract("terminal.ico", WINDRIVE + ":/ProgramData/winLine")
                    except:NotImplemented
                    data.close()
                else:
                    data.extract("terminal.py", WINDRIVE + ":/ProgramData/winLine")
                    data.extract("utilities.py", WINDRIVE + ":/ProgramData/winLine")
                    data.extract("terminal.ico", WINDRIVE + ":/ProgramData/winLine")

                unpackaged = True

        except:
            unpackErrors += 1
            time.sleep(0.5)

            if unpackErrors >= 10:
                print(RED + "\nError: winline.dat could not be opened. The file may be corrupted.")
                time.sleep(999)
                os.abort()

    try:
        with ZipFile(sys.path[0] + "/winline_docs.dat") as data:
            data.extractall(WINDRIVE + ":/ProgramData/winLine/man")
            data.close()
    except Exception as err:NotImplemented
    if not os.path.isdir(WINDRIVE + ":/ProgramData/winLine/components"):
        try:
            with ZipFile(sys.path[0] + "/winline_components.dat") as data:
                data.extractall(WINDRIVE + ":/ProgramData/winLine/components")
                data.close()
        except Exception as err:NotImplemented
    try:
        with ZipFile(sys.path[0] + "/winline_services.dat") as data:
            data.extractall(WINDRIVE + ":/ProgramData/winLine/services")
            data.close()
    except Exception as err:NotImplemented
        
    time.sleep(1.5)

    # time.sleep(1.5)
    os.system("cls")

    time.sleep(0.7)
    os.system("cls")
    print(YELLOW + "Step 5\nCreating desktop shortcut(s)...")

    target = WINDRIVE + ":/ProgramData/winLine/terminal.py"
    wDir = WINDRIVE + ":/ProgramData/winLine/"
    icon = "%s:/ProgramData/winLine/terminal.ico"%WINDRIVE
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(WINDRIVE + ":/Users/" + os.getlogin() + "/Desktop/WinLine.lnk")
    shortcut.Targetpath = target
    shortcut.WorkingDirectory = wDir
    shortcut.description = "A better terminal for Windows"
    shortcut.IconLocation = icon
    shortcut.save()

    installable.remove("WinLine")
    installed.append("WinLine")
    os.remove(PATH + "/winline.dat")
    try:os.remove(PATH + "/winline_docs.dat")
    except:NotImplemented
    try:os.remove(PATH + "/winline_components.dat")
    except:NotImplemented
    try:os.remove(PATH + "/winline_services.dat")
    except:NotImplemented

if not os.path.isfile(sys.path[0] + "/winline.dat"):
    DoNotInstallCXR = True

os.system("title WinLine - Installer")
print(YELLOW + "WinLine Installer\n" + RESET)

print(YELLOW + "By continuing with the installation, you will be granting WinLine the following permissions:\n- Create, modify, and delete WinLine files\n- Read and write to files you open with the application\n- Create, modify, and delete WinLine directories\n- Modify and delete directories you open with the application\n- Create and manage shortcuts on your desktop\n- Access the internet\n- Access system information such as: OS, system version, username, CPU utilization, and battery percentage\n- Interact with other applications on your system (for example, to launch or close them)\n- Install third-party packages to enable additional functionality (win32com, psutil)" + RESET)

allow = input(BLUE + "Would you like to continue? [Y/N] > " + RESET).capitalize()

if allow == "Y":
    installWinLine()

else:
    print(RED + "Exiting installer..." + RESET)
    os.abort()