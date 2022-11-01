import pygame


class Tile(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.rect.Rect

    def __init__(self, pos: tuple[int, int], size: int):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill("grey")
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift: int, y_shift: int):
        self.rect.x += x_shift
        self.rect.y += y_shift
