#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 005")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                             titleName = "ArcheEngine Demo - Motion",)
    MotionDemo().start()
    
    game.run()

class MotionDemo(arche.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (0,0,0)

        self.quitButton = arche.interface.SolidButton(
            width = 50, height = 30,
            colorReset = (100,100,100),
            colorHover = (255,50,50),
            colorPress = (255,150,150),
            command = self.game.quit,
            textObject = arche.Text(
                value = "X",
                x = 0, y = 0,
                color = (255,255,255),
                size = 30,
                font = "font/consola.ttf"),
            )
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1
        self.quitButton.name = "quit button"
        self.addSprite(self.quitButton)

        self.fadingText = arche.Text("Hello World!",
                                          x = self.game.xprop(.50),
                                          y = self.game.yprop(.20),
                                          color = (255,255,255),
                                          size = 30,
                                          font = "font/consola.ttf")

        # Hide the sprite from the view of the application
        #  it will continue to update in the background process
        self.fadingText.hide()

        self.fadingText.name = "fading text"
        self.addSprite(self.fadingText)

        self.appearButton = arche.interface.SolidButton(
            width = self.game.xprop(.30),
            height= self.game.yprop(.30),
            x = self.game.xprop(.30),
            y = self.game.yprop(.70),
            colorReset = (0,180,0),
            colorHover = (0,255,0),
            colorPress = (150,255,150),
            colorDisabled = (120,120,120),
            command = self.textAppear,
            textObject = arche.Text(
                value = "Appear",
                x = 0, y = 0,
                color = (255,255,255),
                size = self.game.xprop(.04),
                font = "font/consola.ttf"),
            )
        self.appearButton.name = "appear button"
        self.addSprite(self.appearButton)
        
        self.disappearButton = arche.interface.SolidButton(
            width = self.game.xprop(.30),
            height= self.game.yprop(.30),
            x = self.game.xprop(.70),
            y = self.game.yprop(.70),
            colorReset = (180,0,0),
            colorHover = (255,0,0),
            colorPress = (255,150,150),
            colorDisabled = (120,120,120),
            command = self.textDisappear,
            textObject = arche.Text(
                value = "Disappear",
                x = 0, y = 0,
                color = (255,255,255),
                size = self.game.xprop(.04),
                font = "font/consola.ttf"),
            )
        
        self.disappearButton.disable() # grey it out and make it useless

        self.disappearButton.name = "disappear button"
        self.addSprite(self.disappearButton)

    def textAppear(self):
        # Trigger a motion fade in command on press of the 'appear' button.
        # This motion class will unhide the text and fade it in to view.
        # Make note that the motion class will except any sprite and the
        #  text object is a child of the Sprite object.

        # note that alpha is used.  alpha is just a term to refer to
        # opacity of a sprite
        #  0 being completely invisible, and 255 being completely solid.
        
        arche.motion.actin.Fade(sprite = self.fadingText,
                                
                                time = 1.000,     # seconds it takes to fade in
                                alpha = 255)    # fade to complete opacity

        self.appearButton.disable()
        self.disappearButton.enable()
        
    def textDisappear(self):
        # simply use a motion class to make the text disappear
        arche.motion.actout.Disappear(self.fadingText)

        self.disappearButton.disable()
        self.appearButton.enable()
        

if __name__ == "__main__":
    arche.debug.test(main)
