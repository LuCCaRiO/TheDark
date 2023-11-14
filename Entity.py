import pygame as pg
from settings import *


class Entity(pg.sprite.Sprite):
    def __init__(self, anm, pos, groups):
        super(Entity, self).__init__(groups)
        self.scale_up(anm, 0)
        self.rect = self.image.get_rect(topleft=pos)

    def scale_up(self, anm, index):
        self.image = pg.transform.scale(anm[index],
                                        (anm[index].get_width() * SCALE_MULTIPLY, anm[index].get_height() * SCALE_MULTIPLY))


class MoveableEntity(Entity):
    def __init__(self, anm, pos, groups):
        super(MoveableEntity, self).__init__(anm, pos, groups)
        self.delta_time = 1 / FPS


class Player(MoveableEntity):
    def __init__(self, pos, groups):
        sprite_sheet = [pg.image.load("images/BlackSprite/blackSprite_0.png"),
                        pg.image.load("images/BlackSprite/blackSprite_1.png"),
                        pg.image.load("images/BlackSprite/blackSprite_2.png"),
                        pg.image.load("images/BlackSprite/blackSprite_3.png")]
        super(Player, self).__init__(sprite_sheet, pos, groups)
        self.anm_index = 0
        self.sprite_sheet = sprite_sheet

    def animation(self):
        self.anm_index += self.delta_time / 130
        if self.anm_index >= len(self.sprite_sheet):
            self.anm_index = 0
        self.scale_up(self.sprite_sheet, int(self.anm_index))

    def update(self, delta_time):
        self.delta_time = delta_time
        self.animation()
