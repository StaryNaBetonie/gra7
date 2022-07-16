import pygame
from settings import TILE_SIZE, ObjectType

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, pos, surface, alpha = 255) -> None:
        super().__init__(groups)
        self.object_type = ObjectType.wall
        self.can_move = False
        self.place_in_net = []

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)

        self.hitbox = self.rect.copy().inflate(0, -10)