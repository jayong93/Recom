from Map import *

x, y = None, None
w, h = None, None
currentMap = None


def GetCameraPos(wx, wy):
    global x, y, w, h
    return wx - x + w / 2, wy - y + h / 2


def SetCameraPos(wx, wy):
    global x, y, w, h
    mw, mh = currentMap.GetSize()
    if wx < w/2:
        x = w/2
    elif wx > mw - w/2:
        x = mw - w/2
    else:
        x = wx

    if wy < h/2:
        y = h/2
    elif wy > mh - h/2:
        y = mh - h/2
    else:
        y = wy


def SetCameraSize(cw, ch):
    global w, h
    w, h = cw, ch


def GetWorldPos(cx, cy):
    pass
