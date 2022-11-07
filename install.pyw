import os, sys, subprocess, time
from threading import Thread as td
import tkinter as tk
from tkinter import messagebox
from zipfile import ZipFile

WINDRIVE = str(os.environ['WINDIR'].split(":\\")[0])
PATH = sys.path[0]
DoNotInstallWinLine = False
readme = """By clicking "install", you grant us permission to:
- Create and edit folders on your device
- Create, edit, and delete (WinLine's) files on your device
- Install additional required software (through Python's PIP)
- Create a shortcut on your desktop

If you do not wish to grant us these permissions, please close the installer."""
installable = []
installed = []
core_only = False

if os.path.isfile(PATH + "/winline.dat"):installable.append("WinLine")

BLUE = "\u001b[34;1m" # The color blue
YELLOW = "\u001b[33;1m" # The color yellow
RED = "\u001b[31;1m" # The color red
GREEN = "\u001b[32;1m"
NORMAL = "\u001b[0m" # Reset to default color

def on_enter(e):e.widget['background'] = 'lightgreen'
def on_leave(e):e.widget['background'] = 'SystemButtonFace'

def RENDER():
    for widgets in root.winfo_children():
        widgets.destroy()
    tk.Label(root, text=readme, wraplength=950, justify="center", background="lightgray").pack()
    tk.Label(root, text=" ", background="lightgray").pack(pady=3)
    inst_main = tk.Button(root, text="Install WinLine", command=installWinLine_strap, width="35")
    dn_inst_main = tk.Button(root, text="Can't Install: winline.dat not found", width="35", state="disabled")

    inst_main.bind("<Enter>", on_enter)
    inst_main.bind("<Leave>", on_leave)
    
    if ("WinLine" in installable):inst_main.pack()
    else:dn_inst_main.pack()

    if (len(installable) == 0 and len(installed) > 0):
        cleanup()

def cleanup():
    os.remove(__file__)
    messagebox.showinfo("WinLine", "Nothing left to install!")
    os.abort()

def nothing_available():
    messagebox.showinfo("WinLine", "Nothing installable found. Make sure the .dat files are in the same directory as this installer.")
    os.abort()

def installWinLine_strap():
    td(name="_installer", target=installWinLine).start()
    root.wm_title("Installing...")
    messagebox.showinfo("Installer", "Please wait while we install WinLine. Don't close the installer.")

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
    try:
        with ZipFile(sys.path[0] + "/winline.dat") as data:
            if not core_only:
                data.extractall(WINDRIVE + ":/ProgramData/winLine")
                data.close()
            else:
                data.extract("terminal.py", WINDRIVE + ":/ProgramData/winLine")
                data.extract("utilities.py", WINDRIVE + ":/ProgramData/winLine")

    except:
        print(RED + "\nError: winline.dat could not be opened. The file may be corrupted.")
        messagebox.showerror("winLine", "An error occured while opening winline.dat. The file may be corrupted.")
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
    root.wm_title("WinLine - Installer")
    RENDER()

# if ("Project" in sys.path[0] or "VisualStudioCode" in sys.path[0]):
#     print(RED + "abort" + NORMAL)
#     os.abort()

if not os.path.isfile(sys.path[0] + "/winline.dat"):
    DoNotInstallCXR = True
print("\n")

## Create screen ##
root = tk.Tk()
root.wm_geometry("600x200")
root.grid_anchor("center")
root.wm_title("WinLine - Installer")
root.wm_resizable(width=False, height=False)
root.config(background="lightgray")

if not ("nt" in os.name):
    messagebox.showinfo("WinLine Installer", "WinLine is only properly supported on Windows")
    root.wm_title("Exiting...")
    os.abort()

RENDER()

if (__name__ == "__main__"):
    # root.eval('tk::PlaceWindow . left')
    root.mainloop()