import pygame as pg
from entity import MoveableEntity
from particles import PlayerParticleSystem
from camera import Camera
from settings import *


class Player(MoveableEntity):
    SPEED = 10
    GRAVITY = 0.7
    JUMP_FORCE = -11.5
    DEATH_HEIGHT = 900
    IMMORTALITY = 1.5
    IMMORTALITY_FADE = 125

    DEATH_SFX = pg.mixer.Sound("sfx/hitHurt.wav")
    HURT_SFX = pg.mixer.Sound("sfx/hitHurt (1).wav")

    def __init__(self, pos, groups, collidable_sprites, map_instance):
        sprite_sheet = {"run": [pg.image.load("images/BlackSprite/BlackSprite0.png"),
                        pg.image.load("images/BlackSprite/BlackSprite1.png")],
                        "fall": [pg.image.load("images/BlackSprite/falling.png")],
                        "heal": [pg.image.load("images/BlackSprite/BlackSprite2.png")]}

        super(Player, self).__init__(sprite_sheet["run"], pos, groups)
        self.start_pos = pg.math.Vector2(pos)
        self.anm_index = 0
        self.sprite_sheet = sprite_sheet

        self.direction = pg.math.Vector2()
        self.flipped = False
        self.hitbox = self.rect.inflate(-12, 0)
        self.on_ground = False
        self.allow_jump = False

        self.collidable_sprites = collidable_sprites

        self.health = 100
        self.magic = 100

        self.immortality_timer = 0
        self.immortal = False

        self.animation_state = "run"

        self.map_instance = map_instance

    def heal(self):
        hp = (self.delta_time / RELATION_DELTA_TIME) * 0.66
        if self.magic > 0 and self.health < 100:
            self.set_magic(self.magic - hp * 1.5)
            self.set_health(self.health + hp)
            self.animation_state = "heal"
            Camera.instance.set_focus(True)
        else:
            Camera.instance.set_focus(False)

    def animation(self):
        self.anm_index += self.delta_time * 0.004

        if self.anm_index >= len(self.sprite_sheet[self.animation_state]) or self.direction.x == 0:
            self.anm_index = 0

        if self.animation_state != "heal" and not self.on_ground:
            self.animation_state = "fall"
            self.anm_index = 0

        self.image = Player.scale_up(self.sprite_sheet[self.animation_state], int(self.anm_index), TILE_SIZE / 8)

        if self.direction.x < 0 or self.flipped:
            self.image = pg.transform.flip(self.image, True, False)
            self.flipped = True
        if self.direction.x > 0:
            self.flipped = False

        if self.immortal:
            self.image.set_alpha(Player.IMMORTALITY_FADE)

    def input(self):
        keys = pg.key.get_pressed()
        self.animation_state = "run"
        if keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pg.K_LALT] and self.on_ground and self.direction.x == 0:
            self.heal()
        else:
            Camera.instance.set_focus(False)

    def jump(self):
        if self.allow_jump:
            if self.on_ground:
                self.direction.y = Player.JUMP_FORCE
            elif self.magic > 0:
                self.direction.y = Player.JUMP_FORCE
                self.allow_jump = False
                pos = self.rect.center + pg.math.Vector2(self.image.get_width() // -2, 0)
                PlayerParticleSystem(pos, (50, 50), self.groups()[0], 1, 4).start()
                self.set_magic(self.magic - 10)

    def restart(self):
        Player.DEATH_SFX.play()
        self.map_instance.restart()

    def set_magic(self, value):
        if 0 > value:
            self.magic = 0
        elif value > 100:
            self.magic = 100
        else:
            self.magic = value

    def set_health(self, value):
        if 0 > value:
            self.health = 0
        elif value > 100:
            self.health = 100
        else:
            self.health = value

    def gravity(self):
        self.direction.y += Player.GRAVITY * (self.delta_time / RELATION_DELTA_TIME)

    def move(self):
        self.pos.x += self.direction.x * Player.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.ground_collision(HORIZONTAL)

        self.pos.y += self.direction.y * (self.delta_time / RELATION_DELTA_TIME)
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

        self.ground_collision(VERTICAL)

    def detect_ground(self):
        self.on_ground = False
        for sprite in self.collidable_sprites["ground"]:
            if abs(sprite.pos.x - self.pos.x) < TILE_SIZE - 9:
                if sprite.rect.top == self.rect.bottom:
                    self.on_ground = True
                    self.allow_jump = True

    def ground_collision(self, direction):
        for sprite in self.collidable_sprites["ground"]:
            if sprite.rect.colliderect(self.hitbox):
                if direction == HORIZONTAL:
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.hitbox.left = sprite.rect.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                elif direction == VERTICAL:

                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom

                    self.direction.y = 0
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def detect_collision(self):
        for sprite in self.collidable_sprites["magic"]:
            mask = pg.mask.from_surface(self.image)
            if mask.overlap(sprite.mask, (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)):
                self.set_magic(self.magic + sprite.magic)
                sprite.kill()

        for sprite in self.collidable_sprites["danger"]:
            mask = pg.mask.from_surface(self.image)
            if mask.overlap(sprite.mask,
                                 (sprite.rect.x - self.rect.x, sprite.rect.y - self.rect.y)) \
                    and not self.immortal:
                self.knockback(sprite)
                self.immortal = True
                self.damage(sprite.get_damage())

    def damage(self, damage):
        if damage >= self.health:
            self.restart()
        else:
            Player.HURT_SFX.play()
            self.health -= damage

    def knockback(self, sprite):
        knockback_direction = (self.pos.x - sprite.pos.x) / abs(self.pos.x - sprite.pos.x) + 0.01  # avoid division by zero
        self.pos.x += knockback_direction * sprite.KNOCKBACK + (sprite.image.get_width() // 2) * knockback_direction
        self.rect.x = round(self.pos.x)
        self.hitbox.x = self.rect.x
        self.direction.x = knockback_direction
        self.ground_collision(HORIZONTAL)
        self.direction.x = 0

    def immortality(self):
        if self.immortal:
            self.immortality_timer += self.delta_time
            if self.immortality_timer > Player.IMMORTALITY * SECOND:
                self.immortal = False
                self.immortality_timer = 0

    def update(self, delta_time):
        if self.pos.y > Player.DEATH_HEIGHT:
            self.restart()

        self.delta_time = delta_time
        self.detect_ground()
        self.input()
        self.gravity()
        self.move()
        self.detect_collision()
        self.immortality()
        self.animation()

