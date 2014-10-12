#!/usr/bin/env python3

import arche
import math

log = arche.debug.log("main")

def main():
    log.info("starting demo 012")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                      titleName = "ArcheEngine Demo - Parent Children")

    Demo().start()

    game.run()

class Walker(arche.Sprite):
    WALKING_SPEED = 300.00 # pixels per second
    def __init__(self):
        super(Walker, self).__init__(
            surface = arche.draw.Rectangle(
                width = 50,
                height = 50,
                color = (255,255,255)),)

        self.x = self.game.xprop(.50)
        self.y = self.game.yprop(.50)

        self.name = "walker parent"

    def onAdd(self):
        rectangle = Rectangle()
        self.addChild(rectangle)
        self.app.addSprite(rectangle)

        rectangleSmaller = Rectangle()
        rectangleSmaller.ANIMATION_RADIUS = 20
        rectangleSmaller.ANIMATION_SCALAR = 5
        rectangleSmaller.color = (0,0,255)
        rectangle.addChild(rectangleSmaller)
        self.app.addSprite(rectangleSmaller)

        super(Walker, self).onAdd()

    def update(self, dt):
        if arche.control.key("left"):
            self.x -= dt * self.WALKING_SPEED
        elif arche.control.key("right"):
            self.x += dt * self.WALKING_SPEED
        if arche.control.key("up"):
            self.y -= dt * self.WALKING_SPEED
        elif arche.control.key("down"):
            self.y += dt * self.WALKING_SPEED

class Rectangle(arche.Sprite):
    ANIMATION_RADIUS = 80
    ANIMATION_SCALAR = 1
    def __init__(self):
        super(Rectangle, self).__init__(
            surface = arche.draw.Rectangle(
                width = 10,
                height = 10,
                color = (255,0,0)),)

        self.x = 0
        self.y = 0

        self._animTime = 0

        self.name = "walker child"

    def update(self, dt):
        self._animTime += dt * self.ANIMATION_SCALAR
        self.x = self.ANIMATION_RADIUS * math.cos(self._animTime)
        self.y = self.ANIMATION_RADIUS * math.sin(self._animTime)

class Demo(arche.engine.Application):
    def __init__(self):
        super(Demo, self).__init__()

        self.backgroundColor = (0,120,0)

        self.walkingPlayer = Walker()
        self.addSprite(self.walkingPlayer)

if __name__ == "__main__":
    arche.debug.test(main)