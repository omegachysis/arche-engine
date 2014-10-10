
__all__ = [
    "console", "debug", "engine", "interface",
    "sprite", "motion", "image", "control",
    "draw", "update", "collision",
    ]

from pygame import locals

from . import compat
from . import config
from . import console
from . import debug
from . import engine
from . import event
from . import interface
from . import sprite
from . import image
from . import control
from . import draw
from . import update
from . import collision

from . import motion

from .sprite import Sprite
from .engine import Game
from .engine import Application
from .sprite import Text
from .collision import Batch

from .update import getVersion
version = getVersion()