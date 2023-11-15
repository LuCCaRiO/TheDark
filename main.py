import pygame as pg
from map import Map
from settings import *
import time


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

        self.map = Map()

    def run(self):
        clock = pg.time.Clock()
        while True:
            delta_time = clock.tick(FPS)
            self.handle_events()

            self.screen.fill((100, 100, 100))
            self.map.update(delta_time)

            pg.display.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()


if __name__ == "__main__":
    Game().run()
