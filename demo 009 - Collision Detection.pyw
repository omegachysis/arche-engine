#!/usr/bin/env python3

import arche
import random

log = arche.debug.log("main")

def main():
    log.info("starting demo 009")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Collision Detection",)

    Demo().start()
    
    game.run()

class Cursor(arche.Sprite):
    def __init__(self):
        super().__init__(
            surface = "image/test.png",
            x = 0, y = 0)

        self.size = 100, 100

        self.name = "cursor"
        self.pickable = False

    def update(self, dt):
        self.x, self.y = arche.control.getMouse()

        # cycle through all the bullets and check for a collision.
        for bullet in self.app.bulletBatch.getCollisions(self):
            # if there was, turn the bullet a reddish color.
            bullet.color = (255,50,50)

        # consistently results in 'true' when the spacebar is being pressed
        if arche.control.key(arche.control.K_SPACE):
            # reset the colors of all the bullets in the bulletBatch
            for bullet in self.app.bulletBatch.sprites:
                bullet.resetColor()

class Bullet(arche.sprite.Sprite):
    def __init__(self):
        super().__init__( # save precious loading time by loading the image once elsewhere.
            surface = Bullet.img)
        
        self.x = self.game.xprop(random.random()-.5)
        self.y = self.game.yprop(random.random()-.5)

        self.resetColor()

        # dx and dy refer to a change in the cooresponding
        #  coordinate per millisecond.
        #  'dx = 1' will make the sprite's 'x' value
        #  move 1 pixel per second
        self.dx = random.random() / 5 * 1000
        self.dy = random.random() / 5 * 1000

    # Create a method to be used later
    def resetColor(self):
        # tint the bullet a pale blue color
        self.color = (50,255,255)

    def update(self, dt):
        if not self.onScreen:
            # If the bullet goes off screen, get rid of it from memory.
            #  This will automatically destroy it from the batch
            #  as well.
            self.destroy()

class Demo(arche.engine.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (50,0,0)

        # create a layer to draw all the bullets on.
        # '1' means it will be above the default layer,
        # which is created on '0'.  The cursor is on that layer.
        self.addLayer("bullets", 1)

        # A batch is a collection of sprites optimized
        # for collision detection that is faster
        # than wasting precious time checking all collisions twice.
        self.bulletBatch = arche.sprite.Batch()

        # If your image does not have per pixel alpha values,
        # always state 'pixelAlpha = False'.  Drawing will be
        # considerably faster with no per pixel alpha values.
        Bullet.img = arche.image.ImageSurface("image/test.png", pixelAlpha = False)

        # Scale the image down
        Bullet.img.setSize((30, 30))

        # Set the source of the image to the new scale
        #  This is irreversable and replaces the image
        #  in memory with the scaled down version we made.
        Bullet.img.permeate()

        self.mouseCursor = Cursor()
        self.addSprite(self.mouseCursor)

        self.addBulletWait = 0
        self.addBulletDelay = 50.0e-3 # in seconds

        # track the total number of sprites on the screen
        # in the game console to make sure they are
        # destroying properly
        self.game.console.addTracker("len(app.sprites)")

    def update(self, dt):
        # dt stands for delta time
        # it represetns the milliseconds between this frame and the last one
        # use it for all changes you do over time or else
        # time dependent dynamics will change per computer based on
        # performance.
        
        self.addBulletWait -= dt
        if self.addBulletWait <= 0.0:
            self.addBulletWait = self.addBulletDelay
            self.addBullet()

    def addBullet(self):
        # "bullets" means to add the bullet on the "bullet" layer we created earlier.
        newBullet = Bullet()
        self.addSprite(newBullet, "bullets")
        self.bulletBatch.addSprite(newBullet)

if __name__ == "__main__":
    arche.debug.test(main)
