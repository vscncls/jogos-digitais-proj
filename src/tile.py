import pygame
from src.helper import import_folder


class Tile(pygame.sprite.Sprite):
    image: pygame.surface.Surface
    rect: pygame.rect.Rect

    def __init__(self, pos: tuple[int, int], size: int):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift: int):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(
        self, pos: tuple[int, int], size: int, surface: pygame.surface.Surface
    ):
        super().__init__(pos, size)
        self.image = surface

class AnimatedTile(Tile):
    animation_speed = .1
    def __init__(self, pos: tuple[int, int], size: int, path: str):
        super().__init__(pos, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift: int):
        super().update(x_shift)
        self.animate()

class Coin(AnimatedTile):
    def __init__(self, pos: tuple[int, int], size: int):
        super().__init__(pos, size, "./src/assets/moeda")
        center_x = pos[0] + int(size/2)
        center_y = pos[1] + int(size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))

