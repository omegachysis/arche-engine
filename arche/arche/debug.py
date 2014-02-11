
import traceback
import logging
from logging import *
import sys

formatLogging = "%(lineno)4d | %(asctime)s | %(levelname)8s | %(name)s |: %(message)s"
levelGameConsole = INFO
levelSystemConsole = INFO
levelLogFile = INFO

exec(open("config/debug.cfg").read())

alog = logging.getLogger("R")
alog.setLevel(DEBUG)

console = logging.StreamHandler()
console.setLevel(levelSystemConsole)
logfile = logging.FileHandler("error.log")
logfile.setLevel(levelLogFile)

formatter = logging.Formatter(formatLogging)

console.setFormatter(formatter)
logfile.setFormatter(formatter)

alog.addHandler(console)
alog.addHandler(logfile)

def log(name):
    name = name.replace(".", " ")
    name = name.title()
    name = name.replace(" ", ".")
    name = "R." + name

    return logging.getLogger(name)

def test(main):
    alog.info("starting tests")
    try:
        main()
    except:
        alog.critical(traceback.format_exc())
