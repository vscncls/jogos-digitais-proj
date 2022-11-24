import pygame
import sys
from src.background import Background
from src.game import Game

from src.settings import screen_width, screen_height

pygame.init()

tick_rate = 60

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

game = Game(screen)

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')

    background = pygame.sprite.GroupSingle(Background())
    background.draw(screen)

    game.event(events)
    game.run()

    pygame.display.update()
    clock.tick(tick_rate)
