
import logging
log = logging.getLogger("R.Collision")

class Batch(object):
    game = None
    def __init__(self, sprites=[]):
        self.sprites = sprites
        self._process()
    def _process(self):
        self.rects = []
        for sprite in self.sprites:
            self.rects.append(sprite.rect)
            
    def addSprite(self, sprite):
        self.sprites.append(sprite)
        self.rects.append(sprite.rect)
        sprite.batches.append(self)
    def removeSprite(self, sprite):
        if sprite in self.sprites:
            self.sprites.remove(sprite)
            self.rects.remove(sprite.rect)
            if self in sprite.batches:
                sprite.batches.remove(self)
            
    def refresh(self):
        for sprite in self.sprites:
            if sprite._destroyed:
                self.removeSprite(sprite)
                
    def getCollisions(self, sprite):
        indices = sprite.rect.collidelistall(self.rects)
        sprites = []
        for index in indices:
            sprites.append(self.sprites[index])
        return sprites