from pygame.locals import *

import logging

log = logging.getLogger("R.Event")

class Handler(object):
    def __init__(self, command=None):
        if command:
            self.run = command
            self._commands = [command]

    def run(self, event, engine):
        pass

class KeyHandler(Handler):
    def __init__(self):
        super().__init__()

        self.commands = {}

    def addCommand(self, key, command, args=[]):
        if key in self.commands:
            if command in self.commands[key]:
                pass # already added this command
            else:
                self.commands[key].append((command, args))
        else:
            self.commands[key] = [(command, args)]

    def getCommands(self, key):
        if key in self.commands:
            return self.commands[key]
        else:
            return []

    def run(self, event, game):
        if event.type == KEYDOWN:
            if event.key in self.commands:
                for commandargs in self.commands[event.key]:
                    commandargs[0](*commandargs[1])

class GameEngineHandler(Handler):
    def __init__(self):
        super().__init__()
        log.debug("game engine handler initialized")
        
    def run(self, event, game):
        if event.type == QUIT:
            game.quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                game.postEvent(QUIT)
            elif event.key == K_BACKQUOTE:
                game.gameConsole.toggleHidden()
            elif event.key == K_RETURN:
                if not engine.gameConsole.hidden:
                    game.gameConsole.executeEntry()
            elif event.key == K_BACKSPACE:
                if not game.gameConsole.hidden:
                    game.gameConsole.entryBackspace()
            else:
                if not game.gameConsole.hidden:
                    game.gameConsole.entryAdd(event.unicode)
        elif event.type == MOUSEBUTTONDOWN:
            if not game.gameConsole.hidden:
                if event.button == 2:
                    game.gameConsole.pickSprite()
                elif event.button == 4:
                    game.gameConsole.scrollUp()
                elif event.button == 5:
                    game.gameConsole.scrollDown()
        elif event.type == KEYUP:
            if event.key == K_BACKSPACE:
                game.gameConsole.backspaceHoldingReset()
