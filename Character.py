__author__ = 'Administrator'

from Object import *


class Animation():
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
