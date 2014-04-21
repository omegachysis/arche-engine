#!/usr/bin/env python3

from arche import debug
from arche import engine
from arche import sprite
from arche import interface
from arche import motion

log = debug.log("main")

def main():
    log.info("starting main")

    game = engine.Game(1024, 768, False)
    StartScreen().start()
    game.run()

class NextScreen(engine.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (100,0,0)

class StartScreen(engine.Application):
    def __init__(self):
        super().__init__()
        
        self.backgroundColor = (0,0,0)

##        self.testSprite = sprite.Sprite("image/test.png", 100, 100)
##        self.testSprite.width = 200
##        self.testSprite.color = (255,100,100)
##        self.testSprite.alpha = 100
##        self.addSprite(self.testSprite)

        self.quitButton = interface.SolidButton(
            width = 50, height = 30,
            colorReset = (100,100,100),
            colorHover = (255,50,50),
            colorPress = (255,150,150),
            command = self.game.quit,
            textObject = sprite.Text(
                "X", 0, 0, (255,255,255), 30, "font/consola.ttf"),
            )
        self.quitButton.right = self.game.width + 1
        self.quitButton.top = -1
        self.addSprite(self.quitButton)

        self.beginButton = interface.SolidButton(
            width = self.game.xprop(.50),
            height= self.game.yprop(.50),
            colorReset = (255,0,150),
            colorHover = (255,50,200),
            colorPress = (255,150,255),
            command = self.nextScreen,
            textObject = sprite.Text(
                "Begin", 0, 0, (255,255,255), self.game.xprop(.08), "font/consola.ttf"),
            )
        self.beginButton.x = self.game.xprop(.50)
        self.beginButton.y = self.game.yprop(.50)
        self.addSprite(self.beginButton)

        self.testText = sprite.Text("Hello World!",
                                    x = self.game.xprop(.20),
                                    y = self.game.yprop(.20),
                                    color = (255,255,255),
                                    size = 20,
                                    font = "font/consola.ttf")
        self.addSprite(self.testText)

        self.testText.alpha = 120
        self.beginButton.alpha = 100

        #motion.actin.Fade(self.beginButton, 4.0, 255)
        
    def nextScreen(self):
        nextApp = NextScreen()
        nextApp.quitButton = self.quitButton
        nextApp.addSprite(self.quitButton)
        nextApp.start()

if __name__ == "__main__":
    debug.test(main)
