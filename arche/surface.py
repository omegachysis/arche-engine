
import pygame
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

        self.composite = None
        self.pixelAlpha = pixelAlpha

    def convert(self):
        if not pixelAlpha:
            return self._surface.convert()
        else:
            return self._surface.convert_alpha()

    def applyScale(self):
        pass

    def reset(self):
        self.composite = self.convert()
