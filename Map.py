__author__ = 'Administrator'

from pico2d import *


class Map:
    def __init__(self, fileName):
        self.image = load_image('resource/' + fileName + '.png')
        self.data = []
        with open('resource/' + fileName + '.txt', 'r') as f:
            text = f.readline()
            self.w = int(text[6:-1])
            text = f.readline()
            self.h = int(text[7:-1])
            text = f.readline()
            self.tw = int(text[10:-1])
            text = f.readline()
            self.th = int(text[11:-1])
            for i in range(0, self.h):
                text = f.readline()
                textList = text.split(',')
                intList = []
                for n in textList:
                    intList.append(int(n))
                self.data.append(intList)
        return

    def Draw(self):
        self.image.draw(self.w * self.tw / 2, self.h * self.th / 2)
