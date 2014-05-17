#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 006")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                    titleName = "ArcheEngine Demo - Mouse Reading",)
    
    game.hideMouse() # Hide the default mouse cursor
    
    MouseReading().start()
    
    game.run()

class MouseReading(arche.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (0,0,0)

        self.cursor = Cursor()
        self.addSprite(self.cursor)

class Cursor(arche.Sprite):
    def __init__(self):
        super().__init__(
            #Create the sprite here.
            surface = "image/test.png",
            x = 0, y = 0)

        self.name = "cursor"

        self.pickable = False # cannot select in the game console view with the middle mouse button

    def update(self, dt): # 'dt' stands for delta time.  We will use it later.
        self.x, self.y = arche.control.getMouse()

if __name__ == "__main__":
    arche.debug.test(main)
