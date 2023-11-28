import pygame as pg
from map import Map
from settings import *
from user_interface import Light, HealthBar, MagicBar, UI


class Game:
    def __init__(self):
        monitor_size = pg.display.Info()
        self.screen = pg.display.set_mode((monitor_size.current_h * TARGET_ASPECT_RATIO,
                                           monitor_size.current_h), pg.FULLSCREEN)

        self.map = Map()

        self.dark = None
        self.health_bar = None
        self.magic_bar = None

        self.time = NORMAL_TIME
        self.ability_on = False

        self.user_interface = pg.sprite.Group()
        self.create_ui()

    def run(self):
        clock = pg.time.Clock()
        while True:
            delta_time = clock.tick(FPS)
            self.handle_events()

            self.screen.fill((75, 75, 75))
            self.ability_mode(delta_time)
            delta_time *= self.time
            self.map.update(delta_time)

            if self.ability_on:
                self.dark.image.fill(ABILITY_COLOR)
            else:
                self.dark.image.fill(NORMAL_COLOR)

            self.user_interface.update(delta_time)
            self.health_bar.set_value(self.map.player.health)
            self.magic_bar.set_value(self.map.player.magic)
            self.user_interface.draw(self.screen)

            pg.display.update()

    def ability_mode(self, delta_time):
        if self.map.player.magic <= 0:
            self.ability_on = False
            self.time = NORMAL_TIME
        elif self.ability_on:
            self.map.player.set_magic(self.map.player.magic - (delta_time / RELATION_DELTA_TIME) * 0.33)

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    self.map.player.jump()
                if event.key == pg.K_SPACE:
                    if not self.ability_on:
                        self.ability_on = True
                        self.time = ABILITY_TIME
                    else:
                        self.ability_on = False
                        self.time = NORMAL_TIME

    def create_ui(self):
        screen_width, screen_height = self.screen.get_size()

        dark = pg.Surface(self.screen.get_size(), pg.SRCALPHA)
        dark.fill(NORMAL_COLOR)

        self.dark = UI([dark], (0, 0), [self.user_interface])
        Light((screen_width // 2 - 200, 0), [self.user_interface], 200, self.map.player)

        self.health_bar = HealthBar((10, 10), [self.user_interface])
        self.magic_bar = MagicBar((10, 100), [self.user_interface])


if __name__ == "__main__":
    pg.init()
    Game().run()
