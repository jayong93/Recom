from pico2d import *
from Collision import *
import Camera


class GameObject:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.isDelete = False

    def Move(self, x, y):
        self.x += x
        self.y += y

    def Draw(self, frame_time):
        pass

    def Update(self, frame_time):
        pass

    def Collision(self, other):
        pass

    def ChangeState(self, state):
        pass


class Animation:
    def __init__(self, img, repeat, frame, w, h, time):
        self.image = load_image(img)
        self.frame = frame
        self.w, self.h = w, h
        self.time = time
        self.repeat = repeat


class Character(GameObject):
    def __init__(self):
        super().__init__()
        self.frame = 0.0
        self.state = None
        self.colBox = None
        self.vx, self.vy = 0.0, 0.0
        self.anim = None

    def ChangeState(self, state):
        self.state = state
        self.frame = 0.0
        if self.animationList is not None:
            self.anim = self.animationList[self.state]


class AnimationObject(GameObject):
    def __init__(self):
        super().__init__()
        self.anim = None
        self.colBox = None
        self.frame = 0

    def GetCollisionBox(self):
        anim = self.anim
        x, y = self.x - anim.w / 2, self.y - anim.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        anim = self.anim
        anim.image.clip_draw(int(self.frame) % anim.frame * anim.w, 0, anim.w, anim.h, x, y)
        pass

    def Update(self, frame_time):
        self.frame += self.anim.frame * (1 / self.anim.time) * frame_time
        if self.frame > self.anim.frame:
            self.frame -= self.anim.frame
        pass


class Teleporter(AnimationObject):
    data = None

    def __init__(self, x=0, y=0):
        super().__init__()

        anim = self.data['animation']
        self.anim = Animation(anim[0], anim[1], anim[2], anim[3], anim[4], anim[5])
        self.colBox = CollisionBox(self.data['cx'], self.data['cx'] + self.data['cw'],
                                   self.data['cy'], self.data['cy'] + self.data['ch'])

        self.x, self.y = x, y

    def Draw(self, frame_time):
        super().Draw(frame_time)

        anim = self.anim
        x, y = Camera.GetCameraPos(self.x, self.y)
        x, y = x - anim.w / 2, y - anim.h / 2
        draw_rectangle(self.colBox.left + x, self.colBox.bottom + y, self.colBox.right + x, self.colBox.top + y)

    def Collision(self, other):
        pass
