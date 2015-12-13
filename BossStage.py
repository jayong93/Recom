import game_framework
import Map
import Player
import Cursor
import Monster
import GameOver
import Clear
import Item
import random
from Object import *
from pico2d import *

objList = None
map = None
bgm = None
player = None
PLAYER, MONSTER, OBJECT, TELEPORT = 0, 1, 2, 3


def enter():
    global objList, map, player, bgm

    player = Player.player
    player.is_boss_stage = True

    objList = {PLAYER: [player], MONSTER: [], OBJECT: [], TELEPORT: []}

    with open('resource/boss_stage.json', 'r') as f:
        mapData = json.load(f)
    map = Map.Map('boss_stage')
    map.w, map.h = mapData['width'], mapData['height']
    cbList = mapData['colBox']
    for cb in cbList:
        map.colBox.append(CollisionBox(cb['left'], cb['right'], cb['bottom'], cb['top']))
    mapObject = mapData['object']
    for obj in mapObject:
        if obj['type'] == 'player':
            player.x, player.y = obj['x'], obj['y']
        elif obj['type'] == 'duck':
            if obj['gun'] == 'random':
                gun = ('pistol', 'machine_gun', 'sniper_rifle')[random.randint(0, 2)]
            else:
                gun = obj['gun']
            m = Monster.Duck(obj['x'], obj['y'], gun)
            objList[MONSTER].append(m)
        elif obj['type'] == 'turtle':
            if obj['gun'] == 'random':
                gun = ('pistol', 'machine_gun', 'sniper_rifle')[random.randint(0, 2)]
            else:
                gun = obj['gun']
            m = Monster.Turtle(obj['x'], obj['y'], gun)
            objList[MONSTER].append(m)
        elif obj['type'] == 'teleporter':
            o = Teleporter(obj['x'], obj['y'])
            objList[TELEPORT].append(o)
        elif obj['type'] == 'shield':
            o = Item.ShieldUpItem(obj['x'], obj['y'])
            objList[OBJECT].append(o)
        elif obj['type'] == 'hp':
            o = Item.HpUpItem(obj['x'], obj['y'])
            objList[OBJECT].append(o)
        elif obj['type'] == 'reload':
            o = Item.ReloadUpItem(obj['x'], obj['y'])
            objList[OBJECT].append(o)
        elif obj['type'] == 'shot':
            o = Item.ShotUpItem(obj['x'], obj['y'])
            objList[OBJECT].append(o)
        elif obj['type'] == 'pistol' or obj['type'] == 'machine_gun' or obj['type'] == 'sniper_rifle':
            o = Item.GunItem(obj['x'], obj['y'], obj['type'])
            objList[OBJECT].append(o)
        elif obj['type'] == 'Boss':
            m = Monster.Boss(obj['x'], obj['y'])
            objList[MONSTER].append(m)

    Camera.currentMap = map
    Camera.offsetX = 300
    Camera.SetCameraPos(player.x, player.y)


def exit():
    global objList, map, bgm, player
    for t in objList:
        for o in objList[t]:
            del o
    del objList, map, bgm
    objList = None
    map = None
    bgm = None
    player = None
    Camera.currentMap = None


def pause():
    pass


def resume():
    pass


def handle_events(frame_time):
    global objList, map, player
    events = get_events()
    for event in events:
        player.HandleEvent(event, frame_time)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            Cursor.x, Cursor.y = event.x, Camera.h - event.y - 1
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()


def update(frame_time):
    global objList, map, nextStage, player

    # 모든 오브젝트 갱신
    for k in objList:
        for o in objList[k]:
            o.Update(frame_time)
            if k == PLAYER and o.state != 'DEATH' and o.y < -20:
                o.ChangeState('DEATH')

    for cb in map.colBox:
        # 플레이어와 몬스터를 맵과 충돌 체크
        for t in range(2):
            for obj in objList[t]:
                if cb.CollisionCheck(obj.GetCollisionBox()):
                    cy = obj.y  # 충돌된 현재 y값
                    obj.y -= obj.vy * obj.PPM * frame_time
                    pcb = obj.GetCollisionBox()
                    obj.y = cy

                    # 충돌 이전에 오브젝트가 더 위에 있었으면
                    if pcb.bottom > cb.top:
                        obj.vy = 0
                        bottom = obj.GetCollisionBox().bottom
                        obj.y += cb.top - bottom
                    elif pcb.right > cb.left > pcb.left:
                        right = obj.GetCollisionBox().right
                        obj.x += cb.left - right
                    elif pcb.left < cb.right < pcb.right:
                        left = obj.GetCollisionBox().left
                        obj.x += cb.right - left

        # 일반 오브젝트(총알)을 맵과 충돌체크
        for obj in objList[OBJECT]:
            if cb.CollisionCheck(obj.GetCollisionBox()):
                obj.Collision('MAP')

    # 카메라가 플레이어를 따라다니게
    Camera.SetCameraPos(player.x, player.y)

    # 중력 적용 체크
    for t in range(2):
        for obj in objList[t]:
            fall_check = True
            pcb = obj.GetCollisionBox()
            pcb.bottom -= 1
            for cb in map.colBox:
                if pcb.CollisionCheck(cb):
                    fall_check = False
                    break
            if fall_check:
                obj.vy -= 0.3 * obj.PPM * frame_time

    for t1 in range(3):
        for obj1 in objList[t1]:
            obj1ColBox = obj1.GetCollisionBox()
            for t2 in range(t1 + 1, 3):
                for obj2 in objList[t2]:
                    obj2ColBox = obj2.GetCollisionBox()
                    if obj1ColBox.CollisionCheck(obj2ColBox):
                        obj1.Collision(obj2)
                        obj2.Collision(obj1)

    # 죽은 오브젝트 삭제
    for t in objList:
        for o in objList[t]:
            if o.isDelete:
                if t == PLAYER:
                    game_framework.change_state(GameOver)
                    return
                else:
                    objList[t].remove(o)
                    if t == MONSTER:
                        game_framework.change_state(Clear)
                        return


def draw(frame_time):
    global objList, map
    clear_canvas()
    map.Draw()
    for k in objList.keys():
        for o in objList[k]:
            o.Draw(frame_time)
    Cursor.draw(frame_time)
    update_canvas()
