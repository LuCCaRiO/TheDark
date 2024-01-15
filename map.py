import pygame as pg
import os
import csv

from settings import *
from camera import Camera
from particles import ParticleSystem



class Map:
    def __init__(self, file, camera_sprites, game_instance):
        self.rendered_entities = camera_sprites
        self.dangerous_entities = pg.sprite.Group()
        self.static_entities = pg.sprite.Group()
        self.interactable_entities = pg.sprite.Group()
        self.level_change_entities = pg.sprite.Group()
        self.magic_entities = pg.sprite.Group()
        self.important_entities = pg.sprite.Group()
        self.collision = {"ground": self.static_entities,
                          "danger": self.dangerous_entities,
                          "magic": self.magic_entities,
                          "level": self.level_change_entities,
                          "important": self.important_entities}

        self.game_instance = game_instance

        self.player = None

        self.file = file

        self.create_level(self.read_csv(file))

    def kill(self):
        for sprite in self.rendered_entities.sprites():
            sprite.kill()
            del sprite

    def restart(self):
        self.kill()
        self.game_instance.load_level(self.file)

    @staticmethod
    def read_csv(file_name):
        level = []
        with open(os.path.join(file_name)) as data:
            data = csv.reader(data, delimiter=',')
            for column in data:
                level.append(list(column))
        return level

    def create_level(self, level):
        from player import Player
        from entity import Tile, Magic, LevelPortal, Entity, MagicDashScroll
        from danger import Slime, Spike, Spiky, Grimskull, ShellSlime

        self.rendered_entities.__init__(self.game_instance.get_display())

        for i, row in enumerate(level):
            for j, element in enumerate(row):
                if str.isnumeric(element):
                    Tile([pg.image.load(f"images/Tiles/tiles{element}.png")],
                         (j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.static_entities])
                else:
                    match element:
                        case "d":
                            Spike((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities])
                        case "p":
                            self.player = Player((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities], self.collision, self, self.game_instance)
                        case "s":
                            Slime((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities],
                                self.collision, self.rendered_entities)
                        case "e":
                            Magic((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.magic_entities])
                        case "q":
                            Spiky((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities])
                        case "G":
                            Grimskull((j * TILE_SIZE, i * TILE_SIZE),
                                    [self.rendered_entities, self.dangerous_entities, self.interactable_entities],
                                    self.collision, self.rendered_entities)
                        case "B":
                            LevelPortal((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.level_change_entities])
                        case "h":
                            ShellSlime((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities], self.collision, self.rendered_entities, 7.7)
                        case "UK":
                            Entity([pg.image.load(f"images/boss/boss_test.png")],
                                 (j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.static_entities])
                        case "SCD":
                            MagicDashScroll((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.important_entities])

    def update(self, delta_time, pause):
        for sprite in self.interactable_entities.sprites():
            sprite.instantiate_player(self.player)

        self.rendered_entities.render(delta_time, self.player)
        if not pause:
            self.rendered_entities.update(delta_time)
