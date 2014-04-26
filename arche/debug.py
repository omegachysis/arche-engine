
import traceback
import logging
from logging import *
import sys
from os import path
import os

import time

from . import config

##formatLogging = "%(lineno)4d | %(asctime)s | %(levelname)8s | %(name)s |: %(message)s"
##levelGameConsole = INFO
##levelSystemConsole = INFO
##levelLogFile = DEBUG

if not os.path.exists("log"):
    os.makedirs("log")
if not os.path.exists("config"):
    os.makedirs("config")

exec(config.loadConfiguration("debug.cfg").read())

alog = logging.getLogger("R")
alog.setLevel(DEBUG)

console = logging.StreamHandler()
console.setLevel(levelSystemConsole)

if standardErrorLog:
    logfile = logging.FileHandler("error.log")
    logfile.setLevel(levelLogFile)

timestampName = "log/{}.log".format(time.strftime("%y %j %H %M %S %A %b %d"))
logfileTimestamp = logging.FileHandler(timestampName)
logfileTimestamp.setLevel(levelLogFile)

formatter = logging.Formatter(formatLogging)

console.setFormatter(formatter)
if standardErrorLog:
    logfile.setFormatter(formatter)

logfileTimestamp.setFormatter(formatter)

alog.addHandler(console)
if standardErrorLog:
    alog.addHandler(logfile)

alog.addHandler(logfileTimestamp)

def log(name):
    name = name.replace(".", " ")
    name = name.title()
    name = name.replace(" ", ".")
    name = "R." + name

    return logging.getLogger(name)

def test(main):
    alog.info("========================================================")
    criticalError = False
    try:
        main()
    except SystemExit as e:
        if e.code:
            criticalError = True
            alog.critical(traceback.format_exc())
        else:
            alog.info("quit with error code 0")
    except:
        criticalError = True
        alog.critical(traceback.format_exc())
    logfileTimestamp.close()
    if not criticalError:
        if purgeNonCriticalLogs:
            os.remove(timestampName)
