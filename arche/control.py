
import pygame
from pygame.locals import *

def getMouse():
    return pygame.mouse.get_pos()

def isEventKeydown(event):
    return (event.type == pygame.locals.KEYDOWN)

class EventTracker(object):
    keydown = []

events = EventTracker()

def clearKeyboardEvents():
    events.keydown = []

def keyPressed(key):
    return (pygame.key.get_pressed()[key])
key = keyPressed

def mousePressed(index):
    return (pygame.mouse.get_pressed()[index])
