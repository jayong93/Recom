from Object import *
from Collision import *

playerData = None
player = None


class Player(Character):
    PPM = None
    RUN_SPEED = None
    animationList = None
    stateList = None

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x, self.y = x, y

        if self.PPM is None:
            self.PPM = 1 / playerData['mpp']

        if self.RUN_SPEED is None:
            self.RUN_SPEED = playerData['run_speed']

        if Player.animationList is None:
            Player.animationList = {}
            for s in playerData['animation']:
                v = playerData['animation'][s]
                Player.animationList[s] = Animation(v[0], v[1], v[2], v[3], v[4], v[5])

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
        self.gun = None
        return

    def GetCollisionBox(self):
        anim = self.animationList[self.state]
        x, y = self.x - anim.w / 2, self.y - anim.h / 2
        return self.colBox.Move(x, y)

    def IdleUpdate(self, frame_time):
        pass

    def MoveUpdate(self, frame_time):
        self.vx = self.RUN_SPEED

    def MeleeUpdate(self, frame_time):
        self.vx = 0
        if self.frame > self.animationList['MELEE'].frame:
            self.state = 'MOVE'
            self.frame = 0

    def Draw(self, frame_time):
        anim = self.animationList[self.state]
        x, y = Camera.GetCameraPos(self.x, self.y)
        anim.image.clip_draw(int(self.frame) % anim.frame * anim.w, 0, anim.w, anim.h, x, y)
        x, y = x - anim.w / 2, y - anim.h / 2
        draw_rectangle(self.colBox.left + x, self.colBox.bottom + y, self.colBox.right + x, self.colBox.top + y)

    def Update(self, frame_time):
        # 애니메이션 프레임 처리
        anim = self.animationList[self.state]
        if self.frame <= anim.frame:
            self.frame += anim.frame * (1 / anim.time) * frame_time
        elif anim.repeat:
            self.frame -= anim.frame

        self.x += self.vx * self.PPM * frame_time
        self.y += self.vy * self.PPM * frame_time

        self.stateList[self.state](frame_time)

    def HandleEvent(self, event, frame_time):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE and self.vy == 0:
                self.vy = 7
            elif event.key == SDLK_a:
                self.state = 'MELEE'
                self.frame = 0
