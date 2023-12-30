import math
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
                                         anm[index].get_height() * scale_multiply))


class MoveableEntity(Entity):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(MoveableEntity, self).__init__(anm, pos, groups, scale_multiply)
        self.delta_time = 1 / FPS


class Tile(Entity):
    def __init__(self, img, pos, groups):
        super(Tile, self).__init__(img, pos, groups)


class Magic(MoveableEntity):
    IMAGE = pg.image.load("images/magic.png")

    def __init__(self, pos, groups):
        super(Magic, self).__init__([Magic.IMAGE], pos, groups, 6)
        self.pos.x += (TILE_SIZE // 2) - (self.image.get_width()) // 2
        self.mask = pg.mask.from_surface(self.image)
        self.timer = 0
        self.magic = 50

    def animation(self):
        self.pos.y += math.sin(self.timer / 150) * 0.8

    def move(self):
        self.rect.centerx = round(self.pos.x)
        self.rect.centery = round(self.pos.y)

    def update(self, delta_time):
        self.delta_time = delta_time
        self.timer += self.delta_time
        self.animation()
        self.move()


class LevelPortal(MoveableEntity):
    IMAGE = pg.image.load("images/end.png")

    def __init__(self, pos, groups):
        super(LevelPortal, self).__init__([LevelPortal.IMAGE], pos, groups)
        self.timer = 0
        self.mask = pg.mask.from_surface(self.image)

    def update(self, delta_time):
        self.delta_time = delta_time
        self.timer += self.delta_time
        self.pos.x += math.sin(self.timer / SECOND * 5)
        self.pos.y += math.cos(self.timer / SECOND * 5)
        self.rect.midbottom = self.pos
