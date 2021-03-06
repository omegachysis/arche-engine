#!/usr/bin/env python3

import arche
import random

log = arche.debug.log("main")

def main():
    log.info("starting demo 011")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Motion Demonstration",)

    Demo().start()
    
    game.run()

class Demo(arche.engine.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (80,80,80)

        self.text = arche.Text(value = "Hello World!", x = self.game.xprop(.5), y = self.game.yprop(.5),
                               color = (255,255,255), size = 50, font = None)
        self.addSprite(self.text)

        self.entrybox = arche.interface.Entry(
            surface = arche.draw.Rectangle(width = 200, height = 50, color = (20,20,20)),
            x = self.game.xprop(.5),
            y = self.game.yprop(.7),
            textObject = arche.Text(value = "Hello kitty!", x = 0, y = 0, 
                        color = (255,255,255), size = 20,),
            padding = 20,
            maxBuffer = 100,
            restricted = []
            )
        self.addSprite(self.entrybox)

    def update(self, dt):
        pass

if __name__ == "__main__":
    arche.debug.test(main)
