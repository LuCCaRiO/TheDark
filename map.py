import pygame as pg
import os
import csv

from settings import *
from camera import Camera
from entity import Tile, Player


class Map:
    def __init__(self):
        self.rendered_entities = Camera()
        self.user_interface = pg.sprite.Group()
        self.collidable_entities = pg.sprite.Group()
        self.danger_entities = pg.sprite.Group()
        self.collision = {"ground": self.collidable_entities,
                          "danger": self.danger_entities}

        self.player = None

        self.create_level(self.read_csv("levels/level_1.csv"))

    @staticmethod
    def read_csv(file_name):
        level = []
        with open(os.path.join(file_name)) as data:
            data = csv.reader(data, delimiter=',')
            for column in data:
                level.append(list(column))
        return level

    def create_level(self, level):
        for i, row in enumerate(level):
            for j, element in enumerate(row):
                if str.isnumeric(element):
                    Tile([pg.image.load(f"images/Tiles/tiles{element}.png")],
                         (j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.collidable_entities])
                elif element == "d":
                    Tile([pg.image.load(f"images/Tiles/tiles1.png")],
                         (j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.danger_entities])
                elif element == "p":
                    self.player = Player((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities], self.collision)

    def update(self, delta_time):
        self.rendered_entities.update(delta_time)
        print(self.player)
        self.rendered_entities.render(self.player)
