
import logging
import traceback
log = logging.getLogger("R.Engine")

_panda = None
try:
    import pygame
    from pygame import locals
    from pygame import transform
    _panda = False
except:
#    #log.warning("*** could not load pygame modules... -> {}".format(traceback.format_exc()))
#    from direct.task.Task import Task as PandaTask
#    from direct.showbase.DirectObject import DirectObject
#    _panda = True
    pass

import sys


import multiprocessing

from os import path

from .motion import action

from . import debug
from . import console
from . import sprite
from . import config
from . import image
from . import event
from . import vars
from . import enum

#if (_panda and vars.BACKEND != enum.backend.PANDA) or \
#    (not _panda and vars.BACKEND == enum.backend.PANDA):
#    log.error(" ---> ************ Major errors loading BACKEND! ************")

#def initGame(width, height, fullscreen=False, titleName="My Game", frame=True,
#         windowIcon="image/arche-engine.bmp", windowIconColorKey=False):
#    if vars.BACKEND == enum.backend.PYGAME:
#        log.info("********* Pygame BACKEND loaded *********")
#        return GamePygame(width, height, fullscreen, titleName, frame, windowIcon, windowIconColorKey)
#    elif vars.BACKEND == enum.backend.PANDA:
#        log.info("********* Panda3D BACKEND loaded *********")
#        return GamePanda(width, height, fullscreen, titleName, frame, windowIcon, windowIconColorKey)
#    else:
#        log.error("vars.BACKEND is specified incorrectly.")
#        return None

#class Game(object): app = None

#if _panda:
#    class _GamePandaObject(DirectObject):
#        def __init__(self, gamePanda):
#            base.disableMouse()
#            self.mainloopTask = taskMgr.add(gamePanda._gameLoop, "mainloop")

#def isUsingPanda():
#    return _panda

#def getGameClass():
#    if _panda:
#        return GamePanda
#    else:
#        return GamePygame

#class GamePanda(object):
#    def __init__(self, width, height, fullscreen=False, titleName="My Game", frame=True,
#                 windowIcon="image/arche-engine.bmp", windowIconColorKey=False):
#        log.info("initializing game engine")

#        import direct.directbase.DirectStart

#        self._pandaGameObject = _GamePandaObject(self)

#        ApplicationPanda.game = self
#        sprite.SpritePanda.game = self

#    def run(self):
#        log.info("starting main loop")
#        run()

#    def quit(self):
#        log.info("calling game.quit() command")
#        sys.exit(0)

#    def _gameLoop(self, task):
#        dt = globalClock.getDt()
#        #fps = globalClock.getFrameTime()
#        return PandaTask.cont

#    def getApp(self):
#        return Game.app
#    def setApp(self, value):
#        Game.app = value
#    app = property(getApp, setApp)

#class ApplicationPanda(object):
#    def __init__(self):
#        log.info("__init__() new ApplicationPanda object")
#        self.backgroundColor = (0,0,0)
#        self.sprites = []

#    def _initialize(self):
#        log.debug("_initialize() ApplicationPanda object")
#        self.setBackgroundColor(self.backgroundColor)

#    def start(self):
#        log.info("Starting ApplicationPanda object")
#        self._initialize()
#        Game.app = self

#    def addSprite(self, sprite):
#        self.sprites.append(sprite)
#        sprite.add()

#    def getBackgroundColor(self):
#        return self._backgroundColor
#    def setBackgroundColor(self, value):
#        self._backgroundColor = value
#        base.setBackgroundColor([i/255.0 for i in value])
#    backgroundColor = property(getBackgroundColor, setBackgroundColor)

class Game(object):
    def __init__(self, width, height, fullscreen=False, titleName="My Game", frame=True,
                 windowIcon="image/arche-engine.bmp", windowIconColorKey=False):
        log.info("initializing game engine")

        try:
            if windowIcon:
                if not windowIconColorKey:
                    pygame.display.set_icon(pygame.image.load(windowIcon))
                else:
                    image = pygame.image.load(windowIcon)
                    image.set_colorkey(image.get_at((0,0)))
                    pygame.display.set_icon(image)
        except:
            log.warning(traceback.format_exc())

        self.limitFramerate = 0

        exec(config.loadConfiguration("engine.cfg").read())
        log.debug("Game.limitFramerate = %d"%(self.limitFramerate))

        self.width = width
        self.height = height

        self.quitting = False

        self._autoPause = False

        self.paused = False
        
        pygame.init()
        
        if fullscreen:
            self.canvas = pygame.display.set_mode((width, height), locals.FULLSCREEN|locals.HWSURFACE)
        else:
            if frame:
                self.canvas = pygame.display.set_mode((width, height))
            else:
                self.canvas = pygame.display.set_mode((width, height), locals.NOFRAME)
        pygame.display.set_caption(titleName)
        self.clock = pygame.time.Clock()

        log.debug("DEBUG.LEVELGAMECONSOLE = {}".format(debug.levelGameConsole))

        self.gameConsole = console.GameConsole(self, Game, debug.levelGameConsole)
        self.console = self.gameConsole

        Application.canvas = self.canvas
        Application.game = self
        sprite.Sprite.game = self
        Task.game = self

        self._handler = event.GameEngineHandler()
        self.handlers = []
        self.keyHandler = event.KeyHandler()

        Game.app = None

    def getApp(self):
        log.warning("--> Using deprecated game.getApp() function.  Use arche.game.app instead: {}".format(traceback.extract_stack(limit=2)))
        return Game.app
    def setApp(self, value):
        log.warning("--> Using deprecated game.setApp() method.  Use arche.game.app instead: {}".format(traceback.extract_stack(limit=2)))
        Game.app = value
    app = property(getApp, setApp)

    def getAutoPause(self):
        return self._autoPause
    def setAutoPause(self, autoPause):
        self._autoPause = autoPause
        if not autoPause:
            self.paused = False
    autoPause = property(getAutoPause, setAutoPause)

    def addHandler(self, eventHandler):
        log.debug("ADDING HANDLER" + repr(eventHandler))
        self.handlers.append(eventHandler)
        log.debug("handlers: " + repr(self.handlers))
    def removeHandler(self, eventHandler):
        if eventHandler in self.handlers:
            self.handlers.remove(eventHandler)

    def xprop(self, proportion):
        return int(self.width * proportion)
    def yprop(self, proportion):
        return int(self.height * proportion)
        
    def startApp(self, application):
        Game.app = application

    def postEvent(self, event):
        log.info("posted event - " + repr(event))
        pygame.event.post(pygame.event.Event(event))

    def hideMouse(self):
        pygame.mouse.set_visible(False)
    def showMouse(self):
        pygame.mouse.set_visible(True)

    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False

##    def pause(self):
##        self.paused = True
##        self.runPaused()
##
##    def runPaused(self):
##        while self.paused:
##            dt = self.clock.get_time()
##
##            self.canvas.fill((0,0,0,255))
##
##            if not self.gameConsole.hidden:
##                self.gameConsole.update(dt)
##                self.gameConsole.draw(self.canvas)
##            for event in pygame.event.get():
##                self._handler.run(event, self)
##                self.keyHandler.run(event, self)
##                for handler in self.handlers:
##                    handler.run(event, self)
##
##            pygame.display.update()
##            self.clock.tick(self.limitFramerate)

    def run(self):
        log.info("starting main loop")

        while True:
            dt = self.clock.get_time() / 1000
         
            if Game.app:
                if not self.paused:
                    Game.app.tick(dt)
                Game.app.draw()
            
            if not self.gameConsole.hidden:
                self.gameConsole.update(dt)
                self.gameConsole.draw(self.canvas)

            for event in pygame.event.get():
                self._handler.run(event, self)
                self.keyHandler.run(event, self)
                for handler in self.handlers:
                    handler.run(event, self)

            pygame.display.update()
            self.clock.tick(self.limitFramerate)

    def quit(self):
        log.info("running game.quit")
        self.quitting = True
        pygame.quit()
        sys.exit(0)

class Application(object):
    canvas = None
    game = None
    def __init__(self):
        self._layers = []
        self.layers = {}
        self._orderedLayers = []
        self.registrar = {}

        self.tasks = []

        log.info("initializing application " + repr(self))
        
        self.width, self.height = Application.canvas.get_size()
        self.backgroundSurface = None
        self.backgroundColor = (0,0,0,255)
        
        self.canvas = Application.canvas

        Task.app = self
        sprite.Sprite.app = self

        self.addLayer("default")

    def addTask(self, task):
        self.tasks.append(task)
    def removeTask(self, task):
        if task in self.tasks:
            self.tasks.remove(task)

    def xprop(self, proportion):
        if self.game:
            return self.game.xprop(proportion)
    def yprop(self, proportion):
        if self.game:
            return self.game.yprop(proportion)

    def getCanvas(self):
        return pygame.display.get_surface()

    def onStart(self):
        pass

    def start(self):
        self.game.startApp(self)
        self.onStart()

    def isActive(self):
        return (self.game.app == self)
    active = property(isActive)

    def refreshLayers(self):
        self._orderedLayers = []
        layersLeft = list(self._layers)
        while len(self._orderedLayers) < len(self._layers):
            minValue = layersLeft[0].getLevel()
            minLayer = layersLeft[0]
            for layer in layersLeft:
                if layer not in self._orderedLayers and layer.getLevel() <= minValue:
                    minLayer = layer
                    minValue = layer.getLevel()
            layersLeft.remove(minLayer)
            self._orderedLayers.append(minLayer)
        self._orderedLayers.reverse()

    def addLayer(self, name, level=0):
        log.info("adding new layer '%s' on level %d"%(name,level))
        layer = Layer(name)
        layer.app = self
        self.layers[name] = layer
        self._layers.append(layer)
        layer.setLevel(level)
        self.refreshLayers()
        
    def removeLayer(self, layer):
        log.info("removing layer '%s' on level %d"%(layer.name, layer.level))
        layer = self.getLayer(layer)
        self._layers.remove(layer)
        del self.layers[layer.name]
        self._orderedLayers.remove(layer)
        
    def renameLayer(self, layer, name):
        log.info("renaming layer '%s' to new name '%s'"%(layer.name,name))
        del self.layers[layer.name]
        self.layers[name] = layer

    def getLayer(self, layer):
        if isinstance(layer, Layer):
            return layer
        elif isinstance(layer, str):
            return self.layers[layer]
        elif isinstance(layer, int):
            return self._layers[layer]
        else:
            return None

    def registerSprite(self, sprite, name):
        sprite._name = name
        #log.debug("registering sprite '%s'"%(sprite.name))
        self.registrar[name.lower()] = sprite
    def unregisterSprite(self, sprite):
        #log.debug("unregistering sprite '%s'"%(sprite.name))
        if sprite.name:
            if sprite.name.lower() in self.registrar:
                log.debug("sprite of name '%s' unregistered successfully"%(sprite.name))
                del self.registrar[sprite.name.lower()]
            else:
                log.warning("sprite of name '%s' is not in application"%(sprite.name))
    def renameSprite(self, sprite, newName):
        sprite._name = newName
        log.debug("renaming sprite '%s' to new name '%s'"%(sprite.name, newName))
        if sprite.name.lower() in self.registrar:
            del self.registrar[sprite.name.lower()]
        else:
            if sprite.name != None:
                log.warning("sprite of name '%s' is not in application"%(sprite.name))
        self.registrar[newName] = sprite
    def reg(self, name):
        if name.lower() in self.registrar:
            return self.registrar[name.lower()]
        else:
            log.warning("sprite of name '%s' is not in application"%(name))

    def addSprite(self, sprite, layer=0):
        #log.debug("adding sprite to layer %s"%(layer))
        if sprite.name != None:
            self.registerSprite(sprite, sprite.name)
        if isinstance(layer, Layer):
            layer.addSprite(sprite)
        elif isinstance(layer, str):
            if layer not in self.layers:
                log.warning(
                ("trying to add sprite '%s' to layer '%s' when that layer " + \
                "does not exist.  Creating layer and adding sprite")%(
                    repr(sprite),layer))
                self.addLayer(layer)
            self.layers[layer].addSprite(sprite)
        elif isinstance(layer, int):
            self._layers[layer].addSprite(sprite)
        else:
            pass
        sprite.onAdd()
        
    def removeSprite(self, sprite):
        #log.debug("removing sprite on level %d"%(sprite.layer.level))
        self._layers[sprite.layer.level].removeSprite(sprite)
        self.unregisterSprite(sprite)
    
    def tick(self, dt):
        #dt /= 1000.0
        for layer in self._orderedLayers:
            layer.update(dt)
        for task in self.tasks:
            task.tick()
        self.update(dt)

    def update(self, dt):
        pass
                
    def draw(self):
        if self.backgroundSurface:
            self.canvas.blit(self.backgroundSurface.get(), (0,0))
        elif self.backgroundColor:
            self.canvas.fill(self.backgroundColor)
        
        for layer in self._orderedLayers:
            layer.draw(Application.canvas)

    def getSprite(self, name):
        return self.reg(name)
    def getSprites(self):
        sprites = []
        for layer in self._layers:
            for sprite in layer.sprites:
                sprites.append(sprite)
        return sprites
    sprites = property(getSprites)

class Task(object):
    app = None
    game = None

    name = ""
    finished = False
    def __init__(self, name):
        #log.debug("Started new Task %s"%(name))
        self.name = name
        self.finished = False
    def tick(self):
        pass
    def onFinish(self):
        pass
    def finish(self):
        #log.debug("Task {} finished!".format(self))
        self.finished = True
        self.app.removeTask(self)
        self.onFinish()

class Layer(object):
    def __init__(self, name, level=0):
        self.sprites = []
        self._name = name
        self.app = None
        self._level = level

    def getLevel(self):
        return self._level
    def setLevel(self, level):
        self._level = level
        if self.app:
            self.app.refreshLayers()
    level = property(getLevel, setLevel)

    def getName(self):
        return self._name
    def setName(self, name):
        self._name = name
        self.app.renameLayer(self, name)
    name = property(getName, setName)

    def addSprite(self, sprite):
        sprite.app = self.app
        sprite.layer = self
        self.sprites.append(sprite)

    def removeSprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)

    def update(self, dt):
        for sprite in self.sprites:
            sprite.tick(dt)
    def draw(self, canvas):
        for sprite in self.sprites:
            sprite.draw(canvas)

#if _panda:
#    Application = ApplicationPanda