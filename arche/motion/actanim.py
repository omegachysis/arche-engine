
from arche.motion.action import Action

import logging

log = logging.getLogger("R.Engine.Motion")

class ChangeColor(Action):
    name = "anim.changecolor"
    def __init__(self, sprite, time):
        self.time = time
        self.b = sprite.color
        super(ChangeColor, self).__init__(sprite)

    def begin(self):
        self.sprite.unhide()

    def update(self, dt):
        self.sprite.hide()
        self.finish()    
