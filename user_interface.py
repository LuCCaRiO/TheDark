import pygame as pg
from entity import Entity
from settings import *


class UI(Entity):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(UI, self).__init__(anm, pos, groups, scale_multiply)


class HealthBar(UI):
    BAR_IMAGE = pg.image.load("images/health_bar.png")
    BAR_EDGE_IMAGE = pg.image.load("images/health_bar_edge.png")

    def __init__(self, pos, groups):
        health_bar = pg.Surface(HealthBar.BAR_IMAGE.get_size())
        health_bar.blit(HealthBar.BAR_IMAGE, (0, 0))
        super(HealthBar, self).__init__([health_bar], pos, groups)
        self.current_health = 0
        self.set_health(0)
        self.draw_health()

    def draw_health(self):
        ratio = (self.image.get_width() - 20) / 100
        self.image.blit(HealthBar.scale_up([HealthBar.BAR_IMAGE], 0, TILE_SIZE / 8), (0, 0))
        pg.draw.rect(self.image, (0, 50, 0), (10, 10, ratio * self.current_health, 64))
        self.image.blit(HealthBar.scale_up([HealthBar.BAR_EDGE_IMAGE], 0, TILE_SIZE / 8), (0, 0))

    def set_health(self, health_to_set):
        if health_to_set < 0:
            self.current_health = 0
        elif health_to_set > 100:
            self.current_health = 100
        else:
            self.current_health = health_to_set
        return self.current_health

    def update(self):
        self.draw_health()


class Light(UI):
    LIGHT_IMAGE = pg.image.load("images/black.png")

    def __init__(self, pos, groups, player):
        screen_width = pg.display.get_surface().get_width()
        image_width = Light.LIGHT_IMAGE.get_width()
        super(Light, self).__init__([Light.LIGHT_IMAGE], pos, groups, screen_width / image_width)
        self.player = player

    def move(self):
        self.pos.y = self.player.pos.y - pg.display.get_surface().get_height()
        self.rect.y = round(self.pos.y)

    def update(self):
        self.move()