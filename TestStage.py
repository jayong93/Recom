__author__ = 'Administrator'

import game_framework
import InputManager
import Map
import Player
import Monster
import random
import Camera
from pico2d import *

objList = None
map = None
PLAYER, MONSTER = 0, 1

def enter():
    open_canvas()
    Camera.w, Camera.h = 800, 600

    global objList, map
    map = Map.Map('test_stage')
    Camera.currentMap = map

    objList = {PLAYER: [], MONSTER: []}
    player = Player.Player()
    player.ChangeState(player.IDLE)
    player.x = 400
    player.y = 150
    Camera.SetCameraPos(player.x, 300)

    objList[PLAYER].append(player)


def exit():
    global objList, map
    for o in objList:
        del o
    del objList, map
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events():
    global objList, map
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            InputManager.KeyDown(event.key)
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_1:
                duck = Monster.Duck1()
                duck.ChangeState(duck.MOVE)
                duck.x, duck.y = random.randint(0,map.GetSize()[0]), 150
                duck.SetTarget(objList[PLAYER][0])
                objList[MONSTER].append(duck)
            elif event.key is SDLK_2:
                duck = Monster.Duck2()
                duck.ChangeState(duck.MOVE)
                duck.x, duck.y = random.randint(0,map.GetSize()[0]), 150
                duck.SetTarget(objList[PLAYER][0])
                objList[MONSTER].append(duck)
        elif event.type == SDL_KEYUP:
            InputManager.KeyUp(event.key)


def update():
    global objList

    # 충돌 체크
    player = objList[PLAYER][0]
    for m in objList[MONSTER]:
        if m.GetCollisionBox().CollisionCheck(player.GetCollisionBox()):
            m.Collision(player)

    for k in objList.keys():
        for o in objList[k]:
            o.Update()
            if o.isDelete is True:
                objList[k].remove(o)

    delay(0.01)


def draw():
    global objList, map
    clear_canvas()
    map.Draw()
    for k in objList.keys():
        for o in objList[k]:
            o.Draw()
    update_canvas()
