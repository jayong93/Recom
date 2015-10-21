__author__ = 'Administrator'

from Character import *
from State import *
from Player import *


class Duck1(Character):
    MOVE = 0
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if self.animationList is None:
            self.animationList = {self.MOVE: Animation('resource/spr_duck_walk.png', 13, 114, 94)}

        if self.stateList is None:
            self.stateList = {self.MOVE: Duck1MoveState()}

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


#
# class PlayerIdleState(StateBase):
#     def Enter(self, owner):
#         owner.frame = 0
#         owner.currentAnimation = owner.IDLE
#
#     def Update(self, owner):
#         super(PlayerIdleState, self).Update(owner)
#
#         if InputManager.GetKeyState(SDLK_a) or InputManager.GetKeyState(SDLK_d):
#             owner.ChangeState(Player.MOVE)
#         elif InputManager.GetKeyState(SDLK_SPACE):
#             owner.ChangeState(Player.MELEE)
#

class Duck1MoveState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.MOVE
        owner.flag = 0

    def Update(self, owner):
        super(Duck1MoveState, self).Update(owner)

        if math.fabs(owner.target.x - owner.x) < 1:
            owner.x = owner.target.x
        elif owner.target.x > owner.x:
            owner.x += 1
        else:
            owner.x -= 1


            # if InputManager.GetKeyState(SDLK_d):
            #     owner.x += 2
            # if InputManager.GetKeyState(SDLK_a):
            #     owner.x -= 2
            # if InputManager.GetKeyState(SDLK_SPACE):
            #     owner.ChangeState(owner.MELEE)
            # elif not InputManager.GetKeyState(SDLK_d) and not InputManager.GetKeyState(SDLK_a):
            #     owner.ChangeState(owner.IDLE)

    def Collision(self, owner, other):
        if type(other) is Player and type(other.state) is PlayerMeleeState and other.x < owner.x and int(other.frame / 6) > 3:
            owner.isDelete = True

#
# class PlayerMeleeState(StateBase):
#     def Enter(self, owner):
#         owner.frame = 0
#         owner.currentAnimation = owner.MELEE
#
#     def Update(self, owner):
#         anim = owner.animationList[owner.currentAnimation]
#         owner.frame = owner.frame + 1
#
#         if owner.frame >= anim.frame * 6:
#             owner.ChangeState(Player.IDLE)
