from Object import *
from Collision import *
import Gun
import math
import Monster
import game_framework

playerData = None
player = None


class Player(Character):
    PPM = None
    RUN_SPEED = None
    animationList = None
    stateList = None

    def __init__(self, x=0, y=0):
        super().__init__()
        self.x, self.y = x, y
        self.maxhp = playerData['hp']
        self.hp = self.maxhp
        self.max_shield = playerData['shield']
        self.shield = self.max_shield
        self.shield_charge_time = playerData['shield_charge_time']
        self.lastHitDuration = self.shield_charge_time
        self.isShieldOn = False
        self.hit_object = {}
        self.is_get_item = False
        self.is_boss_stage = False
        self.boss_stage_dir = 0
        self.direction = 1

        if type(playerData['hit_sound']) == str:
            playerData['hit_sound'] = load_wav(playerData['hit_sound'])
            playerData['hit_sound'].set_volume(100)

        if type(playerData['shield_hit_sound']) == str:
            playerData['shield_hit_sound'] = load_wav(playerData['shield_hit_sound'])
            playerData['shield_hit_sound'].set_volume(80)

        if self.PPM is None:
            self.PPM = 1 / playerData['mpp']

        if self.RUN_SPEED is None:
            self.RUN_SPEED = playerData['run_speed']

        if Player.animationList is None:
            Player.animationList = {}
            for s in playerData['animation']:
                v = playerData['animation'][s]
                Player.animationList[s] = Animation(v[0], v[1], v[2], v[3], v[4], v[5])

        if Player.stateList is None:
            Player.stateList = {
                'IDLE': self.IdleUpdate,
                'MOVE': self.MoveUpdate,
                'MELEE': self.MeleeUpdate,
                'DEATH': self.DeathUpdate
            }

        self.colBox = CollisionBox(playerData['cx'], playerData['cx'] + playerData['cw'],
                                   playerData['cy'], playerData['cy'] + playerData['ch'])

        self.state = playerData['currentState']
        self.ChangeState(self.state)
        self.isShooting = False
        self.gun = Gun.Gun('PLAYER')
        self.targetX, self.targetY = self.x + 1, self.y

    def Init(self):
        self.maxhp = playerData['hp']
        self.hp = self.maxhp
        self.max_shield = playerData['shield']
        self.shield = self.max_shield
        self.shield_charge_time = playerData['shield_charge_time']
        self.lastHitDuration = self.shield_charge_time
        self.isShieldOn = False
        self.hit_object = {}
        self.is_get_item = False
        self.colBox = CollisionBox(playerData['cx'], playerData['cx'] + playerData['cw'],
                                   playerData['cy'], playerData['cy'] + playerData['ch'])
        self.state = playerData['currentState']
        self.ChangeState(self.state)
        self.isShooting = False
        self.gun = Gun.Gun('PLAYER')
        self.targetX, self.targetY = self.x + 1, self.y
        self.isDelete = False
        self.is_boss_stage = False
        self.boss_stage_dir = 0
        self.direction = 1

    def GetCollisionBox(self):
        anim = self.anim
        x, y = self.x - anim.w / 2, self.y - anim.h / 2
        cb = self.colBox.Move(x, y)
        if self.state == 'MELEE':
            cb.right += 30
        return cb

    def IdleUpdate(self, frame_time):
        self.vx = 0

    def MoveUpdate(self, frame_time):
        self.vx = self.RUN_SPEED * self.direction

    def MeleeUpdate(self, frame_time):
        self.vx = 0
        if self.frame > self.anim.frame:
            if self.is_boss_stage:
                self.ChangeState('IDLE')
            else:
                self.ChangeState('MOVE')
            self.hit_object.clear()

    def DeathUpdate(self, frame_time):
        self.vx = 0
        self.isShieldOn = False
        self.isShooting = False
        if self.frame >= self.anim.frame:
            self.frame = self.anim.frame - 1
            self.isDelete = True

    def Draw(self, frame_time):
        anim = self.anim
        x, y = Camera.GetCameraPos(self.x, self.y)
        anim.image.clip_draw(int(self.frame) % anim.frame * anim.w, 0, anim.w, anim.h, x, y)
        game_framework.font.draw(x-20, y + 30, 'hp : %d' % self.hp, (1, 1, 1))
        game_framework.font.draw(x-40, y + 50, 'Shield : %d' % self.shield, (1, 1, 1))
        gunX, gunY = x + 10, y - 25
        if self.state != 'DEATH':
            tx, ty = max(self.targetX, gunX+1), self.targetY
            rad = math.atan2(ty - gunY, tx - gunX)
            self.gun.image.rotate_draw(rad, gunX, gunY)
        else:
            self.gun.image.draw(gunX, gunY)
        if self.isShieldOn:
            shield_anim = self.animationList['shield']
            shield_anim.image.clip_draw(int(self.frame) % shield_anim.frame * shield_anim.w,
                                         0, shield_anim.w, shield_anim.h, x, y)
        x, y = x - anim.w / 2, y - anim.h / 2
        draw_rectangle(self.colBox.left + x, self.colBox.bottom + y, self.colBox.right + x, self.colBox.top + y)

    def Update(self, frame_time):
        # 애니메이션 프레임 처리
        anim = self.anim
        if self.frame < anim.frame:
            self.frame += anim.frame * (1 / anim.time) * frame_time
        elif anim.repeat:
            self.frame -= anim.frame

        if anim == self.animationList['hit'] and self.frame > anim.frame:
            self.ChangeState(self.state)

        # 총 정보 갱신
        self.gun.Update(frame_time)

        # 발포
        if self.isShooting and self.gun.Shoot():
            gx, gy = self.x + 10, self.y - 25
            tx, ty = Camera.GetWorldPos(self.targetX, self.targetY)
            tx = max(tx, gx+1)
            rad = math.atan2(ty-gy, tx-gx)
            vcos, vsin = math.cos(rad), math.sin(rad)

            bullet = Gun.Bullet(vcos + gx, vsin + gy + 3,
                                self.gun.bullet_image, 'PLAYER', self.gun.damage,
                                vcos*self.gun.bullet_speed, vsin*self.gun.bullet_speed, rad, self.gun.piercing)

            stage = game_framework.get_top_state()
            stage.objList[stage.OBJECT].append(bullet)

        # 쉴드 갱신
        if self.lastHitDuration < self.shield_charge_time:
            self.lastHitDuration += frame_time
        elif self.shield < self.max_shield:
            self.shield += 300 * frame_time
            if self.shield > self.max_shield:
                self.shield = self.max_shield

        self.stateList[self.state](frame_time)

        self.x += self.vx * self.PPM * frame_time
        self.y += self.vy * self.PPM * frame_time

    def Hit(self, damage):
        if self.state != 'DEATH' and self.state != 'MELEE':
            self.lastHitDuration = 0
            if self.isShieldOn and self.shield > 0:
                self.shield -= damage
                playerData['shield_hit_sound'].play()
                if self.shield <= 0:
                    self.hp += self.shield
                    self.shield = 0
                    self.isShieldOn = False
            else:
                playerData['hit_sound'].play()
                self.anim = self.animationList['hit']
                self.frame = 0.0
                self.hp -= damage

            if self.hp <= 0:
                self.hp = 0
                self.ChangeState('DEATH')

    def HandleEvent(self, event, frame_time):
        if self.state == 'DEATH':
            return
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_SPACE and self.vy == 0:
                self.vy = 7
            elif event.key == SDLK_q and self.state != 'MELEE':
                self.ChangeState('MELEE')
            elif event.key == SDLK_LSHIFT and self.shield >= 1:
                self.isShieldOn = True
            elif event.key == SDLK_r:
                self.gun.Reload()
            elif event.key == SDLK_e:
                self.is_get_item = True
            if self.is_boss_stage:
                if event.key == SDLK_a:
                    self.boss_stage_dir -= 1
                elif event.key == SDLK_d:
                    self.boss_stage_dir += 1
                if self.boss_stage_dir > 0:
                    self.direction = 1
                    if self.state != 'MOVE':
                        self.ChangeState('MOVE')
                elif self.boss_stage_dir < 0:
                    self.direction = -1
                    if self.state != 'MOVE':
                        self.ChangeState('MOVE')
                else:
                    self.ChangeState('IDLE')

        elif event.type == SDL_KEYUP:
            if event.key == SDLK_LSHIFT:
                self.isShieldOn = False
            elif event.key == SDLK_e:
                self.is_get_item = False

            if self.is_boss_stage:
                if event.key == SDLK_a:
                    self.boss_stage_dir += 1
                elif event.key == SDLK_d:
                    self.boss_stage_dir -= 1
                if self.boss_stage_dir > 0:
                    self.direction = 1
                    if self.state != 'MOVE':
                        self.ChangeState('MOVE')
                elif self.boss_stage_dir < 0:
                    self.direction = -1
                    if self.state != 'MOVE':
                        self.ChangeState('MOVE')
                else:
                    self.ChangeState('IDLE')

        elif event.type == SDL_MOUSEMOTION:
            self.targetX, self.targetY = event.x, Camera.h - event.y - 1

        elif event.type == SDL_MOUSEBUTTONDOWN and self.state != 'DEATH':
            if event.button == SDL_BUTTON_LEFT:
                self.isShooting = True
        elif event.type == SDL_MOUSEBUTTONUP:
            if event.button == SDL_BUTTON_LEFT:
                self.isShooting = False

    def Collision(self, other):
        if self.state == 'MELEE' and self.frame > self.animationList[self.state].frame * 0.7 and isinstance(other, Monster.Monster):
            if not (other in self.hit_object):
                other.Hit(70)
                self.hit_object[other] = True
