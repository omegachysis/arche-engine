
_panda = False
try:
    import pygame
    from pygame import locals
except: 
    _panda = True

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

class _ImageRect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class ImageSurfacePanda(object):
    def __init__(self, surface, pixelAlpha=True):
        if isinstance(surface, str):
            self.surface = loader.loadTexture(surface)

    def getSurface(self):
        return self._surface
    def setSurface(self, value):
        self._surface = value
        self._rect = _ImageRect(0, 0, self.width, self.height)
    surface = property(getSurface, setSurface)

    def getWidth(self):
        return self._surface.getSimpleXSize()
    def getHeight(self):
        return self._surface.getSimpleYSize()
    width = property(getWidth)
    height = property(getHeight)

    def rect(self):
        try:
            return self._rect
        except:
            return None
    def refresh(self):
        pass

class ImageCanvas(object):
    def __init__(self, pygameSurface):
        self.composite = pygameSurface.convert()
        self.clip = None
    def convert(self):
        return self.composite.convert()
    def convertAlpha(self):
        return self.composite.convert_alpha()
    def refresh(self):
        pass
    def rect(self):
        return self.composite.get_rect()
    def get(self):
        return self.composite
    
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

    _clip = None
    _clipX = 0
    _clipY = 0

    def convert(self):
        return self.composite.convert()
    def convertAlpha(self):
        return self.composite.convert_alpha()

    def getPixel(self, x, y):
        return self.get().get_at((x,y))

    def copy(self):
        return ImageSurface(self, self._pixelAlpha)

    def resetClip(self):
        self.setClip((0,0,self.getWidth(),self.getHeight()))
    def removeClip(self):
        self.setClip(None)

    def getClip(self):
        return self._clip
    def setClip(self, value):
        if value:
            self._clipX = value[0]
            self._clipY = value[1]
            self.applyClip()
        self._clip = value
    clip = property(getClip, setClip)

    def getClipX(self):
        return self._clipX
    def setClipX(self, value):
        if not self._clip:
            self.resetClip()
        self._clipX = value
        clip = self.getClip()
        self.setClip((value, clip[1], clip[2], clip[3]))
    clipX = property(getClipX, setClipX)

    def getClipY(self):
        return self._clipY
    def setClipY(self, value):
        if not self._clip:
            self.resetClip()
        self._clipY = value
        clip = self.getClip()
        self.setClip((clip[0], value, clip[2], clip[3]))
    clipY = property(getClipY, setClipY)

    def setAllowPixelAlpha(self, allowPixelAlpha):
        if allowPixelAlpha != self._pixelAlpha:
            if allowPixelAlpha:
                self._surface = self._surface.convert_alpha()
            else:
                self._surface = self._surface.convert()
            self._pixelAlpha = allowPixelAlpha
    def getAllowPixelAlpha(self):
        return self._pixelAlpha
    allowPixelAlpha = property(getAllowPixelAlpha, setAllowPixelAlpha)

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
        if self.source:
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
        self._modScale = scaleImage(self._surface, int(self._width), int(self._height))
        if ImageSurface.debugRevealPixelAlpha:
            if self._pixelAlpha:
                self._modScale.fill((255,0,0,255))
            else:
                self._modScale.fill((0,255,0,255))
        self.applyColor()
        self.applyAlpha()
        self.applyClip()

    def applyColor(self):
        # This is a semi fast pass.  Use the scaling slow passed image.
        if not ImageSurface.debugRevealPixelAlpha:
            if not self._pixelAlpha:
                self._modColor = self._modScale.convert()
                self._modColor.fill((self._red, self._green, self._blue),
                                    None, locals.BLEND_RGB_MULT)
                self.applyAlpha()
            else:
                self._modColor = self._modScale.convert_alpha()
                self._modColor.fill((self._red, self._green, self._blue, self._alpha),
                                    None, locals.BLEND_RGBA_MULT)
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

    def applyClip(self):
        # This is a very fast pass.  Use the triple passed image from scale, color, and alpha
        image = self._modColor
        image.set_clip(self._clip)
        self.composite = image

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

    def setScale(self, scalar):
        self.setSize((self.getWidth() * scalar, self.getHeight() * scalar))

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
        
if _panda:
    ImageSurface = ImageSurfacePanda