__author__ = 'Administrator'

import game_framework
import Stage1 as StartStage
import Player
from pico2d import *

open_canvas(sync=True)
with open('player.json', 'r') as f:
    Player.playerData = json.load(f)
game_framework.run(StartStage)
close_canvas()