__author__ = 'Administrator'

import game_framework
import InputManager
import Player
from pico2d import *

player = None


def enter():
    global player, image
    open_canvas()
    player = Player.Player()
    player.ChangeState(player.IDLE)
    player.x = 400
    player.y = 300


def exit():
    global player
    del player
    close_canvas()


def pause():
    pass


def resume():
    pass


def handle_events():
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            InputManager.KeyDown(event.key)
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
        elif event.type == SDL_KEYUP:
            InputManager.KeyUp(event.key)


def update():
    player.Update()
    delay(0.01)


def draw():
    global player
    clear_canvas()
    player.Draw()
    update_canvas()
