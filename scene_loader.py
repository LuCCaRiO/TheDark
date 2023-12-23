import pygame as pg
from main import Game


class SceneLoader:
    instance = None

    def __init__(self, game):
        self.singleton()
        self.game_instance = game

    def singleton(self):
        if SceneLoader.instance is None:
            SceneLoader.instance = self
        else:
            del self

    def load_level(self, file):
        self.game_instance.load_level(file)

    def next_level(self):
        self.game_instance.next_level()
