
import pygame
import sys
from pygame.locals import *
from pygame import transform
import pygame.freetype
import traceback
import logging

log = logging.getLogger("R.Engine.Sprite")

class Sprite(object):
    game = None
    def __init__(self, surface, x, y):
        self.log = log # Compatibility reasons - refactoring

        # set up any private class variables.
        self._name = None
        self._rect = None
        self._surface = None
        self.__surface__ = None
        
        self.surface = surface
        self.x = x
        self.y = y

        self.alpha = 255

        self.hidden = False

        self.dx = 0
        self.dy = 0

        # App is a variable tracking the game application.
        # It is assigned when the sprite is added to the draw list.
        self.app = None
        self.layer = None

        self.motions = []

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
    
    def getAlpha(self):
        return self._alpha
    def setAlpha(self, alpha):
        self._surface.set_alpha(alpha)
        self._alpha = alpha
    alpha = property(getAlpha, setAlpha)

    def addMotion(self, motion):
        self.log.info("adding motion %s to sprite"%(motion))
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
            canvas.blit(self._surface, self._rect)
            
    def destroy(self):
        self.app.removeSprite(self)

    # ----------------------------------------------
    # Setup class properties
    
    def getX(self):
        return self._x
    def setX(self, x):
        self._rect.centerx = x
        self._x = x
    def getY(self):
        return self._y
    def setY(self, y):
        self._rect.centery = y
        self._y = y
        
    x = property(getX, setX)
    y = property(getY, setY)

    def getLeft(self):
        return self._x - self._rect.width / 2
    def setLeft(self, left):
        self._x = left + self._rect.width / 2
    def getRight(self):
        return self._x + self._rect.width / 2
    def setRight(self, right):
        self._x = right - self._rect.width / 2
    def getTop(self):
        return self._y - self._rect.height / 2
    def setTop(self, top):
        self._y = top + self._rect.height / 2
    def getBottom(self):
        return self._y + self._rect.height / 2
    def setBottom(self, bottom):
        self._y = bottom - self._rect.height / 2
        
    left = property(getLeft, setLeft)
    right = property(getRight, setRight)
    top = property(getTop, setTop)
    bottom = property(getBottom, setBottom)

    def getWidth(self):
        return self._rect.width
    def getHeight(self):
        return self._rect.height
    def setWidth(self, width):
        self._surface = scaleImage(self.__surface__, width, self._rect.height)
        self._rect.width = width
    def setHeight(self, height):
        self._surface = scaleImage(self.__surface__, self._rect.width, height)
        self._rect.height = height
    width = property(getWidth, setWidth)
    height= property(getHeight, setHeight)

    def getSurface(self):
        return self._surface
    def setSurface(self, surface):
        self.__surface__ = surface # __surface__ original, untouched surface object
        self._surface = surface
        if hasattr(self, "_rect"):
            if self._rect == None:
                self._rect = surface.get_rect()
        else:
            self._rect = surface.get_rect()
            
        if surface.get_width() - self._rect.width >= 1 or \
           surface.get_height()- self._rect.height >= 1:
            self.setWidth(self.getWidth())
            self.setHeight(self.getHeight())
        self._rect = self._surface.get_rect()
        
    surface = property(getSurface, setSurface)

    def getRect(self):        
        return self._rect
    def setRect(self, rect):
        self._rect = rect
    rect = property(getRect, setRect)

    #---------------------------------------------

class Text(Sprite):
    game = None
    def __init__(self, value, x, y, color, size, font=None):
        log.debug("initializing text object of value '%s'"%(value))
        
        # manually set values to avoid problems in auto render
        self._font = font
        self._value = value
        self._color = color
        self._size = size

        # setting prop values will auto render the text on each assignment
        self.font = font
        self.value = value
        self.color = color
        self.size = size

        super(Text, self).__init__(self._surface, x, y)

    def render(self):
        self._surface, self._rect = self._font.render(self._value, self._color, None,
                                                rotation = 0, ptsize = self._size)
    
    def getFont(self):
        return self._fontFilename
    def setFont(self, font):
        self._font = pygame.freetype.Font(font, ptsize = self._size)
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
