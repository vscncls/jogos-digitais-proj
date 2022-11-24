import pygame
from src.deathException import DeathException
from src.helper import import_folder

from datetime import datetime


class Player(pygame.sprite.Sprite):
    rect: pygame.rect.Rect
    direction: pygame.math.Vector2

    default_speed = 3
    gravity = 0.65
    jump_speed = 13
    animation_speed = 0.1

    invincibility_duration_ms = 800

    max_health = 5

    _running_animations: list[pygame.surface.Surface]
    _idle_animations: list[pygame.surface.Surface]

    def __import_assets(self):
        self._idle_animations = import_folder(f"src/assets/player/idle")
        self._running_animations = import_folder(f"src/assets/player/run")

    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = self.default_speed
        self.animation_frame = 0

        self.status = "idle"
        self.facing_right = True
        self.on_left = False
        self.on_right = False
        self.on_ground = False
        self.on_ceiling = False

        self.__import_assets()

        self.image = self._running_animations[self.animation_frame]

        self.rect = self.image.get_rect(topleft=pos)

        self.health = self.max_health
        self.last_damage_time = datetime.now()
        self.become_invincible()

    def become_invincible(self):
        self.last_damage_time = datetime.now()
        self.invincible = True

    def remove_invincibility(self):
        self.invincible = False

    def damage(self):
        if self.invincible:
            return False

        self.health -= 1
        if self.health == 0:
            raise DeathException()

        self.become_invincible()

        return True

    def animate(self):
        self.animation_frame += self.animation_speed
        animations = self._idle_animations if self.status == 'idle' else self._running_animations
        if self.animation_frame >= len(animations):
            self.animation_frame = 0
        current_frame = animations[int(self.animation_frame)]
        if self.invincible:
            # copy to not dirty animation buffer
            current_frame = current_frame.copy()
            current_frame.set_alpha(100 if self.invincible else 0)
        if not self.facing_right:
            current_frame = pygame.transform.flip(current_frame, True, False)
        self.image = current_frame

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.status = 'running'
            self.facing_right = True
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.status = 'running'
            self.facing_right = False
            self.direction.x = -1
        else:
            self.status = 'idle'
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            if self.on_ground:
                self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += int(self.direction.y)

    def jump(self):
        self.direction.y -= self.jump_speed

    def update(self):
        self.input()
        self.animate()

        if (
            self.invincible
            and ((datetime.now() - self.last_damage_time).microseconds / 1000)
            > self.invincibility_duration_ms
        ):
            self.remove_invincibility()
