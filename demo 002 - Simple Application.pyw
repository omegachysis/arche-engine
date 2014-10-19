#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 002")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Simple Application")

    # Start our simple application.  It will not run until game.run() is called though.
    SimpleApplication().start()
    
    game.run()

# Applications are used to organize various parts of your game.
# They are analogous to PowerPoint slides or separate slides
#  in a slide show.
class SimpleApplication(arche.Application):
    def __init__(self):
        super(SimpleApplication, self).__init__() # run this at the beginning of every class derivation

        # Change the background color to dark grey
        self.backgroundColor = (255,80,80)

        # Create a little test sprite
        self.testSprite = arche.Sprite("image/test.png", 100, 100, False)
        self.addSprite(self.testSprite)

if __name__ == "__main__":
    arche.debug.test(main)
