#!/usr/bin/env python3

import arche
import random

log = arche.debug.log("main")

def main():
    log.info("starting demo 010")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Moving Sprite",)

    Demo().start()
    
    game.run()

class WalkingRectangle(arche.Sprite):
    
    WALKING_SPEED = 300.00 # pixels per second
    
    def __init__(self):
        super().__init__(
            surface = arche.image.newRectangle(width = 50, height = 50, color = (255,255,0))
            )

        # center the rectangle on the screen
        self.x = self.game.xprop(.5)
        self.y = self.game.yprop(.5)

        self.name = "walking rectangle"

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

        # make sure the player can't walk off the edges of the screen
        if self.right > self.game.width:
            self.right = self.game.width
        if self.left < 0:
            self.left = 0
        if self.bottom > self.game.height:
            self.bottom = self.game.height
        if self.top < 0:
            self.top = 0

        if self.app.obstacleBatch.getCollisions(self):
            self.x -= dx
            self.y -= dy

    def update(self, dt):
        # set of conditions to move the rectangle with the arrow keys
        if arche.control.key("left"):
            self.move(dt * -self.WALKING_SPEED, 0)
        elif arche.control.key("right"):
            self.move(dt * self.WALKING_SPEED, 0)
        if arche.control.key("up"):
            self.move(0, dt * -self.WALKING_SPEED)
        elif arche.control.key("down"):
            self.move(0, dt * self.WALKING_SPEED)

class Obstacle(arche.Sprite):

    def __init__(self, app, width, height, x, y):
        
        super().__init__(
            surface = arche.image.newRectangle(width = width, height = height, color = (80,150,255)),
            )

        self.x = x
        self.y = y

        app.obstacleBatch.addSprite(self)
        app.addSprite(self)

class Demo(arche.engine.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (10,120,20)

        self.player = WalkingRectangle()
        self.addSprite(self.player)

        self.obstacleBatch = arche.sprite.Batch()

        Obstacle(self, 200, 40, self.game.xprop(.30), self.game.yprop(.30))
        Obstacle(self, 200, 40, self.game.xprop(.60), self.game.yprop(.60))

    def update(self, dt):
        pass

if __name__ == "__main__":
    arche.debug.test(main)
