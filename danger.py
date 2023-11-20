import pygame as pg
from entity import MoveableEntity


class Danger(MoveableEntity):
    def __init__(self, anm, pos, groups, damage):
        super(Danger, self).__init__(anm, pos, groups)
        self.mask = pg.mask.from_surface(self.image)
        self.damage = damage

    def get_damage(self):
        return self.damage


class Enemy(Danger):
    def __init__(self, anm, pos, groups, damage):
        super(Enemy, self).__init__(anm, pos, groups, damage)
        self.health = 0
        self.set_health(100)

    def set_health(self, value):
        if value < 0:
            self.health = 0
        elif value > 100:
            self.health = 100


class Slime(Enemy):
    SLIME_IMAGE = pg.image.load("images/slime.png")
    DAMAGE = 34
    
    def __init__(self, pos, groups):
        super(Slime, self).__init__([Slime.SLIME_IMAGE], pos, groups, Slime.DAMAGE)

    def update(self, delta_time):
        self.delta_time = delta_time


class Spike(Danger):
    SPIKE_IMAGE = pg.image.load("images/Tiles/tiles1.png")
    DAMAGE = 100

    def __init__(self, pos, groups):
        super(Spike, self).__init__([Spike.SPIKE_IMAGE], pos, groups, Spike.DAMAGE)
