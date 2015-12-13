from Object import *
import Player
import Gun

itemData = None


class ShieldUpItem(GameObject):
    image = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        data = itemData['shield']

        if self.image is None:
            self.image = load_image(data['image'])

        self.colBox = CollisionBox(data['cx'], data['cx'] + data['cw'], data['cy'], data['cy'] + data['ch'])

    def GetCollisionBox(self):
        x, y = self.x - self.image.w / 2, self.y - self.image.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.draw(x, y)

    def Collision(self, other):
        if isinstance(other, Player.Player):
            other.max_shield += 100
            other.shield += 100
            self.isDelete = True


class HpUpItem(GameObject):
    image = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        data = itemData['hp']

        if self.image is None:
            self.image = load_image(data['image'])

        self.colBox = CollisionBox(data['cx'], data['cx'] + data['cw'], data['cy'], data['cy'] + data['ch'])

    def GetCollisionBox(self):
        x, y = self.x - self.image.w / 2, self.y - self.image.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.draw(x, y)

    def Collision(self, other):
        if isinstance(other, Player.Player):
            other.hp = other.maxhp
            self.isDelete = True


class ShotUpItem(GameObject):
    image = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        data = itemData['shot']

        if self.image is None:
            self.image = load_image(data['image'])

        self.colBox = CollisionBox(data['cx'], data['cx'] + data['cw'], data['cy'], data['cy'] + data['ch'])

    def GetCollisionBox(self):
        x, y = self.x - self.image.w / 2, self.y - self.image.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.draw(x, y)

    def Collision(self, other):
        if isinstance(other, Player.Player):
            other.gun.shot_mul = max(other.gun.shot_mul - 0.3, 0.1)
            self.isDelete = True


class ReloadUpItem(GameObject):
    image = None

    def __init__(self, x=0, y=0):
        super().__init__(x, y)
        data = itemData['reload']

        if self.image is None:
            self.image = load_image(data['image'])

        self.colBox = CollisionBox(data['cx'], data['cx'] + data['cw'], data['cy'], data['cy'] + data['ch'])

    def GetCollisionBox(self):
        x, y = self.x - self.image.w / 2, self.y - self.image.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.draw(x, y)

    def Collision(self, other):
        if isinstance(other, Player.Player):
            other.gun.reload_mul = max(other.gun.reload_mul - 0.3, 0.1)
            self.isDelete = True


class GunItem(GameObject):
    def __init__(self, x=0, y=0, gun_type=None):
        super().__init__(x, y)
        data = itemData[gun_type]
        if type(data['image']) == str:
            data['image'] = load_image(data['image'])
        self.image = data['image']
        self.type = gun_type

        self.colBox = CollisionBox(data['cx'], data['cx'] + data['cw'], data['cy'], data['cy'] + data['ch'])

    def GetCollisionBox(self):
        x, y = self.x - self.image.w / 2, self.y - self.image.h / 2
        return self.colBox.Move(x, y)

    def Draw(self, frame_time):
        x, y = Camera.GetCameraPos(self.x, self.y)
        self.image.draw(x, y)

    def Collision(self, other):
        if isinstance(other, Player.Player) and other.is_get_item:
            if self.type == 'pistol':
                other.gun.change_gun(Gun.pistolData)
            elif self.type == 'machine_gun':
                other.gun.change_gun(Gun.machineGunData)
            elif self.type == 'sniper_rifle':
                other.gun.change_gun(Gun.sniperRifleData)
            self.isDelete = True
