import pygame as pg
from settings import *


class Entity(pg.sprite.Sprite):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(Entity, self).__init__(groups)
        self.image = Entity.scale_up(anm, 0, scale_multiply)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pg.math.Vector2(self.rect.center)

    @staticmethod
    def scale_up(anm, index, scale_multiply):
        return pg.transform.scale(anm[index],
                                        (anm[index].get_width() * scale_multiply,
                                         anm[index].get_height() * scale_multiply)).convert_alpha()


class MoveableEntity(Entity):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(MoveableEntity, self).__init__(anm, pos, groups, scale_multiply)
        self.delta_time = 1 / FPS


class Player(MoveableEntity):
    SPEED = 10
    GRAVITY = 0.7
    JUMP_FORCE = -11
    DEATH_HEIGHT = 1200
    KNOCKBACK = 60
    IMMORTALITY = 1.5
    IMMORTALITY_FADE = 125

    def __init__(self, pos, groups, collidable_sprites):
        sprite_sheet = {"run": [pg.image.load("images/BlackSprite/blackSprite_0.png"),
                        pg.image.load("images/BlackSprite/blackSprite_1.png"),
                        pg.image.load("images/BlackSprite/blackSprite_2.png"),
                        pg.image.load("images/BlackSprite/blackSprite_3.png")],
                        "fall": [pg.image.load("images/BlackSprite/falling.png")]}

        super(Player, self).__init__(sprite_sheet["run"], pos, groups)
        self.start_pos = pg.math.Vector2(pos)
        self.anm_index = 0
        self.sprite_sheet = sprite_sheet

        self.direction = pg.math.Vector2()
        self.flipped = False
        self.hitbox = self.rect.inflate(-10, 0)
        self.on_ground = False
        self.allow_jump = False

        self.collidable_sprites = collidable_sprites

        self.health = 100

        self.immortality_timer = 0
        self.immortal = False

    def animation(self):
        self.anm_index += self.delta_time * 0.008

        if self.anm_index >= len(self.sprite_sheet["run"]) or self.direction.x == 0:
            self.anm_index = 0

        if self.on_ground:
            self.image = Player.scale_up(self.sprite_sheet["run"], int(self.anm_index), TILE_SIZE / 8)
        else:
            self.image = Player.scale_up(self.sprite_sheet["fall"], 0, TILE_SIZE / 8)

        if self.direction.x < 0 or self.flipped:
            self.image = pg.transform.flip(self.image, True, False)
            self.flipped = True
        if self.direction.x > 0:
            self.flipped = False

        if self.immortal:
            self.image.set_alpha(Player.IMMORTALITY_FADE)

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def jump(self):
        if self.allow_jump:
            self.direction.y = Player.JUMP_FORCE
            if not self.on_ground:
                self.allow_jump = False

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

    def detect_danger(self):
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
            self.health -= damage

    def restart(self):
        self.__init__(self.start_pos, self.groups(), self.collidable_sprites)

    def knockback(self, sprite):
        knockback_direction = (self.pos.x - sprite.pos.x) / abs(self.pos.x - sprite.pos.x)
        self.pos.x += knockback_direction * Player.KNOCKBACK + (sprite.image.get_width() // 2) * knockback_direction
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
        self.detect_danger()
        self.immortality()
        self.animation()


class Tile(Entity):
    def __init__(self, img, pos, groups):
        super(Tile, self).__init__(img, pos, groups)
