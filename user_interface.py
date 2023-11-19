import pygame as pg
import math as mt
from entity import Entity
from settings import *


class UI(Entity):
    def __init__(self, anm, pos, groups, scale_multiply=TILE_SIZE/8):
        super(UI, self).__init__(anm, pos, groups, scale_multiply)


class HealthBar(UI):
    BAR_IMAGE = pg.image.load("images/health_bar.png")
    BAR_EDGE_IMAGE = pg.image.load("images/health_bar_edge.png")

    def __init__(self, pos, groups):
        health_bar = pg.Surface(HealthBar.BAR_IMAGE.get_size(), pg.SRCALPHA)
        health_bar.blit(HealthBar.BAR_IMAGE, (0, 0))
        super(HealthBar, self).__init__([health_bar], pos, groups)
        self.current_health = 0
        self.set_health(0)
        self.draw_health()

    def draw_health(self):
        ratio = (self.image.get_width() - 20) / 100
        self.image.blit(HealthBar.scale_up([HealthBar.BAR_IMAGE], 0, TILE_SIZE / 8), (0, 0))
        pg.draw.rect(self.image, (0, 100, 0, 100), (10, 10, ratio * self.current_health, 64))
        self.image.blit(HealthBar.scale_up([HealthBar.BAR_EDGE_IMAGE], 0, TILE_SIZE / 8), (0, 0))

    def set_health(self, health_to_set):
        if health_to_set < 0:
            self.current_health = 0
        elif health_to_set > 100:
            self.current_health = 100
        else:
            self.current_health = health_to_set
        return self.current_health

    def update(self, delta_time):
        self.draw_health()


class Light(UI):
    def __init__(self, pos, groups, radius, player):
        image = pg.Surface((radius * 2, radius * 2), pg.SRCALPHA)
        super(Light, self).__init__([image], pos, groups, 1)
        self.player = player
        self.screen = pg.display.get_surface()
        self.delta_time = RELATION_DELTA_TIME
        self.timer = 0
        self.radius = radius

    def move(self):
        screen_height = self.screen.get_height()

        self.pos.y = self.player.hitbox.top - screen_height // 2
        self.rect.y = round(self.pos.y)

    def draw(self):
        self.image.fill((0, 0, 0, 0))
        pg.draw.circle(self.image, (255, 255, 255, 65), (self.radius, self.radius), self.radius - abs(mt.sin(self.timer / 300) * 10))
        pg.draw.circle(self.image, (255, 255, 255, 80), (self.radius, self.radius), self.radius // 1.3 - abs(mt.cos(self.timer / 350) * 10))
        pg.draw.circle(self.image, (255, 255, 255, 95), (self.radius, self.radius), self.radius // 1.8 - abs(mt.cos(self.timer / 400) * 10))

    def update(self, delta_time):
        self.delta_time = delta_time / SECOND
        self.timer += delta_time
        self.move()
        self.draw()