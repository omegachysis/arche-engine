#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 012")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                      titleName = "ArcheEngine Demo - Parent Children")

    Demo().start()

    game.run()

class Demo(arche.engine.Application):
    def __init__(self):
        super(Demo, self).__init__()
