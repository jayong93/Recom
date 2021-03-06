from Object import *
from Collision import *
import Gun
import math
import Player
import game_framework

monsterData = None


class Monster(Character):
    PPM = None
    LEFT, RIGHT = 0, 1

    def __init__(self, x=0, y=0):
        super().__init__()
        if self.PPM is None:
            self.PPM = 1 / monsterData['mpp']
        self.x, self.y = x, y
        self.maxhp = 0
        self.hp = 0
        self.direction = self.LEFT
        self.stateList = {'IDLE': self.IdleUpdate, 'MOVE': self.MoveUpdate, 'DEATH': self.DeathUpdate}
        self.run_speed = 0
        self.detect_range = 0
        self.isShooting = False
        self.gun = Gun.Gun('MONSTER')
        self.target = Player.player

    def GetCollisionBox(self):
        anim = self.animationList[self.state]
        if self.direction == self.RIGHT:
            x, y = self.x - anim.w / 2, self.y - anim.h / 2
        else:
            cb = self.colBox
            x, y = self.x - anim.w / 2 + (anim.w - cb.right - cb.left), self.y - anim.h / 2
        return self.colBox.Move(x, y)

    def IdleUpdate(self, frame_time):
        self.vx = 0
        dist = math.fabs(self.target.x - self.x)
        if dist <= self.detect_range:
            self.ChangeState('MOVE')

    def MoveUpdate(self, frame_time):
        dist = math.fabs(self.target.x - self.x)
        if self.x > self.target.x:
            self.direction = self.LEFT
        else:
            self.direction = self.RIGHT

        if dist >= self.detect_range / 2:
            if self.direction == self.LEFT:
                self.vx = -self.run_speed
            else:
                self.vx = self.run_speed
        else:
            self.vx = 0

        if self.vy == 0:
            cbList = game_framework.get_top_state().map.colBox
            rayBox = self.GetCollisionBox()

            # 장애물 점프
            rayBox.top, rayBox.bottom = self.y + 1, self.y - 1
            if self.direction == self.LEFT:
                rayBox.right = rayBox.left
                rayBox.left -= self.run_speed
            else:
                rayBox.left = rayBox.right
                rayBox.right += self.run_speed
            for cb in cbList:
                if cb.CollisionCheck(rayBox):
                    self.vy = 7
                    break

            # 낭떨어지 정지
            rayBox = self.GetCollisionBox()
            rayBox.top = rayBox.bottom
            rayBox.bottom -= 500
            if self.direction == self.LEFT:
                rayBox.right = rayBox.left - 1
                rayBox.left -= 5
            else:
                rayBox.left = rayBox.right + 1
                rayBox.right += 5

            isFall = True
            for cb in cbList:
                if cb.CollisionCheck(rayBox):
                    isFall = False
                    break
            if isFall:
                self.vx = 0

    def DeathUpdate(self, frame_time):
        self.vx = 0
        self.target = None
        if self.frame >= self.anim.frame:
            self.isDelete = True

    def Draw(self, frame_time):
        anim = self.anim
        x, y = Camera.GetCameraPos(self.x, self.y)
        anim.image.clip_draw(int(self.frame) % anim.frame * anim.w, anim.h * self.direction, anim.w, anim.h, x, y)
        game_framework.font.draw(x - 20, y + 30, 'hp : %d' % self.hp, (1, 1, 1))

        if self.direction == self.LEFT:
            gunX = x - 10
        else:
            gunX = x + 10
        gunY = y - 25
        if self.target is not None:
            tx, ty = Camera.GetCameraPos(self.target.x, self.target.y)
            if self.direction == self.LEFT:
                tx = min(tx, gunX - 1)
            else:
                tx = max(tx, gunX + 1)
            rad = math.atan2(ty - gunY, tx - gunX)
            if self.direction == self.RIGHT:
                self.gun.image.rotate_draw(rad, gunX, gunY)
            else:
                self.gun.left_image.rotate_draw(rad + math.pi, gunX, gunY)
        elif self.direction == self.LEFT:
            self.gun.left_image.draw(gunX, gunY)
        else:
            self.gun.image.draw(gunX, gunY)

        # if self.direction == self.RIGHT:
        #     x, y = x - anim.w / 2, y - anim.h / 2
        # else:
        #     cb = self.colBox
        #     x, y = x - anim.w / 2 + (anim.w - cb.right - cb.left), y - anim.h / 2
        # draw_rectangle(self.colBox.left + x, self.colBox.bottom + y, self.colBox.right + x, self.colBox.top + y)

    def Update(self, frame_time):
        # 애니메이션 프레임 처리
        anim = self.anim
        if self.frame <= anim.frame:
            self.frame += anim.frame * (1 / anim.time) * frame_time
        elif anim.repeat:
            self.frame -= anim.frame

        if anim == self.animationList['hit'] and self.frame >= self.anim.frame:
            self.ChangeState(self.state)

        # 총 정보 갱신
        self.gun.Update(frame_time)

        # 발포
        if self.state == 'MOVE' and self.gun.Shoot():
            if self.direction == self.LEFT:
                gx = self.x - 10
            else:
                gx = self.x + 10
            gy = self.y - 25
            tx, ty = self.target.x, self.target.y
            if self.direction == self.LEFT:
                tx = min(tx, gx - 1)
            else:
                tx = max(tx, gx + 1)
            rad = math.atan2(ty - gy, tx - gx)
            vcos, vsin = math.cos(rad), math.sin(rad)

            bullet = Gun.Bullet(vcos + gx, vsin + gy + 3,
                                self.gun.bullet_image, 'MONSTER', self.gun.damage,
                                vcos * self.gun.bullet_speed, vsin * self.gun.bullet_speed, rad, self.gun.piercing)

            stage = game_framework.get_top_state()
            stage.objList[stage.OBJECT].append(bullet)

        self.stateList[self.state](frame_time)

        self.x += self.vx * self.PPM * frame_time
        self.y += self.vy * self.PPM * frame_time

    def Hit(self, damage):
        if self.state != 'DEATH':
            self.hp -= damage
            self.hit_sound.play()
            self.ChangeState('MOVE')
            self.anim = self.animationList['hit']
            self.frame = 0.0
            if self.hp <= 0:
                self.hp = 0
                self.ChangeState('DEATH')


class Duck(Monster):
    hit_sound = None
    animationList = None

    def __init__(self, x=0, y=0, gun='pistol'):
        super().__init__(x, y)
        data = monsterData['Duck']
        if self.hit_sound is None:
            self.hit_sound = load_wav(data['hit_sound'])
            self.hit_sound.set_volume(30)
        if self.animationList is None:
            self.animationList = {}
            for s in data['animation']:
                a = data['animation'][s]
                self.animationList[s] = Animation(a[0], a[1], a[2], a[3], a[4], a[5])
        self.maxhp = data['hp']
        self.hp = self.maxhp
        self.state = data['init_state']
        self.ChangeState(self.state)
        self.run_speed = data['run_speed']
        self.detect_range = data['detect_range']
        cb = data['colBox']
        self.colBox = CollisionBox(cb[0], cb[1], cb[2], cb[3])

        if gun == 'pistol':
            self.gun.change_gun(Gun.pistolData)
        elif gun == 'machine_gun':
            self.gun.change_gun(Gun.machineGunData)
        elif gun == 'sniper_rifle':
            self.gun.change_gun(Gun.sniperRifleData)


class Turtle(Monster):
    hit_sound = None
    animationList = None

    def __init__(self, x=0, y=0, gun='pistol'):
        super().__init__(x, y)
        data = monsterData['Turtle']
        if self.hit_sound is None:
            self.hit_sound = load_wav(data['hit_sound'])
            self.hit_sound.set_volume(30)
        if self.animationList is None:
            self.animationList = {}
            for s in data['animation']:
                a = data['animation'][s]
                self.animationList[s] = Animation(a[0], a[1], a[2], a[3], a[4], a[5])
        self.maxhp = data['hp']
        self.hp = self.maxhp
        self.state = data['init_state']
        self.ChangeState(self.state)
        self.run_speed = data['run_speed']
        self.detect_range = data['detect_range']
        cb = data['colBox']
        self.colBox = CollisionBox(cb[0], cb[1], cb[2], cb[3])

        if gun == 'pistol':
            self.gun.change_gun(Gun.pistolData)
        elif gun == 'machine_gun':
            self.gun.change_gun(Gun.machineGunData)
        elif gun == 'sniper_rifle':
            self.gun.change_gun(Gun.sniperRifleData)


class Boss(Monster):
    hit_sound = None
    animationList = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        data = monsterData['Boss']
        if self.hit_sound is None:
            self.hit_sound = load_wav(data['hit_sound'])
            self.hit_sound.set_volume(120)
        if self.animationList is None:
            self.animationList = {}
            for s in data['animation']:
                a = data['animation'][s]
                self.animationList[s] = Animation(a[0], a[1], a[2], a[3], a[4], a[5])
        self.maxhp = data['hp']
        self.hp = self.maxhp
        self.state = data['init_state']
        self.ChangeState(self.state)
        self.run_speed = data['run_speed']
        self.detect_range = data['detect_range']
        cb = data['colBox']
        self.colBox = CollisionBox(cb[0], cb[1], cb[2], cb[3])

        self.gun.change_gun(Gun.bossGunData)