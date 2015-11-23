x, y = None, None
w, h = 800, 600
currentMap = None
offsetX, offsetY = 0, 0


def GetCameraPos(wx, wy):
    global x, y, w, h
    return int(wx - x + w / 2), int(wy - y + h / 2)


def SetCameraPos(wx, wy):
    global x, y, w, h
    wx += offsetX
    wy += offsetY
    mw, mh = currentMap.w, currentMap.h
    # 화면 왼쪽으로 넘어가려 할 때
    if wx < w/2:
        x = w/2
    # 화면 오른쪽으로 넘어가려 할 때
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
    global x, y, w, h
    return cx + x - w/2, cy + y - h/2
