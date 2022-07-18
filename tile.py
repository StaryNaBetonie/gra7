import pygame
from support2 import get_rect

class Tile(pygame.sprite.Sprite):
    def __init__(self, groups, surface, object_type, layer, hitbox_offset, **pos) -> None:
        super().__init__(groups)
        self._layer = layer
        self.object_type = object_type
        self.place_in_net = []
    
        self.image_origin = surface
        self.image = surface
        self.rect = get_rect(self.image, pos)
        self.hitbox = self.rect.copy().inflate(hitbox_offset)