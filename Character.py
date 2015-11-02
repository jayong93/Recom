from Object import *


class Animation:
    def __init__(self, img, frame, w, h):
        self.animImage = load_image(img)
        self.frame = frame
        self.w, self.h = w, h


class Character(GameObject):
    def __init__(self):
        super().__init__()
        self.currentAnimation = None
        self.frame = None
        self.state = None
        self.isDelete = False
        self.colBoxW = 0
        self.colBoxH = 0
        self.colBoxX = 0
        self.colBoxY = 0
        return

    def ChangeState(self, newState):
        if self.state is not None:
            self.state.Exit(self)
        self.state = self.stateList[newState]
        self.state.Enter(self)

    def Update(self):
        if self.state is not None:
            self.state.Update(self)

    def Draw(self):
        if self.state is not None:
            self.state.Draw(self)

    def Collision(self, other):
        if self.state is not None:
            self.state.Collision(self, other)


class Rect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def CollisionCheck(self, other):
        if (other.x < self.x):
            other.x, self.x = self.x, other.x
        if (other.x + other.w - self.x < other.w + self.w) and (other.y + other.h - self.y < other.h + self.h):
            return True
        return False
