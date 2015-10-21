__author__ = 'Administrator'

class StateBase:
    def Draw(self, owner):
        anim = owner.animationList[owner.currentAnimation]
        anim.animImage.clip_draw(int(owner.frame/6) * anim.w, 0, anim.w, anim.h, owner.x, owner.y)

    def Update(self, owner):
        anim = owner.animationList[owner.currentAnimation]
        owner.frame = (owner.frame + 1) % (anim.frame * 6)

    def Enter(self, owner):
        pass

    def Exit(self, owner):
        pass

    def Collision(self, other):
        pass