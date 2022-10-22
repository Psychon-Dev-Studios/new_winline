""" Functions used in WinLine that are messy af """
import sys

def colorCpuUsage(core:int, number:int, RED, DULLYELLOW, SPECIALDRIVE, RESET):
    """ Return a colored version of the inputted number """

    if (number > 85):
        return str(RED + str(core) + ": " + str(number) + "%" + RESET)

    elif (number > 50):
        return str(DULLYELLOW + str(core) + ": " + str(number) + "%" + RESET)

    else:
        return str(SPECIALDRIVE + str(core) + ": " + str(number) + "%" + RESET)

def colorCpuTime(category:str, percent:int, RED, DULLYELLOW, SPECIALDRIVE, RESET):
    if (percent > 85):
        return str(RED + str(category) + ": " + str(percent) + "%" + RESET)

    elif (percent > 50):
        return str(DULLYELLOW + str(category) + ": " + str(percent) + "%" + RESET)

    else:
        return str(SPECIALDRIVE + str(category) + ": " + str(percent) + "%" + RESET)

def colorCpuTimeInverse(category:str, percent:int, RED, DULLYELLOW, SPECIALDRIVE, RESET):
    if (percent > 85):
        return str(SPECIALDRIVE + str(category) + ": " + str(percent) + "%" + RESET)

    elif (percent > 50):
        return str(DULLYELLOW + str(category) + ": " + str(percent) + "%" + RESET)

    else:
        return str(RED + str(category) + ": " + str(percent) + "%" + RESET)

def colorRamUsage(number:int, total:int, RED, DULLYELLOW, SPECIALDRIVE, RESET):
    """ Return a colored version of the inputted number """
    if (number > 12): # 6.5
        return str(RED + str(round(number, 1)) + " GB / " + str(round(total,1)) + " GB" + RESET)
    elif (number > 8): # 5.0
        return str(DULLYELLOW + str(round(number, 1)) + " GB / " + str(round(total,1)) + " GB" + RESET)
    else:
        return str(SPECIALDRIVE + str(round(number, 1)) + " GB / " + str(round(total,1)) + " GB" + RESET)

def colorBatteryPercentage(number:int, battery, RED, DULLYELLOW, SPECIALDRIVE, BLUE, CRITICAL_BATTERY, RESET):

    if not (battery.power_plugged):
        if (number > 60):
            return str(SPECIALDRIVE + str(number) + "% | " + secs2hours(battery.secsleft) + " remaining" + RESET)
        elif (number > 40):
            return str("\u001b[38;5;190m" + str(number) + "% | " + secs2hours(battery.secsleft) + " remaining" + RESET)
        elif (number > 15):
            return str("\u001b[38;5;11m" + str(number) + "% | low | " + secs2hours(battery.secsleft) + " remaining" + RESET)
        elif (number > 8):
            return str(RED + str(number) + "% | very low | " + secs2hours(battery.secsleft) + " remaining" + RESET)
        else:
            return str(CRITICAL_BATTERY + str(number) + "% | critical | " + secs2hours(battery.secsleft) + " remaining" + RESET)
    else:
        return str(BLUE + str(number) + "%, charging" + RESET)

def colorNetStatus(online:bool, RED, DULLYELLOW, SPECIALDRIVE, RESET):
    if (online):
        return str(SPECIALDRIVE + "functional" + RESET)
    else:
        return str(RED + "down" + RESET)

def colorBool(input:bool, RED, SPECIALDRIVE, RESET):
    if (input):
        return str(SPECIALDRIVE + "online" + RESET)
    else:
        return (str(RED + "offline" + RESET))

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

def network_connected():
    """ Check if there's any kind of network connection. Reqires requests """
    import requests

    try:
        requests.get("google.com")
        return True
    except:
        return False