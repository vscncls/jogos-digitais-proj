import pygame
from src.returnToMenuException import ReturnToMenuException

from src.scoreboard import Scoreboard
from src.settings import screen_width

class ScoreboardScreen:
    def __init__(self, screen: pygame.surface.Surface, scoreboard: Scoreboard) -> None:
        self.screen = screen
        self.scoreboard = scoreboard
        self.font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 20)

    def event(self, events: list[pygame.event.Event]):
        self.events = events

    def show(self):
        text = self.font.render(
            f"Aperte qualquer tecla para voltar ao menu",
            True,
            (0, 0, 0),
        )

        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 40)))

        y = 100
        for idx, score in enumerate(self.scoreboard.scores()):
            text = self.font.render(
                    f"{idx} - Nome: {score.name} = Moedas: {score.coins} = Horario: {score.time.strftime('%m/%d/%Y - %H:%M:%S')}",
                True,
                (0, 0, 0),
            )

            self.screen.blit(text, text.get_rect(center=(screen_width / 2, y)))

            y += 80

    def input(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                raise ReturnToMenuException()

    def run(self):
        self.input()
        self.show()
