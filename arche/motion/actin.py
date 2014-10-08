
from arche.motion.action import Action

import logging

log = logging.getLogger("R.Engine.Motion")

class Appear(Action):
    name = "in.appear"
    def __init__(self, sprite):
        super(Appear, self).__init__(sprite)

    def begin(self):
        self.sprite.hide()
        
    def update(self, dt):
        self.sprite.unhide()
        self.finish()

class Fade(Action):
    name = "in.fade"
    def __init__(self, sprite, time, alpha):
        self.time = time
        self.alpha = alpha
        self.m = float(alpha)/float(time)

        super(Fade, self).__init__(sprite)

    def begin(self):
        self.t = 0.0
        self.sprite.alpha = 0.0
        self.sprite.unhide()
        
    def update(self, dt):
        self.t += dt
        if self.t >= self.time:
            self.sprite.alpha = self.alpha
            self.finish()
        else:
            self.sprite.alpha = self.m * self.t

    def cancel(self):
        self.sprite.alpha = self.alpha
        super(Fade, self).cancel()
