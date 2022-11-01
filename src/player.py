import pygame
from src.helper import get_assets
import datetime

class Player(pygame.sprite.Sprite):
    rect: pygame.rect.Rect
    direction: pygame.math.Vector2

    default_speed = 8
    gravity = .8
    jump_speed = 3
    animation_speed = 0.1

    _animations:  list[pygame.surface.Surface]

    def __import_assets(self):
        self._animations = get_assets(f'player/run')

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = self.default_speed
        self.animation_frame = 0
        self.last_jump = datetime.datetime(1, 1, 1)

        self.__import_assets()

        self.image = self._animations[self.animation_frame]

        self.rect = self.image.get_rect(topleft=pos)

    def animate(self):

        self.animation_frame += self.animation_speed
        if self.animation_frame >= len(self._animations):
            self.animation_frame = 0
        current_frame = self._animations[int(self.animation_frame)]
        self.image = current_frame

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += int(self.direction.y)

    def jump(self):
        now = datetime.datetime.now()
        print((now - self.last_jump).seconds)
        if (now - self.last_jump).seconds < 1:
            return

        self.last_jump = now
        self.direction.y -= self.jump_speed

    def update(self):
        self.get_input()
        self.animate()
