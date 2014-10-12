
import pygame
import sys
from pygame import locals
import traceback
import logging
from .motion.action import Action

from pygame import transform

from . import compat
from . import image
from . import control

log = logging.getLogger("R.Sprite")

class Sprite(object):
    game = None

    _x = 0
    _y = 0
    def __init__(self, surface, x=0, y=0, pixelAlpha=True):
        self.log = log # Compatibility reasons - refactoring

        # set up any private class variables.
        self._name = None

        self._parent = None
        self._children = []

        self.pickable = True

        self._pixelAlpha = pixelAlpha
        
        #if not isinstance(surface, image.ImageSurface):
        #    surface = image.ImageSurface(surface)

        self.surface = surface
        #self.rect = self._surface.rect()

        self.x = x
        self.y = y

        self.hidden = False

        self.dx = 0
        self.dy = 0

        self.app = None
        self.layer = None

        self.motions = []

        self.batches = []

    def onAdd(self):
        """ Called when the sprite is added to the application. """
        pass

    def isOnScreen(self):
        return (self.right > 0 and \
                self.left < self.game.width and \
                self.bottom > 0 and \
                self.top < self.game.height)
    onScreen = property(isOnScreen)

    def getActive(self):
        return  (self in self.layer.sprites)
    def setActive(self, active):
        if not active:
            self.destroy()
        else:
            self.layer.addSprite(self)
    active = property(getActive, setActive)

    def getParent(self):
        return self._parent
    def setParent(self, parent):
        self._parent = parent
        self._parent.addChild(self)
    parent = property(getParent, setParent)

    def getChild(self, id=None):
        if isinstance(id, str):
            for child in self._children:
                if child.name.lower() == name.lower():
                    return child
        elif isinstance(id, int):
            return self._children[name]
        else:
            return None
    def getChildren(self):
        return self._children
    children = property(getChildren)
        
    def __repr__(self):
        return "sprite '{}' {}".format(self.name, self.__class__)

    #def _pprop(self, prop, default):
    #    if self._parent:
    #        return getattr(self._parent, prop)
    #    else:
    #        return default

    def addChild(self, child):
        log.debug("Added child '%s' to parent '%s'" % (child, self))
        if child not in self._children:
            log.debug(" ^--> Not in children, will add")
            self._children.append(child)
            child._parent = self
            log.debug(" * child.x = {}".format(child.x))
            log.debug(" * child.y = {}".format(child.y))
            log.debug(" * parent.x = {}".format(self.x))
            log.debug(" * parent.y = {}".format(self.y))

            self._refreshChildren(('x','y'))
##            child.x = child.x - self.x
##            child.y = child.y - self.y
##            child.alpha = child.alpha

    def getSurface(self):
        return self._surface
    def setSurface(self, surface):
        if not isinstance(surface, image.ImageSurface):
            self._surface = image.ImageSurface(surface, self._pixelAlpha)
        else:
            self._surface = surface
        self._surface.refresh()
        self.rect = self._surface.rect()
    surface = property(getSurface, setSurface)

    def getAlpha(self):
        return self._surface.alpha
    def setAlpha(self, alpha):
        delta = alpha - self._surface.alpha
        self._surface.alpha = alpha
        self._influenceChildren("alpha", delta)
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
        #self.log.debug("adding motion %s to sprite"%(motion))
        self.motions.append(motion)
        motion.begin()

    def removeMotion(self, motion):
        #self.log.debug("removing motion %s from sprite"%(motion))
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

        for child in self._children:
            child.update(dt)

    def update(self, dt):
        pass
    
    def draw(self, canvas):
        if not self.hidden:
            canvas.blit(self._surface.get(), self.rect, self._surface.clip)
        for child in self._children:
            child.draw(canvas)
            
    def destroy(self):
        self.app.removeSprite(self)
        for batch in self.batches:
            batch.removeSprite(self)

    #def _influenceChild(self, child, variableName, delta):
    #    setattr(child, variableName, getattr(child, variableName)+delta)
    #def _influenceChildren(self, variableName, delta):
    #    log.debug("Influencing Children: %s %s"%(variableName, delta))
    #    for child in self._children:
    #        self._influenceChild(child, variableName, delta)
    def _refreshChildren(self, vars=['x','y']):
        for child in self._children:
            for variableName in vars:
                #self._influenceChild(child, variableName, getattr(self, variableName))
                setattr(child, variableName, getattr(child, variableName))

    def getAbsoluteX(self):
        if self.parent:
            return self._x + self.parent.getAbsoluteX()
        else:
            return self._x
    def getAbsoluteY(self):
        if self.parent:
            return self._y + self.parent.getAbsoluteY()
        else:
            return self._y
    
    def getX(self):
        return self._x
    def setX(self, x):
        if self.parent:
            self.rect.centerx = x + self.parent.getAbsoluteX()
        else:
            self.rect.centerx = x
        #dx = x - self._x
        self._x = x

        self._refreshChildren(('x'))
        #if dx:
        #    self._influenceChildren("x", dx)
    def getY(self):
        return self._y
    def setY(self, y):
        if self.parent:
            self.rect.centery = y + self.parent.getAbsoluteY()
        else:
            self.rect.centery = y
        #dy = y - self._y
        self._y = y

        self._refreshChildren(('y'))
        #if dy:
        #    self._influenceChildren("y", dy)
        
    x = property(getX, setX)
    y = property(getY, setY)

    def getPos(self):
        return (self._x, self._y)
    def setPos(self, value):
        self._x = value[0]
        self._y = value[1]
    pos = property(getPos, setPos)
    position = property(getPos, setPos)

    def getLeft(self):
        return self._x - self.rect.width / 2
    def setLeft(self, left):
        self.x = left + self.rect.width / 2
    def getRight(self):
        return self._x + self.rect.width / 2
    def setRight(self, right):
        self.x = right - self.rect.width / 2
    def getTop(self):
        return self._y - self.rect.height / 2
    def setTop(self, top):
        self.y = top + self.rect.height / 2
    def getBottom(self):
        return self._y + self.rect.height / 2
    def setBottom(self, bottom):
        self.y = bottom - self.rect.height / 2
        
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

    def getSize(self):
        return (self.rect.width, self.rect.height)
    def setSize(self, size):
        self.setWidth(size[0])
        self.setHeight(size[1])
    size = property(getSize, setSize)

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

        self.surface = image.createDefaultSurface()
        
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

#class MovingSprite(Sprite):
#    def __init__(self, speed=100, keyMoveLeft="left", keyMoveRight="right",
#                 keyMoveDown="down", keyMoveUp="up", obstacleBatch=None):

#        self.speed = speed

#        self.keyMoveLeft = keyMoveLeft
#        self.keyMoveRight = keyMoveRight
#        self.keyMoveDown = keyMoveDown
#        self.keyMoveUp = keyMoveUp

#        self.obstacleBatch = obstacleBatch

#    def tick(self, dt):
#        super().tick(dt)
#        if control.key(self.keyMoveLeft):
#            self.move(dt * -self.WALKING_SPEED, 0)
#        elif control.key(self.keyMoveRight):
#            self.move(dt * self.WALKING_SPEED, 0)
#        if control.key(self.keyMoveUp):
#            self.move(0, dt * -self.WALKING_SPEED)
#        elif control.key(self.keyMoveDown):
#            self.move(0, dt * self.WALKING_SPEED)

#    def move(self, dx, dy):
#        self.x += dx
#        self.y += dy

#        if self.right > self.game.width:
#            self.right = self.game.width
#        if self.left < 0:
#            self.left = 0
#        if self.bottom > self.game.height:
#            self.bottom = self.game.height
#        if self.top < 0:
#            self.top = 0

#        if self.obstacleBatch and self.obstacleBatch.getCollisions(self):
#            self.x -= dx
#            self.y -= dy
