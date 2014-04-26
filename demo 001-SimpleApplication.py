#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

log.info("starting demo")

game = arche.engine.Game(width = 1280, height = 800, fullscreen = False)
game.run()
