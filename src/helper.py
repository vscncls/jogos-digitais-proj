import os
import pygame
import csv
from src.settings import tile_size


def import_folder(path: str):
    imgs: list[pygame.surface.Surface] = []
    for _,__,files in os.walk(path):
        for file in files:
            full_path = f'{path}/{file}'
            imgs.append(pygame.image.load(full_path).convert_alpha())
    return imgs

def get_tile_set(asset_path: str) -> list[pygame.surface.Surface]:
    surface = pygame.image.load(asset_path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    tile_set = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size))
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            tile_set.append(new_surf)

    return tile_set


def get_layout(path: str):
    layout: list[list[str]] = []
    with open(path) as file:
        layout_csv = csv.reader(file, delimiter=",")
        for row in layout_csv:
            layout.append(row)
    return layout
