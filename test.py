#!/usr/bin/env python3

from arche import debug
from arche import engine

log = debug.log("main")

def main():
    log.info("starting main")

    game = engine.Game(1024, 768, False)
    game.startApp(BlankScreen())
    game.run()

class BlankScreen(engine.Application):
    def __init__(self):
        super(BlankScreen, self).__init__()
        
        self.backgroundColor = (122,122,122)

if __name__ == "__main__":
    debug.test(main)
