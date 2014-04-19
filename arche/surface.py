
import pygame
from pygame.locals import *
import logging

log = logging.getLogger("R.Surface")

def scaleImage(surface, width, height):
    """ Return surface scaled to fit width and height. """
    log.debug("scaled image %s" % repr(surface))
    return transform.smoothscale(surface, (width, height))

class ImageSurface(object):
    def __init__(self, pygameSurface, pixelAlpha=True):
        if not pixelAlpha:
            self._surface = pygameSurface.convert()
        else:
            self._surface = pygameSurface.convert_alpha()

        self.composite = self._surface
        self._modScale = None
        self._modColor = None
        self._pixelAlpha = pixelAlpha

    def convert(self):
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
            self.applyColor(self._red, self._green, self._blue, self._alpha)

    def getWidth()
    def setWidth()

    def getHeight()
    def setHeight()

    def getSize()
    def setSize()

    def getRed()
    def setRed()

    def getGreen()
    def setGreen()

    def getBlue()
    def setBlue()

    def getAlpha()
    def setAlpha()
        
            
