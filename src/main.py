import pygame
import sys
from src.background import Background

from src.settings import screen_width, screen_height
from level import Level

pygame.init()

tick_rate = 60

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

level = Level(screen, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('black')

    background = pygame.sprite.GroupSingle(Background())
    background.draw(screen)

    level.run()

    pygame.display.update()
    clock.tick(tick_rate)
