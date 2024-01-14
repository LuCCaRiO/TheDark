import math

import pygame as pg
from entity import MoveableEntity
from settings import *
from particles import SlimeParticleSystem, GrimskullParticleSystem


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
    
    def __init__(self, pos, groups, collidable_sprites, camera):
        super(Slime, self).__init__([Slime.SLIME_IMAGE], pos, groups, Slime.DAMAGE)
        self.direction = pg.math.Vector2(1, 0)
        self.collidable_sprites = collidable_sprites
        self.flip = False
        self.particle_timer = 0
        self.camera = camera

    def move(self):
        self.pos.x += self.direction.x * Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.x = round(self.pos.x)

    def detect_collision(self):
        for sprite in self.collidable_sprites["ground"]:
            if sprite.rect.colliderect(self.rect):
                if self.direction.x > 0:
                    self.rect.right = sprite.rect.left - Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
                else:
                    self.rect.left = sprite.rect.right + Slime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
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

            SlimeParticleSystem(pos, (50, 50), self.camera, 3, 2).start()

    def update(self, delta_time):
        self.delta_time = delta_time
        self.mask = pg.mask.from_surface(self.image)
        self.detect_collision()
        self.move()
        self.animation()

        if len(self.groups()) > 1:
            self.create_particles()


class ShellSlime(Enemy):
    IMAGE = pg.image.load("images/shell_slime.png").convert_alpha()
    DAMAGE = 50
    KNOCKBACK = 100
    SPEED = 18
    DEATH_HEIGHT = 1200

    def __init__(self, pos, groups, collidable_sprites, camera):
        super(ShellSlime, self).__init__([ShellSlime.IMAGE], pos, groups, ShellSlime.DAMAGE)

        self.direction = pg.math.Vector2(-1, 0)
        self.collidable_sprites = collidable_sprites
        self.dead = False
        self.angle = 0
        self.camera = camera
        self.moving = False
        self.image_copy = self.image

    def move(self):
        self.pos.x += self.direction.x * ShellSlime.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.x = round(self.pos.x)
        if not self.dead:
            self.collision()
        self.pos.y += self.direction.y * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.y = round(self.pos.y)

    def collision(self):
        for sprite in self.collidable_sprites["ground"]:
            if self.rect.colliderect(sprite.rect):
                self.dead = True
                self.direction.y = -10
                self.direction.x = 0
                self.image_copy.set_alpha(170)
                self.groups()[self.groups().index(self.collidable_sprites["danger"])].remove(self)

    def death(self):
        self.angle += (self.delta_time / RELATION_DELTA_TIME) * 3
        self.image = pg.transform.rotate(self.image_copy, self.angle)
        self.direction.y += (self.delta_time / RELATION_DELTA_TIME)
        if self.pos.y > ShellSlime.DEATH_HEIGHT:
            self.kill()

    def update(self, delta_time):
        if (self.camera.get_target_offset().x + WIDTH) >= self.rect.left - TILE_SIZE:
            self.moving = True
        self.delta_time = delta_time
        print(self.camera.get_target_offset().x)
        if self.moving:
            self.move()
            if self.dead:
                self.death()


class Spike(Danger):
    SPIKE_IMAGE = pg.image.load("images/Tiles/tiles1.png")
    DAMAGE = 100
    KNOCKBACK = 0

    def __init__(self, pos, groups):
        super(Spike, self).__init__([Spike.SPIKE_IMAGE], pos, groups, Spike.DAMAGE)


class Spiky(Danger):
    SPIKY_IMAGE = pg.image.load("images/spikey.png")
    DAMAGE = 15
    KNOCKBACK = 100

    def __init__(self, pos, groups):
        super(Spiky, self).__init__([Spiky.SPIKY_IMAGE], pos, groups, Spiky.DAMAGE)


class Grimskull(Enemy):
    IMAGES = [pg.image.load("images/grimskull.png"),
              pg.image.load("images/attack.png")]
    DAMAGE = 30
    SPEED = 6
    GRAVITY = 0.5
    KNOCKBACK = 80

    def __init__(self, pos, groups, collidable_sprites, camera):
        super(Grimskull, self).__init__(Grimskull.IMAGES, pos, groups, Grimskull.DAMAGE)
        self.direction = pg.math.Vector2(0, 0)
        self.collidable_sprites = collidable_sprites
        self.hitbox = self.rect
        self.player = None
        self.flip = False
        self.state = "normal"
        self.on_ground = False
        self.camera = camera

    def instantiate_player(self, instance):
        self.player = instance

    def animation(self):
        if self.state == "attack":
            self.image = self.scale_up(Grimskull.IMAGES, 1, TILE_SIZE / 8)
        elif self.state == "normal":
            self.image = self.scale_up(Grimskull.IMAGES, 0, TILE_SIZE / 8)

        if self.direction.x < 0 or self.flip:
            self.image = pg.transform.flip(self.image, True, False)
            self.flip = True
        if self.direction.x > 0:
            self.flip = False

    def detect_ground(self, direction):
        for sprite in self.collidable_sprites["ground"]:
            if sprite.rect.colliderect(self.rect):
                if direction == HORIZONTAL:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.direction.x = 0
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.left

                elif direction == VERTICAL:

                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

                    self.direction.y = 0
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.top

    def detect_collision(self):
        self.on_ground = False
        for sprite in self.collidable_sprites["ground"]:
            if abs(sprite.pos.x - self.pos.x) < TILE_SIZE - 9:
                if sprite.rect.top == self.rect.bottom:
                    self.on_ground = True

        for sprite in self.collidable_sprites["danger"]:
            if sprite is not self:
                if self.mask.overlap(sprite.mask, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)):
                    GrimskullParticleSystem((self.rect.centerx, self.rect.top), (50, 100), self.camera, 2, 5).start()
                    self.kill()

    def move(self):
        self.pos.x += self.direction.x * Grimskull.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.x = round(self.pos.x)

        self.detect_ground(HORIZONTAL)

        distance = self.player.rect.centerx - self.rect.centerx
        self.direction.x = 0 if distance == 0 else distance // abs(distance)

        if abs(self.player.pos.x - self.pos.x) <= Grimskull.SPEED * (self.delta_time / RELATION_DELTA_TIME):
            self.direction.x = 0

        self.pos.y += self.direction.y * (self.delta_time / RELATION_DELTA_TIME)
        self.rect.y = round(self.pos.y)

        self.detect_ground(VERTICAL)

    def gravity(self):
        self.direction.y += Grimskull.GRAVITY * (self.delta_time / RELATION_DELTA_TIME)

    def attack(self):
        self.direction.y = -13
        distance = self.player.rect.centerx - self.rect.centerx
        self.direction.x = 0 if distance == 0 else distance // abs(distance)

        self.direction.x *= 1.2

    def update(self, delta_time):
        self.delta_time = delta_time
        self.gravity()
        self.move()
        self.detect_collision()
        if self.on_ground:
            self.state = "normal"

        self.animation()

        distance = math.hypot(abs(self.player.rect.centerx - self.rect.centerx),
                              abs(self.player.rect.centery - self.rect.centery))
        if self.on_ground and distance < 250:
            self.attack()
            self.state = "attack"
