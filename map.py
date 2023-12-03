import pygame as pg
import os
import csv

from settings import *
from camera import Camera
from entity import Tile, Magic
from player import Player
from danger import Slime, Spike, Spiky, Grimskull
from particles import ParticleSystem


class Map:
    def __init__(self, level):
        self.rendered_entities = Camera()
        self.dangerous_entities = pg.sprite.Group()
        self.collidable_entities = pg.sprite.Group()
        self.interactable_entities = pg.sprite.Group()
        self.magic_entities = pg.sprite.Group()
        self.collision = {"ground": self.collidable_entities,
                          "danger": self.dangerous_entities,
                          "magic": self.magic_entities}

        self.player = None

        self.level = level

        self.create_level(self.read_csv(level))

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
                    Spike((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities])
                elif element == "p":
                    self.player = Player((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities], self.collision)
                elif element == "s":
                    Slime((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities], self.collision)
                elif element == "e":
                    Magic((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.magic_entities])
                elif element == "q":
                    Spiky((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities])
                elif element == "G":
                    Grimskull((j * TILE_SIZE, i * TILE_SIZE), [self.rendered_entities, self.dangerous_entities, self.interactable_entities], self.collision)

    def update(self, delta_time):
        for sprite in self.interactable_entities.sprites():
            sprite.instantiate_player(self.player)

        self.rendered_entities.update(delta_time)
        self.rendered_entities.render(delta_time, self.player)
