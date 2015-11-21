from Object import *



class Animation:
    def __init__(self, img, frame, w, h, time):
        self.image = load_image(img)
        self.frame = frame
        self.w, self.h = w, h
        self.time = time


class Character(GameObject):
    def __init__(self):
        super().__init__()
        self.frame = 0.0
        self.state = None
        self.isDelete = False
        self.colBox = None
        self.vx, self.vy = 0.0, 0.0
