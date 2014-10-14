
try:
    import pygame
    from pygame import locals
except:
    pass

def getMouse():
    """ Return the current mouse pointer position. """
    return pygame.mouse.get_pos()

def isEventKeydown(event):
    """ Check if the pygame event is of the KEYDOWN type """
    return (event.type == pygame.locals.KEYDOWN)

def keyPressed(key):
    """ Check if a certain key (of string type) is pressed. """
    if isinstance(key, str):
        key = eval("locals.K_" + key.upper())
    return (pygame.key.get_pressed()[key])

key = keyPressed

def mousePressed(index):
    """ Return whether the mouse button of index is being pressed. """
    return (pygame.mouse.get_pressed()[index])

def isLeftClicking():
    return mousePressed(0)
def isRightClicking():
    return mousePressed(2)
def isWheelClicking():
    return mousePressed(1)