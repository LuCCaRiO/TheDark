import pygame as pg
from entity import MoveableEntity
from settings import *


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
    SPEED = 3
    
    def __init__(self, pos, groups, collidable_sprites):
        super(Slime, self).__init__([Slime.SLIME_IMAGE], pos, groups, Slime.DAMAGE)
        self.direction = pg.math.Vector2(1, 0)
        self.collidable_sprites = collidable_sprites
        self.flip = False

    def move(self):
        self.pos.x += self.direction.x * Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.x = round(self.pos.x)

    def detect_collision(self):
        for sprite in self.collidable_sprites["ground"]:
            if sprite.rect.colliderect(self.rect):
                self.direction.x *= -1

    def animation(self):
        if self.direction.x > 0 and not self.flip:
            self.flip = True
            self.image = pg.transform.flip(self.image, True, False)
        elif self.direction.x < 0 and self.flip:
            self.flip = False
            self.image = pg.transform.flip(self.image, True, False)

    def update(self, delta_time):
        self.delta_time = delta_time
        self.mask = pg.mask.from_surface(self.image)
        self.detect_collision()
        self.animation()
        self.move()

class Spike(Danger):
    SPIKE_IMAGE = pg.image.load("images/Tiles/tiles1.png")
    DAMAGE = 100

    def __init__(self, pos, groups):
        super(Spike, self).__init__([Spike.SPIKE_IMAGE], pos, groups, Spike.DAMAGE)