from Object import *
from pico2d import *
import Cursor
import Camera
import Player
import Monster

pistolData = None
machineGunData = None
sniperRifleData = None
reloadSound = None


class Gun:
    def __init__(self, owner_type):
        self.image = None
        self.left_image = None
        self.bullet_image = None
        self.shoot_sound = None
        self.damage = 0
        self.shot_speed = 0
        self.shot_mul = 1
        self.piercing = False
        self.reload_speed = 0
        self.reload_mul = 1
        self.bullet_speed = 0
        self.total_bullet_num = 0
        self.remain_bullet_num = 0
        self.last_shoot_duration = 0
        self.reload_duration = 0
        self.is_reloading = False
        self.owner_type = owner_type

    def change_gun(self, data):
        if type(data['image']) == str:
            data['left_image'] = load_image(data['image'][0:-4] + '_left.png')
            data['image'] = load_image(data['image'])
        if type(data['bullet_image']) == str:
            data['bullet_image'] = load_image(data['bullet_image'])
        if type(data['shoot_sound']) == str:
            data['shoot_sound'] = load_wav(data['shoot_sound'])
            data['shoot_sound'].set_volume(70)
        self.image = data['image']
        self.left_image = data['left_image']
        self.bullet_image = data['bullet_image']
        self.shoot_sound = data['shoot_sound']
        self.damage = data['damage']
        self.shot_speed = data['shot_speed']
        if data['piercing'] == 0:
            self.piercing = False
        else:
            self.piercing = True
        self.reload_speed = data['reload_speed']
        self.bullet_speed = data['bullet_speed']
        self.total_bullet_num = data['total_bullet_num']
        self.remain_bullet_num = self.total_bullet_num
        self.last_shoot_duration = self.shot_speed
        self.reload_duration = 0
        self.is_reloading = False
        Cursor.is_reload = False
        
    def Update(self, frame_time):
        if self.shot_speed * self.shot_mul > self.last_shoot_duration:
            self.last_shoot_duration += frame_time
        if self.is_reloading:
            if self.reload_duration == 0 and self.owner_type == 'PLAYER':
                global reloadSound
                Mix_PlayChannelTimed(-1, reloadSound.wav, -1, int(self.reload_speed * self.reload_mul *1000))
                Cursor.speed = self.reload_speed * self.reload_mul
                Cursor.is_reload = True
                Cursor.total_frame = 0
            Cursor.update(frame_time)
            self.reload_duration += frame_time
            if self.reload_speed * self.reload_mul <= self.reload_duration:
                self.remain_bullet_num = self.total_bullet_num
                self.reload_duration = 0
                self.is_reloading = False
                if self.owner_type == 'PLAYER':
                    Cursor.is_reload = False

    def Shoot(self):
        if self.shot_speed * self.shot_mul <= self.last_shoot_duration and not self.is_reloading:
            self.remain_bullet_num -= 1
            self.last_shoot_duration = 0
            if self.remain_bullet_num == 0:
                self.is_reloading = True
            self.shoot_sound.play()
            return True
        return False

    def Reload(self):
        if self.remain_bullet_num < self.total_bullet_num and not self.is_reloading:
            self.is_reloading = True


class Bullet(GameObject):
    PPM = 1/0.015

    def __init__(self, x, y, image, owner, damage=0, vx=0, vy=0, angle=0, piercing=False):
        super().__init__()
        self.x, self.y = x, y
        self.image = image
        self.damage = damage
        self.angle = angle
        self.piercing = piercing
        self.owner = owner
        self.vx, self.vy = vx, vy
        self.hit_object = {}

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.rotate_draw(self.angle, x, y)

    def Update(self, frame_time):
        self.x += self.vx * self.PPM * frame_time
        self.y += self.vy * self.PPM * frame_time

    def Collision(self, other):
        if other == 'MAP':
            self.isDelete = True
        elif (self.owner == 'PLAYER' and isinstance(other, Monster.Monster)) or\
                (self.owner == 'MONSTER' and isinstance(other, Player.Player)):
            if not (other in self.hit_object):
                other.Hit(self.damage)
                self.hit_object[other] = True
            if self.piercing is False and other.state != 'DEATH':
                self.isDelete = True

    def GetCollisionBox(self):
        w, h = self.image.w, self.image.h
        return CollisionBox(self.x - w/2, self.x + w/2, self.y - h/2, self.y + h/2)