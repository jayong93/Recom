from pico2d import *

image = None
reload_image = None
x, y = 0, 0
w, h = 0, 0
frame = 0
total_frame = 0
speed = 0
is_reload = False


def draw(frame_time):
    if is_reload:
        reload_image.clip_draw(int(total_frame) % frame * w, 0, w, h, x, y)
    else:
        image.draw(x, y)


def update(frame_time):
    global frame, total_frame, speed
    if is_reload:
        total_frame += frame * (1 / speed) * frame_time


def init():
    global image, reload_image, w, h, frame
    with open('resource/cursor.json','r') as f:
        data = json.load(f)
        image = load_image(data['image'])
        reload_image = load_image(data['reload_image'])
        w, h = data['width'], data['height']
        frame = data['frame']