import pygame as pg


class Camera(pg.sprite.Group):
    def __init__(self):
        super(Camera, self).__init__()
        self.offset = pg.math.Vector2()

    def render(self):
        for sprite in self.sprites():
            pg.display.get_surface().blit(sprite.image, sprite.rect.topleft + self.offset)