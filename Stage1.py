import game_framework
import Map
import InputManager
import Player
from Object import *
from pico2d import *

objList = None
map = None
nextStage = None
player = None
PLAYER, MONSTER, OBJECT, TELEPORT = 0, 1, 2, 3


def enter():
    global objList, map, nextStage, player

    player = Player.player
    objList = {PLAYER: [player], MONSTER: [], OBJECT: [], TELEPORT: []}

    with open('resource/stage1.json', 'r') as f:
        mapData = json.load(f)
    map = Map.Map('stage1')
    map.w, map.h = mapData['width'], mapData['height']
    cbList = mapData['colBox']
    for cb in cbList:
        map.colBox.append(CollisionBox(cb['left'], cb['right'], cb['bottom'], cb['top']))
    mapObject = mapData['object']
    for obj in mapObject:
        if obj['type'] == 'player':
            player.x, player.y = obj['x'], obj['y']
        elif obj['type'] == 'monster':
            pass
        elif obj['type'] == 'teleporter':
            o = Teleporter(obj['x'], obj['y'])
            objList[TELEPORT].append(o)

    Camera.currentMap = map
    Camera.SetCameraPos(player.x + 300, player.y)


def exit():
    global objList, map
    for t in objList:
        for o in objList[t]:
            del o
    del objList, map


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
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else:
                InputManager.KeyDown(event.key)
        elif event.type == SDL_KEYUP:
            InputManager.KeyUp(event.key)


def update(frame_time):
    global objList, map, nextStage, player

    # 모든 오브젝트 갱신
    for k in objList:
        for o in objList[k]:
            o.Update(frame_time)
            if o.isDelete is True:
                objList[k].remove(o)

    for cb in map.colBox:
        # 플레이어와 몬스터를 맵과 충돌 체크
        for t in range(2):
            for obj in objList[t]:
                if cb.CollisionCheck(obj.GetCollisionBox()):
                    cy = obj.y                          # 충돌된 현재 y값
                    obj.y -= obj.vy*obj.PPM*frame_time
                    pcb = obj.GetCollisionBox()
                    obj.y = cy

                    # 충돌 이전에 오브젝트가 더 위에 있었으면
                    if pcb.bottom > cb.top:
                        obj.vy = 0
                        bottom = obj.GetCollisionBox().bottom
                        obj.y += cb.top - bottom
                    elif pcb.right >= cb.left:
                        right = obj.GetCollisionBox().right
                        obj.x += cb.left - right
                    elif pcb.left <= cb.right:
                        left = obj.GetCollisionBox().left
                        obj.x += cb.right - left

    # 카메라가 플레이어를 따라다니게
    Camera.SetCameraPos(player.x + 300, player.y)

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

    # 플레이어와 몬스터, 기타 오브젝트 충돌체크
    pcb = player.GetCollisionBox()
    for t in range(1, 3):
        for obj in objList[t]:
            ocb = obj.GetCollisionBox()
            if pcb.CollisionCheck(ocb):
                obj.Collision(player)

    # 출구 충돌 체크
    pcb = player.GetCollisionBox()
    for tp in objList[TELEPORT]:
        tcb = tp.GetCollisionBox()
        if tcb.CollisionCheck(pcb):
            if nextStage is None:
                game_framework.quit()


def draw(frame_time):
    global objList, map
    clear_canvas()
    map.Draw()
    for k in objList.keys():
        for o in objList[k]:
            o.Draw(frame_time)
    update_canvas()
