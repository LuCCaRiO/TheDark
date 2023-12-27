import pygame as pg
import os
import csv

from settings import *
from camera import Camera
from particles import ParticleSystem



class Map:
    def __init__(self, level, camera_sprites):
        self.rendered_entities = camera_sprites
        self.dangerous_entities = pg.sprite.Group()
        self.collidable_entities = pg.sprite.Group()
        self.interactable_entities = pg.sprite.Group()
        self.level_change_entities = pg.sprite.Group()
        self.magic_entities = pg.sprite.Group()
        self.collision = {"ground": self.collidable_entities,
                          "danger": self.dangerous_entities,
                          "magic": self.magic_entities,
                          "level": self.level_change_entities}

        self.player = None

        self.level = level

        self.create_level(self.read_csv(level))

    def kill(self):
        for sprite in self.rendered_entities.sprites():
            sprite.kill()
            del sprite

    def restart(self):
        self.kill()
        self.create_level(self.read_csv(self.level))

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
        from entity import Tile, Magic, LevelPortal
        from danger import Slime, Spike, Spiky, Grimskull

        for i, row in enumerate(level):
            for j, element in enumerate(row):
                if str.isnumeric(element):
                    Tile([pg.image.load(f"images/Tiles/tiles{element}.png")],
                         (j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.collidable_entities])
                else:
                    match element:
                        case "d":
                            Spike((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities])
                        case "p":
                            self.player = Player((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities], self.collision, self)
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
                                    self.collision)
                        case "B":
                            LevelPortal((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.level_change_entities])

    def update(self, delta_time):
        for sprite in self.interactable_entities.sprites():
            sprite.instantiate_player(self.player)

        self.rendered_entities.update(delta_time)
        self.rendered_entities.render(delta_time, self.player)
