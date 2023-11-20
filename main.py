import pygame as pg
from map import Map
from settings import *
from user_interface import Light, HealthBar, UI


class Game:
    def __init__(self):
        monitor_size = pg.display.Info()
        self.screen = pg.display.set_mode((monitor_size.current_h * TARGET_ASPECT_RATIO,
                                           monitor_size.current_h), pg.FULLSCREEN)

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
            self.user_interface.update(delta_time)
            self.health_bar.set_health(self.map.player.health)
            self.user_interface.draw(self.screen)

            pg.display.update()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

    def create_ui(self):
        screen_width, screen_height = self.screen.get_size()

        dark = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        dark.fill((0, 0, 0, 220))
        UI([dark], (0, 0), [self.user_interface])
        Light((screen_width // 2 - 200, 0), [self.user_interface], 200, self.map.player)

        self.health_bar = HealthBar((10, 10), [self.user_interface])


if __name__ == "__main__":
    pg.init()
    Game().run()
