
import pygame
import sys
from pygame.locals import *
import traceback
import logging
from .motion.action import Action

from pygame import transform

from . import compat
from . import surf

log = logging.getLogger("R.Engine.Sprite")

class Sprite(object):
    game = None
    def __init__(self, surface, x, y, pixelAlpha=True):
        self.log = log # Compatibility reasons - refactoring

        # set up any private class variables.
        self._name = None

        self.pickable = True

        self._pixelAlpha = pixelAlpha
        self.surface = surf.ImageSurface(surface, pixelAlpha)

        self.x = x
        self.y = y

        self.hidden = False

        self.dx = 0
        self.dy = 0

        # App is a variable tracking the game application.
        # It is assigned when the sprite is added to the draw list.
        self.app = None
        self.layer = None

        self.motions = []

    def getSurface(self):
        return self._surface
    def setSurface(self, surface):
        self._surface = surf.ImageSurface(surface, self._pixelAlpha)
        self.rect = self._surface.rect()
    surface = property(getSurface, setSurface)

    def getAlpha(self):
        return self._surface.alpha
    def setAlpha(self, alpha):
        self._surface.alpha = alpha
    alpha = property(getAlpha, setAlpha)

    def getColor(self):
        return self._surface.color
    def setColor(self, color):
        self._surface.color = color
    color = property(getColor, setColor)

    def getName(self):
        return self._name
    def setName(self, name):
        if self.app:
            if self._name:
                self.app.renameSprite(self, name)
            else:
                self.app.registerSprite(self, name)
        self._name = name
    name = property(getName, setName)

    def getHidden(self):
        return self._hidden
    def setHidden(self, hidden):
        self._hidden = hidden
    hidden = property(getHidden, setHidden)
    def hide(self):
        self.log.debug("hiding sprite")
        self.hidden = True
    def unhide(self):
        self.log.debug("unhiding sprite")
        self.hidden = False

    def isActive(self):
        return (self.app != None)

    def addMotion(self, motion):
        self.log.debug("adding motion %s to sprite"%(motion))
        self.motions.append(motion)
        motion.begin()

    def removeMotion(self, motion):
        self.log.debug("removing motion %s from sprite"%(motion))
        if isinstance(motion, Action):
            motion.cancel()
            self.motions.remove(motion)
        elif isinstance(motion, str):
            for imotion in self.motions:
                if imotion.name == motion.lower():
                    imotion.cancel()
            self.motions = [imotion for imotion in self.motions if not imotion.canceled]
    
    def tick(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

        if self.motions:
            for motion in self.motions:
                motion.update(dt)

        self.update(dt)

    def update(self, dt):
        pass
    
    def draw(self, canvas):
        if not self.hidden:
            canvas.blit(self._surface.get(), self.rect)
            
    def destroy(self):
        self.app.removeSprite(self)
    
    def getX(self):
        return self._x
    def setX(self, x):
        self.rect.centerx = x
        self._x = x
    def getY(self):
        return self._y
    def setY(self, y):
        self.rect.centery = y
        self._y = y
        
    x = property(getX, setX)
    y = property(getY, setY)

    def getLeft(self):
        return self._x - self.rect.width / 2
    def setLeft(self, left):
        self._x = left + self.rect.width / 2
    def getRight(self):
        return self._x + self.rect.width / 2
    def setRight(self, right):
        self._x = right - self.rect.width / 2
    def getTop(self):
        return self._y - self.rect.height / 2
    def setTop(self, top):
        self._y = top + self.rect.height / 2
    def getBottom(self):
        return self._y + self.rect.height / 2
    def setBottom(self, bottom):
        self._y = bottom - self.rect.height / 2
        
    left = property(getLeft, setLeft)
    right = property(getRight, setRight)
    top = property(getTop, setTop)
    bottom = property(getBottom, setBottom)

    def getWidth(self):
        return self.rect.width
    def getHeight(self):
        return self.rect.height
    def setWidth(self, width):
        self.rect.width = width
        self._surface.width = width
    def setHeight(self, height):
        self.rect.height = height
        self._surface.height = height
    width = property(getWidth, setWidth)
    height= property(getHeight, setHeight)

class Text(Sprite):
    game = None
    def __init__(self, value, x, y, color, size, font=None):
        log.debug("initializing text object of value '%s'"%(value))

        super(Text, self).__init__(None, x, y)
        
        # manually set values to avoid problems in auto render
        self._font = font
        self._value = value
        self._color = color
        self._size = size
        self._alpha = 255

        # setting prop values will auto render the text on each assignment
        self.font = font
        self.value = value
        self.color = color
        self.size = size

        self.surface = surf.createDefaultSurface()
        
        self.render()

    def render(self):
        surface, rect = compat.freetypeRender(
            self._font, self._value, self._color, 
            rotation = 0, size = self._size)

        self.surface.source = surface
        self.rect = self.surface.rect()
    
    def getFont(self):
        return self._fontFilename
    def setFont(self, font):
        self._font = compat.freetypeFont(font, self._size)
        self._fontFilename = font
        self.render()
    font = property(getFont, setFont)

    def getValue(self):
        return self._value
    def setValue(self, value):
        self._value = value
        self.render()
    value = property(getValue, setValue)

    def getColor(self):
        return self._color
    def setColor(self, color):
        self._color = color
        self.render()
    color = property(getColor, setColor)

    def getSize(self):
        return self._size
    def setSize(self, size):
        self._size = size
        self.render()
    size = property(getSize, setSize)

def scaleImage(surface, width, height):
    """ Return surface scaled to fit width and height. """
    log.debug("scaled image %s" % repr(surface))
    return transform.smoothscale(surface, (width, height))
