import pygame
from src.helper import get_layout

from src.tile import AnimatedTile, Tile, StaticTile, Coin
from src.enemy import Enemy
from src.settings import tile_size, screen_width
from src.helper import get_tile_set


class Level:
    def __init__(self, surface: pygame.surface.Surface):
        self.display_surface = surface
        self.setup_level()
        self.setup_player()
        self.world_shift = 0

    def setup_level(self):
        terreno_layout = get_layout("./src/assets/mapa/terreno.csv")
        self.terreno_tile_set = get_tile_set(
            "./src/assets/0x72_DungeonTilesetII_v1.4/0x72_DungeonTilesetII_v1.4.png"
        )
        self.terreno_sprites = self.create_tile_group(terreno_layout, "terreno")

        moeda_layout = get_layout("./src/assets/mapa/moedas.csv")
        self.moeda_sprites = self.create_tile_group(moeda_layout, "moeda")

        inimigo_layout = get_layout("./src/assets/mapa/inimigo.csv")
        self.inimigo_sprites = self.create_tile_group(inimigo_layout, 'inimigo')

        inimigo_bloqueio_layout = get_layout("./src/assets/mapa/inimigo-bloqueio.csv")
        self.inimigo_bloqueio_sprites = self.create_tile_group(inimigo_bloqueio_layout, 'inimigo-bloqueio')

    def setup_player(self):
        player_layout = get_layout("./src/assets/mapa/jogador.csv")
        for row_index, row in enumerate(player_layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == '0':
                    pass
                elif cell == '2':
                    princess_sprite = AnimatedTile((x, y), tile_size, './src/assets/princesa')

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
                    elif name == 'inimigo':
                        sprite = Enemy((x,y), tile_size)
                    elif name == 'inimigo-bloqueio':
                        sprite = Tile((x,y), tile_size)
                    else:
                        raise Exception(f"invalid name: {name}")
                    group.add(sprite)

        return group

    def enemy_collision_w_block(self):
        for _inimigo in self.inimigo_sprites.sprites():
            inimigo: Enemy = _inimigo  # type: ignore
            if pygame.sprite.spritecollide(inimigo, self.inimigo_bloqueio_sprites, False):
                inimigo.collided_w_block()

    def run(self):
        self.terreno_sprites.update(self.world_shift)
        self.terreno_sprites.draw(self.display_surface)

        self.moeda_sprites.update(self.world_shift)
        self.moeda_sprites.draw(self.display_surface)

        self.inimigo_sprites.update(self.world_shift)
        self.inimigo_bloqueio_sprites.update(self.world_shift)
        self.enemy_collision_w_block()
        self.inimigo_sprites.draw(self.display_surface)
        self.inimigo_bloqueio_sprites.draw(self.display_surface)
