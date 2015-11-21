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
    global objList, map
    map = Map.Map('stage1')
    Camera.currentMap = map
    Camera.w, Camera.h = 800, 600

    objList = {PLAYER: [], MONSTER: []}
    player = Player.Player()
    player.x = 400
    player.y = 310
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
    player = objList[PLAYER][0]
    events = get_events()
    for event in events:
        player.HandleEvent(event, frame_time)
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

    for k in objList.keys():
        for o in objList[k]:
            o.Update(frame_time)
            if o.isDelete is True:
                objList[k].remove(o)

    Camera.SetCameraPos(player.x, player.y)

    for cb in map.colBox:
        if cb.CollisionCheck(player.GetCollisionBox()):
            cy = player.y
            player.y -= player.vy*player.PPM*frame_time
            oldy = player.y
            pcb = player.GetCollisionBox()
            player.y = cy

            if pcb.bottom > cb.top:
                player.vy = 0
                player.y = oldy
            elif pcb.right >= cb.left or pcb.left <= cb.right:
                player.x -= player.vx*player.PPM*frame_time
                player.vx = 0

    fall_check = True
    pcb = player.GetCollisionBox()
    for cb in map.colBox:
        if (cb.left < pcb.left < cb.right) or (cb.left < pcb.right < cb.right):
            if pcb.bottom - 2 < cb.top:
                fall_check = False
                break
    if fall_check:
        player.vy -= 0.3 * player.PPM * frame_time


def draw(frame_time):
    global objList, map
    clear_canvas()
    map.Draw()
    for k in objList.keys():
        for o in objList[k]:
            o.Draw(frame_time)
    update_canvas()
