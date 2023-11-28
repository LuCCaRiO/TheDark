import random
import pygame as pg
from particles import SlimeParticleSystem
from entity import Magic


class Camera(pg.sprite.Group):
    def __init__(self):
        super(Camera, self).__init__()
        self.offset = pg.math.Vector2()

    def render(self, player):
        if player is not None:
            self.offset.x = player.rect.centerx - pg.display.get_surface().get_width() // 2
            self.offset.y = pg.display.get_surface().get_height() // 3

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
