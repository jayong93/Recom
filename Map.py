from pico2d import *
from Collision import *
import Camera


class Map:
    def __init__(self, fileName):
        self.image = load_image('resource/' + fileName + '.png')
        self.w = 0
        self.h = 0
        self.colBox = []

    def Draw(self):
        x, y = Camera.GetCameraPos(self.w / 2, self.h / 2)
        self.image.draw(x, y)
        # x, y = x-self.w/2, y-self.h/2
        # for cb in self.colBox:
        #     draw_rectangle(cb.left+x, cb.bottom+y, cb.right+x, cb.top+y)
