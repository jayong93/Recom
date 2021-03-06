import game_framework
import TitleState as StartStage
import Player
import Object
import Gun
import Monster
import Cursor
import Item
from pico2d import *

open_canvas(sync=True)
# 믹서 채널 할당
Mix_AllocateChannels(50)
# 커서 숨기기
hide_cursor()
# 커서 로딩
Cursor.init()
# 폰트 로딩
game_framework.font = load_font('resource/pf_arma_five.ttf')
# 오브젝트 데이터 로드
with open('resource/player.json', 'r') as f:
    Player.playerData = json.load(f)
with open('resource/monster.json', 'r') as f:
    Monster.monsterData = json.load(f)
with open('resource/teleporter.json', 'r') as f:
    Object.Teleporter.data = json.load(f)
with open('resource/item.json', 'r') as f:
    Item.itemData = json.load(f)
with open('resource/pistol.json', 'r') as f:
    Gun.pistolData = json.load(f)
with open('resource/machine_gun.json', 'r') as f:
    Gun.machineGunData = json.load(f)
with open('resource/sniper_rifle.json', 'r') as f:
    Gun.sniperRifleData = json.load(f)
with open('resource/boss_gun.json', 'r') as f:
    Gun.bossGunData = json.load(f)

Player.player = Player.Player()
Gun.reloadSound = load_wav('resource/reload.wav')
Gun.reloadSound.set_volume(64)
game_framework.run(StartStage)
close_canvas()
