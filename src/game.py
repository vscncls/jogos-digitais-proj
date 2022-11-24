import pygame
from src.coins import Counter
from src.deathException import DeathException
from src.gameOver import GameOver

from src.level import Level, LevelDoesntExistException, LevelOverException
from src.menu import Menu, MenuScoreboardException, MenuStartGameException

from datetime import datetime
from src.returnToMenuException import ReturnToMenuException

from src.scoreboard import Score, Scoreboard
from src.scoreboardScreen import ScoreboardScreen
from src.soundController import SoundController


class Game:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen
        self.scoreboard = Scoreboard()

        self.coins = Counter()

        self.sound_controller = SoundController()

        self.create_menu()

        self.sound_controller.play_music()

    def save_score(self):
        now = datetime.now()
        self.scoreboard.add_score(Score(self.coins.amount(), now))
        self.scoreboard.persist()
        self.coins.zero()

    def create_level(self, level: int):
        self.level = Level(self.screen, level, self.coins, self.sound_controller)
        self.current_runner = self.level

    def create_menu(self):
        self.menu = Menu(self.screen, self.sound_controller)
        self.current_runner = self.menu

    def create_scoreboard(self):
        self.scoreboard_screen = ScoreboardScreen(self.screen, self.scoreboard)
        self.current_runner = self.scoreboard_screen

    def create_game_over(self):
        self.current_runner = GameOver(self.screen)

    def event(self, events: list[pygame.event.Event]):
        self.events = events

    def run(self):
        try:
            self.current_runner.event(self.events)
            self.current_runner.run()
        except MenuStartGameException:
            self.create_level(0)
        except LevelOverException:
            try:
                self.create_level(self.level.curr_level + 1)
            except LevelDoesntExistException:
                self.save_score()
                self.create_menu()
        except (LevelDoesntExistException, ReturnToMenuException):
            self.create_menu()
        except MenuScoreboardException:
            self.create_scoreboard()
        except DeathException:
            self.create_game_over()
