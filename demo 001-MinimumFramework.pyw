#!/usr/bin/env python3

import arche

# Create a logging object for this file
log = arche.debug.log("main")

def main():
    # Log the successful loading of this file
    log.info("starting demo 001")
    
    # Start a default game engine
    game = arche.Game(width = 1280, height = 800, fullscreen = False,
                    titleName = "ArcheEngine Demo - Minimum Framework")
    game.run()

if __name__ == "__main__":
    
    # Do this to handle the final error checking
    arche.debug.test(main)
