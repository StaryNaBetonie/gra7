from csv import reader
import pygame
from os import walk
from random import randint
from settings import TILE_SIZE, BulletType, ObjectType
from tile import Tile
import datetime

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
    surface = import_graphics(path)
    size_x, size_y = size
    tile_num_x = int(surface.get_size()[0] // size_x)
    tile_num_y = int(surface.get_size()[1] // size_y)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * size_x
            y = row * size_y
            new_surf = pygame.Surface((size_x, size_y), flags = pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, size_x, size_y))
            cut_tiles.append(new_surf)
    return cut_tiles

def get_surface(size, color):
        surface = pygame.Surface(size)  
        surface.set_colorkey('black')  
        surface.fill(color)
        return surface

def import_graphics(path):
    image = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale2x(image)

def add_tile(groups, pos, image):
    Tile(groups, image, ObjectType.wall, 0, (0, -10), topleft = pos)

def add_date_to_text_file():
    ct = datetime.datetime.now()
    file = open('number_of_games.txt', 'a')

    file.write('\n')
    file.write('date: ' + f'{ct.day, ct.month, ct.year}' + '\n')
    file.write('time: ' + f'{ct.hour, ct.minute, ct.second}' + '\n')

