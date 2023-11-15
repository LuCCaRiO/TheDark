import pygame as pg


class Camera(pg.sprite.Group):
    def __init__(self):
        super(Camera, self).__init__()
        self.offset = pg.math.Vector2()

    def render(self, player):
        print(player.rect.topleft)
        if player is not None:
            self.offset.x = player.rect.centerx - pg.display.get_surface().get_width() // 2

        for sprite in self.sprites():
            pg.display.get_surface().blit(sprite.image, sprite.rect.topleft - self.offset)