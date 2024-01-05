import math

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
    COLOR = (0, 120, 0, 200)
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
    COLOR = (95, 0, 183, 200)
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
        distance = pg.math.Vector2((Camera.instance.offset.x - self.player().pos.x) * 2 + pg.display.get_surface().get_width(), 0)
        self.pos.x = self.player().rect.centerx - Camera.instance.offset.x + distance.x - self.image.get_width() // 2
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


class Dialogue(Entity):
    IMAGE = pg.transform.scale(pg.image.load("images/dialogue.png"), (WIDTH // 1.5, 300))
    CONTINUE_IMAGE = pg.transform.scale(pg.image.load("images/continue.png"), (50, 50))
    FONT = pg.font.SysFont("joystixmonospaceregular", 50)

    def __init__(self, text, pos, groups):
        super(Dialogue, self).__init__([Dialogue.IMAGE], pos, groups)
        self.surface = pg.Surface((Dialogue.IMAGE.get_width(), Dialogue.IMAGE.get_height()), pg.SRCALPHA)
        self.rect.topleft = (WIDTH // 2 - Dialogue.IMAGE.get_width() // 2, HEIGHT - Dialogue.IMAGE.get_height())
        self.text = text
        self.text_index = 0
        self.element = 0
        self.delta_time = RELATION_DELTA_TIME
        self.pressed = False
        self.timer = 0
        self.running = True

    def render_text(self, text):
        output = ""
        for element in range(int(self.element)):
            output += text[element]

        rendered_text = Dialogue.FONT.render(output, False, (0, 0, 0))
        self.surface.blit(rendered_text, (Dialogue.IMAGE.get_width() // 2 - rendered_text.get_width() // 2, self.surface.get_height() // 2 - rendered_text.get_height() // 2))

    def input(self):
        keys = pg.key.get_pressed()
        if not self.pressed and keys[pg.K_SPACE]:
            self.pressed = True
            if self.text_index < len(self.text) - 1:
                self.text_index += 1
                self.element = 0
            else:
                self.kill()
                self.running = False
        elif self.pressed and not keys[pg.K_SPACE]:
            self.pressed = False

    def update(self, delta_time):
        self.delta_time = delta_time
        self.timer += self.delta_time

        if self.element <= len(self.text[self.text_index]):
            self.element += (self.delta_time / RELATION_DELTA_TIME) * 0.3

        self.input()
        self.surface.blit(Dialogue.IMAGE, (0, 0))
        self.render_text(self.text[self.text_index])

        c_img = Dialogue.CONTINUE_IMAGE
        c_x = self.surface.get_width() - c_img.get_width() - 40
        c_y = self.surface.get_height() - c_img.get_height() - 40 + math.sin(self.timer / 200) * 7
        self.surface.blit(Dialogue.CONTINUE_IMAGE, (c_x, c_y))

        self.image = self.surface
