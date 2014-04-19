
import pygame
from pygame.locals import *
import logging

log = logging.getLogger("R.Surface")

def scaleImage(surface, width, height):
    """ Return surface scaled to fit width and height. """
    log.debug("scaled image %s" % repr(surface))
    return pygame.transform.smoothscale(surface, (width, height))

class ImageSurface(object):
    def __init__(self, surface, pixelAlpha=True):
        if isinstance(surface, str):
            surface = pygame.image.load(surface)
        
        if not pixelAlpha:
            self._surface = surface.convert()
        else:
            self._surface = surface.convert_alpha()

        self.composite = self._surface
        self._modScale = None
        self._modColor = None
        self._pixelAlpha = pixelAlpha

        self._width  = self._surface.get_width()
        self._height = self._surface.get_height()

        self._red = 255
        self._green = 255
        self._blue = 255
        self._alpha = 255

        self.refresh()

    def refresh(self):
        """ Apply all modified image parameters. """
        self.applyScale()

    def replace(self, surface, normalize=True):
        """ Replace source surface with another. """
        if not self._pixelAlpha:
            self._surface = surface.convert()
        else:
            self._surface = surface.convert_alpha()
        self.refresh()
        if normalize:
            self.normalize()

    def normalize(self):
        """ Reset scaling parameters to fit source surface. """
        self.size = self._surface.get_size()

    def get(self):
        """ Get the finished composite surface. """
        return self.composite

    def rect(self):
        """ Get rectangle of compsite surface. """
        return self.composite.get_rect()

    def convert(self):
        """ Return a converted version of the source surface. """
        if not self._pixelAlpha:
            return self._surface.convert()
        else:
            return self._surface.convert_alpha()

    def applyScale(self):
        # This is a slow pass.  Do this as little as possible.
        self._modScale = scaleImage(self._surface, self._width, self._height)
        self.applyColor()
        self.applyAlpha()

    def applyColor(self):
        # This is a semi fast pass.  Use the scaling slow passed image.
        if not self._pixelAlpha:
            self._modColor = self._modScale.convert()
            self._modColor.fill((self._red, self._green, self._blue),
                                None, BLEND_RGB_MULT)
            self.applyAlpha()
        else:
            self._modColor = self._modScale.convert_alpha()
            self._modColor.fill((self._red, self._green, self._blue, self._alpha),
                                None, BLEND_RGBA_MULT)
            self.composite = self._modColor
        
    def applyAlpha(self):
        # This is a fast pass.  Use the double passed image from scale and color.
        if not self._pixelAlpha:
            self._modColor.set_alpha(alpha)
            self.composite = self._modColor
        else:
            self.applyColor()

    def getWidth(self):
        return self._width
    def setWidth(self, width):
        self._width = width
        self.applyScale()
    width = property(getWidth, setWidth)

    def getHeight(self):
        return self._height
    def setHeight(self, height):
        self._height = height
        self.applyScale()
    height = property(getHeight, setHeight)

    def getSize(self):
        return (self._width, self._height)
    def setSize(self, size):
        self._width = size[0]
        self._height = size[1]
        self.applyScale()
    size = property(getSize, setSize)

    def getRed(self):
        return self._red
    def setRed(self, red):
        self._red = red
        self.applyColor()
    red = property(getRed, setRed)

    def getGreen(self):
        return self._green
    def setGreen(self, green):
        self._green = green
        self.applyColor()
    green = property(getGreen, setGreen)

    def getBlue(self):
        return self._blue
    def setBlue(self, blue):
        self._blue = blue
        self.applyColor()
    blue = property(getBlue, setBlue)

    def getAlpha(self):
        return self._alpha
    def setAlpha(self, alpha):
        self._alpha = alpha
        self.applyAlpha()
    alpha = property(getAlpha, setAlpha)

    def getColor(self):
        return (self._red, self._green, self._blue)
    def setColor(self, color):
        self._red = color[0]
        self._green = color[1]
        self._blue = color[2]
        self.applyColor()
    color = property(getColor, setColor)
        
            
