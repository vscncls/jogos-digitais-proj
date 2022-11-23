import pygame

class MenuStartGameException(Exception):
    pass

class MenuScoreboardException(Exception):
    pass

class Menu:
    def __init__(self, screen: pygame.surface.Surface) -> None:
        self.screen = screen

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            raise MenuStartGameException()

    def run(self):
        self.screen.fill('blue')
        self.get_input()
