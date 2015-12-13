import game_framework
import TitleState
from pico2d import *

name = "TitleState"
image = None


def enter():
    global image
    image = load_image('resource/clear.png')


def exit():
    global image
    del image


def handle_events(frame_time):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_SPACE:
                game_framework.change_state(TitleState)
                return


def draw(frame_time):
    image.draw(400, 300)
    update_canvas()


def update(frame_time):
    pass


def pause():
    pass


def resume():
    pass
