import pygame

from src.tile import Tile
from src.player import Player
from src.settings import tile_size, screen_width


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout: list[str]):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for column_index, column in enumerate(row):
                x = tile_size * column_index
                y = tile_size * row_index

                if column == "X":
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif column == "P":
                    player = Player((x, y))
                    self.player.add(player)

    def scroll_x(self):
        player: Player = self.player.sprite  # type: ignore
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < (screen_width * 0.2) and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > (screen_width * 0.8) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.default_speed

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite  # type: ignore
        player.rect.x += int(player.direction.x) * player.speed

        for sprite in self.tiles.sprites():
            tile: Tile = sprite  # type: ignore
            if tile.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = tile.rect.right
                elif player.direction.x > 0:
                    player.rect.right = tile.rect.left

    def vertical_movement_collision(self):
        player: Player = self.player.sprite  # type: ignore
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            tile: Tile = sprite  # type: ignore
            if tile.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = tile.rect.bottom
                    player.direction.y = 0
                elif player.direction.y > 0:
                    player.rect.bottom = tile.rect.top
                    player.direction.y = 0

    def run(self):
        self.tiles.update(self.world_shift, 0)
        self.tiles.draw(self.display_surface)
        self.scroll_x()

        self.player.update()
        self.vertical_movement_collision()
        self.horizontal_movement_collision()
        self.player.draw(self.display_surface)
