
import traceback
import logging
from logging import *
import sys
from os import path

import time

from . import config

##formatLogging = "%(lineno)4d | %(asctime)s | %(levelname)8s | %(name)s |: %(message)s"
##levelGameConsole = INFO
##levelSystemConsole = INFO
##levelLogFile = DEBUG

exec(config.loadConfiguration("debug.cfg").read())

alog = logging.getLogger("R")
alog.setLevel(DEBUG)

console = logging.StreamHandler()
console.setLevel(levelSystemConsole)
##logfile = logging.FileHandler(logFile)
##logfile.setLevel(levelLogFile)

logfileTimestamp = logging.FileHandler("log/{}.log".format(time.strftime("%y %j %H %M %S %A %b %d")))
logfileTimestamp.setLevel(levelLogFile)

formatter = logging.Formatter(formatLogging)

console.setFormatter(formatter)
##logfile.setFormatter(formatter)

logfileTimestamp.setFormatter(formatter)

alog.addHandler(console)
##alog.addHandler(logfile)

alog.addHandler(logfileTimestamp)

def log(name):
    name = name.replace(".", " ")
    name = name.title()
    name = name.replace(" ", ".")
    name = "R." + name

    return logging.getLogger(name)

def test(main):
    alog.info("starting tests")
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
