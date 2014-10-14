
__all__ = [
    "console", "debug", "engine", "interface",
    "sprite", "motion", "image", "control",
    "draw", "update", "collision",
    ]

try:
    from pygame import locals
except:
    pass

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
from . import enum
from . import vars

from . import motion

from .sprite import Sprite
from .engine import initGame as Game
from .engine import Game as game
from .engine import Application
from .sprite import Text
from .collision import Batch
from .engine import Task

try:
    from .update import getVersion
    version = getVersion()
except:
    pass
