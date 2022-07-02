from csv import reader
import pygame
from os import walk

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')

        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    
    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = f'{path}/{image}'
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surface)
    return surface_list

def import_cut_graphicks(path, size):
    surface = pygame.image.load(path)
    tile_num_x = int(surface.get_size()[0] / size[0])
    tile_num_y = int(surface.get_size()[1] / size[1])

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size[0]
            y = row * size[1]
            new_surf = pygame.Surface((size[0], size[1]), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size[0], size[1]))
            cut_tiles.append(new_surf)
    return cut_tiles