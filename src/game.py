import pygame
from src.coins import CoinsCount
from src.deathException import DeathException

from src.level import Level, LevelDoesntExistException, LevelOverException
from src.menu import Menu, MenuStartGameException

from datetime import datetime

from src.scoreboard import Score, Scoreboard


class Game:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen
        self.scoreboard = Scoreboard()

        self.coins = CoinsCount()

        self.create_menu()

    def save_score(self):
        now = datetime.now()
        self.scoreboard.add_score(Score(self.coins.amount(), now))
        self.scoreboard.persist()
        self.coins.zero()

    def create_level(self, level: int):
        self.level = Level(self.screen, level, self.coins)
        self.current_runner = self.level

    def create_menu(self):
        self.menu = Menu(self.screen)
        self.current_runner = self.menu

    # def create_scoreboard(self):
    #     self.scoreboard = Scoreboard(self.screen)
    #     self.current_runner = self.scoreboard

    def run(self):
        try:
            self.current_runner.run()
        except MenuStartGameException:
            self.create_level(0)
        except LevelOverException:
            try:
                self.create_level(self.level.curr_level + 1)
            except LevelDoesntExistException:
                self.save_score()
                self.create_menu()
        except (LevelDoesntExistException, DeathException):
            self.create_menu()
