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


class EndOfCutScene(CutScene):
    FONT = pg.font.SysFont('joystixmonospaceregular', 110)

    def  __init__(self):
        super(EndOfCutScene, self).__init__()
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.alpha = 0
        self.text_image = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
        text1 = EndOfCutScene.FONT.render("End of the", False, (255, 255, 255))
        self.text_image.blit(text1, (WIDTH // 2 - text1.get_width() // 2, HEIGHT // 2 - text1.get_height() // 2 - 50))
        text2 = EndOfCutScene.FONT.render("demonstration", False, (255, 255, 255))
        self.text_image.blit(text2, (WIDTH // 2 - text2.get_width() // 2, HEIGHT // 2 - text2.get_height() // 2 + 50))
        self.surface.blit(self.text_image, (WIDTH // 2 - self.text_image.get_width() // 2, HEIGHT // 2 - self.text_image.get_height() // 2))

    def end(self):
        pass

    def get_surface(self):
        return self.surface

    def update(self, delta_time):
        self.delta_time = delta_time
        self.alpha += (self.delta_time / RELATION_DELTA_TIME) * 1.5

        # Ensure alpha is between 0 and 255
        self.alpha = max(0, min(255, self.alpha))

        # Set the alpha value based on the updated self.alpha
        self.text_image.set_alpha(self.alpha)

        # Clear the surface and then redraw the text with the updated alpha
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.text_image, (0, 0))


class StoryCutScene(CutScene):
    FONT = pg.font.SysFont('Verdana', 70)
    IMAGES = [pg.image.load("images/dark_night2.png"),
              pg.image.load("images/dark_night.png")]
    MUSIC = pg.mixer.Sound("music/intro.wav")

    def __init__(self):
        super(StoryCutScene, self).__init__()
        self.surface = pg.Surface((WIDTH, HEIGHT))
        self.timer = 0
        self.alpha = 255

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

        if time_in_seconds > 35:
            surface = pg.Surface((self.surface.get_width(), self.surface.get_height())).convert()
            surface.blit(dark_image, dark_image_pos)
            self.text("You are our only hope", (0, 0), surface)
            surface.set_alpha(self.alpha)
            self.alpha -= (self.delta_time / RELATION_DELTA_TIME) * 4
            self.surface.blit(surface, (0, 0))
        elif time_in_seconds > 33:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("You are our only hope", (0, 0), self.surface)
        elif time_in_seconds > 28:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("You survived as the chosen one", (0, -20), self.surface)
            self.text("to defeat the underworld's king", (0, 50), self.surface)
        elif time_in_seconds > 25:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("Until everyone", (0, -20), self.surface)
            self.text("was transformed", (0, 50), self.surface)
        elif time_in_seconds > 20.5:
            self.surface.blit(dark_image, dark_image_pos)
            self.text("He started to transform people", (0, -20), self.surface)
            self.text("into creatures", (0, 50), self.surface)
        elif time_in_seconds > 15:
            self.surface.blit(image, image_pos)
            self.text("But no one had any idea", (0, -20), self.surface)
            self.text("that this was the underworld's king", (0, 50), self.surface)
        elif time_in_seconds > 10:
            self.surface.blit(image, image_pos)
            self.text("People were scared", (0, 0), self.surface)
        elif time_in_seconds > 5:
            self.surface.blit(image, image_pos)
            self.text("A mysterious figure with", (0, -20), self.surface)
            self.text("shining eyes was spotted", (0, 50), self.surface)
        else:
            self.surface.blit(image, image_pos)
            self.text("Once in a dark night...", (0, 0), self.surface)

        return  self.timer / SECOND > 37

    def text(self, text, pos, surface):
        text_surface = StoryCutScene.FONT.render(text, False, (255, 255, 255))
        x_pos = (WIDTH // 2) - text_surface.get_width() // 2
        y_pos = (HEIGHT // 2) - text_surface.get_height() // 2
        actual_x = x_pos + pos[0]
        actual_y = y_pos + pos[1]

        if 0 <= actual_x <= WIDTH - text_surface.get_width() and 0 <= actual_y <= HEIGHT - text_surface.get_height():
            surface.blit(text_surface, (actual_x, actual_y))

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
