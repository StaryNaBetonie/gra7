import pygame
from settings import TILE_SIZE, BulletType

def get_rect(image, kwargs):
    rect = image.get_rect()
    for key, value in kwargs.items():
        if key == 'center': rect.center = value
        elif key == 'topleft': rect.topleft = value
    return rect

def generate_shadow(speed):
    surface = pygame.Surface((TILE_SIZE, 42))
    color = 255
    for i in range(42):
        rect = pygame.Rect((0, 0), (TILE_SIZE, 42 - i))
        pygame.draw.rect(surface, (color, color, color), rect)
        color -= speed
    return surface