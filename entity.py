import pygame as pg
from settings import *


class Entity(pg.sprite.Sprite):
    def __init__(self, anm, pos, groups):
        super(Entity, self).__init__(groups)
        print(pos)
        self.scale_up(anm, 0, TILE_SIZE / 8)
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pg.math.Vector2(self.rect.center)

    def scale_up(self, anm, index, scale_multiply):
        self.image = pg.transform.scale(anm[index],
                                        (anm[index].get_width() * scale_multiply,
                                         anm[index].get_height() * scale_multiply))


class MoveableEntity(Entity):
    def __init__(self, anm, pos, groups):
        super(MoveableEntity, self).__init__(anm, pos, groups)
        self.delta_time = 1 / FPS


class Player(MoveableEntity):
    SPEED = 10
    GRAVITY = 0.2
    JUMP_FORCE = -2.3

    def __init__(self, pos, groups, collidable_sprites):
        sprite_sheet = [pg.image.load("images/BlackSprite/blackSprite_0.png"),
                        pg.image.load("images/BlackSprite/blackSprite_1.png"),
                        pg.image.load("images/BlackSprite/blackSprite_2.png"),
                        pg.image.load("images/BlackSprite/blackSprite_3.png")]

        super(Player, self).__init__(sprite_sheet, pos, groups)
        self.anm_index = 0
        self.sprite_sheet = sprite_sheet

        self.direction = pg.math.Vector2()
        self.flipped = False
        self.hitbox = self.rect.inflate(-10, 0)

        self.on_ground = False

        self.collidable_sprites = collidable_sprites

    def animation(self):
        self.anm_index += self.delta_time / 130
        if self.anm_index >= len(self.sprite_sheet) or self.direction.x == 0:
            self.anm_index = 0
        self.scale_up(self.sprite_sheet, int(self.anm_index), TILE_SIZE / 8)

        if self.direction.x < 0 or self.flipped:
            self.image = pg.transform.flip(self.image, True, False)
            self.flipped = True
        if self.direction.x > 0:
            self.flipped = False

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pg.K_w] and self.on_ground:
            self.direction.y = Player.JUMP_FORCE

    def gravity(self):
        self.direction.y += Player.GRAVITY * (self.delta_time / RELATION_DELTA_TIME)

    def move(self):
        self.pos.x += self.direction.x * Player.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.collision(HORIZONTAL)

        self.pos.y += self.direction.y * Player.SPEED * (self.delta_time / RELATION_DELTA_TIME)
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

        self.on_ground = False
        self.collision(VERTICAL)

    def collision(self, direction):
        for sprite in self.collidable_sprites:
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
                        self.on_ground = True
                    elif self.direction.y < 0:
                        self.hitbox.top = sprite.rect.bottom
                    self.direction.y = 0
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def update(self, delta_time):
        self.delta_time = delta_time
        self.input()
        self.gravity()
        self.move()
        self.animation()


class Tile(Entity):
    def __init__(self, img, pos, groups):
        super(Tile, self).__init__(img, pos, groups)
