import pygame as pg
from settings import *


class Entity(pg.sprite.Sprite):
    def __init__(self, anm, pos, groups):
        super(Entity, self).__init__(groups)
        print(pos)
        self.scale_up(anm, 0, TILE_SIZE / 8)
        self.rect = self.image.get_rect(topleft=pos)

    def scale_up(self, anm, index, scale_multiply):
        self.image = pg.transform.scale(anm[index],
                                        (anm[index].get_width() * scale_multiply,
                                         anm[index].get_height() * scale_multiply))


class MoveableEntity(Entity):
    def __init__(self, anm, pos, groups):
        super(MoveableEntity, self).__init__(anm, pos, groups)
        self.delta_time = 1 / FPS


class Player(MoveableEntity):
    SPEED = 7

    def __init__(self, pos, groups):
        sprite_sheet = [pg.image.load("images/BlackSprite/blackSprite_0.png"),
                        pg.image.load("images/BlackSprite/blackSprite_1.png"),
                        pg.image.load("images/BlackSprite/blackSprite_2.png"),
                        pg.image.load("images/BlackSprite/blackSprite_3.png")]

        super(Player, self).__init__(sprite_sheet, pos, groups)
        self.anm_index = 0
        self.sprite_sheet = sprite_sheet
        self.velocity = pg.math.Vector2()

    def animation(self):
        self.anm_index += self.delta_time / 130
        if self.anm_index >= len(self.sprite_sheet) or self.velocity == pg.math.Vector2():
            self.anm_index = 0
        self.scale_up(self.sprite_sheet, int(self.anm_index), TILE_SIZE / 8)

    def move(self):
        keys = pg.key.get_pressed()
        self.velocity = pg.math.Vector2()
        if keys[pg.K_LEFT]:
            self.velocity.x = -Player.SPEED
        if keys[pg.K_RIGHT]:
            self.velocity.x = Player.SPEED
        self.rect.topleft += self.velocity * (self.delta_time / ((1 / FPS) * SECOND))

    def update(self, delta_time):
        self.delta_time = delta_time
        self.move()
        self.animation()


class Tile(Entity):
    def __init__(self, img, pos, groups):
        super(Tile, self).__init__(img, pos, groups)
