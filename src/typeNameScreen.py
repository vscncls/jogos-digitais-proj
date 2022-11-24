import pygame

from src.settings import screen_width

class FormCompletedException(Exception):
    name: str
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name

class TypeNameScreen:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 32)

        self.user_text = ""

    def event(self, events: list[pygame.event.Event]):
        self.events = events

    def show(self):
        text = self.font.render(
            f"Parabens! Voce venceu!",
            True,
            (0, 0, 0),
        )

        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 100)))

        text = self.font.render(
            f"Digite seu nome: (aperte ENTER para continuar)",
            True,
            (0, 0, 0),
        )

        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 300)))

        text = self.font.render(
            self.user_text,
            True,
            (0, 0, 0),
        )

        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 400)))

    def input(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and self.user_text:
                    raise FormCompletedException(self.user_text)
                elif event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    self.user_text += event.unicode

    def run(self):
        self.input()
        self.show()
