
class Action(object):
    def __init__(self, sprite):
        self.loop = 1
        self.canceled = False
        self.sprite = sprite
        sprite.addMotion(self)
        
    def begin(self):
        pass
    
    def update(self, dt):
        pass
    
    def finish(self):
        self.loop -= 1
        if self.loop:
            self.begin()
        else:
            self.sprite.removeMotion(self)

    def cancel(self):
        self.canceled = True
