import random
import pygame as pg
from particles import SlimeParticleSystem
from entity import Magic
from settings import *


class Camera(pg.sprite.Group):
    instance = None

    def __init__(self):
        self.singleton()

        super(Camera, self).__init__()
        self.offset = pg.math.Vector2()
        self.target_offset = pg.math.Vector2()
        self.focus = False

    def singleton(self):
        if Camera.instance is not None:
            del self
        else:
            Camera.instance = self

    def set_focus(self, value):
        self.focus = value

    def render(self, delta_time, player):
        if player is not None:
            if self.focus:
                self.target_offset.x = player.rect.centerx - pg.display.get_surface().get_width() // 2
                self.target_offset.y = player.rect.centery - pg.display.get_surface().get_height() // 2
            else:
                self.target_offset.x = player.rect.centerx - pg.display.get_surface().get_width() // 2
                self.target_offset.y = pg.display.get_surface().get_height() // 3

        factor = 0.14 * (delta_time / RELATION_DELTA_TIME)

        self.offset.x += round((self.target_offset.x - self.offset.x) * factor)
        self.offset.y += round((self.target_offset.y - self.offset.y) * factor)

        sprites = self.sort_algorithm()
        for sprite in sprites:
            pg.display.get_surface().blit(sprite.image, sprite.rect.topleft - self.offset)

    def sort_algorithm(self):
        sprites = []
        sort = [SlimeParticleSystem, Magic]
        for sprite in self.sprites():
            for class_ in sort:
                if sprite.__class__ == class_:
                    sprites.append(sprite)

        for sprite in self.sprites():
            if sprite not in sprites:
                sprites.append(sprite)
        return sprites
