import pygame
from src.coins import CoinsCount

from src.player import Player

class GUI:
    def __init__(self, screen: pygame.surface.Surface, coins: CoinsCount, player: Player) -> None:
        self.screen = screen

        self.coins = coins
        self.player = player

        self.font = pygame.font.Font('src/assets/fonts/Pixeled.ttf', 32)
        self.health_image = pygame.image.load('./src/assets/heart.png').convert_alpha()
        self.coin_image = pygame.image.load('./src/assets/moeda.png').convert_alpha()


    def render_health(self):
        health_text = self.font.render(f'x {str(self.player.health)}', True, (0,0,0), None)
        self.screen.blit(health_text, (50, -25))

        self.screen.blit(self.health_image, (5,10))

    def render_coins(self):
        health_text = self.font.render(f'x {str(self.coins.amount())}', True, (0,0,0), None)
        self.screen.blit(health_text, (195, -25))

        self.screen.blit(self.coin_image, (150,10))

    def render(self):
        self.render_health()
        self.render_coins()
