
import pygame
import sys
from pygame.locals import *
from pygame import transform
import pygame.freetype
import traceback
import logging

from os import path

from .motion import action

from . import debug
#import Interface
from . import console
from . import sprite
from . import config
from . import image
from . import event

log = logging.getLogger("R.Engine")

class Game(object):
    
    def __init__(self, width, height, fullscreen=False, titleName="My Game", frame=True,
                 windowIcon="image/arche-engine.bmp", windowIconColorKey=False):
        log.info("initializing game engine")

        if windowIcon:
            if not windowIconColorKey:
                pygame.display.set_icon(pygame.image.load(windowIcon))
            else:
                image = pygame.image.load(windowIcon)
                image.set_colorkey(image.get_at((0,0)))
                pygame.display.set_icon(image)

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
            self.canvas = pygame.display.set_mode((width, height), FULLSCREEN)
        else:
            if frame:
                self.canvas = pygame.display.set_mode((width, height))
            else:
                self.canvas = pygame.display.set_mode((width, height), NOFRAME)
        pygame.display.set_caption(titleName)
        self.clock = pygame.time.Clock()

        log.debug("DEBUG.LEVELGAMECONSOLE = {}".format(debug.levelGameConsole))

        self.gameConsole = console.GameConsole(self, debug.levelGameConsole)
        self.console = self.gameConsole

        Application.canvas = self.canvas
        Application.game = self
        sprite.Sprite.game = self

        self._handler = event.GameEngineHandler()
        self.handlers = []
        self.keyHandler = event.KeyHandler()

        self.app = None

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
        self.app = application

    def postEvent(self, event):
        log.info("posted event - " + repr(event))
        pygame.event.post(pygame.event.Event(event))

    def hideMouse(self):
        pygame.mouse.set_visible(False)
    def showMouse(self):
        pygame.mouse.set_visible(True)

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
            
            if self.app:
                if not self.paused:
                    self.app.tick(dt)
                self.app.draw()
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
        self.registrar = {}

        log.info("initializing application " + repr(self))
        
        self.width, self.height = Application.canvas.get_size()
        self.backgroundsurface = None
        self.backgroundColor = (0,0,0,255)
        
        self.canvas = Application.canvas

        self.addLayer("default")

    def getCanvas(self):
        return pygame.display.get_surface()

    def start(self):
        self.game.startApp(self)

    def isActive(self):
        return (self.game.app == self)
    active = property(isActive)

    def getLayerlevel(self, layer):
        return self._layers.index(layer)

    def addLayer(self, name, level=0):
        log.info("adding new layer '%s' on level %d"%(name,level))
        layer = Layer(name)
        layer.app = self
        self.layers[name] = layer
        self._layers.append(layer)
        layer.level = len(self.layers) - 1
        layer.setLevel(level)
        
    def removeLayer(self, layer):
        log.info("removing layer '%s' on level %d"%(layer.name, layer.level))
        layer = self.getLayer(layer)
        self._layers.remove(layer)
        del self.layers[layer.name]
        
    def renameLayer(self, layer, name):
        log.info("renaming layer '%s' to new name '%s'"%(layer.name,name))
        del self.layers[layer.name]
        self.layers[name] = layer
        
    def moveLayer(self, layer, level):
        log.info("moving layer '%s' to level %d"%(layer.name,level))
        layer = self.getLayer(layer)
        
        if level < -1:
            level = len(self._layers) - level
        
        if level >= len(self._layers) or level == -1:
            self._layers.append(layer)
        else:
            self._layers = self._layers[:level] + [layer] + self._layers[level:]
            
        self.layers[layer.name] = layer

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
        
    def removeSprite(self, sprite):
        #log.debug("removing sprite on level %d"%(sprite.layer.level))
        self._layers[sprite.layer.level].removeSprite(sprite)
        self.unregisterSprite(sprite)
    
    def tick(self, dt):
        #dt /= 1000.0
        i = len(self._layers)
        while i > 0:
            i -= 1
            self._layers[i].update(dt)
        self.update(dt)

    def update(self, dt):
        pass
                
    def draw(self):
        if self.backgroundsurface:
            self.canvas.blit(self.backgroundsurface, (0,0))
        elif self.backgroundColor:
            self.canvas.fill(self.backgroundColor)
        
        i = len(self._layers)
        while i > 0:
            i -= 1
            self._layers[i].draw(Application.canvas)

    def getSprite(self, name):
        return self.reg(name)
    def getSprites(self):
        sprites = []
        for layer in self._layers:
            for sprite in layer.sprites:
                sprites.append(sprite)
        return sprites
    sprites = property(getSprites)

class Layer(object):
    def __init__(self, name):
        self.sprites = []
        self._name = name
        self.app = None

    def getLevel(self):
        return self.app.getLayerlevel(self)
    def setLevel(self, level):
        if level != self.getLevel():
            self.app.moveLayer(self, level)
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
