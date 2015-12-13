import game_framework
import Player
import Gun
import Stage1 as NextStage
from pico2d import *

image = None


def enter():
    global image
    image = load_image('resource/title.png')


def exit():
    global image
    del image

    player = Player.player
    player.Init()
    player.gun.change_gun(Gun.pistolData)


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_state(NextStage)
                return


def draw(frame_time):
    clear_canvas()
    image.draw(400, 300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass
