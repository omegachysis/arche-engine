
import pygame
import logging
import traceback
import sys

from os import path

from . import config
from . import compat

from pygame.locals import *

log = logging.getLogger("R.Console")

##class DialogEntry(object):
##    def __init__(self, game, prompt):
##        log.info("intializing DialogEntry for prompt '{}'".format(prompt))
##        self._dialogSurface = pygame.Surface(
##            (int(game.width / 2), int(game.height / 2)))
##        self._dialogSurface.fill((255,255,255))
##        self._dialogSurface = self._dialogSurface.convert()
##        self._dialogRect = self._dialogSurface.get_rect()
##        self._dialogRect.centerx = game.width / 2
##        self._dialogRect.centery = game.height / 2
##
##        self.font = compat.freetypeFont("font/consola.ttf", 12)
##
##        self._promptSurface, self._promptRect = \
##                             self.font.render(prompt, (0,0,0,255))
##        self._promptRect.centerx = game.width // 2
##        self._promptRect.centery = game.width // 3
##
##        self.entry = ""
##        self.game = game
##
##        self.value = None
##
##        self._renderEntry()
##
##    def get(self):
##        while self.value == None:
##            for event in pygame.event.get():
##                if event.type == QUIT:
##                    game.quit()
##                elif event.type == KEYDOWN:
##                    if event.key == K_ESCAPE:
##                        self.postEvent(QUIT)
##                    elif event.key == K_RETURN:
##                        self.value = str(self.entry)
##                    elif event.key == K_BACKSPACE:
##                        self.entryBackspace()
##                    else:
##                        self.entryAdd(event.unicode)
##
##            self.draw(self.game.canvas)
##
##            pygame.display.update()
##
##        log.debug("Return VALUE: {}".format(repr(self.value)))
##        return str(self.value)
##    
##    def draw(self, canvas):
##        canvas.blit(self._dialogSurface, self._dialogRect)
##        canvas.blit(self._promptSurface, self._promptRect)
##        canvas.blit(self._entrySurface, self._entryRect)
##        
##    def _renderEntry(self):
##        surface, rect = self.font.render(self.entry, (0,0,0,255))
##        rect.centerx = self.game.width/2
##        rect.centery = self.game.height/2
##
##        self._entrySurface = surface
##        self._entryRect = rect
##
##    def entryAdd(self, unicode):
##        self.entry += unicode
##        self._renderEntry()
##    def entryBackspace(self):
##        self.entry = self.entry[:-1]
##        self._renderEntry()

class ConsoleSTDOUT(object):
    """
    Used to recieve output from python calls to print() and similar functions.  It then transfers
    these calls to the GameConsole.
    """
    def __init__(self, gameConsole):
        self.val = None
        self.gameConsole = gameConsole
    def write(self, data):
        stream = "INFO ; STDOUT ; " + data + "\n"
        log.debug("!@ STDOUT received " + data + " ]]")
        if data != "\n":
            self.gameConsole.write(stream)
            self.gameConsole.flush()

def splitLine(string, overflow=70):
    """
    Split a line with new lines where the line buffer width is 'overflow'
    """
    w=[]
    n=len(string)
    for i in range(0,n,overflow):
        w.append(string[i:i+overflow])
    return w

class Shell(object): pass

class GameConsole(object):
    MESSAGE_HEIGHT = 15 # spacing in pixels to give each message, including the message itself
    CONSOLE_PADDING = 50 # space in pixels from the bottom of the screen where messages start
    ENTRY_PADDING = 15 # space in pixels from the bottom of the screen where the entry box starts
    PADDING_LEFT = 15 # padding in pixels from the left of the screen to text.
    LINE_LENGTH_MONITOR = 15 # pixels between each monitor in vertical position
    DARKEN_WIDTH = .80 # percent of screen width to darken from console background
    TEXT_OVERFLOW = 80 # characters at 1280 px width
    LOGSOURCE_SPACING = 25 # characters to space after logging source values
    MESSAGE_BUFFER_LENGTH = 100 # messages to render before deleting

    BACKSPACE_HOLDING_DELAY = 500.0e-3
    BACKSPACE_HOLDING_ERASE_DELAY = 40.0e-3
    
    def __init__(self, game, level=logging.INFO):
        sys.stdout = ConsoleSTDOUT(self)
        
        rootLogger = logging.getLogger("R")

        self.shell = Shell()

        self.sprite = None

        self.fps = 0
        
        self._monitorUpdateWait = 0
        self.trackerUpdateDelay = 100.0e-3

        self.monitors = [("fps", "self.fps"),
                         ("sprite", "self.sprite"),
                         ("game.autoPause", "self.game.autoPause")]
        self._monitorBlits = []

        self._backspaceHolding = False
        self._backspaceHoldingWait = self.BACKSPACE_HOLDING_DELAY
        self._backspaceHoldingEraseWait = 0
        self._backspaceHoldingErasing = False

        self.scrollOffset = 1

        GameConsole.TEXT_OVERFLOW = int(
            GameConsole.TEXT_OVERFLOW * float(game.width) / 1280.0)
        
        self.messages = []
        self.game = game
        self.hidden = True
        self.env = self
        self.stream = ""
        self.entry = ""

        self._everyOtherLine = -1

        self._entrySurface = None
        self._entryRect = None

        self._consoleSurface = pygame.Surface(
            (GameConsole.DARKEN_WIDTH*game.width, game.height)
            )
        self._consoleSurface.fill((0,0,0))
        self._consoleSurface.set_alpha(200)
        self._consoleSurface = self._consoleSurface.convert_alpha()

        self.font = compat.freetypeFont("font/consola.ttf", 12)

        self._renderEntry()

        handler = logging.StreamHandler(self)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "%(levelname)s ; %(name)s ; %(message)s")
        handler.setFormatter(formatter)
        rootLogger.addHandler(handler)

        self.resetConfiguration()

        for blacklistedSource in GameConsole.blacklistedSources:
            self.blacklistSource(blacklistedSource)

    def addTracker(self, name, source=None):
        if source:
            self.monitors.append((name, source))
        else:
            if name[0] == "@":
                self.monitors.append((name, "self.sprite." + name[1:]))
            else:
                self.monitors.append((name, name))
    def removeTracker(self, name):
        for monitorBit in self.monitors:
            if name.lower() == monitorBit[0].lower():
                self.monitors.remove(monitorBit)
    def resetTrackers(self):
        self.monitors = [("fps", "self.fps")]

    def sprite(self, spriteName):
        """ Return sprite from application registry """
        return self.game.app.reg(spriteName)
        
    def resetConfiguration(self):
        """ Load default console configuration. """
        exec(config.loadConfiguration("console.cfg").read())

    def blacklistSource(self, source):
        """ Prevent a logging source from logging to the console. """
        log.info("blacklisting " + source)
        if source not in GameConsole.blacklistedSources:
            GameConsole.blacklistedSources.append(source)

    def isSourceBlacklisted(self, source):
        """ Return whether a given logsource is not allowed to log to the console. """
        components = source.split(".")
        i = 0
        for component in components:
            i += 1
            testing = components[:i]
            if ".".join(testing) in GameConsole.blacklistedSources:
                return True
        return False
    def isEnvironment(self, environment):
        # Deprecated!
        """ Return whether 'environment' is a suitable environ for the console. """
        return hasattr(environment, 'execute')
    isEnv = isEnvironment

    def getEnvironment(self):
        return self._environment
    def setEnvironment(self, environment):
        if self.isEnv(environment):
            self._environment = environment
        else:
            log.error("(execute) " + str(environment) + " is not an environment.")
    env = property(getEnvironment, setEnvironment)
    environment = property(getEnvironment, setEnvironment)
    def resetEnvironment(self):
        self.env = self
    def resetEnv(self): #shorthand
        self.env = self

    def runScript(self, script):
        """
        Run script from script directory.
        See console command guide for shortcut ($)
        """
        c = self
        game = self.game
        app = self.game.app
        shell = self.shell
        sprite = self.sprite
        s = shell
        self = self.env
        exec(open("script/" + script).read())

    def execute(self, c, command):
        """ Execute a console command with 'c' as the GameConsole instance. """
        c = self # we only use 'c' in the execute function for compatibility with other environments!
        game = self.game
        app = self.game.app
        shell = self.shell
        sprite = self.sprite
        s = shell
        self = self.env
        
        log.info("(execute) " + command)
        try:
            if command[0] == "$":
                self.runScript(command[1:] + ".py")
            else:
                if command[0] == "#":
                    self = c
                    if command[-1] == "?":
                        exec("print(" + command[1:-1] + ")")
                    else:
                        exec(command[1:])
                elif command[0] == ".":
                    if command[-1] == "?":
                        exec("print(c.shell." + command[1:-1] + ")")
                    else:
                        exec("c.shell." + command[1:])
                else:
                    if command[-1] == "?":
                        exec("print(" + command[:-1] + ")")
                    else:
                        exec(command)
        except:
            log.error("(execute) " + traceback.format_exc())

    def executeEntry(self):
        self.execute(self, self.entry)
        self.entry = ""
        self._renderEntry()

    def hide(self):
        self.hidden = True
    def unhide(self):
        self.hidden = False
    def toggleHidden(self):
        self.hidden = not self.hidden

    def _renderEntry(self):
        surface, rect = self.font.render(self.entry, (255,255,255,255))
        rect.left = GameConsole.PADDING_LEFT
        rect.bottom = self.game.height - GameConsole.ENTRY_PADDING

        self._entrySurface = surface
        self._entryRect = rect

    def _renderMonitors(self):
        self._monitorBlits = []
        i = -1
        for monitor in self.monitors:
            i += 1
            surface, rect = self._renderMonitor(monitor[0], monitor[1])
            rect.left = self.PADDING_LEFT
            rect.top = self.PADDING_LEFT + self.LINE_LENGTH_MONITOR * i
            self._monitorBlits.append((surface, rect))

    def _renderMonitor(self, name, source):
        c = self
        game = self.game
        app = self.game.app
        shell = self.shell
        sprite = self.sprite
        s = shell
        self = self.env
        try:
            if name[0] != "@":
                surface, rect = self.font.render(name + " = " + repr(eval(source)), (255,255,255,255))
            else:
                if self.sprite.app.active:
                    surface, rect = self.font.render(name + " = " + repr(eval(source)), (150,255,150,255))
                else:
                    surface, rect = self.font.render(name + " = " + repr(eval(source)), (80,120,80,255))
        except:
            surface, rect = self.font.render(name + " = INVALID", (255,255,100,255))
        return surface, rect

    def renderMessage(self, stream):
        #log.debug("!@ rendering message stream: " + stream)
        if self.game.quitting == False:
            try:
                levelname, source, message = stream.split(" ; ")
                if not self.isSourceBlacklisted(source):
                    color = {"DEBUG":(200,200,200,255),"INFO":(150,150,255,255),
                             "WARNING":(255,255,50,255),"ERROR":(255,50,50,255),
                             "CRITICAL":(255,20,255,255)}[levelname]

##                  if self._everyOtherLine < 0:
##                      #log.debug("!@ EVERY OTHER LINE")
##                      color = lightenColor(color, 80)
##                  self._everyOtherLine = -self._everyOtherLine

                    multiline = message.split("\n")
                    newMultiline = []
                    for line in multiline:
                        if len(line) >= self.TEXT_OVERFLOW:
                            newMultiline += splitLine(line, self.TEXT_OVERFLOW)
                        else:
                            newMultiline += [line]
                    multiline = newMultiline
                            
                    multiline[0] = source + " " * (self.LOGSOURCE_SPACING - len(source)) + multiline[0]
                    i = 0
                    for line in multiline[1:]:
                        i += 1
                        multiline[i] = " "*self.LOGSOURCE_SPACING + multiline[i]

                    for msg in multiline:
                        surface, rect = self.font.render(msg, color)
                        self.messages.append([surface,rect])
                        if len(self.messages) > self.MESSAGE_BUFFER_LENGTH:
                            self.messages = self.messages[1:]

                    self._recalculateCoordinates()
            except:
                if False:
                    log.error("!@ error rendering last stream" +\
                          traceback.format_exc())
                else:
                    pass

    def _recalculateCoordinates(self):
        i = len(self.messages)
        for message in self.messages:
            i -= 1
            message[1].top = self.game.height - \
                                GameConsole.MESSAGE_HEIGHT * (i + self.scrollOffset) - \
                                GameConsole.CONSOLE_PADDING
            message[1].left = GameConsole.PADDING_LEFT

    def draw(self, canvas):
        canvas.blit(self._consoleSurface, (0,0))
        canvas.blit(self._entrySurface, self._entryRect)
        for message in self.messages:
            if message[1].top > GameConsole.CONSOLE_PADDING + self.LINE_LENGTH_MONITOR*len(self.monitors) and\
               message[1].bottom < self.game.height - GameConsole.CONSOLE_PADDING:
                canvas.blit(message[0], message[1])
                
        for monitorBlit in self._monitorBlits:
            canvas.blit(monitorBlit[0], monitorBlit[1])

    def entryAdd(self, unicode):
        self.entry += unicode
        self._renderEntry()
    def entryBackspace(self, keyed=True):
        if keyed: self._backspaceHolding = True
        self.entry = self.entry[:-1]
        self._renderEntry()
    def scrollUp(self, messages=1):
        """ Move one message upwards through the Console buffer. """
        self.scrollOffset -= messages
        self._recalculateCoordinates()
    def scrollDown(self, messages=1):
        """ Move one message downwards through the Console buffer. """
        if self.scrollOffset < 1:
            self.scrollOffset += messages
            self._recalculateCoordinates()

    def backspaceHoldingReset(self):
        self._backspaceHolding = False
        self._backspaceHoldingWait = self.BACKSPACE_HOLDING_DELAY
        self._backspaceHoldingErasing = False
        self._backspaceHoldingEraseWait = self.BACKSPACE_HOLDING_ERASE_DELAY
        
    def update(self, dt):
        self._monitorUpdateWait -= dt
        if self._monitorUpdateWait <= 0.0:
            self.fps = int(self.game.clock.get_fps())
            self._renderMonitors()
            self._monitorUpdateWait = self.trackerUpdateDelay
            
        if self._backspaceHolding:
            if not self._backspaceHoldingErasing:
                self._backspaceHoldingWait -= dt
                if self._backspaceHoldingWait <= 0.0:
                    self._backspaceHoldingWait = self.BACKSPACE_HOLDING_DELAY
                    self._backspaceHoldingErasing = True
            else:
                self._backspaceHoldingEraseWait -= dt
                if self._backspaceHoldingEraseWait <= 0.0:
                    self.entryBackspace(keyed = False)
                    self._backspaceHoldingEraseWait = self.BACKSPACE_HOLDING_ERASE_DELAY

    def pickSprite(self):
        mousex, mousey = pygame.mouse.get_pos()
        for sprite in self.game.app.sprites:
            if sprite.left < mousex < sprite.right and \
               sprite.top  < mousey < sprite.bottom and \
               sprite.pickable:
                self.sprite = sprite
                log.info("-> {}".format(repr(sprite)))

    def write(self, data):
        try:
            self.stream += str(data)
        except:
            log.critical("!@ " + traceback.format_exc())

    def flush(self):
        try:
            # ANYTHING you don't want to render to the
            # game console, precede with these symbols:
            # "!@ " (not including quotes)
            if "!@ " not in self.stream:
                self.renderMessage(self.stream[:-1])
            self.stream = ""
        except:
            log.critical("!@ " + traceback.format_exc())
