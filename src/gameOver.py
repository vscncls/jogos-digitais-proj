import pygame
from src.returnToMenuException import ReturnToMenuException

from src.settings import screen_width

class GameOver:
    def __init__(
        self, screen: pygame.surface.Surface
    ) -> None:
        self.screen = screen
        self.small_font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 32)
        self.big_font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 50)

    def event(self, events: list[pygame.event.Event]):
        self.events = events

    def input(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                raise ReturnToMenuException()


    def show(self):
        text = self.big_font.render("GAME OVER", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 400)))

        text = self.small_font.render("Aperte qualquer tecla para continuar", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 500)))

    def run(self):
        self.input()
        self.show()
