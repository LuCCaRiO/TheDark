import pygame as pg
import math as mt
from entity import Entity
from settings import *
from camera import Camera


class UI(Entity):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(UI, self).__init__(anm, pos, groups, scale_multiply)


class Bar(UI):
    def __init__(self, pos, groups, bar_image, bar_edge_image):
        self.bar_image = bar_image
        self.bar_edge_image = bar_edge_image
        bar = pg.Surface(self.bar_image.get_size(), pg.SRCALPHA)
        bar.blit(bar_image, (0, 0))
        super(Bar, self).__init__([bar], pos, groups)
        self.current_value = 0

    def draw(self, color, height):
        ratio = (self.image.get_width() - 20) / 100
        self.image.blit(HealthBar.scale_up([self.bar_image], 0, TILE_SIZE / 8), (0, 0))
        pg.draw.rect(self.image, color, (10, 10, ratio * self.current_value, height))
        self.image.blit(HealthBar.scale_up([self.bar_edge_image], 0, TILE_SIZE / 8), (0, 0))

    def set_value(self, value):
        if value < 0:
            self.current_value = 0
        elif value > 100:
            self.current_value = 100
        else:
            self.current_value = value
        return self.current_value


class HealthBar(Bar):
    BAR_IMAGE = pg.image.load("images/health_bar.png")
    BAR_EDGE_IMAGE = pg.image.load("images/health_bar_edge.png")
    COLOR = (0, 100, 0, 100)
    HEIGHT = 64

    def __init__(self, pos, groups):
        super(HealthBar, self).__init__(pos, groups, HealthBar.BAR_IMAGE, HealthBar.BAR_EDGE_IMAGE)
        self.set_value(100)
        self.draw(HealthBar.COLOR, HealthBar.HEIGHT)

    def update(self, delta_time):
        self.draw(HealthBar.COLOR, HealthBar.HEIGHT)


class MagicBar(Bar):
    BAR_IMAGE = pg.image.load("images/ability_bar.png")
    BAR_EDGE_IMAGE = pg.image.load("images/ability_bar_edge.png")
    COLOR = (138, 43, 226, 70)
    HEIGHT = 32

    def __init__(self, pos, groups):
        super(MagicBar, self).__init__(pos, groups, MagicBar.BAR_IMAGE, MagicBar.BAR_EDGE_IMAGE)
        self.set_value(100)
        self.draw(MagicBar.COLOR, MagicBar.HEIGHT)

    def update(self, delta_time):
        self.draw(MagicBar.COLOR, MagicBar.HEIGHT)


class Light(UI):
    def __init__(self, pos, groups, radius, get_player):
        image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        super(Light, self).__init__([image], pos, groups, 1)
        self.player = get_player
        self.screen = pg.display.get_surface()
        self.delta_time = RELATION_DELTA_TIME
        self.timer = 0
        self.radius = radius

    def move(self):
        self.pos.x = self.player().rect.centerx - Camera.instance.offset.x - self.image.get_width() // 2
        self.pos.y = self.player().rect.centery - Camera.instance.offset.y - self.image.get_height() // 2
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, (200, 200, 200, 17), (self.radius, self.radius), self.radius - abs(mt.sin(self.timer / 300) * 7))
        pg.draw.circle(self.image, (200, 200, 200, 22), (self.radius, self.radius), self.radius // 1.3 - abs(mt.cos(self.timer / 350) * 7))
        pg.draw.circle(self.image, (200, 200, 200, 27), (self.radius, self.radius), self.radius // 1.8 - abs(mt.cos(self.timer / 400) * 7))

    def update(self, delta_time):
        self.delta_time = delta_time / SECOND
        self.timer += delta_time
        self.move()
        self.draw()