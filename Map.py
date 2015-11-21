from pico2d import *
from Collision import *
import Camera


class Map:
    def __init__(self, fileName):
        self.image = load_image('resource/' + fileName + '.png')
        with open('resource/' + fileName + '.json', 'r') as f:
            data = json.load(f)
            self.w = data['width']
            self.h = data['height']
            cbList = data['colBox']
            self.colBox = []
            for cb in cbList:
                self.colBox.append(CollisionBox(cb['left'],cb['right'],cb['bottom'],cb['top']))

    def Draw(self):
        x, y = Camera.GetCameraPos(self.w / 2, self.h / 2)
        self.image.draw(x, y)
        x, y = x-self.w/2, y-self.h/2
        for cb in self.colBox:
            draw_rectangle(cb.left+x, cb.bottom+y, cb.right+x, cb.top+y)
