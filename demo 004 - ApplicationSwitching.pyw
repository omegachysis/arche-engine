#!/usr/bin/env python3

import arche

log = arche.debug.log("main")

def main():
    log.info("starting demo 004")

    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                titleName = "ArcheEngine Demo - Application Switching",)

    StartScreen().start()
    
    game.run()

class StartScreen(arche.Application):
    def __init__(self):
        super().__init__()

        self.backgroundColor = (50,0,0)

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

        self.nextButton = arche.interface.SolidButton(
            width = self.game.xprop(.50),
            height= self.game.yprop(.50),
            colorReset = (255,0,150),
            colorHover = (255,50,200),
            colorPress = (255,150,255),
            command = self.nextScreen, # refer to an internal command
            textObject = arche.Text(
                "Next", 0, 0, (255,255,255), self.game.xprop(.08), "font/consola.ttf"),
            )
        self.nextButton.x = self.game.xprop(.50)
        self.nextButton.y = self.game.yprop(.50)
        self.nextButton.name = "next button"
        self.addSprite(self.nextButton)

        # Set up the next application but
        # pass the quit button to allow it to persist.
        # remember that when you switch applications,
        # all the sprites from the last application
        # disappear from the screen because sprites
        # only belong to one application.
        self.nextApp = NextScreen(self, self.quitButton)

    def nextScreen(self):
        #Switch to the next application
        self.nextApp.start()

class NextScreen(arche.Application):
    def __init__(self, firstApp, quitButton):
        super().__init__()

        self.backgroundColor = (0,120,200) # Clearly a different background color

        self.quitButton = quitButton
        self.addSprite(quitButton)

        self.prevButton = arche.interface.SolidButton(
            width = self.game.xprop(.50),
            height= self.game.yprop(.50),
            colorReset = (0,255,150),
            colorHover = (50,255,200),
            colorPress = (150,255,255),
            command = self.prevScreen,
            textObject = arche.Text(
                "Previous", 0, 0, (255,255,255), self.game.xprop(.08), "font/consola.ttf"),
            )
        self.prevButton.x = self.game.xprop(.50)
        self.prevButton.y = self.game.yprop(.50)
        self.prevButton.name = "previous button"
        self.addSprite(self.prevButton)

        self.firstApp = firstApp

        # don't initialize another application this time because
        # you must be sure to call an initalizer on each application
        # only once!

    def prevScreen(self):
        # Go back to the first application
        self.firstApp.start()

if __name__ == "__main__":
    arche.debug.test(main)
