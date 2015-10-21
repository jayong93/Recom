__author__ = 'Administrator'

from Character import *
from State import *
import InputManager


class Player(Character):
    ANIM_IDLE, ANIM_MOVE, ANIM_MELEE = 0, 1, 2

    def __init__(self):
        super().__init__()
        self.animationList[Player.ANIM_IDLE] = Animation('resource/spr_jimmy_idle.png', 12, 114, 94)
        self.animationList[Player.ANIM_MOVE] = Animation('resource/spr_jimmy_sprint.png', 6, 114, 94)
        self.animationList[Player.ANIM_MELEE] = Animation('resource/spr_jimmy_melee.png', 7, 114, 94)
        self.currentAnimation = None
        self.state = None
        return


class PlayerIdleState(StateBase):
    def __init__(self, owner):
        super().__init__(owner)

    def Enter(self):
        self.owner.frame = 0
        self.owner.currentAnimation = self.owner.ANIM_IDLE

    def Update(self):
        super(PlayerIdleState, self).Update()

        if InputManager.GetKeyState(SDLK_a) or InputManager.GetKeyState(SDLK_d):
            self.owner.ChangeState(PlayerMoveState)
        elif InputManager.GetKeyState(SDLK_SPACE):
            self.owner.ChangeState(PlayerMeleeState)


class PlayerMoveState(StateBase):
    def __init__(self, owner):
        super().__init__(owner)

    def Enter(self):
        self.owner.frame = 0
        self.owner.currentAnimation = self.owner.ANIM_MOVE

    def Update(self):
        super(PlayerMoveState, self).Update()

        if InputManager.GetKeyState(SDLK_d):
            self.owner.x += 2
        if InputManager.GetKeyState(SDLK_a):
            self.owner.x -= 2
        if InputManager.GetKeyState(SDLK_SPACE):
            self.owner.ChangeState(PlayerMeleeState)
        elif not InputManager.GetKeyState(SDLK_d) and not InputManager.GetKeyState(SDLK_a):
            self.owner.ChangeState(PlayerIdleState)


class PlayerMeleeState(StateBase):
    def __init__(self, owner):
        super().__init__(owner)

    def Enter(self):
        self.owner.frame = 0
        self.owner.currentAnimation = self.owner.ANIM_MELEE

    def Update(self):
        owner = self.owner
        anim = owner.animationList[owner.currentAnimation]
        owner.frame = owner.frame + 1

        if owner.frame >= anim.frame * 6:
            owner.ChangeState(PlayerIdleState)
