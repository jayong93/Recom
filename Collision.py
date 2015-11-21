class CollisionBox:
    def __init__(self, l, r, b, t):
        self.left = l
        self.right = r
        self.bottom = b
        self.top = t

    def CollisionCheck(self, cb):
        if self.left >= cb.right or self.right <= cb.left:
            return False
        if self.bottom >= cb.top or self.top <= cb.bottom:
            return False
        return True

    def Move(self, x, y):
        return CollisionBox(self.left + x, self.right + x, self.bottom + y, self.top + y)
