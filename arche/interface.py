
import pygame
from pygame import locals
import logging

from . import engine
from . import sprite

log = logging.getLogger("R.Interface")

def main():
    game = Engine.Game(1280, 720)

    testApp = Engine.Application()
    testApp.backgroundColor = (0, 0, 0, 255)

    testButton = SolidButton(100, 200, 50, 50,
                             (0,0,255,255), (255,0,255,255), (0,255,0,255),
                             None)

    testApp.addSprite(testButton)

    testButton2 = SolidButton(400, 200, 200, 200,
                             (255,0,0,255), (255,0,255,255), (0,255,0,255),
                             game.quit)

    testButton2.text = Sprite.Text("X", 50, 50, (255,255,255,255), 250, "consola.ttf")

    testApp.addSprite(testButton2)

    game.startApp(testApp)
    game.run()

def loadButtonImageGroup(prefix, suffix, group=("Reset","Hover","Press"),
                         perPixelAlpha=True):
    """
    Loads a button image group ('reset', 'press', 'hover') on
    those characteristics.  The group identifier is placed between
    'prefix' and 'suffix'
    """
    if perPixelAlpha:
        return (pygame.image.load(prefix+group[0]+suffix).convert_alpha(),
                pygame.image.load(prefix+group[1]+suffix).convert_alpha(),
                pygame.image.load(prefix+group[2]+suffix).convert_alpha())
    else:
        return (pygame.image.load(prefix+group[0]+suffix).convert(),
                pygame.image.load(prefix.group[1]+suffix).convert(),
                pygame.image.load(prefix+group[2].suffix).convert())

class Button(sprite.Sprite):
    STATE_RESET = 0
    STATE_HOVER = 1
    STATE_PRESS = 2
    def __init__(self, surface, x=0, y=0, command=None, textObject=None,
                 pixelAlpha=True):

        self.text = None # Changing coordinates in init would
                         # cause problems without defining this.
        self._enabled = True
        
        super(Button, self).__init__(surface, 0, 0, pixelAlpha)

        self.surface = surface

        self.state = Button.STATE_RESET

        self.text = textObject
        self.text.parent = self

        self.x = x
        self.y = y

        self.command = command

    def getEnabled(self):
        return self._enabled
    def setEnabled(self, enabled):
        if enabled:
            self._enable()
        else:
            self._disable()
    enabled = property(getEnabled, setEnabled)

    def enable(self):
        self._enable()
        self._enabled = True
    def disable(self):
        self._disable()
        self._enabled = False
    def _enable(self): pass
    def _disable(self): pass

    def update(self, dt):
        pass

    def tick(self, dt):
        if self._enabled:
            mousex, mousey = pygame.mouse.get_pos()

            if mousex > self.left and mousex < self.right and \
               mousey > self.top  and mousey < self.bottom:
                if pygame.mouse.get_pressed()[0]:
                    self._press()
                else:
                    self._hover()
            else:
                self._reset()

            super(Button, self).tick(dt)

            self.update(dt)

    def hover(self): pass
    def press(self): pass
    def reset(self): pass

    def _triggerState(self):
        """ Refresh a button by setting its state to itself. """
        state = self.state
        self.state = None
        if state == Button.STATE_HOVER:
            self._hover()
        elif state == Button.STATE_PRESS:
            self._press()
        elif state == Button.STATE_RESET:
            self._reset()

    def refresh(self):
        self._triggerState()
    
    def _hover(self):
        """State invoked when the mouse is on top of the button."""
        if self.state != Button.STATE_HOVER:
            self.hover()
            if self.state == Button.STATE_PRESS:
                if self.command:
                    self.command()
            self.state = Button.STATE_HOVER
    def _press(self):
        """State invoked when the mouse is on top of the button and clicks."""
        if self.state != Button.STATE_PRESS:
            self.press()
            self.state = Button.STATE_PRESS
    def _reset(self):
        """State invoked when the mouse is outside of the button boundary."""
        if self.state != Button.STATE_RESET:
            self.reset()
            self.state = Button.STATE_RESET

class SolidButton(Button):
    def __init__(self, x=0, y=0, width=50, height=50,
                 colorReset=(0,0,0), colorHover=(0,0,0), colorPress=(0,0,0),
                 colorDisabled=(0,0,0),
                 command=None, textObject=None):
        """
        Create a solid colored button that runs 'command' when clicked.
        """
        log.debug("intializing new solid button")

        self._pixelAlpha = False

        # Fill a rectangular and blank surface with plain white color
        self.surface = pygame.Surface((width, height))
        self.surface.source.fill((255,255,255,255))

        super(SolidButton, self).__init__(self.surface, x, y, command, textObject,
                                          pixelAlpha = False)

        self.color = colorReset

        self.colorReset = colorReset
        self.colorHover = colorHover
        self.colorPress = colorPress
        self.colorDisabled = colorDisabled

    def hover(self):
        self.color = self.colorHover
    def press(self):
        self.color = self.colorPress
    def reset(self):
        self.color = self.colorReset
        
    def _disable(self):
        self.color = self.colorDisabled
    def _enable(self):
        self.refresh()

class ImageButton(Button):
    STATE_RESET = 0
    STATE_HOVER = 1
    STATE_PRESS = 2
    def __init__(self, x=0, y=0, width=50, height=50, imageGroup=None,
                 imageReset=None, imageHover=None, imagePress=None,
                 command=None, textObject=None):
        """
        Create a button that runs 'command' when clicked.
        """
        log.debug("initializing new image button")

        if imageGroup:
            self.imageReset, self.imageHover, self.imagePress = imageGroup
        else:
            self.imageReset = imageReset
            self.imageHover = imageHover
            self.imagePress = imagePress

        self._imageReset = self.imageReset
        self._imageHover = self.imageHover
        self._imagePress = self.imagePress

        self.surface = self.imageReset

        super(ImageButton, self).__init__(self.surface, x, y, command, textObject)

        self.width = width
        self.height = height

    def setWidth(self, width):
        self.imageReset = Sprite.scaleImage(self._imageReset, width, self.height)
        self.imageHover = Sprite.scaleImage(self._imageHover, width, self.height)
        self.imagePress = Sprite.scaleImage(self._imagePress, width, self.height)
        self._rect.width = self.imageReset.get_width()
        self.refresh()
    def setHeight(self, height):
        self.imageReset = Sprite.scaleImage(self._imageReset, self.width, height)
        self.imageHover = Sprite.scaleImage(self._imageHover, self.width, height)
        self.imagePress = Sprite.scaleImage(self._imagePress, self.width, height)
        self._rect.height = self.imageReset.get_height()
        self.refresh()
    width = property(Button.getWidth, setWidth)
    height= property(Button.getHeight, setHeight)

    def hover(self):
        self._surface = self.imageHover
    def press(self):
        self._surface = self.imagePress
    def reset(self):
        self._surface = self.imageReset

class Entry(object):
    def __init__(self, surface, font, fontColor, fontSize, padding, maxBuffer=100,
                 restricted=[]):
        pass

if __name__ == "__main__":
    import Debug
    Debug.test(main)
