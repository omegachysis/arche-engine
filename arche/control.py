
import pygame
from pygame import locals

def getMouse():
    return pygame.mouse.get_pos()

def isEventKeydown(event):
    return (event.type == pygame.locals.KEYDOWN)

def keyPressed(key):
    if isinstance(key, str):
        key = eval("K_" + key.upper())
    return (pygame.key.get_pressed()[key])
key = keyPressed

def mousePressed(index):
    return (pygame.mouse.get_pressed()[index])
