
from Arche.Motion.Action import Action

import logging

log = logging.getLogger("R.Engine.Motion")

class Disappear(Action):
    name = "out.appear"
    def __init__(self, sprite):
        super(Disappear, self).__init__(sprite)

    def begin(self):
        self.sprite.unhide()

    def update(self, dt):
        self.sprite.hide()
        self.finish()    
