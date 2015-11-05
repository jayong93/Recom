from Character import *
from State import *
import Camera
import InputManager

playerData = None


class Player(Character):
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if Player.animationList is None:
            Player.animationList = {}
            for s in playerData['animation']:
                v = playerData['animation'][s]
                Player.animationList[s] = Animation(v[0], v[1], v[2], v[3])

        if Player.stateList is None:
            Player.stateList = {
                'IDLE': PlayerIdleState(),
                'MOVE': PlayerMoveState(),
                'MELEE': PlayerMeleeState()
            }

        self.colBoxX = playerData['cx']
        self.colBoxY = playerData['cy']
        self.colBoxW = playerData['cw']
        self.colBoxH = playerData['ch']

        self.currentAnimation = playerData['currentState']
        self.state = Player.stateList[playerData['currentState']]
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.currentAnimation]
        cbx = self.x - anim.w / 2 + self.colBoxX
        cby = self.y - anim.h / 2 + self.colBoxY
        return Rect(cbx, cby, self.colBoxW, self.colBoxH)


class PlayerIdleState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = 'IDLE'

    def Update(self, owner):
        super(PlayerIdleState, self).Update(owner)

        if not (InputManager.GetKeyState(SDLK_LEFT) and InputManager.GetKeyState(SDLK_RIGHT)):
            if InputManager.GetKeyState(SDLK_LEFT) or InputManager.GetKeyState(SDLK_RIGHT):
                owner.ChangeState('MOVE')
        elif InputManager.GetKeyState(SDLK_SPACE):
            owner.ChangeState('MELEE')


class PlayerMoveState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = 'MOVE'

    def Update(self, owner):
        super(PlayerMoveState, self).Update(owner)

        if InputManager.GetKeyState(SDLK_RIGHT):
            owner.x += 2
            Camera.SetCameraPos(owner.x, Camera.y)
        if InputManager.GetKeyState(SDLK_LEFT):
            owner.x -= 2
            Camera.SetCameraPos(owner.x, Camera.y)
        if InputManager.GetKeyState(SDLK_SPACE):
            owner.ChangeState('MELEE')
        elif InputManager.GetKeyState(SDLK_RIGHT) and InputManager.GetKeyState(SDLK_LEFT):
            owner.ChangeState('IDLE')
        elif not InputManager.GetKeyState(SDLK_RIGHT) and not InputManager.GetKeyState(SDLK_LEFT):
            owner.ChangeState('MOVE')


class PlayerMeleeState(StateBase):
    def Enter(self, owner):
        owner.frame = 0
        owner.currentAnimation = 'MELEE'

    def Update(self, owner):
        anim = owner.animationList[owner.currentAnimation]
        owner.frame += 1

        if owner.frame >= anim.frame * 6:
            owner.ChangeState('IDLE')
