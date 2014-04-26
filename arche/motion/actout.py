
from arche.motion.action import Action

import logging

log = logging.getLogger("R.Engine.Motion")

class Disappear(Action):
    name = "out.appear"
    def __init__(self, sprite):
        super(Disappear, self).__init__(sprite)

    def begin(self):
        pass

    def update(self, dt):
        self.sprite.alpha = 0
        self.sprite.hide()
        self.finish()    
