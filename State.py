__author__ = 'Administrator'

import Camera

class StateBase:
    def Draw(self, owner):
        x, y = Camera.GetCameraPos(owner.x, owner.y)
        anim = owner.animationList[owner.currentAnimation]
        anim.animImage.clip_draw(int(owner.frame/6) * anim.w, 0, anim.w, anim.h, x, y)

    def Update(self, owner):
        anim = owner.animationList[owner.currentAnimation]
        owner.frame = (owner.frame + 1) % (anim.frame * 6)

    def Enter(self, owner):
        pass

    def Exit(self, owner):
        pass

    def Collision(self, owner, other):
        pass