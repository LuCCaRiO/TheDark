import pygame as pg
from settings import *


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

    def run(self):
        clock = pg.time.Clock()
        while True:
            self.handle_events()
            clock.tick(FPS)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()


if __name__ == "__main__":
    Game().run()
