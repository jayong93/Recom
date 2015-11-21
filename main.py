__author__ = 'Administrator'

import game_framework
import Stage1 as StartStage
from pico2d import *

open_canvas(sync=True)
game_framework.run(StartStage)
close_canvas()