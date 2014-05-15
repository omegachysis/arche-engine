
import pygame
from pygame.locals import *
import logging

log = logging.getLogger("R.Surface")

def scaleImage(surface, width, height):
    """ Return surface scaled to fit width and height. """
    #log.debug("scaled image %s" % repr(surface))
    return pygame.transform.smoothscale(surface, (width, height))

def profilerRecordImageSurfaces():
    log.info("PERFORMANCE PROFILER ENGAGED: RecordImageSurfaces")
    ImageSurface.debugRecordSurfaces = True
def profilerRevealPixelAlpha():
    log.info("PERFORMANCE PROFILER ENGAGED: RevealPixelAlpha")
    ImageSurface.debugRevealPixelAlpha = True
    for surf in ImageSurface.imageSurfaces:
        surf.refresh()
    if not ImageSurface.debugRecordSurfaces:
        log.warning("PERFORMANCE PROFILER FAILED: Not recording surfaces; "+\
                    "inconsistancies may occur.")

def createDefaultSurface():
    surface = pygame.Surface((1,1))
    surface.fill((255,255,255,255))
    return surface

newDefaultSurface = createDefaultSurface

def newRectangle(width, height, color = (255,255,255)):
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface
    
class ImageSurface(object):
    imageSurfaces = []
    debugRecordSurfaces = False
    debugRevealPixelAlpha = False
    if debugRevealPixelAlpha:
        log.debug("PERFORMANCE PROFILER ENGAGED: RevealPixelAlpha")
    def __init__(self, surface, pixelAlpha=True):
        if ImageSurface.debugRecordSurfaces:
            ImageSurface.imageSurfaces.append(self)
            
        if isinstance(surface, str):
            surface = pygame.image.load(surface)
        elif isinstance(surface, ImageSurface):
            surface = surface.source
        
        if surface:
            if not pixelAlpha:
                self._surface = surface.convert()
            else:
                self._surface = surface.convert_alpha()
        else:
            self._surface = None

        self.composite = None
        self._modScale = None
        self._modColor = None
        
        self._pixelAlpha = pixelAlpha

        if self._surface:
            self._width  = self._surface.get_width()
            self._height = self._surface.get_height()
        else:
            self._width = 0
            self._height = 0

        self._red = 255
        self._green = 255
        self._blue = 255
        self._alpha = 255

        if self._surface:
            self.refresh()

    def _revealPixelAlpha(self):
        if self._pixelAlpha:
            surface = pygame.Surface((self._width, self._height)).convert_alpha()
            surface.fill((255,0,0,255))
            return surface
        else:
            surface = pygame.Surface((self._width, self._height)).convert()
            surface.fill((0,255,0,255))
            return surface

    def refresh(self):
        """ Apply all modified image parameters. """
        self.applyScale()

    def replace(self, surface, normalize=True):
        """ Replace source surface with another. """
        if ImageSurface.debugRevealPixelAlpha:
            surface = self._revealPixelAlpha()
        if not self._pixelAlpha:
            self._surface = surface.convert()
        else:
            self._surface = surface.convert_alpha()
        self.refresh()
        if normalize:
            self.normalize()

    def permeate(self):
        """ Set the source image surface to the current composite surface. """
        self.source = self.composite

    def normalize(self):
        """ Reset scaling parameters to fit source surface. """
        self.size = self._surface.get_size()

    def get(self):
        """ Get the finished composite surface. """
        return self.composite

    def rect(self):
        """ Get rectangle of compsite surface. """
        if self.composite:
            return self.composite.get_rect()
        else:
            return pygame.Rect((0,0,1,1))

    def convert(self):
        """ Return a converted version of the source surface. """
        if not self._pixelAlpha:
            return self._surface.convert()
        else:
            return self._surface.convert_alpha()

    def applyScale(self):
        # This is a slow pass.  Do this as little as possible.
        self._modScale = scaleImage(self._surface, self._width, self._height)
        if ImageSurface.debugRevealPixelAlpha:
            if self._pixelAlpha:
                self._modScale.fill((255,0,0,255))
            else:
                self._modScale.fill((0,255,0,255))
        self.applyColor()
        self.applyAlpha()

    def applyColor(self):
        # This is a semi fast pass.  Use the scaling slow passed image.
        if not ImageSurface.debugRevealPixelAlpha:
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
        else:
            self.composite = self._modScale
        
    def applyAlpha(self):
        # This is a fast pass.  Use the double passed image from scale and color.
        if not ImageSurface.debugRevealPixelAlpha:
            if not self._pixelAlpha:
                self._modColor.set_alpha(self._alpha)
                self.composite = self._modColor
            else:
                self.applyColor()
        else:
            self.composite = self._modScale

    def getSource(self):
        return self._surface
    def setSource(self, source):
        self.replace(source, True)
        
    source = property(getSource, setSource)
    image = property(getSource, setSource)

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
        
            
