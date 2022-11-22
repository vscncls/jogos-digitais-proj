import pygame

from src.level import Level

class Game:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen

        self.coins = 0

        self.status = 'overworld'

    def create_level(self, level: int):
        self.level = Level(self.screen, level)
        self.status = 'level'
