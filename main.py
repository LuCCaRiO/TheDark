import pygame as pg
from map import Map
from settings import *
from entity import UI
from health_bar import HealthBar


class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((1920, 1080), pg.FULLSCREEN)

        self.user_interface = pg.sprite.Group()
        self.create_ui()

        self.map = Map()

    def run(self):
        clock = pg.time.Clock()
        while True:
            delta_time = clock.tick(FPS)
            self.handle_events()

            self.screen.fill((100, 100, 100))
            self.map.update(delta_time)
            self.user_interface.update()
            self.user_interface.draw(self.screen)
            self.health_bar.set_health(self.health_bar.current_health + (delta_time / SECOND) * 10)
            pg.display.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def create_ui(self):
        screen_width, screen_height = self.screen.get_size()

        black_image = pg.image.load("images/black.png")
        image_width, image_height = black_image.get_size()
        UI([black_image], (0, -130), [self.user_interface], screen_width / image_width)

        self.health_bar = HealthBar((10, 10), [self.user_interface])


if __name__ == "__main__":
    Game().run()
