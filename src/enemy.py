import pygame
from src.tile import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, pos: tuple[int, int], size: int):
        super().__init__(pos, size, "./src/assets/inimigo")
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = 1

    def move(self):
        self.rect.x += self.speed

    def collided_w_block(self):
        self.reverse()

    def reverse(self):
        self.speed *= -1

    def invert_image(self):
        if self.speed < 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        super().update(shift)
        self.move()
        self.invert_image()
