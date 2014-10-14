
import traceback
import logging
log = logging.getLogger("R.Vars")

from . import config
from . import enum

BACKEND = enum.backend.PYGAME

configDefault = """
BACKEND = enum.backend.PYGAME
"""

try:
    exec(configDefault)
    config.configDefaults["variables.cfg"] = configDefault
    configuration = config.loadConfiguration("variables.cfg")
    exec(configuration.read())
except:
    log.error("Crash in vars.py: {}".format(traceback.format_exc()))