import pygame as pg
from entity import MoveableEntity
from settings import *
from particles import SlimeParticleSystem


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
    KNOCKBACK = 60
    SPEED = 3
    SPAWN_PARTICLE_TIME = 0.2
    
    def __init__(self, pos, groups, collidable_sprites):
        super(Slime, self).__init__([Slime.SLIME_IMAGE], pos, groups, Slime.DAMAGE)
        self.direction = pg.math.Vector2(1, 0)
        self.collidable_sprites = collidable_sprites
        self.flip = False
        self.particle_timer = 0

    def move(self):
        self.pos.x += self.direction.x * Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.x = round(self.pos.x)

    def detect_collision(self):
        for sprite in self.collidable_sprites["ground"]:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left - self.direction.x * Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
                else:
                    self.rect.left = sprite.rect.right + self.direction.x * Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
                self.direction.x *= -1

    def animation(self):
        if self.direction.x > 0 and not self.flip:
            self.flip = True
            self.image = pg.transform.flip(self.image, True, False)
        elif self.direction.x < 0 and self.flip:
            self.flip = False
            self.image = pg.transform.flip(self.image, True, False)

    def create_particles(self):
        self.particle_timer += self.delta_time
        if self.particle_timer > Slime.SPAWN_PARTICLE_TIME * SECOND:
            self.particle_timer = 0
            pos = self.rect.center + pg.math.Vector2(0, 8) if self.direction.x < 0 else self.rect.midleft + pg.math.Vector2(-8, 8)

            SlimeParticleSystem(pos, (50, 50), self.groups()[0], 3, 2).start()

    def update(self, delta_time):
        self.delta_time = delta_time
        self.mask = pg.mask.from_surface(self.image)
        self.detect_collision()
        self.animation()
        self.move()
        self.create_particles()


class Spike(Danger):
    SPIKE_IMAGE = pg.image.load("images/Tiles/tiles1.png")
    DAMAGE = 100
    KNOCKBACK = 0

    def __init__(self, pos, groups):
        super(Spike, self).__init__([Spike.SPIKE_IMAGE], pos, groups, Spike.DAMAGE)


class Spiky(Danger):
    SPIKY_IMAGE = pg.image.load("images/spikey.png")
    DAMAGE = 50
    KNOCKBACK = 100

    def __init__(self, pos, groups):
        super(Spiky, self).__init__([Spiky.SPIKY_IMAGE], pos, groups, Spiky.DAMAGE)
