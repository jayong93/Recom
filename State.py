__author__ = 'Administrator'

from pico2d import *

class StateBase():
    def __init__(self, owner):
        self.owner = owner

    def Draw(self):
        clear_canvas()
        owner = self.owner
        anim = owner.animationList[owner.currentAnimation]
        anim.animImage.clip_draw(int(owner.frame/6) * anim.w, 0, anim.w, anim.h, owner.x, owner.y)
        update_canvas()

    def Update(self):
        owner = self.owner
        anim = owner.animationList[owner.currentAnimation]
        owner.frame = (owner.frame + 1) % (anim.frame * 6)

    def Enter(self):
        pass

    def Exit(self):
        pass
