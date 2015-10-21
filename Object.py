from pico2d import *


class GameObject:
    def __init__(self):
        self.x = 0
        self.y = 0
        return

    def Move(self, x, y):
        self.x += x
        self.y += y
        return


class DrawableObject(GameObject):
    def __init__(self, imgName):
        super().__init__()
        self.image = load_image(imgName)
        self.scaleX, self.scaleY = 1, 1
        self.direction = 1  # 오른쪽이 기본값
        self.angle = 0
        return

    def Draw(self):
        self.image.draw(self.x, self.y)
        return
