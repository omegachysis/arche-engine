#!/usr/bin/env python3

from arche import debug
from arche import engine
from arche import sprite
from arche import interface

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
        
    def nextScreen(self):
        nextApp = NextScreen()
        nextApp.quitButton = self.quitButton
        nextApp.addSprite(self.quitButton)
        nextApp.start()

if __name__ == "__main__":
    debug.test(main)
