import pygame


class Player(pygame.sprite.Sprite):
    rect: pygame.rect.Rect
    direction: pygame.math.Vector2

    default_speed = 8
    gravity = .8
    jump_speed = 3

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill("red")
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = self.default_speed

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
        self.direction.y -= self.jump_speed

    def update(self):
        self.get_input()
