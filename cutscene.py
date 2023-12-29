import math

import pygame as pg
from settings import *


class CutScene:
    def __init__(self):
        self.delta_time = None
        self.timer = 0
        self.surface = None

    def start(self):
        pass

    def process(self):
        pass

    def update(self, delta_time):
        self.delta_time = delta_time

    def draw(self, screen):
        pass


class StoryCutScene(CutScene):
    FONT = pg.font.SysFont('Verdana', 70)
    IMAGES = [pg.image.load("images/dark_night2.png"),
              pg.image.load("images/dark_night.png")]
    MUSIC = pg.mixer.Sound("music/intro.wav")

    def __init__(self):
        super(StoryCutScene, self).__init__()
        self.surface = pg.Surface((WIDTH, HEIGHT))

    def start(self):
        pg.mixer.Sound.play(StoryCutScene.MUSIC)

    def end(self):
        pg.mixer.Sound.stop(StoryCutScene.MUSIC)

    def process(self):
        image = pg.transform.scale(StoryCutScene.IMAGES[0], (WIDTH * 1.5, HEIGHT * 1.5))
        dark_image = pg.transform.scale(StoryCutScene.IMAGES[1], (WIDTH * 1.5, HEIGHT * 1.5))
        image_pos = (-50 + math.cos(self.timer / SECOND * 2) * 8, -50 + self.timer / -100)
        dark_image_pos = (image_pos[0], self.timer / 100 - HEIGHT * 0.66)
        time_in_seconds = self.timer / SECOND

        if time_in_seconds > 33:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("You are our only hope", (0, 0))
        elif time_in_seconds > 28:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("You survived as the chosen one", (0, -20))
            self.text("to defeat the underworld's king", (0, 50))
        elif time_in_seconds > 25:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("These creatures are", (0, -20))
            self.text("using mana to live", (0, 50))
        elif time_in_seconds > 20.5:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("He started to transform people", (0, -20))
            self.text("into creatures", (0, 50))
        elif time_in_seconds > 15:
            self.surface.blit(image, image_pos)
            self.text("But no one had any idea", (0, -20))
            self.text("that this was the underworld's king", (0, 50))
        elif time_in_seconds > 10:
            self.surface.blit(image, image_pos)
            self.text("None thought anything of it", (0, 0))
        elif time_in_seconds > 5:
            self.surface.blit(image, image_pos)
            self.text("A mysterious individual with", (0, -20))
            self.text("shining eyes was spotted", (0, 50))
        else:
            self.surface.blit(image, image_pos)
            self.text("Once in a dark night...", (0, 0))

        return  self.timer / SECOND > 36

    def text(self, text, pos):
        text_surface = StoryCutScene.FONT.render(text, False, (255, 255, 255))
        x_pos = (WIDTH // 2) - text_surface.get_width() // 2
        y_pos = (HEIGHT // 2) - text_surface.get_height() // 2
        actual_x = x_pos + pos[0]
        actual_y = y_pos + pos[1]

        if 0 <= actual_x <= WIDTH - text_surface.get_width() and 0 <= actual_y <= HEIGHT - text_surface.get_height():
            self.surface.blit(text_surface, (actual_x, actual_y))

    def update(self, delta_time):
        self.delta_time = delta_time
        self.timer += self.delta_time
        self.surface.fill("black")
        return self.process()

    def get_surface(self):
        return self.surface


class CutSceneManager:
    def __init__(self, screen):
        self.cut_scene = None
        self.cut_scene_running = False
        self.screen = screen

    def start_cut_scene(self, cut_scene):
        if not self.cut_scene_running:
            self.cut_scene = cut_scene
            self.cut_scene.start()
            self.cut_scene_running = True

    def end_cut_scene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self, delta_time):
        if self.cut_scene_running:
            if self.cut_scene.update(delta_time):
                self.cut_scene.end()
                self.end_cut_scene()

    def draw(self):
        if self.cut_scene_running:
            self.screen.blit(self.cut_scene.get_surface(), (0, 0))
