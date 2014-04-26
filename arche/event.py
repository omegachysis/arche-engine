from pygame.locals import *

class Handler(object):
    def __init__(self, command=None):
        self.run = command
        self._commands = [command]

    def run(self, event, engine):
        pass

class GameEngineHandler(Handler):
    def __init__(self): pass
    def run(self, event, engine):
        if event.type == QUIT:
            engine.quit()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                engine.postEvent(QUIT)
            elif event.key == K_BACKQUOTE:
                engine.gameConsole.toggleHidden()
            elif event.key == K_RETURN:
                if not engine.gameConsole.hidden:
                    engine.gameConsole.executeEntry()
            elif event.key == K_BACKSPACE:
                if not engine.gameConsole.hidden:
                    engine.gameConsole.entryBackspace()
            else:
                if not engine.gameConsole.hidden:
                    engine.gameConsole.entryAdd(event.unicode)
        elif event.type == MOUSEBUTTONDOWN:
            if not engine.gameConsole.hidden:
                if event.button == 4:
                    engine.gameConsole.scrollUp()
                elif event.button == 5:
                    engine.gameConsole.scrollDown()
        elif event.type == KEYUP:
            if event.key == K_BACKSPACE:
                engine.gameConsole.backspaceHoldingReset()
