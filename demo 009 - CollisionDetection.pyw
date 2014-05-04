#!/usr/bin/env python3

import arche
import random

log = arche.debug.log("main")

def main():
    log.info("starting demo 009")

    game = arche.engine.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Collision Detection",)

    Demo().start()
    
    game.run()

class Cursor(arche.sprite.Sprite):
    def __init__(self):
        super().__init__(
            surface = "image/test.png",
            x = 0, y = 0)

        self.size = 100, 100

        self.name = "cursor"
        self.pickable = False

    def update(self, dt):
        self.x, self.y = arche.control.getMouse()

        for bullet in self.app.bulletBatch.getCollisions(self):
            bullet.color = (255,50,50)

class Bullet(arche.sprite.Sprite):
    def __init__(self):
        super().__init__(
            surface = Bullet.img, imageInstance=False)
        self.x = self.game.xprop(random.random()-.5)
        self.y = self.game.yprop(random.random()-.5)

        self.color = (50,255,255)

        self.dx = random.random() / 5
        self.dy = random.random() / 5

    def update(self, dt):
        if self.x > self.game.width or self.y > self.game.height:
            self.destroy()

class Demo(arche.engine.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (50,0,0)

        self.addLayer("bullets", 1)

        self.bulletBatch = arche.sprite.Batch()

        Bullet.img = arche.surf.ImageSurface("image/test.png", False)
        Bullet.img.setSize((30, 30))
        Bullet.img.source = Bullet.img.composite

        self.mouseCursor = Cursor()
        self.addSprite(self.mouseCursor)

        self.addBulletWait = 0
        self.addBulletDelay = 50

        self.game.console.addTracker("len(app.sprites)")

    def update(self, dt):
        self.addBulletWait -= dt
        if self.addBulletWait <= 0.0:
            self.addBulletWait = self.addBulletDelay
            self.addBullet()

    def addBullet(self):
        self.bulletBatch.addSprite(self, Bullet(), "bullets")

if __name__ == "__main__":
    arche.debug.test(main)
