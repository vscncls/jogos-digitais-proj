import pygame

from src.soundController import SoundController
from src.settings import screen_width


class MenuStartGameException(Exception):
    pass


class MenuScoreboardException(Exception):
    pass


class Menu:
    def __init__(
        self, screen: pygame.surface.Surface, sound_controller: SoundController
    ) -> None:
        self.screen = screen
        self.small_font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 32)
        self.big_font = pygame.font.Font("src/assets/fonts/Pixeled.ttf", 44)
        self.current_selected_option = 0
        self.sound_controller = sound_controller
        self.options = [
            self.start_game,
            self.open_scoreboard,
            self.sound_controller.toggle,
        ]

    def start_game(self):
        raise MenuStartGameException()

    def open_scoreboard(self):
        raise MenuScoreboardException()

    def event(self, events: list[pygame.event.Event]):
        self.events = events

    def input(self):
        for event in self.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.options[self.current_selected_option]()
                elif event.key in (pygame.K_DOWN ,pygame.K_s):
                    self.current_selected_option += 1
                    self.current_selected_option = self.current_selected_option % len(
                        self.options
                    )
                elif event.key in (pygame.K_UP, pygame.K_w):
                    self.current_selected_option -= 1
                    self.current_selected_option = self.current_selected_option % len(
                        self.options
                    )


    def show(self):
        text = self.small_font.render("Aperte SPACE para selecionar", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 100)))
        text = self.small_font.render("use as setinhas para navegar", True, (0, 0, 0))
        self.screen.blit(text, text.get_rect(center=(screen_width / 2, 150)))

        y = 350
        for i in range(len(self.options)):
            font = (
                self.big_font if i == self.current_selected_option else self.small_font
            )
            text = None
            if i == 0:
                text = font.render("Start", True, (0, 0, 0))
            elif i == 1:
                text = font.render("Scoreboad", True, (0, 0, 0))
            elif i == 2:
                text = font.render(
                    "Desmutar" if self.sound_controller.is_muted() else "Mutar",
                    True,
                    (0, 0, 0),
                )
            else:
                raise Exception("Menu text not specified")

            self.screen.blit(text, text.get_rect(center=(screen_width / 2, y)))

            y += 100

    def run(self):
        self.input()
        self.show()
