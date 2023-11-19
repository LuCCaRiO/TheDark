import pygame as pg
from map import Map
from settings import *
from user_interface import Light, HealthBar


class Game:
    def __init__(self):
        monitor_size = pg.display.Info()
        self.screen = pg.display.set_mode((monitor_size.current_w, monitor_size.current_h), pg.FULLSCREEN)

        self.map = Map()

        self.health_bar = None

        self.user_interface = pg.sprite.Group()
        self.create_ui()

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
        Light((0, -130), [self.user_interface], self.map.player)

        self.health_bar = HealthBar((10, 10), [self.user_interface])


if __name__ == "__main__":
    pg.init()
    Game().run()
