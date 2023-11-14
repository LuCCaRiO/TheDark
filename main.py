import pygame as pg
from Entity import Player
from settings import *


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

        self.render_entities = pg.sprite.Group()

        Player((0, 0), [self.render_entities])

    def run(self):
        clock = pg.time.Clock()
        while True:
            delta_time = clock.tick(FPS)

            self.handle_events()

            self.render_entities.update(delta_time)

            self.screen.fill((100, 100, 100))
            self.render_entities.draw(self.screen)

            pg.display.update()


    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()


if __name__ == "__main__":
    Game().run()
