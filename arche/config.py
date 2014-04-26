
from os import path

import logging

log = logging.getLogger("R.Config")

configDefaultConsole = """
GameConsole.blacklistedSources = [

#Add any locations that the game console should NOT recieve messages from.

#"R.Interface",

]

"""

configDefaultDebug = """
# OPTIONS ARE:
#  DEBUG
#  INFO
#  WARNING
#  ERROR
#  CRITCAL

levelGameConsole =	 INFO
levelSystemConsole =	 INFO
levelLogFile =		 DEBUG

formatLogging = "%(levelname)8s | %(lineno)4d | %(name)-15s |: %(message)s"

# Delete logs in the '/log' folder that are not critical error logs
purgeNonCriticalLogs = True

# Use the top level 'error.log' file.  Note that this log will not automatically recycle.
standardErrorLog = True
"""

configDefaultEngine = """
# Limit framerate to this number of frames per second.  Zero for no limit.  Lower numbers save energy.
self.limitFramerate = 0

# Store all ImageSurface objects in memory for profiling and debugging.
#  (uncomment to enable)
#surf.profilerRecordImageSurfaces()

"""

configDefaults = {

    "console.cfg" : configDefaultConsole,
    "debug.cfg"   : configDefaultDebug,
    "engine.cfg"  : configDefaultEngine,

    }

def createConfigurationDefault(filename):
    log.info("Creating configuration default: {}".format(filename))
    try:
        file = open("config/{}".format(filename), "w")
    except:
        log.error("Failed to create configuration default!")
    else:
        if filename in configDefaults:
            file.write(configDefaults[filename])
        file.close()

def loadConfiguration(filename):
    file = None
    log.info("Loading configuration {}".format(filename))
    if path.exists("config/{}".format(filename)):
        file = open("config/{}".format(filename))
    else:
        createConfigurationDefault(filename)
        if path.exists("config/{}".format(filename)):
            file = open("config/{}".format(filename))
    if file == None:
        if not path.exists("config_null"):
            file = open("config_null", "w")
            file.write("\n")
            file.close()
        file = open("config_null", "r")
    log.debug("Asked to load configuration, returning {}".format(repr(file)))
    return file
