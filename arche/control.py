
import pygame

def getMouse():
    return pygame.mouse.get_pos()

def isEventKeydown(event):
    return (event.type == pygame.locals.KEYDOWN)
