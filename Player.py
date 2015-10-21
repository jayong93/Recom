__author__ = 'Administrator'

from Character import *
from State import *
import InputManager


class Player(Character):
    IDLE, MOVE, MELEE = 0, 1, 2
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if Player.animationList is None:
            Player.animationList = {Player.IDLE: Animation('resource/spr_jimmy_idle.png', 12, 114, 94),
                                  Player.MOVE: Animation('resource/spr_jimmy_sprint.png', 6, 114, 94),
                                  Player.MELEE: Animation('resource/spr_jimmy_melee.png', 7, 114, 94)}

        if Player.stateList is None:
            Player.stateList = {Player.IDLE: PlayerIdleState(),
                                Player.MOVE: PlayerMoveState(),
                                Player.MELEE: PlayerMeleeState()}

        self.colBoxX = 36
        self.colBoxY = 87
        self.colBoxW = 40
        self.colBoxH = 60
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.currentAnimation]
        cbx = self.x - anim.w / 2 + self.colBoxX
        cby = self.y - anim.h / 2 + self.colBoxY
        return Rect(cbx, cby, self.colBoxW, self.colBoxH)


class PlayerIdleState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.IDLE

    def Update(self, owner):
        super(PlayerIdleState, self).Update(owner)

        if InputManager.GetKeyState(SDLK_a) or InputManager.GetKeyState(SDLK_d):
            owner.ChangeState(Player.MOVE)
        elif InputManager.GetKeyState(SDLK_SPACE):
            owner.ChangeState(Player.MELEE)


class PlayerMoveState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.MOVE

    def Update(self, owner):
        super(PlayerMoveState, self).Update(owner)

        if InputManager.GetKeyState(SDLK_d):
            owner.x += 2
        if InputManager.GetKeyState(SDLK_a):
            owner.x -= 2
        if InputManager.GetKeyState(SDLK_SPACE):
            owner.ChangeState(Player.MELEE)
        elif not InputManager.GetKeyState(SDLK_d) and not InputManager.GetKeyState(SDLK_a):
            owner.ChangeState(Player.IDLE)


class PlayerMeleeState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = owner.MELEE

    def Update(self, owner):
        anim = owner.animationList[owner.currentAnimation]
        owner.frame = owner.frame + 1

        if owner.frame >= anim.frame * 6:
            owner.ChangeState(Player.IDLE)
