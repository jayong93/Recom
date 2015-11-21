from Character import *
from Collision import *
import Camera
import InputManager

playerData = None


class Player:
    PPM = 1 / 0.015
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
                'IDLE': self.IdleUpdate(),
                'MOVE': self.MoveUpdate(),
                'MELEE': self.MeleeUpdate()
            }

        self.colBox = CollisionBox(playerData['cx'], playerData['cy'],
                                   playerData['cx'] + playerData['cw'], playerData['cy'] + playerData['ch'])

        self.currentAnimation = playerData['currentState']
        self.state = Player.stateList[playerData['currentState']]
        self.isJump = False
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.currentAnimation]
        return self.colBox.Move(self.x - anim.w/2,self.y - anim.h/2)

    def IdleUpdate(self):
        pass

    def MoveUpdate(self):
        pass

    def MeleeUpdate(self):
        pass

    def Draw(self, frame_time):
        pass

    def Update(self, frame_time):
        pass
