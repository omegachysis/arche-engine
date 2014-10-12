
import pygame

from . import image

class Rectangle(image.ImageSurface):

    _width = None
    _height = None
    def __init__(self, width, height, color, pixelAlpha=False):
        self._width = width
        self._height = height

        super(Rectangle, self).__init__(
            self.renderRectangle(), pixelAlpha)

        self.color = color

    def renderRectangle(self):
        rectSurface = pygame.Surface((self._width, self._height))
        rectSurface.fill((255,255,255))
        return rectSurface

    def refreshRectangle(self):
        self.setSource(self.renderRectangle())

    def getWidth(self):
        return self._width
    def setWidth(self, value):
        self._width = value
        self.refreshRectangle()
    width = property(getWidth, setWidth)

    def getHeight(self):
        return self._height
    def setHeight(self, value):
        self._height = value
        self.refreshRectangle()
    height = property(getHeight, setHeight)