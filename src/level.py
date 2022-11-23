import os
import pygame
from src.coins import CoinsCount
from src.deathException import DeathException
from src.gui import GUI
from src.helper import get_layout
from src.player import Player

from src.tile import AnimatedTile, Tile, StaticTile, Coin
from src.enemy import Enemy
from src.settings import tile_size, screen_width, screen_height
from src.helper import get_tile_set


class LevelDoesntExistException(Exception):
    pass


class LevelOverException(Exception):
    pass


class Level:
    def __init__(self, surface: pygame.surface.Surface, curr_level: int, coins: CoinsCount):
        self.curr_level = curr_level
        self.base_path = f"./src/assets/mapa/{self.curr_level}"
        self.check_level_exists()
        self.display_surface = surface
        self.goal = pygame.sprite.GroupSingle()
        self.player = pygame.sprite.GroupSingle()
        self.setup_level()
        self.setup_player()
        self.world_shift = 0
        self.collected_coins = coins
        player: Player = self.player.sprite  # type: ignore
        self.gui = GUI(self.display_surface, self.collected_coins, player)

    def check_level_exists(self):
        if not os.path.exists(f"{self.base_path}"):
            raise LevelDoesntExistException()

    def setup_level(self):
        terreno_layout = get_layout(f"{self.base_path}/terreno.csv")
        self.terreno_tile_set = get_tile_set(
            "./src/assets/0x72_DungeonTilesetII_v1.4/0x72_DungeonTilesetII_v1.4.png"
        )
        self.terreno_sprites = self.create_tile_group(terreno_layout, "terreno")

        moeda_layout = get_layout(f"{self.base_path}/moedas.csv")
        self.moeda_sprites = self.create_tile_group(moeda_layout, "moeda")

        inimigo_layout = get_layout(f"{self.base_path}/inimigo.csv")
        self.inimigo_sprites = self.create_tile_group(inimigo_layout, "inimigo")

        inimigo_bloqueio_layout = get_layout(f"{self.base_path}/inimigo-bloqueio.csv")
        self.inimigo_bloqueio_sprites = self.create_tile_group(
            inimigo_bloqueio_layout, "inimigo-bloqueio"
        )

    def setup_player(self):
        player_layout = get_layout(f"{self.base_path}/jogador.csv")
        for row_index, row in enumerate(player_layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "4":
                    player = Player((x, y))
                    self.player.add(player)
                elif cell == "5":
                    princess_sprite = AnimatedTile(
                        (x, y), tile_size, "./src/assets/princesa"
                    )
                    self.goal.add(princess_sprite)

    def create_tile_group(self, layout: list[list[str]], name: str):
        group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size
                    sprite = None
                    if name == "terreno":
                        sprite = StaticTile(
                            (x, y), tile_size, self.terreno_tile_set[int(val)]
                        )
                    elif name == "moeda":
                        sprite = Coin((x, y), tile_size)
                    elif name == "inimigo":
                        sprite = Enemy((x, y), tile_size)
                    elif name == "inimigo-bloqueio":
                        sprite = Tile((x, y), tile_size)
                    else:
                        raise Exception(f"invalid name: {name}")
                    group.add(sprite)

        return group

    def enemy_collision_w_block(self):
        for _inimigo in self.inimigo_sprites.sprites():
            inimigo: Enemy = _inimigo  # type: ignore
            if pygame.sprite.spritecollide(
                inimigo, self.inimigo_bloqueio_sprites, False
            ):
                inimigo.collided_w_block()

    def horizontal_movement_collision(self):
        player: Player = self.player.sprite  # type: ignore
        player.rect.x += int(player.direction.x * player.speed)
        collidable_sprites = self.terreno_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect is None:
                raise Exception("Sprite with empty rect")

            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (
            player.rect.left < self.current_x or player.direction.x >= 0
        ):
            player.on_left = False
        if player.on_right and (
            player.rect.right > self.current_x or player.direction.x <= 0
        ):
            player.on_right = False

    def vertical_movement_collision(self):
        player: Player = self.player.sprite  # type: ignore
        player.apply_gravity()
        collidable_sprites = self.terreno_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect is None:
                raise Exception("Sprite with empty rect")

            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player: Player = self.player.sprite  # type: ignore
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -player.default_speed
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = player.default_speed

    def check_enemy_collision(self):
        player: Player = self.player.sprite  # type: ignore
        collisions = pygame.sprite.spritecollide(player, self.inimigo_sprites, False)
        for inimigo in collisions:
            if inimigo.rect is None:
                raise Exception("inimigo.rect is none")

            if player.direction.y > player.gravity:
                inimigo.kill()
                player.jump()
                player.jump()
            else:
                player.damage()

    def check_coin_collision(self):
        player: Player = self.player.sprite  # type: ignore
        collisions = pygame.sprite.spritecollide(player, self.moeda_sprites, False)
        for moeda in collisions:
            if moeda.rect is None:
                raise Exception("inimigo.rect is none")

            moeda.kill()
            self.collected_coins.add()

    def out_of_bounds_check(self):
        player: Player = self.player.sprite  # type: ignore
        if player.rect.topleft[1] > screen_height:
            raise DeathException()

    def check_win_condition(self):
        player: Player = self.player.sprite  # type: ignore
        collisions = pygame.sprite.spritecollide(player, self.goal, False)
        if collisions:
            raise LevelOverException()

    def run(self):
        self.terreno_sprites.update(self.world_shift)
        self.terreno_sprites.draw(self.display_surface)

        self.moeda_sprites.update(self.world_shift)
        self.moeda_sprites.draw(self.display_surface)

        self.inimigo_sprites.update(self.world_shift)
        self.inimigo_bloqueio_sprites.update(self.world_shift)
        self.enemy_collision_w_block()
        self.inimigo_sprites.draw(self.display_surface)

        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        self.scroll_x()

        self.player.draw(self.display_surface)

        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)

        self.out_of_bounds_check()
        self.check_enemy_collision()
        self.check_coin_collision()

        self.gui.render()
        self.check_win_condition()
