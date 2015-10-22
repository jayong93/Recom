__author__ = 'Administrator'

from Player import *


class Duck1(Character):
    MOVE, DEATH = 0, 1
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if self.animationList is None:
            self.animationList = {self.MOVE: Animation('resource/spr_duck_walk.png', 13, 114, 94),
                                  self.DEATH: Animation('resource/spr_duck_death.png', 12, 114, 94)}

        if self.stateList is None:
            self.stateList = {self.MOVE: DuckMoveState(),
                              self.DEATH: DuckDeathState()}

        self.colBoxX = 37
        self.colBoxY = 89
        self.colBoxW = 45
        self.colBoxH = 55

        self.flag = 0
        self.dir = 1
        self.target = None
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.currentAnimation]
        cbx = self.x - anim.w / 2 + self.colBoxX
        cby = self.y - anim.h / 2 + self.colBoxY
        return Rect(cbx, cby, self.colBoxW, self.colBoxH)

    def SetTarget(self, t):
        self.target = t
        return


class Duck2(Character):
    MOVE,DEATH = 0, 1
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if self.animationList is None:
            self.animationList = {self.MOVE: Animation('resource/spr_duck2_walk.png', 6, 114, 94),
                                  self.DEATH: Animation('resource/spr_duck2_death.png', 12, 114, 94)}

        if self.stateList is None:
            self.stateList = {self.MOVE: DuckMoveState(),
                              self.DEATH: DuckDeathState()}

        self.colBoxX = 37
        self.colBoxY = 89
        self.colBoxW = 45
        self.colBoxH = 55

        self.flag = 0
        self.dir = 1
        self.target = None
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.currentAnimation]
        cbx = self.x - anim.w / 2 + self.colBoxX
        cby = self.y - anim.h / 2 + self.colBoxY
        return Rect(cbx, cby, self.colBoxW, self.colBoxH)

    def SetTarget(self, t):
        self.target = t
        return


class DuckMoveState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.MOVE
        owner.flag = 0

    def Update(self, owner):
        super(DuckMoveState, self).Update(owner)

        if math.fabs(owner.target.x - owner.x) < 1:
            owner.x = owner.target.x
        elif owner.target.x > owner.x:
            owner.x += 1
        else:
            owner.x -= 1

    def Collision(self, owner, other):
        if type(other) is Player and type(other.state) is PlayerMeleeState and other.x < owner.x and int(other.frame / 6) > 3:
            owner.ChangeState(owner.DEATH)


class DuckDeathState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.DEATH
        owner.flag = 0

    def Update(self, owner):
        super(DuckDeathState, self).Update(owner)

        if int(owner.frame / 6) >= 11:
            owner.isDelete = True
