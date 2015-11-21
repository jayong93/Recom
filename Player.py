from Character import *
from Collision import *
import Camera
import InputManager

playerData = None


class Player(Character):
    PPM = None
    MPS = None
    animationList = None
    stateList = None

    def __init__(self):
        super().__init__()
        if self.PPM is None:
            self.PPM = 1 / playerData['mpp']

        if self.MPS is None:
            self.MPS = playerData['mps']

        if Player.animationList is None:
            Player.animationList = {}
            for s in playerData['animation']:
                v = playerData['animation'][s]
                Player.animationList[s] = Animation(v[0], v[1], v[2], v[3], v[4])

        if Player.stateList is None:
            Player.stateList = {
                'IDLE': self.IdleUpdate,
                'MOVE': self.MoveUpdate,
                'MELEE': self.MeleeUpdate
            }

        self.colBox = CollisionBox(playerData['cx'], playerData['cx'] + playerData['cw'],
                                   playerData['cy'], playerData['cy'] + playerData['ch'])

        self.state = playerData['currentState']
        self.isJump = False
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.state]
        cb = self.colBox
        x, y = self.x - anim.w/2, self.y - anim.h/2
        return CollisionBox(x+cb.left, x+cb.right, y+cb.bottom, y+cb.top)

    def IdleUpdate(self, frame_time):
        if InputManager.GetKeyState(SDLK_LEFT) != InputManager.GetKeyState(SDLK_RIGHT):
            self.state = 'MOVE'
            self.frame = 0.0

    def MoveUpdate(self, frame_time):
        self.vx = self.MPS

    def MeleeUpdate(self, frame_time):
        pass

    def Draw(self, frame_time):
        anim = self.animationList[self.state]
        x, y = Camera.GetCameraPos(self.x, self.y)
        anim.image.clip_draw(int(self.frame) % anim.frame * anim.w, 0, anim.w, anim.h, x, y)
        x, y = x - anim.w/2, y - anim.h/2
        draw_rectangle(self.colBox.left+x,self.colBox.bottom+y, self.colBox.right+x, self.colBox.top+y)

    def Update(self, frame_time):
        self.stateList[self.state](frame_time)

        # 애니메이션 프레임 처리
        anim = self.animationList[self.state]
        self.frame += anim.frame * (1 / anim.time) * frame_time
        if self.frame > anim.frame:
            self.frame -= anim.frame

        self.x += self.vx * self.PPM * frame_time
        self.y += self.vy * self.PPM * frame_time

        print("x : %f, y : %f" % (self.x, self.y))


    def HandleEvent(self, event, frame_time):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE and self.vy == 0:
                self.vy = 7
