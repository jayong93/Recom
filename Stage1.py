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
    Camera.w, Camera.h = 800, 600

    with open('player.json', 'r') as f:
        Player.playerData = json.load(f)

    global objList, map
    map = Map.Map('stage1')
    Camera.currentMap = map

    objList = {PLAYER: [], MONSTER: []}
    player = Player.Player()
    player.x = 400
    player.y = 400
    Camera.SetCameraPos(player.x, 400)

    objList[PLAYER].append(player)


def exit():
    global objList, map
    for o in objList:
        del o
    del objList, map


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    global objList, map
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                InputManager.KeyDown(event.key)
        elif event.type == SDL_KEYUP:
            InputManager.KeyUp(event.key)


def update(frame_time):
    global objList, map

    player = objList[PLAYER][0]
    player.vy -= player.PPM * 0.5 * 0.01

    for k in objList.keys():
        for o in objList[k]:
            o.Update(frame_time)
            if o.isDelete is True:
                objList[k].remove(o)

    for cb in map.colBox:
        if cb.CollisionCheck(player.GetCollisionBox()):
            player.x -= player.vx*player.PPM*frame_time
            player.y -= player.vy*player.PPM*frame_time
            if player.GetCollisionBox().bottom > cb.top:
                player.vy = 0
            break


def draw(frame_time):
    global objList, map
    clear_canvas()
    map.Draw()
    for k in objList.keys():
        for o in objList[k]:
            o.Draw(frame_time)
    update_canvas()
