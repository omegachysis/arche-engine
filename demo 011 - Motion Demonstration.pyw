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

    def update(self, dt):
        pass

if __name__ == "__main__":
    arche.debug.test(main)
