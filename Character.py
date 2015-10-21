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
        self.animationList = {}
        self.currentAnimation = 0
        self.frame = 0
        self.state = None
        return

    def ChangeState(self, newState):
        if self.state is not None:
            self.state.Exit()
        self.state = newState(self)
        self.state.Enter()
