#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 003")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                         titleName = "ArcheEngine Demo - Interface Example",
                         frame = False, # don't show the os window stuff
                         )

    InterfaceExample().start()
    
    game.run()

# Applications are used to organize various parts of your game.
# They are analogous to PowerPoint slides or separate slides
#  in a slide show.
class InterfaceExample(arche.Application):
    def __init__(self):
        super().__init__() # run this at the beginning of every class derivation

        self.backgroundColor = (50,0,0)

        # Create an 'x' button in the corner of the screen
        self.quitButton = arche.interface.SolidButton(
            
            # all widths and heights are in pixels
            width = 50, height = 30,
            
            # the reset color is the default color of the unselected button
            colorReset = (100,100,100),

            # the hover color is the color of the button when hilighting
            colorHover = (255,50,50),

            # the press color is the color when clicking the button
            colorPress = (255,150,150),

            # all applications inherit the 'game' attribute
            command = self.game.quit,

            # create a caption
            textObject = arche.Text(
                value = "X",
                
                # x and y values are parented attributes relative to the button center
                x = 0, y = 0,
                
                color = (255,255,255),
                size = 30,
                font = "font/consola.ttf"),
            )

        # You can move sprites as much as you want after you create them.
        # You can set and get coordinates by 'left', 'right', 'top', 'bottom',
        #   'x', 'y', and 'rect' values.
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1

        # You never have to name sprites like this, but it's a good idea
        self.quitButton.name = "quit button"

        # you must add sprites to the applications
        # with the 'addSprite' command before they appear!
        self.addSprite(self.quitButton)

        # Create a greeting text sprite
        self.greetingText = arche.Text(
            value = "Hello World!  Press the X button in the upper right corner " + \
            "of the screen to quit.",

            # the 'game.-prop' commands allow you to control coordinates based on
            # the resolution or screen size that the client has chosen to allow.
            # .50 means that it is centered on the screen proportional to that metric.
            x = self.game.xprop(.50),
            y = self.game.yprop(.50),
            
            color = (255,255,255),
            size = 20,
            font = "font/consola.ttf",
            )
        
        self.addSprite(self.greetingText)

if __name__ == "__main__":
    arche.debug.test(main)
